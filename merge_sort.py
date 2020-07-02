"""merge sort
It's a stable sort, O(Nlog(N)), space complexity is O(n)
if r > l:
	find the middle point to divide the array into two halves: m = (l+r) // 2
	call merge sort for first half mergesort(arr, 1, m)
	call merge sort for second half mergesort(arr, m+1, r)
	merge the two halves in step 2 and 3
"""

def merge_sort(arr):
	if len(arr) == 1: return arr 
	mid = len(arr) // 2
	left, right = arr[:mid], arr[mid:]
	merge_sort(left)
	merge_sort(right)

	i = j = k = 0
	while i < len(left) and j < len(right):
		if left[i] < right[j]:
			arr[k] = left[i]
			i += 1
		else:
			arr[k] = right[j]
			j += 1

		k += 1

	## check is any element left 
	while i < len(left):
		arr[k] = left[i]
		i += 1
		k += 1
	while j < len(right):
		j += 1
		k += 1

if __name__ == '__main__':
	arr = [12, 11, 13, 5, 6, 7]  
	merge_sort(arr)
	print(arr)