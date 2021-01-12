mysql表类型
- MyISAM
- Heap
- Merge
- INNODB （事务安全存储引擎）
- ISAM （索引舒徐访问）

存储文件表定义，数据文件以及索引文件。


## 事务的特性
- atomic (fail or success)
- consistent (事务的一致性，转账，和不变)
- durable (并发的事务，相互隔离)
- eventual (对数据的改变永久)

## 并发
- 脏读 事务处理读取到另一个未提交数据
- 不可重复读 多次查询返回不同结果，由于时间间隔导致另事务修改并提交了
- 幻读 相同的查询计划，第二次查询返回的结果集跟第一个查询不同；

## 隔离
- 串行化 避免脏读，不可重复读，幻读
- 可重复读 可避免脏读，不可重复读
- 读已提交  可避免脏读
- 读未提交 任何情况无法保证

mysql 默认repeatable read, oracle支持串行化和读已提交，默认为读已提交

## 事务
mysql autocommit 所有数据库更新都会即时提交

set autocommit=0, 那么需要手动commit提交更改，或者使用rollback回滚。、

## 锁
mysql默认行锁
- 表级锁： 开销小，加锁快，不会出现死锁，并发量最低
- 行锁：开销大，加锁慢，会出现死锁，发生冲突的概率小，并发度高


## 索引
保存在额外的文件
提高检索速度，但创建和维护索引需要时间，提高查询速度，减慢写入速度

mysql 索引在存储引擎而不是服务器层实现。

- 普通索引
- 唯一索引
- 主键索引 加速索引+列值唯一+表中只有一个
- 组合索引 多列值组成索引
- 全文索引 文本分词

## Heap 表
不允许blob或者text字段
只能使用比较运算符 = < > => <=
不支持AUTO_INCREMENT
索引不可为NULL
通过max_heap_table_size配置heap表的大小

## Trigger
- before insert
- after insert
- before update
- after update
- before delete
- after delete

## char_length vs length
char_length表示字符，lenght表示字节  
latin字符两个数据是相同的，unicode会出现不同

char值被存储时，被用空格填充到特定长度，检索char需要删除尾随空格。

myisamchk 压缩MyISAM表，减少磁盘或内存使用

federated表：允许访问位于其他服务器数据库上的表

blob和text的唯一区别在于blob值进行排序和比较区分大小写，text值不作区分

mysql_fetch_array 结果行作为关联数组或者来自数据库的常规数组返回
mysql_fetch_object 数据库返回结果行作为对象

## ACL
access control list 与对象关联的权限列表，缓存在内存