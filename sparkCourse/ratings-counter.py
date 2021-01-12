from pyspark import SparkConf, SparkContext 
import collections

conf = SparkConf().setMaster('local').setAppName('RatingsHistogram')
sc = SparkContext(conf = conf)

lines = sc.textFile("/Users/zhizhong/Documents/PyProject/software_engineer/sparkCourse/ml-100k/u.data")
ratings = lines.map(lambda x: x.split()[2])

result = ratings.countByValue()

sortedResults = collections.OrderedDict(sorted(result.items()))
for key, val in sortedResults.items():
	print(key, val)