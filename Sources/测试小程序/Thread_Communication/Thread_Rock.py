import threading

# 用法和 threading Lock() 一致，区别是 threading.Rlock() 允许多次锁资源，
# acquire() 和 release() 必须成对出现，也就是说加了几把锁就得释放几把锁。
lock = threading.Lock()
# 死锁
lock.acquire()
lock.acquire()
print('...')
lock.release()
lock.release()

rlock = threading.RLock()
# 同一线程内不会阻塞线程
rlock.acquire()
rlock.acquire()
print('...')
rlock.release()
rlock.release()