import redis
from datetime import date
import struct
import zlib
import sys

"""struct
< little-endian
> big-endian
= native
! network

I unsigned int
Q unsigned long long
"""

# for x in [[1,2,3], [1,2,3,4,5,6,7,8,9,10]]:
# 	val = struct.pack("<%dI" % len(x), *x)
# 	val_compress = zlib.compress(struct.pack("<%dI" % len(x), *x))
# 	# val = struct.pack("I" * len(x) , *x)
# 	print(val, len(val), val_compress, len(val_compress))
# 	unpack_val = struct.unpack("<%dI" % (len(val) // 4), val)
# 	unpack_val_decompress = struct.unpack("<%dI" % (len(zlib.decompress(val_compress)) // 4), zlib.decompress(val_compress))
# 	print(unpack_val, unpack_val_decompress)


for x in [['21906702', '22087584', '21935597', '21907929', '21913145', '21948519', '22015885', '21922400', '21908807', '21922539', '21975291', '21880793', '22183629', '22207082', '21908826', '21963358', '21907003', '22093821', '22058565', '22146190', '22053404', '21939815', '21907325', '21906617', '22129098', '22201922', '21931815', '21906845', '21908302', '22212511']]:
	print('size of x', sys.getsizeof(x))
	x = [int(el) for el in x]
	print('size of x after int', sys.getsizeof(x))
	val = struct.pack("<%dI" % len(x), *x)
	print('size of x after struct ', sys.getsizeof(val))
	val_compress = zlib.compress(struct.pack("<%dI" % len(x), *x))
	print('size of x after compress', sys.getsizeof(val_compress))
	# val = struct.pack("I" * len(x) , *x)
	print(val, len(val), val_compress, len(val_compress))
	unpack_val = struct.unpack("<%dI" % (len(val) // 4), val)
	unpack_val_decompress = struct.unpack("<%dI" % (len(zlib.decompress(val_compress)) // 4), zlib.decompress(val_compress))
	print(unpack_val, unpack_val_decompress)


for x in [['21906702', '22087584', '21935597', '21907929', '21913145', '21948519', '22015885', '21922400', '21908807', '21922539', '21975291', '21880793', '22183629', '22207082', '21908826', '21963358', '21907003', '22093821', '22058565', '22146190', '22053404', '21939815', '21907325', '21906617', '22129098', '22201922', '21931815', '21906845', '21908302', '22212511']]:
	print('size of x', sys.getsizeof(x))
	x = "*".join(x)
	print('size of x after join', sys.getsizeof(x))

	# val = struct.pack("<s" , *x)
	val_compress = zlib.compress(x.encode('utf-8'))
	print('size of x after compress', sys.getsizeof(val_compress))
	print(val_compress)

	# unpack_val = struct.unpack("<s" % (len(val) // 4), val)
	unpack_val_decompress = zlib.decompress(val_compress)
	print(unpack_val_decompress)

# r = redis.Redis()

# r.set('foo', bar)
# value = r.get('foo')

# print(value)

def check_rows():
	"""print number of keys in redis

	redis-cli INFO Keyspace | grep ^db
	DBSIZE
	redis-cli KEYS "*" | wc -l

	"""
	r = redis.StrictRedis(host='localhost', port=6379)
	iter = 1000
	print ('Approximately', r.dbsize() * float(sum([r.randomkey().startswith('prefix_') for i in xrange(iter)])) / iter)

def batcher(iterable, n):
	args = [iter(iterable)] * n
	return izip_longest(*args)

for keybatch in batcher(r.scan_iter('user:*'), 500):
	r.delete(*keybatch)

## get all keys from redis
def get_all_keys():
	for key in r.scan_iter("user:*"):
		r.delete(key)

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
