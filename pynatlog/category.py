import re

class Category:
      """Class for modeling syntactic categories and their
      combinatorics. The categories function like types, controlling
      what can combine with what."""
      def __init__(self, string):
            """Initialized on a string representing the category."""
            self.string = string
            self.input, self.output = self.__parse()

      def combine(self, mcat):
            """Combine the current object with the argument cat, if possible."""
            if self.input == mcat:
                  return self.output
            raise Exception("Category mismatch; %s cannot combine with %s" % (self, mcat))

      def combines_with(self, mcat):
            if self.input == mcat:
                  return True
            else:
                  return False

      def is_atomic(self):
            """Returns true of the category has no slash in it, else false."""
            if re.search("/", self.string):
                  return False
            else:
                  return True

      def __parse(self):
            """Internal method for parsing categories into input and output."""
            string = re.sub(r"\s", "", self.string)
            if self.is_atomic():
                  return [self.string,self.string]                  
            bc = 0
            for i, char in enumerate(list(string)):
                  if char == "(":
                        bc += 1
                        bracket_seen = True
                  elif char == ")":
                        bc -= 1
                  elif bc == 1 and char == "/":
                        left = string[1:i]
                        right = string[i+1:-1]
                        return [Category(left), Category(right)]
            raise Exception("Couldn't parse input string: %s" % self.string)

      def __str__(self):
            """Returns the input string, unchanged."""
            return self.string

      def __eq__(self, other):
            """Category identity is string identity."""
            return str(self) == str(other)

      def __ne__(self, other):
            """Category non-identity is string inequality."""
            return str(self) != str(other)
            
