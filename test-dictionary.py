#!/usr/bin/env python

from pynatlog.symbols import *
from pynatlog.dictionary import Dictionary

######################################################################
# TESTING WITH EMPTY DICTIONARY

def test_empty_dict():
    # Load the empty dictionary.
    filename = None
    dictionary = Dictionary(filename)
    
    # Rely on WN to create some new lexical relationships.
    print "Looking up poodle, dog ..."
    dictionary.lookup('n', "poodle", "dog")
    print "Looking up dog, mammal .."
    dictionary.lookup('n', "dog", "mammal")

    # View the expanded dictionary.
    print dictionary.to_xml()

test_empty_dict()   

######################################################################
# TESTING WITH THE MAIN DICTIONARIES

def test_main_dict():
    # Load the dictionary files.
    filename = "dictionaries/dictionary.xml"
    dictionary = Dictionary(filename)
    # View the dictionary.
    print dictionary.to_xml()

test_main_dict()

######################################################################
