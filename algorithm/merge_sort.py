"""归并排序
O(nlogn)  稳定排序，外排序

将数组分成子序列，让子序列有序，再将子序列间有序，合并成有序数组
长度为n的输入序列分成长度为n/2的子序列
对两个子序列采用归并排序
合并所有子序列
""" 

def merge_sort(nums):
	if len(nums) <= 1:
		return nums 

	mid = len(nums) // 2
	left = merge_sort(nums[:mid])
	right = merge_sort(nums[mid:])

	return merge(left, right)

def merge(left, right):
	res = []
	i = 0 
	j = 0 
	while i < len(left) and j < len(right):
		if left[i] <= right[j]:
			res.append(left[i])
			i += 1
		else:
			res.append(right[j])
			j += 1

	res += left[i:]
	res += right[j:]

	return res 

