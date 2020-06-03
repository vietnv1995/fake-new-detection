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
        X = self.all_data()
        self.nbrs = pickle.load(open("model.pkl", "rb"))

    def read_data(self):
        ent_embedding = self.read_pickle(os.path.join(self.path_to_embedding, "ent_embedding.pickle"))
        ent_labels = self.read_pickle(os.path.join(self.path_to_embedding, "ent_labels.pickle"))
        ent_embedding["label"] = ent_labels
        rel_embedding = self.read_pickle(os.path.join(self.path_to_embedding, "rel_embedding.pickle"))
        rel_labels = self.read_pickle(os.path.join(self.path_to_embedding, "rel_labels.pickle"))
        rel_embedding["label"] = rel_labels
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

fakeClf = FakeNewClassifier("/Users/vietnguyen/Workspace/Codes/Python/Knowledge-Graph-Intro/my_dataset/embeddings/TransE")