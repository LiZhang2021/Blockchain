from threading import Thread
from datetime import datetime

def thread_func(name):
    print('我是线程：', name)


def multi_thread():
    threads = []
    for i in range(100):
        T = Thread(target=thread_func, args=[i])
        threads.append(T)
    for T in threads:
        T.start()


if __name__ == '__main__':
    start = datetime.today().now()
    multi_thread()
    period = datetime.today().now() - start
    print("运行总时间：", period)