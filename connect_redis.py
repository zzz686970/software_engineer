import redis
import struct
import zlib

# r = redis.Redis(host = 'integration-redis.guruestate.com',
#                 port = '6379', db = '14', password = None, socket_timeout = None)

key = 'a'
r = redis.Redis(host = 'localhost',
                port = '6379', db = '1', password = None, socket_timeout = None)
mapping = {'a':0, 'b': 5, 'c': 8, 'd': 20}

# with r.pipeline() as pipe:

if r.exists('channel'):
	r.delete('channel')
r.zadd('channel', mapping)
res = r.zrange('channel', 0, -1, withscores=True)
# r.execute()
print(res)


# pipe = r.pipeline()
# if pipe.exists('a'):
#     pipe.delete(key)
# # rank = range(1, len(value_list) + 1)
# pipe.execute()
# # r.zrange()
# redis.zrange(
#             'data_science:aire:{}:similar_property_cf:{}'.format(
#                 country, property_id),
#             0, limit - 1,
#             desc=False,
#             withscores=True
#         )
#         cf_recom = [k[0].decode() for k in cf_recom]



# In [294]: r.zadd('channel', 'a', 0, 'b', 5, 'c', 8, 'd', 20)
# Out[294]: 4

# In [295]: r.zrange('channel', 0, -1, withscores=True)
# Out[295]: [(b'a', 0.0), (b'b', 5.0), (b'c', 8.0), (b'd', 20.0)]
