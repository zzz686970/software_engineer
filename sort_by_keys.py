from bisect import bisect_left, insort_left

"""insert key into dict and keep the order

Insert item x in list a, and keep it sorted assuming a is sorted.

    If x is already in a, insert it to the left of the leftmost x.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
"""

def my_insort_left(a, x, lo = 0, hi = None):
	x_key = x[1]
	if lo < 0:
		raise ValueError('lo must be non-negative')

	if hi is None:
		hi = len(a)

	while lo < hi:
		mid = (lo + hi) // 2
		if a[mid][1] < x_key: lo = mid + 1
		else: hi = mid 

	a.insert(lo, x)

if __name__ == '__main__':
	my_insort_left(data, ('brown', 7))


