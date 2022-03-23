# Thread Communication

线程之间通信的测试小程序

## client_TCP.py

Socket 编程中的客户端程序

## Server_TCP.py

Socket 编程中的服务端程序

## multi_threads_commu.py

多线程消息发送和接收测试程序，模仿QQ

## MultiThread.py

通过线程类实现多线程测试程序

## Parallel_Tread.py

多线程中的线程测试程序

## test.py

线程通信测试程序

## Thread_Condition.py

线程高级的锁，比 Lock 和 Rlock 的用法更高级，能处理一些复杂的线程同步问题。threading.Condition() 创建一把资源锁（默认是Rlock），提供 acquire() 和 release() 方法，用法和 Rlock 一致。此外 Condition 还提供 wait()、Notify() 和 NotifyAll() 方法。
* wait()：线程挂起，直到收到一个 Notify() 通知或者超时（可选参数），wait() 必须在线程得到 Rlock 后才能使用。
* Notify() ：在线程挂起的时候，发送一个通知，让 wait() 等待线程继续运行，Notify() 也必须在线程得到 Rlock 后才能使用。 Notify(n=1)，最多唤醒 $n$ 个线程。
* NotifyAll() ：在线程挂起的时候，发送通知，让所有 wait() 阻塞的线程都继续运行。

## Thread_Event.py

threading.Event() 原理是在线程中立了一个 Flag，默认值是 False ，当一个或多个线程遇到 event.wait() 方法时阻塞，直到 Flag 值 变为 True 。threading.Event() 通常用来实现线程之间的通信，使一个线程等待其他线程的通知 ，把 Event 传递到线程对象中。
* event.wait() ：阻塞线程，直到 Flag 值变为 True
* event.set() ：设置 Flag 值为 True
* event.clear() ：修改 Flag 值为 False
* event.isSet() :  仅当 Flag 值为 True 时返回

## Thread_lock.py

如果多个线程对某一资源同时进行修改，可能会存在不可预知的情况。为了修改数据的正确性，需要把这个资源锁住，只允许线程依次排队进去获取这个资源。当线程A操作完后，释放锁，线程B才能进入。

## Thread_lock1.py

线程锁的测试程序，用threading.Lock() 锁住这个变量，等操作完再释放这个锁。lock.acquire() 给资源加一把锁，对资源处理完成后，lock.release() 再释放锁。

## Thread_Queue.py

采用队列的方式实现线程通信的测试小程序

## Thread_Rock.py

线程锁的测试小程序，使用threading.Lock() 锁住变量，等操作完再释放这个锁。lock.acquire() 给资源加一把锁，对资源处理完成之后，lock.release() 再释放锁。