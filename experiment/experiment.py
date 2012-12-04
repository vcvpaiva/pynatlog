#!/usr/bin/env python

import re
from ..pynatlog import *

######################################################################

class Experiment:
    def __init__(self, corpus_filename, dictionary_filename):
        self.corpus = Corpus(corpus_filename)
        self.dictionary = Dictionary(dictionary_filename)
        self.correct = 0
        self.incorrect = 0
        
    def run(self):
        for prob in self.corpus.problems:
            actual_relation = prob.relation
            sem = Subtree(prob.align, self.dictionary).intrprt()
            print "======================================================================"
            print sem
            hypothesized_relation = sem.lex
            if actual_relation == hypothesized_relation:
                self.correct += 1                
            else:
                self.incorrect += 1

    def results(self):
        s = ""
        s += "Correct: %s\n" % self.correct
        s += "Incorrect: %s\n" % self.incorrect
        return s

######################################################################

class Corpus:

    problem_re = re.compile(r"<problem.*?>.+?</problem>", re.DOTALL | re.MULTILINE)
    
    def __init__(self, filename):
        self.filename = filename
        contents = open(filename).read()
        self.problems = map(Problem, Corpus.problem_re.findall(contents))

######################################################################

class Problem:
    def __init__(self, xml):        
        d = self.__get_fields(xml)
        num = re.search(r"<problem num=([0-9]+)", xml)
        if num:
            self.num = int(num.group(1))
        else:
            raise Exception("No index for %s" % xml)        
        self.source   = self.__clean_value(d["source"])
        self.text     = self.__clean_value(d["text"])
        self.align    = self.__clean_value(d["align"])
        self.relation = self.__clean_value(d["relation"])
        if self.relation not in RELS:
            raise Exception("Relation %s is not a PyNatLog relation." % self.relation)
        self.note = d.get("note", "")

    def __get_fields(self, xml):
        """Gets field values, ignoring embedding level but scanning only individual lines."""
        field_re = re.compile(r"^\t*<([^>]+)>(.*?)</\1>", re.MULTILINE | re.DOTALL)
        initial_pairs = field_re.findall(xml)
        return dict(initial_pairs)

    def __clean_value(self, val):
        return val.strip().strip("\n")

######################################################################





