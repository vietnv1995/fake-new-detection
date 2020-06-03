# Extracting SPOs.
# python -m spacy download en -> To donwload the en model of spacy.

import spacy
import textacy
import rename_pronouns
# Subject Verb Object detection


class KnowledgeExtraction:
    def __init__(self):
        self.renameObj = rename_pronouns.RenamePronouns()


    def retrieveKnowledge(self, textInput):
        nlp = spacy.load('en')
        text = nlp(textInput)
        text_ext = textacy.extract.subject_verb_object_triples(text)
        return list(text_ext)

    def preprocess(self, text):
        text = self.renameObj.replace_pronouns(text)
        return text

    def get_triples_from_text(self, text):
        sop_list_strings = []
        text = self.preprocess(text)
        sop_list = self.retrieveKnowledge(text)
        for sop in sop_list:
            temp = []
            temp.append(sop[0].text)
            temp.append(sop[1].text)
            temp.append(sop[2].text)
            sop_list_strings.append(temp)
        return sop_list_strings

    def extract_triple_by_openIO(self, text):
        from openie import StanfordOpenIE
        triples = []
        with StanfordOpenIE() as client:
            # text = 'French Open organisers working with authorities to avoid US Open clash.'
            print('Text: %s.' % text)
            for triple in client.annotate(text):
                triples.append([triple["subject"], triple["relation"], triple["object"]])
        return triples
