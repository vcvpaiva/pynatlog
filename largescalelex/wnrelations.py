#!/usr/bin/env python

"""
This module seeks to use Wordnet's structure to infer NatLog relations
between pairs of (string, pos) pairs.  The basic logic is as follows:

  1. Initialize WnRelation objects with two strings str1 and str2 and
     a WordNet pos, interpreting thesese as (str1, pos) and (str2, pos).

  2. Get the synsets associated with each (str, pos) pair. Call these
     synsets S1 and S2.

  3. Use S1 and S2 to make an inference about the relation between
     (str1, pos) and (str2, pos):

     a. Equality: S1 and S2 are the same.

     b. Forward entailment: there is a hypernym path from a synset in
        S1 to a synset in S2.

     c. Backward entailment: reverse of Forward.

     d. Negation: a lemma of a synset of S1 is an antonym of a lemma
        of a synset of S2.

     e. Alternation: S1 and S2 each contain synsets that have a common
        parent.

If this file is called with the main method (say, from the command
line) then it runs a small test.  The results are good for 'n' but too
sparse for the others, which don't have solid hypernym/hyponym
coverage (if the have any such coverage at all).

---Chris Potts
"""

from nltk.corpus import wordnet as wn
from collections import defaultdict

FORWARD = "<"
BACKWARD = ">"
NEGATION = "^"
ALTERNATION = "|"
COVER = "_"
EQUALITY = "="
INDEPENDENT = "#"

class WnRelation:
    def __init__(self, s1, s2, pos):
        """
        Arguments
        s1, s2 -- strings representing words
        pos -- a WordNet category (must be a,n,v,r)

        Attributes
        self.s1 -- s1
        self.s2 -- s2
        self.pos -- pos
        self.relation -- the inferred relation, derived by the
        central method self.wn_lexical_relation()
        """
        self.s1 = s1
        self.s2 = s2
        self.pos = pos
        if self.pos not in ("a", "n", "v", "r"):
            raise ValueError("%s is not a WordNet category; must be in {a,n,v,r}")
        self.relation = self.wn_lexical_relation()

    def wn_lexical_relation(self):
        """
        Builds the synsets and then tries to infer a relation,
        using various relations-specific methods.
        """
        syns1 = wn.synsets(self.s1, self.pos)
        syns2 = wn.synsets(self.s2, self.pos)
        if self.strong_synonyms(syns1, syns2):
            return EQUALITY
        if self.hypernyms(syns1, syns2):
            return FORWARD
        elif self.hyponyms(syns1, syns2):
            return BACKWARD
        elif self.antonyms(syns1, syns2):
            return NEGATION
        elif self.weak_synonyms(syns1, syns2):
            return EQUALITY
        elif self.alternates(syns1, syns2):
            return ALTERNATION
        return INDEPENDENT

    def strong_synonyms(self, syns1, syns2):
        """Returns True if syns1 == syns2, else False."""
        if syns1 == syns2:
            return True
        else:
            return False

    def weak_synonyms(self, syns1, syns2):
        """
        Returns True if there is a syn1 in syns1 and a syn2 in syns2
        such that syn1 == syn2, else False.
        """
        for syn1 in syns1:
            if syn1 in syns2:
                return True
        return False

    def hypernyms(self, syns1, syns2):
        """
        Returns True if syns2 contains a synset that is on the
        hypernym path of a synset in syns1, else False.
        """
        for syn1 in syns1:
            for syn2 in syns2:
                if syn1 != syn2:
                    for path in syn1.hypernym_paths():
                        if syn2 in path:
                            return True
        return False

    def hyponyms(self, syns1, syns2):
        """Reverses self.hypernyms()."""
        return self.hypernyms(syns2, syns1)

    def antonyms(self, syns1, syns2):
        """
        Returns True if there is a lemma of a synset of syns2 that is
        an antonym of a lemma of a synset of syns1, else False.
        """
        for syn1 in syns1:
            for lemma1 in syn1.lemmas:
                for syn2 in syns2:
                    for lemma2 in syn2.lemmas:
                        if lemma2 in lemma1.antonyms():
                            return True
        return False

    def alternates(self, syns1, syns2):
        """Returns False if syns1 and syns2 each contain synsets that
        have a common parent, else False.
        """
        for syn1 in syns1:
            for syn2 in syns2:
                distances = syn1.hypernym_distances()
                for hyp, d in distances:
                    if d == 1:
                        return True
        return False

######################################################################

if __name__ == "__main__":

    examples = (('great', 'good', 'a'),
                )

    for s1, s2, pos in examples:
        wnr = WnRelation(s1, s2, pos)
        print s1, s2, pos, wnr.wn_lexical_relation()

######################################################################

