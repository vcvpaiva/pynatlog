#!/usr/bin/env python

from pynatlog import *
from pynatlog.subtree import Subtree

######################################################################
# EXAMPLE FROM ALIGNED PARSES TO INTERPRETATIONS

# Note: All white space and newlines are optional except for the white
# space between the category label and the terminal.
#
# Non-terminals that aren't pre-terminals can be included, but they
# will be ignored (removed) by the parser.

sents = ["[(S/NP) wolf/mammal]",
         "[[((S/NP)/(S/NP)) not/not][(S/NP) dog/poodle]]",
         "[ [[((S/NP)/S) fido/fido]] [  [((S/NP)/(S/NP)) not/not] [(S/NP) dog/poodle]]]",
         """[
              [((S/NP)/S) fido/fido]
              [VP
                [VP
                  [((S/NP)/(S/NP)) is ]
                  [(S/NP) running/walking]
                ]
                [((S/NP)/(S/NP)) today ]]]""",
         "[ [N fido/fido] [V run/sprint]]",
         """[
              [ (((S/NP)/(S/NP))/S) every/every ]
              [ (S/NP) dog/poodle ] ]"""
         ]

for sent in sents:
    print "======================================================================"
    sbt = Subtree(sent)
    print "---------- Regularized:\n"
    print sbt
    print "\n---------- Prettified:\n"
    print sbt.prettify()

