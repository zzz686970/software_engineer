import random
## directly generate unique numbers, notice population is huge
res = random.sample(range(1000), 1000)
assert len(res) == len(set(res))
lst = list(range(100))
random.shuffle(lst)
print(lst[:10])

## sample extremely large numbers, cannot use range



## generate a list 0 ~ n-1

def generate_unique_arr(n, k):
	arr = [i for i in range(n)]
	i = 0
	while i < k:
		t = random.randint(0,n-i-1) + i
		## exchange value for index i and t
		# make sure x[i] exchange with x[t] where t is between i to n-1
		arr[i], arr[t] = arr[t], arr[i]
		i += 1

	return arr[:5]

print(generate_unique_arr(6, 5))