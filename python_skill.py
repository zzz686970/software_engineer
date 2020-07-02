## transpose two-d array

original = [['a','b'], ['c','d'], ['e','f']]
transposed = zip(*original)
# [('a', 'c', 'e'), ('b', 'd', 'f')]
print(list(transposed))


## chained function

print((product if b else add)(5,7))

## shallow copy, reference
## copy list1.copy()
## deepcopy for nested lists: deepcopy(l)
## typecasting a = [1,2], print(list(a))

## sort dict 
from operator import itemgetter
print(sorted(d.items(), key = lambda x: x[1]))
print(sorted(d.items(), key = itemgetter(1)))
print(sorted(d.items(), key = d.get))

## map
print(",".join(map(str, data_list)))


## merge dict
print({**d1, **d2})
print(dict(d1.items() | d2.items()))

print(d1.update(d2))


## index in list

lst = [40, 10, 20, 30]

print(min(range(len(lst)), key = lst.__getitem__))


## remove dup in list
from collections import OrderedDict
print(list(OrderedDict.fromkeys(items_list).keys()))
