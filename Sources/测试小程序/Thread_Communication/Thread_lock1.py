import threading

# 用 threading.Lock() 锁住这个变量，
# 等操作完再释放这个锁。lock.acquire() 给资源
# 加一把锁，对资源处理完成之后，lock.release() 再释放锁。
money = 0
def Order(n):
    global money
    money = money + n
    money = money - n

class thread(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name='线程' + threadname)
        self.threadname = int(threadname)

    def run(self):
        for i in range(1000000):
            lock.acquire()
            Order(self.threadname)
            lock.release()
#        print('%s:Now timestamp is %s'%(self.name,time.time()))

lock = threading.Lock()
t1 = thread('1')
t2 = thread('5')
t1.start()
t2.start()
t1.join()
t2.join()
print(money)