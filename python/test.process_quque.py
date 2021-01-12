from multiprocessing import Process, Queue
import os, time, random 

def write(q):
	print(f"process to write: {os.getpid()}")
	for value in ['A', 'B', 'C']:
		print(f"put {value} to queue")
		q.put(value)
		time.sleep(random.random())

def read(q):
	print(f"process to read: {os.getpid()}")
	while True:
		value = q.get()
		print(f"get {value} from queue")


if __name__ == '__main__':
	## 创建Queue, 传给各个子进程
	q = Queue()
	pw = Process(target = write, args = (q, ))
	pr = Process(target = read,  args = (q, ))

	## 启动子进程pw
	pw.start()
	## 启动子进程pr
	pr.start()
	## 等待pw结束
	pw.join()

	
	## terminate pr 
	pr.terminate()