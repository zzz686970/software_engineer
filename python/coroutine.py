"""协程

子程序或者函数，在所有语言中都是层级调用的，一个线程就是执行一个子程序

子程序调用是一个入口，一次返回，调用顺序是明确的

协程 在执行过程中可以内部中断，执行别的程序，再返回接着执行。

优势：
1. 提升执行效率，子程序切换不是线程切换，而是由程序自身控制，因此没有线程切换的开销。相比多线程，性能优势明显。
2. 不需要多线程的锁机制，不存在写变量冲突，共享资源不加锁，只需要判断状态。

多进程 + 协程
""" 

## 传统生产消费者模型， 一个线程写消息，一个线程获取消息，通过锁机制控制队列和等待，但可能会有死锁出现。
## 改用协程，生产者生产消息，直接通过yield跳转到消费者开始执行，待消费者执行完毕后，切换回生产者继续生产。

"""process

consumer 函数是一个generator
把一个consumer传入produce后，调用next(c) 启动生成器
一旦生产了东西，通过c.send(n) 切换到consumer执行
consumer 通过yield拿到消息，处理，又通过yield把结果传回
producer拿到consumer处理的结果，继续生产下一条消息
produce决定不生产，通过c.close()关闭consumer
整个过程无锁，由一个线程执行，produce和consumer协作完成任务。而非线程的抢占式多任务。
"""

import time 

def consumer():
	r = ''
	while True:
		n = yield r 
		if not n:
			return 
		print(f'consuming {n}')
		time.sleep(1)
		r = '200 OK'

def produce(c):
	next(c)
	n = 0 
	while n < 5:
		n = n + 1
		print(f'producing {n}')
		r = c.send(n)
		print(f'consumer return {r}')

	c.close()

if __name__ == '__main__':
	c = consumer()
	produce(c)