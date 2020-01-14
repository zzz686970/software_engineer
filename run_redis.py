import redis 
from datetime import date 

r = redis.Redis()

r.set('foo', bar)
value = r.get('foo')

print(value)

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
