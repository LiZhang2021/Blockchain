# 模仿qq  同时可以发送信息和接受信息多线程


from socket import *
from time import sleep
import threading

# 负责接收数据
def recvData():
    udpRecvSocket = socket(AF_INET,SOCK_DGRAM)
    # 默认使用8080端口
    myRecvPort = 8080
    bindAddr = ('',8080)
    #try为了防止端口被占用  如果被占用有一次的修改机会  反正系统就被崩溃
    try:
        #绑定地址
        udpRecvSocket.bind(bindAddr)
    #端口被占用后的修改
    except OSError:
        myRecvPort = int(input("请输入本机接受端口端口："))
        bindAddr = ('',myRecvPort)
        udpRecvSocket.bind(bindAddr)
    #socket模块中自带的方法 用来获取用户名和ip地址
    myIpAddr = gethostbyname(getfqdn(gethostname()))
    #打印本机ip地址和所用的端口
    print("本机ip地址为[{}]，接受数据的端口为[{}]".format(myIpAddr,myRecvPort))

    #防止受到的消息部分丢失而引发的异常问题
    while True:
        try:
            recvData = udpRecvSocket.recvfrom(1024)  #最大字节数为1024
            #recvData = recvData.decode('GB2312')
            print('对方电脑输出的内容是：{}'.format(recvData))
        except error as e:
            print(e)


#负责发送数据
def sendData():
    #防止和上文同时输入产生风险  所以发送数据暂停10秒后再运行
    sleep(10)
    udpSendSocket = socket(AF_INET,SOCK_DGRAM)
    #用户输入接受方信息并存储在 sendAddr 中
    sendIpAddr = input('请输入接受方的ip地址：')
    sendPort = int(input('请输入接受方的端口：'))
    sendAddr = (sendIpAddr,sendPort)


    while True:
        sendData = input('请输入要发送的内容：')
        udpSendSocket.sendto(sendData.encode(),sendAddr)


#负责多线程
def main():
    #多线程同时运行两个方法
    t1 = threading.Thread(target=recvData)
    t2 = threading.Thread(target=sendData)
    t1.start()
    t2.start()
    t1.join()
    t2.jion()


if __name__ == '__main__':
    main()
