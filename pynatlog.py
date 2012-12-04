#!/usr/bin/env python

import sys
import random
from pynatlog import *
from pynatlog.subtree import Subtree
from pynatlog.dictionary import Dictionary
from pynatlog.interpretation import Interpretation

dictionary_filename = "dictionaries/dictionary.xml"

sents = ["[N wolf/mammal]",
         # not is a dog/poodle
         """[
              [(VP/VP) not/not]
              [
                [((N/N)/VP) is/is ]
                [
                  [(N/(N/N)) a/a]
                  [N dog/poodle]]]]""",
         # Fido not is a dog/poodle --- apologies for the position of negation!
         """[
              [(VP/S) fido/fido]
              [
                [(VP/VP) not/not]
                [
                  [((N/N)/VP) is/is ]
                  [
                    [(N/(N/N)) a/a]
                    [N dog/poodle]
                  ]
                 ]
                ]
             ]""",
         # Fido not is a poodle/dog
          """[
              [(VP/S) fido/fido]
              [
                [(VP/VP) not/not]
                [
                  [((N/N)/VP) is/is ]
                  [
                    [(N/(N/N)) a/a]
                    [N poodle/dog]
                  ]
                 ]
                ]
             ]""",
         # Fido run/spring
         "[ [(VP/S) fido/fido] [VP run/sprint]]",
         # every poodle/dog
         """[
             [ (N/(VP/S)) every/every ]
             [ N poodle/dog ]
            ]""",
         #  poodle/poodle
         "[N poodle/poodle]",
         #  dog/poodle
         "[N dog/poodle]",
         # poodle/dog
         "[N poodle/dog]",
         # every poodle/dog run/sprint
         """[
              [
               [ (N/(VP/S)) every/every ]
               [ N poodle/dog ]
              ]
              [VP run/sprint]]"""]

if __name__ == "__main__":
    """Command-line parse or a random example."""
    sent = None
    if len(sys.argv) >= 2:
        sent = sys.argv[1]
        print "Your input:"
    else:        
        sent = sents[random.randint(0, len(sents)-1)]
        print "Random choice:"
    sbt = Subtree(sent)
    print "Structure:"
    print sbt.prettify()
    print "Interpretation:"
    print Interpretation(Dictionary(dictionary_filename)).interpret(sbt)

       
