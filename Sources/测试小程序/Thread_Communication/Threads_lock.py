import threading
# 如果多个线程对某一资源同时进行修改，可能会存在不可预知的情况。
# 为了修改数据的正确性，需要把这个资源锁住，只允许线程依次排队
# 进去获取这个资源。当线程A操作完后，释放锁，线程B才能进入。
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
            Order(self.threadname)

t1 = thread('1')
t2 = thread('5')
t1.start()
t2.start()
t1.join()
t2.join()
print(money)