import threading
import time

class thread(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name='线程' + threadname)

    def run(self):
        print('%s:Now timestamp is %s'%(self.name,time.ctime()))

threads = []
for a in range(5):  # 线程个数
    threads.append(thread(str(a)))
for t in threads:  # 开启线程
    t.start()
for t in threads:  # 阻塞线程
    t.join()
print('END')

