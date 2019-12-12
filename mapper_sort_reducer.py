"""
mapper
"""

import sys
for line in sys.stdin:
	line = line.strip()
	words = line.split()
	for word in words:
		# print(f'{word}, 1')
		print >> sys.stdout, '%s\t%s' %(word, 1)


"""reducer

read from stdin
"""
from operator import itemgetter
import sys
prev_word = None
prev_count = 0

for line in sys.stdin:
	line = line.strip()
	## only split the first tab delimiter
	word, count = line.split('\t', 1)
	try:
		count = int(count)
	except ValueError:
		continue

	if prev_word == word:
		prev_count += count
	else:
		## for initial start
		if prev_word:
			print(f"{prev_word}\t{prev_count}")

		prev_count = count
		prev_word = word

## last word if same as previous one
if prev_word == word:
	print(f"{prev_word}\t{prev_count}")


"""
test

cat test.file | mapper.py | sort -k1, 1 | reducer.py

## copy from local
bin/hadoop dfs -copyFromLocal /test.txt /user/zhizhong/test_folder

bin/hadoop jar contrib/streaming/hadoop-*streaming*.jar \
-file mapper.py    -mapper mapper.py \
-file reducer.py   -reducer reducer.py \
-input /user/zhizhong/test_folder/* -output /user/zhizhong/output

"""


### version 2.0
# group by using hadoop
# take advantage of yield

## mapper.py

import sys
def read_input(file):
	for line in file:
		yield line.split()

def main(separator='\t'):
	data = read_input(sys.stdin)
	for words in data:
		for word in words:
			print(f"{word}{separator},1")

if __name__ == '__main__':
	main()


## reducer.py
from itertools import groupby
from operator import itemgetter
import sys

def read_mapper_output(file, separator='\t'):
	for line in file:
		yield line.rstrip().split(separator, 1)

def main(separator='\t'):
	data = read_mapper_output(sys.stdin, separator=separator)
	for current_word, group in groupby(data, itemgetter(0)):
		try:
			total_count = sum(int(count) for current_word, count in group)
			print(f"{word}{separator},{total_count}")
		except ValueError:
			pass

if __name__ == '__main__':
	main()



