import threading,time

# threading.Condition() 可以理解为更加高级的锁，比 Lock 和 Rlock 的用法更高级，
# 能处理一些复杂的线程同步问题。threading.Condition() 创建一把资源锁（默认是Rlock），
# 提供 acquire() 和 release() 方法，用法和 Rlock 一致。此外 Condition 还提供 wait()、Notify() 和 NotifyAll() 方法。
# wait()：线程挂起，直到收到一个 Notify() 通知或者超时（可选参数），wait() 必须在线程得到 Rlock 后才能使用。
# Notify() ：在线程挂起的时候，发送一个通知，让 wait() 等待线程继续运行，Notify() 也必须在线程得到 Rlock 后才能使用。 Notify(n=1)，最多唤醒 n 个线程。
#NotifyAll() ：在线程挂起的时候，发送通知，让所有 wait() 阻塞的线程都继续运行。

def TestA():
    cond.acquire()
    print('李白：看见一个敌人，请求支援')
    cond.wait()
    time.sleep(2)
    print('李白：好的')
    cond.notify()
    cond.release()

def TestB():
    time.sleep(2)
    cond.acquire()
    print('亚瑟：等我...')
    cond.notify()
    cond.wait()
    time.sleep(2)
    print('亚瑟：我到了，发起冲锋...')

if __name__=='__main__':
    cond = threading.Condition()
    testA = threading.Thread(target=TestA)
    testB = threading.Thread(target=TestB)
    testA.start()
    testB.start()
    testA.join()
    testB.join()
