import time

def time_wrapper(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		start = time.perf_counter()
		# start = time.process_time()
		func_return_val = func(*args, **kwargs)
		end = time.perf_counter()
		print('{0:<10}.{1:<8} : {2:<8}'.format(func.__module__, func.__name__, end - start))
		return func_return_val

	return wrapper

## python3 -m cProfile -s time test.py