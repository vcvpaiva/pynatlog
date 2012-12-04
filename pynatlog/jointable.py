from symbols import *

class JoinTable:
      """Class for modeling the join table."""

      # The join table.
      rel_join = {
            EQUALITY:   IDENT,
            FORWARD:    {EQUALITY:FORWARD,    FORWARD:FORWARD,    BACKWARD:INDEPENDENT,NEGATION:ALTERNATION,ALTERNATION:ALTERNATION,COVER:INDEPENDENT,INDEPENDENT:INDEPENDENT},
            BACKWARD:   {EQUALITY:BACKWARD,   FORWARD:INDEPENDENT,BACKWARD:BACKWARD,   NEGATION:COVER,      ALTERNATION:INDEPENDENT,COVER:COVER,      INDEPENDENT:INDEPENDENT},
            NEGATION:   {EQUALITY:NEGATION,   FORWARD:COVER,      BACKWARD:ALTERNATION,NEGATION:EQUALITY,   ALTERNATION:BACKWARD,COVER:FORWARD,    INDEPENDENT:INDEPENDENT},
            ALTERNATION:{EQUALITY:ALTERNATION,FORWARD:INDEPENDENT,BACKWARD:ALTERNATION,NEGATION:FORWARD,    ALTERNATION:INDEPENDENT,COVER:FORWARD,    INDEPENDENT:INDEPENDENT},
            COVER:      {EQUALITY:COVER,      FORWARD:COVER,      BACKWARD:INDEPENDENT,NEGATION:BACKWARD,   ALTERNATION:BACKWARD,   COVER:INDEPENDENT,INDEPENDENT:INDEPENDENT},
            INDEPENDENT:INDY
      }

      def join(self, rel1, rel2):
            """Given two recognized relations, returns their join
            according to rel_join."""
            for rel in (rel1, rel2):
                  if rel not in JoinTable.rel_join:
                        raise Exception("%s is not a recognized relation" % rel1)
            return JoinTable.rel_join[rel1][rel2]
