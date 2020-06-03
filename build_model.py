from sklearn.neighbors import NearestNeighbors
import pickle
import os
import pandas as pd
import numpy as np
import knowledgeExtraction

class FakeNewClassifier:
    def __init__(self, path_to_embedding):
        self.path_to_embedding = path_to_embedding
        self.read_data()
        self.knExtraction = knowledgeExtraction.KnowledgeExtraction()
        self.nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree')

    def read_data(self):
        ent_embedding = self.read_pickle(os.path.join(self.path_to_embedding, "ent_embedding.pickle"))
        ent_labels = self.read_pickle(os.path.join(self.path_to_embedding, "ent_labels.pickle"))
        ent_embedding["label"] = ent_labels
        rel_embedding = self.read_pickle(os.path.join(self.path_to_embedding, "rel_embedding.pickle"))
        rel_labels = self.read_pickle(os.path.join(self.path_to_embedding, "rel_labels.pickle"))
        rel_embedding["label"] = rel_labels
        self.entities = ent_labels
        self.rels = rel_labels
        self.df_ent = ent_embedding
        self.df_ent = self.df_ent.set_index("label")
        self.df_rel = rel_embedding
        self.df_rel = self.df_rel.set_index("label")
        # print(self.df_ent.head())
        # print(self.df_rel.head())

    def all_data(self):
        df_train = pd.read_csv(os.path.join(self.path_to_embedding, "tennis-train.txt"), sep="\t", names=["sub", "rel", "obj"])
        vecs = np.zeros((df_train.shape[0], 150))
        for idx, row in df_train.iterrows():
            vecs[idx] = self.make_vector_for_triple(list(row))
        return vecs

    def make_vector_for_triple(self, triple):
        sub = triple[0]
        rel = triple[1]
        obj = triple[2]
        vec_length = 50
        if sub in self.df_ent.index:
            print(self.df_ent.loc[sub].to_list())
            sub_vec = np.array(self.df_ent.loc[sub].to_list())
        else:
            sub_vec = np.zeros(vec_length)
        if rel in self.df_rel.index:
            rel_vec = np.array(self.df_rel.loc[rel].to_list())
        else:
            rel_vec = np.zeros(vec_length)
        if obj in self.df_ent.index:
            obj_vec = np.array(self.df_ent.loc[obj].to_list())
        else:
            obj_vec = np.zeros(vec_length)
        vec = np.concatenate((sub_vec, rel_vec, obj_vec), axis=None)
        return vec


    def read_pickle(self, path):
        return pickle.load(open(path, "rb"))

    def get_score_triple(self, triple):
        vec = self.make_vector_for_triple(triple)
        distances, indices = self.nbrs.kneighbors([vec])
        print(distances)
        print(indices)
        scores = 1 - distances
        score = scores[0]
        return score

    def average(self, lst):
        if len(lst) == 0:
            return 0
        return sum(lst) / len(lst)

    def detect_fake_new(self, text):
        triples = self.knExtraction.get_triples_from_text(text)
        print("Triples: ", triples)
        scores = []
        for triple in triples:
            scores.append(self.get_score_triple(triple))
        return self.average(scores)

    def find_entity_sentence(self, text):
        text = text.lower()
        ent_find = []
        for ent in self.entities:
            if " {} ".format(ent) in text or text.startswith("{} ".format(ent)) or text.endswith(" {}".format(ent))  or text.endswith(" {}.".format(ent)):
                ent_find.append(ent)
        ent_find = sorted(ent_find, key=len, reverse=True)
        return ent_find

    def find_relation_sentence(self, text):
        text = text.lower()
        rel_find = []
        for rel in self.rels:
            if " {} ".format(rel) in text:
                rel_find.append(rel)
        rel_find = sorted(rel_find, key=len, reverse=True)
        return rel_find

    def make_vector(self, text):
        vec_len = 50
        ent_find = self.find_entity_sentence(text)
        ent_find = ent_find[0:4]
        print("Entity find: ", ent_find)
        rel_find = self.find_relation_sentence(text)
        rel_find = rel_find[0:2]
        print("Rel find: ", rel_find)
        i = 0
        vecs = []
        for ent in ent_find:
            i += 1
            ent_vec = np.array(self.df_ent.loc[ent].to_list())
            vecs.append(ent_vec)
        if i < 4:
            while i < 4:
                i += 1
                vecs.append(np.zeros(vec_len))

        i = 0
        for rel in rel_find:
            i += 1
            rel_vec = np.array(self.df_rel.loc[rel].to_list())
            vecs.append(rel_vec)
        if i < 2:
            while i < 2:
                i += 1
                vecs.append(np.zeros(vec_len))
        vec = np.concatenate(tuple(vecs), axis=None)
        print(vec.shape)
        return vec

fakeClf = FakeNewClassifier("/Users/vietnguyen/Workspace/Codes/Python/Knowledge-Graph-Intro/my_dataset/embeddings/TransE")