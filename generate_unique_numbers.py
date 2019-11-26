import random
## directly generate unique numbers, notice population is huge
print(random.sample(range(100), 10))
lst = list(range(100))
random.shuffle(lst)
print(lst[:10])

##


## generate a list 0 ~ n-1

def generate_unique_arr(n, k):
	arr = [i for i in range(n)]
	i = 0
	while i < k:
		t = random.randint(0,n-i-1) + i
		## exchange value for index i and t
		arr[i], arr[t] = arr[t], arr[i]
		i += 1

	return arr[:5]

print(generate_unique_arr(6, 5))