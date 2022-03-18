import  threading
 
event  =  threading.Event()
 
def  a():
     print ( "我是第一个线程函数a，我在等待函数b来触发我..." )
     event.wait()
     print ( "函数a说：尼玛！我被函数b给触发了..." )
 
def  b():
     print ( "我是第二个线程函数b,我开始去触发函数a..." )
     event. set ()
 
p  =  threading.Thread(target = a)
c  =  threading.Thread(target = b)
 
p.start()
c.start()