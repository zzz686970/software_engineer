import redis 
from datetime import date 
import struct 
import zlib 

"""struct
< little-endian 
> big-endian
= native
! network

I unsigned int
Q unsigned long long 
"""

for x in [[1,2,3], [1,2,3,4,5,6,7,8,9,10]]:
	val = struct.pack("<%dI" % len(x), *x)
	val_compress = zlib.compress(struct.pack("<%dI" % len(x), *x))
	# val = struct.pack("I" * len(x) , *x)
	print(val, len(val), val_compress, len(val_compress))
	unpack_val = struct.unpack("<%dI" % (len(val) // 4), val)
	unpack_val_decompress = struct.unpack("<%dI" % (len(zlib.decompress(val_compress)) // 4), zlib.decompress(val_compress))
	print(unpack_val, unpack_val_decompress)
# r = redis.Redis()

# r.set('foo', bar)
# value = r.get('foo')

# print(value)

def functions(mappings, key):
	r.mset(mappings)
	r.get(key)

	## add sorted set
	today = date.today()
	visitors = {"dan", "jon", "alex"}
	r.sadd(today, *visitors)
	r.smembers(today.isoformat())
	## {b'dan', b'alex', b'jon'}
	r.scard(today.isoformat())
