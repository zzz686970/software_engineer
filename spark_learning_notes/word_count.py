from pyspark import SparkConf, SparkContext 

## 如何连接到集群，单机单线程
## 应用名，在集群管理器的用户界面找到应用
conf = SparkConf().setMaster("local").setAppName("My APP")
sc.SparkContext(conf = conf)

lines = sc.textFile('README.md')
py_lines = lines.filter(lambda line: 'python' in line)
lines.count()
lines.first()

## var lines = sc.textFile('README.md')
## py_lines = lines.filter(line => line.contains("python"))
## lines.count()
## lines.first()

## 关闭spark
## stop()
## sys.exit()

