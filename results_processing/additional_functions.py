from functools import reduce
from itertools import chain

def join_lists(x):
    return list(chain.from_iterable(x))

def get_positive_values(x):
    return [y for y in x if y > 0]

def get_negative_values(x):
    return [y for y in x if y < 0]

def sum_lists_elemnet_wise(x):
    sums = [sum(i) for i in zip(*x)]
    if sums == []:
        return sums
    s = len(x)
    r = [i/s for i in sums]
    return r

def mean_foreach(x):
    s=0
    for y in x:
       s+= sum(y) 
    return(s/len(x))

def count_foreach_positive(x):
    s=0
    for y in x:
       s+= len([z for z in y if z >0]) 
    return(s/len(x))

def count_foreach_negative(x):
    s=0
    for y in x:
       s+= len([z for z in y if z <0]) 
    return(s/len(x))

def count_foreach_zero(x):
    s=0
    for y in x:
       s+= len([z for z in y if z == 0]) 
    return(s/len(x))

def compose(*functions):
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def sign(number):
    if number > 0 : return 1
    elif number < 0 : return -1
    else : return 0

def get_lenghts_nonnegative_nonpositive_sequences(sequence):
    np = list()
    nn = list()
    pointer = 0
    cnp = 0
    cnn = 0
    for x in sequence:
        s = sign(x)
        if pointer == 0:
            if s == 1:
                pointer = 1
                cnn += 1
                continue
            if s == -1:
                pointer = -1
                cnp += 1
                continue
            if s == 0:
                continue
        if pointer == 1:
            if s >= 0:
                cnn += 1
                continue
            else:
                nn.append(cnn)
                cnn = 0
                pointer = -1
                cnp += 1
                continue
        if pointer == -1:
            if s <= 0:
                cnp += 1
                continue
            else:
                np.append(cnp)
                cnp = 0
                pointer = 1
                cnn += 1
                continue
    if pointer == 1:
        nn.append(cnn)
    if pointer == -1:
        np.append(cnp)
    return nn, np

def mean_foreach_sep(x):
    s=0
    for y in x:
       s+= sum(y)/len(y) 
    return(s/len(x))