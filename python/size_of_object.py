import sys
import pickle
import numpy
from pympler import asizeof

asizeof.asizeof(my_object)
"""for third-extension objects, evalute in other methods

A = rand(1000)
A.nbytes
Empty
Bytes  type        scaling notes
28     int         +4 bytes about every 30 powers of 2
37     bytes       +1 byte per additional byte
49     str         +1-4 per additional character (depending on max width)
48     tuple       +8 per additional item
64     list        +8 for each additional
224    set         5th increases to 736; 21nd, 2272; 85th, 8416; 341, 32992
240    dict        6th increases to 368; 22nd, 1184; 43rd, 2280; 86th, 4704; 171st, 9320
136    func def    does not include default args and other attrs
1056   class def   no slots 
56     class inst  has a __dict__ attr, same scaling as dict above
888    class def   with slots
16     __slots__   seems to store in mutable tuple-like structure
                   first slot grows to 48, and so on.

import sys
from types import ModuleType, FunctionType
from gc import get_referents

# Custom objects know their class.
# Function objects seem to know way too much, including modules.
# Exclude modules as well.
BLACKLIST = type, ModuleType, FunctionType

### sum size of object & members.

def getsize(obj):
    if isinstance(obj, BLACKLIST):
        raise TypeError('getsize() does not take argument of type: '+ str(type(obj)))
    seen_ids = set()
    size = 0
    objects = [obj]
    while objects:
        need_referents = []
        for obj in objects:
            if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
                seen_ids.add(id(obj))
                size += sys.getsizeof(obj)
                need_referents.append(obj)
        objects = get_referents(*need_referents)
    return size                   
"""

def get_size(obj ,seen=None):
	"""recursively find size of objects
	
	[description]
	
	Arguments:
		obj {[type]} -- [description]
	
	Keyword Arguments:
		seen {[type]} -- [description] (default: {None})
	"""
	size = sys.getsizeof(obj)
	if seen is None:
		seen = set()
	obj_id = id(obj)
	if obj_id in seen:
		return 0 

	seen.add(obj_id)

	if isinstance(obj, dict):
		size += sum([get_size(v, seen) for v in obj.values()])
		size += sum([get_size(k, seen) for v in obj.keys()])
	elif hasattr(obj, '__dict__'):
		size += get_size(obj.__dict__, seen)
	elif hasattr(obk, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
		size += sum(get_size(i, see) for i in obj)

	return size

def sizeof(obj):
	size = sys.getsizeof(obj)
	if isinstance(obj, dict): return size + sum(map(sizeof(obj.keys()))) + sum(map(sizeof(obj.values())))
	if isinstance(obj, (list, tuple, set, frozenset)): return size + sum(map(sizeof, obj))

size_estimage = len(pickle.dumps(o))