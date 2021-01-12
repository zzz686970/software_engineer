"""选择排序
O(N^2)
在未排序的序列中找到最小（大）元素，存放到排序序列的起始位置，然后从剩余未排序元素中继续寻找最小最大元素，放到已经排序序列的末尾。
""" 

def selection_sort(nums):
	n = len(nums)
	for i in range(n):
		for j in range(i, n):
			if nums[i] > nums[j]:
				nums[i], nums[j] = nums[j], nums[i]

	return nums 



