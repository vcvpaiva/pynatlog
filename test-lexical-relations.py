#!/usr/bin/env python

from nltk.corpus import wordnet as wn
from pynatlog.lexlearner import LexLearner

pairs = (("correct", "untrue", "a"),)

for w1, w2, pos in pairs:
    print w1, w2, LexLearner(w1, w2, pos).get_lexical_relation()


        
            
