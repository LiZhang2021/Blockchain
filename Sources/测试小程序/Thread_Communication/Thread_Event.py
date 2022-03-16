import threading
import datetime,time

# threading.Event() 原理是在线程中立了一个 Flag ，
# 默认值是 False ，当一个或多个线程遇到 event.wait() 
# 方法时阻塞，直到 Flag 值 变为 True 。
# threading.Event() 通常用来实现线程之间的通信，
# 使一个线程等待其他线程的通知 ，把 Event 传递到线程对象中。

# event.wait() ：阻塞线程，直到 Flag 值变为 True
# event.set() ：设置 Flag 值为 True
# event.clear() ：修改 Flag 值为 False
# event.isSet() :  仅当 Flag 值为 True 时返回

class thread(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name='线程' + threadname)
        self.threadname = int(threadname)

    def run(self):
        event.wait()
        print('子线程运行时间：%s'%datetime.datetime.now())

if __name__ == '__main__':
    event = threading.Event()
    t1 = thread('0')
    #启动子线程
    t1.start()
    print('主线程运行时间：%s'%datetime.datetime.now())
    time.sleep(2)
    # Flag设置成True
    event.set()
    t1.join()

# threading.active_count()：返回当前存活的线程对象的数量
# threading.current_thread()：返回当前线程对象
# threading.enumerate()：返回当前所有线程对象的列表
# threading.get_ident()：返回线程pid
# threading.main_thread()：返回主线程对象