# # -*-* encoding:UTF-8 -*-
# import threading
# import time
# arr = [0,0,0,0,0,0,0,0,0,0,0,0]
# class myThread(threading.Thread):
#     def __init__(self,threadId,name,counter):
#         threading.Thread.__init__(self)
#         self.threadId = threadId
#         self.name = name
#         self.counter = counter
#     def run(self):
#         print ("开始线程:",self.name)
#         # 获得锁，成功获得锁定后返回 True
#         # 可选的timeout参数不填时将一直阻塞直到获得锁定
#         # 否则超时后将返回 False
#         threadLock.acquire()
#         print_time(self.name,self.counter,arr.__len__())
#         # 释放锁
#         threadLock.release()
#     def __del__(self):
#         print (self.name,"线程结束！")
# def print_time(threadName,delay,counter):
#     while counter:
#         time.sleep(delay)
#         arr[counter-1] += 1
#         print ("[%s] %s 修改第 %d 个值，修改后值为:%d" % (time.ctime(time.time()),threadName,counter,arr[counter-1]))
#         counter -= 1
# threadLock = threading.Lock()
# threads = []
# # 创建新线程
# thread1 = myThread(1,"Thread-1",1)
# thread2 = myThread(2,"Thread-2",2)
# # 开启新线程
# thread1.start()
# thread2.start()
# # 添加线程到线程列表
# threads.append(thread1)
# threads.append(thread2)
# # 等待所有线程完成
# for t in threads:
#     t.join()
# print("主进程结束！")




import queue as Queue
import threading
import time
 
exitFlag = 0
 
class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print ("Starting " + self.name)
        process_data(self.name, self.q)
        print ("Exiting " + self.name)
 
def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print ("%s processing %s" % (threadName, data))
        else:
            queueLock.release()
        time.sleep(1)
 
threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = Queue.Queue(10)
threads = []
threadID = 1
 
# 创建新线程
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1
 
# 填充队列
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()
 
# 等待队列清空
while not workQueue.empty():
    pass
 
# 通知线程是时候退出
exitFlag = 1
 
# 等待所有线程完成
for t in threads:
    t.join()
print ("Exiting Main Thread")



# import threading
# import time
 
# exitFlag = 0
 
# class myThread (threading.Thread):   #继承父类threading.Thread
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#     def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
#         print ("Starting " + self.name + '\n')
#         print_time(self.name, self.counter, 5)
#         print ("Exiting " + self.name)
 
# def print_time(threadName, delay, counter):
#     while counter:
#         # if exitFlag:
#         #     (threading.Thread).exit()
#         time.sleep(delay)
#         print ("%s: %s" % (threadName, time.ctime(time.time())))
#         counter -= 1
 
# # 创建新线程
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)
 
# # 开启线程
# thread1.start()
# thread2.start()
 
# print ("Exiting Main Thread")