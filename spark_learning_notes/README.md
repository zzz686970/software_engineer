## Why
- 专注计算本身
- 效率。支持交互使用和复杂算法。
- 通用引擎。SQL查询，文本处理，机器学习等
- 接口丰富，配合其他大数据工具使用

Spark vs Hadoop
- 内存计算，交互式查询和流处理

![spark](architecture.png?raw=true "Title")

## Spark Core
任务调度、内存管理、错误恢复、存储系统交互，对弹性分布式数据的API定义

RDD: 分布在多个计算节点可以并行操作的集合，分布式数据集

## Spark SQL
HQL查询数据，支持多种数据源，比如Hive, Parquet, JSON

## Spark Streaming
数据流，提供用来操作数据流的API
> 网页服务器日志，用户提交状态更新组成的消息队列

## MLib
分类回归、聚类、协同过滤

## GraphX
并行图计算，穿件一个顶点和边都包含任意属性的有向图  
常用图算法（PageRank 三角计数）  
图分割的subgraph和操作所有顶点的mapVertices

## 集群管理器
高效计算一个节点到数千个计算节点之间伸缩计算，包括Hadoop YARN, Apache Mesos, 以及Spark自带的简易调度器  


## 应用
日志文件处理 

实时分析

## example
```py
from pyspart import SparkContext
sc = SparkContext('local')
nums = sc.parallelize([[1,2,3],[4,5,6],[7,8,9],[10,11,12,13]])
nums = nums.flatMap(lambda x:[(a,1) for a in x])
result = nums.reduce(lambda x, y: x[0]+y[0], x[1] + y[1])
result = 1.0 * result[0] / result[1]

## aggregate way
## aggregate （初始化累加器，累加器与每个值操作，累加器之间操作）
nums = sc.parallelize([[1,2,3],[4,5,6],[7,8,9],[10,11,12,13]])
nums = nums.flatMap(lambda x:[a for a in x]) #把每个值提取出来
result = nums.aggregate((0,0),  #设置累加器初始值
                        (lambda acc,value: (acc[0]+value,acc[1]+1)),
                        (lambda acc1,acc2: (acc1[0]+acc2[0],acc1[1]+acc2[1]))
                        )
result = 1.0*result[0]/result[1]

```

## 原理
1. 每一个Spark由driver program发起集群的并行操作，驱动器程序包含应用的main函数，定义了集群的分布式数据集，还对这些分布式数据集应用了相关操作。
spark shell本身就是驱动器程序。
1. 初始化SparkContext对象访问Spark，用该对象连接计算机群。shell启动它自动会创建这个对象，命名为sc。
1. 在此基础上创建RDD。sc.textFile(),然后进行操作。

> 驱动器管理多个executor节点，如果在集群上操作，不同节点会统计文件的不同部分的行数。本地模式下，所有工作会在单个节点执行。  
> 驱动器程序 -->  工作节点（执行器 --> 任务）  

python脚本需要spark自带的bin/spark-submit脚本来运行，会导入spark依赖。

```
bin/spark-submit my_script.py
```


