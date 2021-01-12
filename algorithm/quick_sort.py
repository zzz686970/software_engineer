"""快速排序

O(nlogn), 内排序，不稳定排序
选取一个pivot，将小于pivot的放在左边，大于pivot的放在右边，分割成两部分。这个分区退出以后，该基准处于数列中间，称为partition操作
递归把小于基准的子数列和大于基准元素的子数列排序

""" 

def quick_sort(nums):
	n = len(nums)

	def quick(left, right):
		if left >= right:
			return nums 

		pivot = left 
		i = left 
		j = right 
		while i < j:
			while i < j and nums[j] > nums[pivot]:
				j -= 1
			while i < j and nums[i] < nums[pivot]:
				i += 1

			nums[i], nums[j] = num[j], nums[i]

		## pivot element will be in the middle to split two partitions
		nums[pivot], nums[j] = nums[j], nums[pivot]
		## recursive for sub-partitions
		quick(left, j - 1)
		quick(j+1, right)

		return nums 

	return quick(0, n-1)