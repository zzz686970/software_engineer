"""冒泡排序
O(N^2)
相邻元素比较，大的数沉底
""" 

def bubble_sort(nums):
	n = len(nums)
	for c in range(n):
		for i in range(1, n - c):
			if nums[i - 1] > nums[i]:
				nums[i-1], nums[i] = nums[i], nums[i-1]

	return nums