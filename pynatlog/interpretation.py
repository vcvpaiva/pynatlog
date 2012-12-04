from phrase import Phrase
from dictionary import Dictionary
from jointable import JoinTable

class Interpretation:
    def __init__(self, dictionary=Dictionary()):
        self.dictionary = dictionary

    def interpret(self, subtree):
        """Recursively interpret the tree."""
        # For atomic cases.
        if subtree.is_atomic():
            return self.atomic_interpret(subtree.cat, subtree.daughters[0])
        # For non-branching cases.
        elif len(subtree.daughters) == 1:
            return self.interpret(subtree.daughters[0])
        # For branching cases.
        elif len(subtree.daughters) == 2:
            left = self.interpret(subtree.daughters[0])
            right = self.interpret(subtree.daughters[1])
            return self.fa(left, right)
        else:
            raise Exception("We have no provision for interpreting branching nodes greater than 2.")

    def atomic_interpret(self, cat, leaf):
        """Interprets category, leaf pairs using the dictionary."""
        return self.dictionary.lookup(cat, leaf)
    
    def fa(self, arg1, arg2):
        """Functional application between Phrase objects. The heart of the theory."""
        left = None
        right = None
        if arg1.mcat.combines_with(arg2.mcat):
            left = arg1
            right = arg2
        elif arg2.mcat.combines_with(arg1.mcat):
            left = arg2
            right = arg1
        else:
            raise Exception("Categories uncombinable: %s, %s" % (arg1.mcat, arg2.mcat))
        # Output prem and hyp, as strings.
        out_prem = "(%s %s)" % (left.prem, right.prem)
        out_conc = "(%s %s)" % (left.conc, right.conc)
        # Output projectivity.
        out_proj_value = left.projs[0].get(right.lex, None)
        # Increment the projectivity function.
        left.projs.pop(0)
        # Output lex according to Alex's rule of inference.
        out_lex = JoinTable().join(left.lex, out_proj_value)
        # Output category.
        out_mcat = left.mcat.combine(right.mcat)
        out_proj = {}
        # For quantifiers and other things with multiple projectivity, pass on all remaining proj dictionaries.
        if left.projs:
            out_proj = left.projs
        phrase = Phrase(out_prem, out_conc, out_mcat, out_lex, out_proj)
        return phrase                      
                

