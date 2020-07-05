import timeit
import itertools
from copy import deepcopy

def merge_two_dicts(x, y):
	z = x.copy()
	z.update(y)
	return z

def merge_dicts(*dict_args):
	result = {}
	for d in dict_args:
		result.update(d)
	return result

def dict_merge(x, y):
	"""merge nested dicts

	can only merge nested dicts

	Arguments:
		x {dict} -- nested dict
		y {dict} -- nested dict

	Returns:
		[result] -- nested dict
	"""
	z = {}
	overlapping = x.keys() & y.keys()
	for key in overlapping:
		z[key] = dict_merge(x[key], y[key])
	for key in x.keys() - overlapping:
		z[key] = deepcopy(x[key])
	for key in y.keys() - overlapping:
		z[key] = deepcopy(y[key])

	return z

if __name__ == '__main__':
	# z = {k: v for d in (x, y) for k, v in d.items()}
	# z1 = dict(itertools.chain(x.iteritems(), y.iteritems()))
	# z2 = dict((k, v) for d in (x, y) for k, v in d.items())
	# z3 = {**x, **y}