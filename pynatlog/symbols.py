######################################################################
# RELATION SYMBOLS

FORWARD = "<"
BACKWARD = ">"
NEGATION = "^"
ALTERNATION = "|"
COVER = "_"
EQUALITY = "="
INDEPENDENT = "#"

# The set R.
RELS = [FORWARD,BACKWARD,NEGATION,ALTERNATION,COVER,EQUALITY,INDEPENDENT]

# Common functions in R --> R --> R.
IDENT = {}
INDY = {}
for rel in RELS:
      IDENT[rel] = rel
      INDY[rel]  = INDY
      
DEFAULT_PROJ = IDENT

######################################################################


