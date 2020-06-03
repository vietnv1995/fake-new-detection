import spacy
# load NeuralCoref and add it to the pipe of SpaCy's model
import neuralcoref


class RenamePronouns():
    def __init__(self):
        self.nlp = spacy.load('en')
        coref = neuralcoref.NeuralCoref(self.nlp.vocab)
        self.nlp.add_pipe(coref, name='neuralcoref')

    def replace_pronouns(self, text):
        doc = self.nlp(text)
        check_has_coref = doc._.has_coref
        if check_has_coref:
            text = doc._.coref_resolved
        return text