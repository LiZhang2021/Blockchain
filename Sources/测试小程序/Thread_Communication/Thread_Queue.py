from queue import Queue
import random, threading, time

# 生产者类
class Producer(threading.Thread):
    def __init__(self, name, queue):
        threading.Thread.__init__(self, name=name)
        self.data = queue
    def run(self):
        for i in range(5):
            print("生产者 %s 将产品 %d 加入队列" % (self.name, i))
            self.data.put(i)
            time.sleep(2)
        print("生产者 %s 完成" % self.name)

# 消费者类
class Consumer(threading.Thread):
    def __init__(self, name, queue):
        threading.Thread.__init__(self, name=name)
        self.data = queue
    def run(self):
        for i in range(5):
            val = self.data.get()
            print("消费者 %s 将产品 %d 从队列中取出" % (self.name, val))
            time.sleep(2)
        print("消费者 %s 完成" % self.name)

if __name__ == '__main__':
    print("---主线程开始---")
    queue = Queue()                         # 实例化队列
    producer = Producer("Producer", queue)  # 实例化线程 Producer，并传入队列作为参数
    consumer = Consumer("Consumer", queue)  # 实例化线程 Consumer，并传入队列作为参数
    producer.start()                        # 启动线程 Producer
    consumer.start()                        # 启动线程 Consumer
    producer.join()                         # 等待线程 Producer 结束
    consumer.join()                         # 等待线程 Consumer 结束
    print("---主线程结束---")
