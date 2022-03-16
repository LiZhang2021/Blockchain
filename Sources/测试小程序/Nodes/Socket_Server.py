import socket

#默认tcp方式传输
sk=socket.socket()
#绑定IP与端口
ip_port=('210.76.195.10',8888)
#绑定监听
sk.bind(ip_port)
#最大连接数
sk.listen(5)
#不断循环 接受数据
while True:
    #提示信息
    print("正在等待接收数据。。。。")
    #接受数据  连接对象与客户端地址
    conn, address = sk.accept()
    #定义信息
    msg = "连接成功"
    #返回信息
    #注意 python3.x以上，网络数据的发送接收都是byte类型
    #如果发送的数据是str型，则需要编码
    conn.send(msg.encode())
    #不断接收客户端发来的消息
    while True:
        #接收客户端消息
        data = conn.recv(1024)
        print(data.decode())
        #接收到退出指令
        if data == b'exit':
            break
        #处理客户端信息 本实例直接将接收到的消息重新发回去
        conn.send(data)
    #主动关闭连接
    conn.close()