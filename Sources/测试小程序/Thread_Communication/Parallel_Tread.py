from threading import Thread
from datetime import datetime

def thread_func():
    print('我是线程函数：', datetime.now())

def execute_func():
    for i in range(20):
        thread_func()


def multi_thread():
    start = datetime.now()
    print("开始时间", start)
    threads = []
    for i in range(25):
        T = Thread(target=execute_func)
        threads.append(T)
    for T in threads:
        T.start()
        T.join()
    
    period = datetime.now() - start
    print("运行总时间：", period)

if __name__ == '__main__':
    multi_thread()
    