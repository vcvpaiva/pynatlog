#!/usr/bin/env python

import re
from pynatlog import *
from experiment import *


corpus_filename = "aligned-sample.xml"
dictionary_filename = "dictionary.xml"
exp = Experiment(corpus_filename, dictionary_filename)
exp.run()
print exp.results()
