# def getNext(t):
# 	j, i = -1, 0
# 	next = [-1] * len(t)

# 	while i < len(t) - 1:
# 		if j == -1 or t[i] == t[j]:
# 			i, j = i+j, j+1
# 			next[i] = j
# 		else:
# 			j = next[j]

# 	return next

# def KMP(s, t):
# 	next = getNext(t)
# 	j, i = -1, -1
# 	while j != len(t) and i < len(s):
# 		if s[i] == t[j] or j == -1:
# 			i, j = i+1, j+1
# 		else:
# 			j = next[j]

# 	return (i-j, True) if j == len(t) else "None"

# print(KMP("ababxbabcdabdfdsss","abx"))