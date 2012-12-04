import re

class Subtree:

    # Always reference these using the variables to allow easy global changes to the format.
    left_bracket = r"["
    right_bracket = r"]"
    
    def __init__(self, s):
        self.s = self.__basic_cleanup(s) # Ensures that the spacing is properly regularized.
        self.cat = ""       # Will stay null for non-atomic trees.
        self.daughters = [] # List of daughter subtrees; singleton containing the terminal for atomic cases.
        self.__parse()

    ##################################################################
    # PARSING.

    def __parse(self):
        """Recursively parse the input string."""
        if self.is_atomic():
            cat, terminal = self.__remove_outer_brackets(self.s).split(" ")
            self.cat = cat
            self.daughters = [terminal]
        else:
            bracket_count = 0
            start = 1 # Left of the current daughter; initialize to 1 because of the outermost bracket.
            for i in range(len(self.s)):
                char = self.s[i]
                if char == Subtree.left_bracket:
                    bracket_count += 1
                elif char == Subtree.right_bracket:
                    bracket_count -= 1
                # If this condition is met, we are at ] marking the right boundary of a daughter.
                if bracket_count == 1 and char == Subtree.right_bracket:
                    # Grab the daughter, going back to the start of this daughter.
                    self.daughters.append(Subtree(self.s[start:i+1]))
                    # Move the starting point forward to the following [ bracket.
                    start = i+1

    def is_atomic(self):
        """An atomic tree is one of the form [CAT TERMINAL], with brackets at its outermost edges and no brackets in between."""
        atomic_re = re.compile(r"^\%s[^\%s]+\%s$" % (Subtree.left_bracket, Subtree.right_bracket, Subtree.right_bracket))
        if atomic_re.search(self.s):
            return True
        else:
             return False

    def __basic_cleanup(self, s):
        """Regularizes the input string so that the whitespace can be
        counted on: a single whitespace between category label and
        terminal is preserved, and all other whitespace is
        removed. This function also removes any nonterminals that are
        not directly above terminals.
        """
        # Remove any newlines.
        newline_re = re.compile(r"\s*\n+", re.M)
        s = newline_re.sub(" ", s)
        # Ensure that multiple sequences of spaces are reduced to a single one, to ensure proper parsing.
        s = re.sub(r"\s{2,}", " ", s)
        # Ensure that brackets are adjacent.
        s = re.sub(r"\s*([\%s\%s])\s*" % (Subtree.left_bracket, Subtree.right_bracket), r"\1", s)
        # Get rid of any errant non-terminal labels.
        nonterminal_re = re.compile(r"\%s\s*[\(A-Z/\)]+\s*\%s" % (Subtree.left_bracket, Subtree.left_bracket))
        s = nonterminal_re.sub("%s%s" % (Subtree.left_bracket, Subtree.left_bracket), s)
        return s
            
    def __remove_outer_brackets(self, s):
        outer_bracket_re = re.compile(r"(^\%s|\%s$)" % (Subtree.left_bracket, Subtree.right_bracket))
        return outer_bracket_re.sub(r"", s)
 
    ##################################################################
    # PRINTING.
    
    def __str__(self):
        """Returns the input string, unchanged."""
        return self.s

    def prettify(self, depth=0):
        """Returns a string version of the input that better reveals constituency."""
        tab = "  " * depth
        s = ""
        if self.is_atomic():
            s += tab + Subtree.left_bracket + self.cat + " " + self.daughters[0] + Subtree.right_bracket
        else:
            s += tab + Subtree.left_bracket
            for d in self.daughters:
                s += "\n" + d.prettify(depth+1)
            s += Subtree.right_bracket
        return s


