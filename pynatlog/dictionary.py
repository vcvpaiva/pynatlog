import codecs
import datetime
import shutil
import re
from symbols import *
from jointable import JoinTable
from phrase import Phrase
from category import Category
from lexlearner import LexLearner

class Dictionary:
      def __init__(self, filename=None):
            self.contents = ""
            if filename:
                  self.contents = open(filename).read()
            self.item_dict = {}
            self.__get_items()
            self.m_closure()

      def m_closure(self):
            """Method for closing a dictionary under symmetry and the class of MacCartney relations."""                        
            sym = (EQUALITY, NEGATION, COVER, ALTERNATION, INDEPENDENT) # Symmetic relations.
            for phc, phrase in self.item_dict.items():
                  prem, conc, pcat = phc
                  if (conc, prem, pcat) not in self.item_dict.keys():
                        new_rel = None
                        # Closure under symmetry.
                        if phrase.lex in sym:
                              new_rel = phrase.lex
                        # Closure under reversals.
                        elif phrase.lex == FORWARD:
                              new_rel = BACKWARD
                        elif phrase.lex == BACKWARD:
                              new_rel = FORWARD
                        if new_rel:
                              new_phrase = Phrase(conc, prem, phrase.mcat, new_rel, phrase.projs)
                              self.item_dict[(conc, prem, pcat)] = new_phrase
            # Closure under the join table.
            #for phc1, phrase1 in self.item_dict.items():
                  #prem1, conc1, pcat1 = phc1
                  #for phc2, phrase2 in self.item_dict.items():
                        #prem2, conc2, pcat2 = phc2
                        #if pcat1 == pcat2:
                              #shared_pcat = pcat1
                              #if conc1 == prem2 and prem1 != conc2:
                                    #new_lex = JoinTable().rel_join[phrase1.lex][phrase2.lex]                              
                                    #new_phrase = Phrase(conc1, conc2, phrase2.mcat, new_lex, phrase2.projs)
                                    #self.item_dict[(conc1, conc2, shared_pcat)] = new_phrase

      def lookup(self, pcat, *args):
            """Returns the value of (prem, conc, cat) in self.item_dict, else returns None."""
            prem = None
            conc = None
            if len(args) == 1:
                  prem, conc = args[0].strip().split("/")
            else:
                  prem, conc = args
            temp = self.item_dict.get((prem, conc, pcat), None)
            if temp:
                  return temp
            else:                  
                  new_lex = LexLearner(prem, conc, pcat).get_lexical_relation()
                  if new_lex:
                        ph = Phrase(prem, conc, Category(pcat), new_lex, [DEFAULT_PROJ])
                        self.item_dict[(prem, conc, pcat)] = ph
                        # Reclose the dictionary taking the newly added things into account.
                        # self.m_closure()
                        return ph
                  else:
                        raise Exception("Lexical failure: Cannot identify lexical pair (%s, %s) with category %s." % (prem, conc, pcat))
                  
      def __get_items(self):
            """Internal method for parsing the input files and turning their contents into self.item_dict."""
            item_re = re.compile(r"<item>(.+?)</item>", re.DOTALL | re.MULTILINE)
            # Parse the file.
            item_strs = item_re.findall(self.contents)
            # Convert everything to phrases.
            for item_str in item_strs:
                  phrase = Phrase(item_str)
                  self.item_dict[(phrase.prem, phrase.conc, phrase.pcat)] = phrase

      def to_xml(self):
            s = u""
            # Sort the output dictionary by premise.
            sorter = (lambda x, y : x[1].prem <= y[1].prem)
            sorted_dict = sorted(self.item_dict.items(), cmp=sorter)
            for key, ph in sorted_dict:
                  s += ph.to_xml() + u"\n"
            return s

      def __str__(self):
            return self.to_xml()
                         
          
