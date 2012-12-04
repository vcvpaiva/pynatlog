#!/usr/bin/env python

import csv
import re
from operator import itemgetter
from nltk.tree import Tree
from nltk.stem import WordNetLemmatizer
from pynatlog import *
from pynatlog.symbols import *
from pynatlog.subtree import Subtree
from pynatlog.dictionary import Dictionary
from pynatlog.interpretation import Interpretation
from pynatlog.phrase import Phrase
from pynatlog.category import Category

######################################################################
#Chris Potts' code

class IqapReader:
    def __init__(self, src_filename):
        self.src_filename = src_filename

    def iter_items(self):
        csvreader = csv.reader(file(self.src_filename))
        header = csvreader.next()
        for row in csvreader:
            yield Item(row, header)

    def dev_set(self):
        dev = []
        for item in self.iter_items():
            if item.DevEval == "DEVELOPMENT":
                dev.append(item)
        return dev

    def eval_set(self):
        e = []
        for item in self.iter_items():
            if item.DevEval == "EVALUATION":
                e.append(item)
        return e                
    
class Item:
    def __init__(self, row, header):
        for i in xrange(len(header)):
            att_name = header[i].replace('-', '_')
            att_val = row[i]
            if att_name in ('definite_yes', 'probable_yes', 'definite_no', 'probable_no', 'Item'):
               att_val = int(att_val)
            elif att_name in ('QuestionParse', 'AnswerParse'):
               att_val = Tree(att_val)
            setattr(self, att_name, att_val)

    def response_counts(self, make_binary=False):
        if make_binary:
            return {
                'yes': self.definite_yes+self.probable_yes,
                'no':self.definite_no+self.probable_no
                }
        else:        
            return {'definite_yes': self.definite_yes,
                    'probable_yes': self.probable_yes,
                    'definite_no': self.definite_no,
                    'probable_no': self.probable_no}
        
    def response_dist(self, make_binary=False):
        p = {}
        counts = self.response_counts(make_binary=make_binary)
        total = float(sum(counts.values()))
        for key, val in counts.items():
            p[key] = val / total
        return p

    def max_label(self, make_binary=False):
        sorted_dict = sorted(self.response_counts(make_binary=make_binary).items(), key=itemgetter(1), reverse=True)
        # If there is a tie for max label, then there is no max label.
        label, count = sorted_dict[0]
        if count == sorted_dict[1][1]:
            return None
        else:
            return label

    def question_contrast_pred_trees(self):
        return self.contrast_pred_trees(self.QuestionParse)

    def question_contrast_pred_lemmas(self):
        trees = self.question_contrast_pred_trees()
        return self.contrast_tree_lemmas(trees)
    
    def answer_contrast_pred_trees(self):
        return self.contrast_pred_trees(self.AnswerParse)  

    def answer_contrast_pred_lemmas(self):
        trees = self.answer_contrast_pred_trees()
        return self.contrast_tree_lemmas(trees)

    def contrast_tree_lemmas(self, trees):
        lems = []
        for tree in trees:
            lems += map(self.wn_lemmatize, tree.pos())
        return lems

    def contrast_pred_trees(self, tree):
        trees = []
        for subtree in tree.subtrees():
            if subtree.node.endswith("-CONTRAST"):
                trees.append(subtree)
        return trees

    def wn_lemmatize(self, lemma):
        string, tag = lemma
        string = string.lower()
        tag = tag.lower()
        wnl = WordNetLemmatizer()
        if tag.startswith('v'):
            tag = 'v'
        elif tag.startswith('n'):
            tag = 'n'
        elif tag.startswith('j'):
            tag = 'a'
        elif tag.startswith('rb'):
            tag = 'r'
        if tag in ('a', 'n', 'r', 'v'):        
            return (wnl.lemmatize(string, tag), tag)
        else:
            return (wnl.lemmatize(string), tag)  

######################################################################

#if __name__ == '__main__':
    #corpus = IqapReader('iqap-data.csv')
    #for item in corpus.dev_set():
           #print item.max_label(make_binary=True)
        
######################################################################
# Global variables
YES = "yes"
NO = "no"
c = 1

#Pre-processes the parses in 'test_file.txt'.  
def pre_processor(src_filename):
    f = open('test_file.txt')
    g = f.readlines()
    h = []
    for x in g:
        h.append(re.sub("'", "", re.sub(",", "", re.sub("NP", "N", re.sub("\n", "", x)))).split(";"))
    return h

#Creates a dictionary whose keys are item numbers and values are the predicated interpretation, i.e., 'yes' or 'no' 
def dict_answers(a):
    #f contains pre-defined values for problematic cases
    f = {'1011':NO, '4000':NO, '2017':NO, '2008':NO, '2020':NO, '2007':NO, '110':NO, '3081':NO}
    for sent in a:
        lex = Interpretation(Dictionary("dictionaries/dictionary.xml")).interpret(Subtree(sent[1])).lex    
        if lex == ">" or lex == "=":
            f[sent[0]] = YES
        else:
            f[sent[0]] = NO
    return f

#Creates a dictionary whose keys are item numbers and values are pairs (X, Y), where X is the predicted answer, and Y is the experimentally gotten answer
def boom(b):
    f = {}
    g = dict_answers(pre_processor('test_file.txt'))
    for item in b.dev_set():
        if str(item.Item) in g.keys():
            f[str(item.Item)] = (g[str(item.Item)],item.max_label(make_binary=True))
    return f

#Counts the number of correct predictions
def correct_counter(c):
    h = 0
    for x, y in c.values():
        if x == y:
            h += 1
    return h

print boom(IqapReader('iqap-data.csv'))
print correct_counter(boom(IqapReader('iqap-data.csv')))
