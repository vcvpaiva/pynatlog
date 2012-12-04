from nltk.corpus import wordnet as wn
from symbols import *

class LexLearner:
    def __init__(self, s1, s2, pos):
        self.s1 = s1
        self.s2 = s2
        self.pos = pos

    def get_lexical_relation(self):
        return self.wn_lexical_relation()

    def cat2wn(self, cat):
        pcat2wn_map = {
            "N":"n",            # common noun
            "VP":"v",           # intransitive V
            "(NP/(NP/VP))":"v", # transitive V
            "((N/N)/VP)": "v",  # predicative 'be', 'consider', ...
            "(N/N)":"a",        # adjective
            "(VP/VP)":"r",      # VP adverb
            "(S/S)":"r"         # sentential adverb                                    
            }
        cat = str(cat)
        return pcat2wn_map.get(cat, 0)    

    def wn_lexical_relation(self):
        if self.pos not in ["a", "n", "v", "r"]: # WordNet categories.
            self.pos = self.cat2wn(self.pos)
        if not self.pos:
            return None
        syns1 = wn.synsets(self.s1, self.pos)
        syns2 = wn.synsets(self.s2, self.pos)
        if self.synonyms(syns1, syns2):
            return EQUALITY
        elif self.hypernyms(syns1, syns2):
            return FORWARD
        elif self.hyponyms(syns1, syns2):
            return BACKWARD
        elif self.antonyms(syns1, syns2):
            return ALTERNATION
        return INDEPENDENT

    def synonyms(self, syns1, syns2):    
        for syn1 in syns1:
            if syn1 in syns2:
                return True
        for syn2 in syns2:
            if syn2 in syns1:
                return True
        return False

    def hypernyms(self, syns1, syns2):
        for syn1 in syns1:        
            for syn2 in syns2:
                for path in syn1.hypernym_paths():
                    if syn2 in path:
                        return True
        return False

    def hyponyms(self, syns1, syns2):
        return self.hypernyms(syns2, syns1)

    def antonyms(self, syns1, syns2):
        for syn1 in syns1:
            for lemma1 in syn1.lemmas:
                for syn2 in syns2:
                    for lemma2 in syn2.lemmas:
                        if lemma2 in lemma1.antonyms():
                            return True
        return False
