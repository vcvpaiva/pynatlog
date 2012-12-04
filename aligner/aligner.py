import re

def make_list(s):
    reg_ex = re.compile(r"([\[ ]*)([^\[\] ]+)([\] ])")
    s = re.sub(reg_ex, r'\1"\2"\3', s)
    return eval(s.replace(" ", ", "))

def flatten(iterable):
  it = iter(iterable)
  for e in it:
    if isinstance(e, (list, tuple)):
        for f in flatten(e):
            yield f
    else:
        yield e

def phrase(ls):
    phrase = reduce(lambda x, y: x + y, [x + " " for x in flatten(ls) if re.search("[\(,\),/,A-Z]+",x) == None]).rstrip()
    return phrase

def parse_cat(cat):
    # Parses a category into a python list
    step1 = re.sub(r"([A-Z]+)", r'"\1"', cat)               # add quotes around atoms
    step2 = re.sub(r"\)", r"]", re.sub(r"\(", r"[",step1))  # turn parens into brackets
    step3 = re.sub(r"/", r"],[", step2)                     # break up blocks at slashes
    step4 = "[" + step3 + "]"                               # add outer brackets and return
    return eval(step4)                                      # reify the list

def is_mod(cat):
    # Checks if a category tag is a modifier one
    ls = parse_cat(cat)
    if len(ls) != 2:
        return False
    else:
        a,b = ls
        return a == b

def has_mod(ls):
    # Check if list has a modifier
    if type(ls) != list or (len(ls) == 1 and type(ls[0]) == str):
        return False
    for x in ls:
        if is_mod(x[0]):
            return True
    return False

def lcmp(x,y):
    # Compares the lengths of categories
    return cmp(len(x[0]),len(y[0]))

def is_atom(ls):
    # Check to see if term is atomic
    return len(ls) == 1 and type(ls[0]) == str

def align(ls1,ls2):
    cat1, ds1 = ls1[0], ls1[1:]
    cat2, ds2 = ls2[0], ls2[1:]
    if has_mod(ds1) and has_mod(ds2):
        ds1.sort(lcmp)
        ds2.sort(lcmp)
        return [cat1] + [align(ds1[i],ds2[i]) for i in range(len(ds1))]
    elif has_mod(ds1) and not has_mod(ds2):
        ds1.sort(lcmp)
        if is_atom(ds2):
            ds2 = [[ds1[0][0]] + ds2]
        ds2 = ds2 + [[ds1[1][0], "*"]]
        return [cat1] + [align(ds1[i],ds2[i]) for i in range(len(ds1))]
    elif has_mod(ds2) and not has_mod(ds1):
        ds2.sort(lcmp)
        if is_atom(ds1):
            ds1 = [[ds2[0][0]] + ds1]
        ds1 = ds1 + [[ds2[1][0], "*"]]
        return [cat1] + [align(ds1[i],ds2[i]) for i in range(len(ds1))]
    else:
        # If something is an atom, quit
        if is_atom(ds1) or is_atom(ds2) or (len(ds1) != len(ds2)):
            return [cat2, phrase(ds1)+"/"+phrase(ds2)]
        else:
            # else order the lists for and check if alignable
            old_ds1 = ds1
            old_ds2 = ds2
            ds1.sort(lcmp)
            ds2.sort(lcmp)
            # check category tags to see if alignable
            if reduce(lambda x, y: x and y, [ds1[i][0] == ds2[i][0] for i in range(len(ds1))]):
                return [cat1] + [align(ds1[i],ds2[i]) for i in range(len(ds1))]
            # if not alignable, we quit and use the original ordering we were passed
            else:
                return [cat1, phrase(old_ds1)+"/"+phrase(old_ds2)]

############

#test1 = "[NP dallas]"
#test2 = "[NP [(NP/NP) fat] [NP [(NP/NP) big] [NP dog]]]"
test1 = "[NP pig]"
test2 = "[NP [(NP/NP) small] [NP dog]]"

#shit = "[['(NP/NP)', 'fat'], ['NP', ['(NP/NP)', 'big'], ['NP', 'dog']]]"
#poop = eval(shit)
#poop.sort(lcmp)
#print poop



ex1_ls = make_list(test1)
ex2_ls = make_list(test2)

#print ex1_ls
#print ex2_ls
print align(ex1_ls, ex2_ls)

