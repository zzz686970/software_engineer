A distributed process has access to the computational resources across a number of machines connected through a network.


## Hadoop
- distributed very large files across multiple machines. 
- HDFS (Master/Slave node)
> 128MB by default, 3 replicates
> smaller blocks provide more parallelization  
> multiple copies prevent loss of data due to failure of a node. 

## MapReduce
- Job Tracker 
> send code to run on task tracker
- Task Tracker 
> allocate cpu and memory for tasks

## Spark

- mapreduce requires files to be stored in HDFS (read/write)
- spark keeps data in memory after each transformation 


### RDD
- distributed collection of data
- fault-tolerant
- parallel operation - partitioned 
- ability to use many data sources

Driver program (SparkContext) --> Worker Node (Executor (Task))

 



