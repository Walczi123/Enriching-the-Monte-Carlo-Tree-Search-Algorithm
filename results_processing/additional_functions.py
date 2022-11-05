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