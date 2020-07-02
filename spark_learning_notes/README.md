
## Why
- 专注计算本身
- 效率。支持交互使用和复杂算法。
- 通用引擎。SQL查询，文本处理，机器学习等
- 接口丰富，配合其他大数据工具使用

Spark vs Hadoop
- 内存计算，交互式查询和流处理

## Spark Core
任务调度、内存管理、错误恢复、存储系统交互

RDD: 分布在多个计算节点可以并行操作的集合

## Spark SQL
HQL查询数据，支持多种数据源，比如Hive, Parquet, JSON

## Spark Streaming
数据流，提供用来操作数据流的API

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