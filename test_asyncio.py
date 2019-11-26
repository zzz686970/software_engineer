import asyncio

async def compute_square(x):
	await asyncio.sleep(1)
	return x * x

async def square(x):
	print('Square', x)
	# await asyncio.sleep(1)
	res = await compute_square(x)
	print('End square', x)
	# return x * x
	return res

async def when_done(tasks):
	for res in asyncio.as_completed(tasks):
		print('Result', await res)

loop = asyncio.get_event_loop()

# results = loop.run_until_complete(asyncio.gather(square(1), square(2), square(3)))
# print(results)
results = loop.run_until_complete(when_done([square(1), square(2), square(3)]))

loop.close()

