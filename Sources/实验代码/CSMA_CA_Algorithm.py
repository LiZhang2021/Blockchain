import random
import math
import collections
import operator  #导入operator 包,pip install operator

maxSimulationTime = 10000
R = 1 * pow(10, 6)

class Node:
    def __init__(self,ID):
        self.nodeid = ID
        self.sendqueue = []         # 记录发送消息的队列——先进先出原则
        self.queuetime = []         # 记录各个消息的发送时间队列
        self.receivequeue = []      # 记录接收消息的队列——先进先出原则
        self.channelstate = 0       # 信道的状态，空闲或者忙碌
    
    # 添加交易消息到发送队列
    def send_trans(self, R):
        # 如果是交易数据，R是信道速率bps 一个交易的大小设为512字节
        t_trans = 512*8 /float(R)
        return t_trans
    
    # 添加区块消息到发送队列，R是信道速率bps 一个区块的大小设为1MB
    def send_block(self,  R):
        # 如果是交易数据，R是信道速率bps 
        t_block = pow(2, 20)*8 /float(R)
        return t_block
    
    # 添加签名消息到发送队列，R是信道速率bps 一个签名的大小设为1024bit 
    def send_sign(self, R):
        t_sign = 1024 /float(R)
        return t_sign

    # 将发送消息添加到队列
    def add_sendqueue(self, data, R):
        packets = []
        arrival_time_sum = 0
        # 当消息到达时间小于最大仿真时间，添加新的包到达时间到包中，并且对包排序
        while arrival_time_sum <= maxSimulationTime:
            if data == 'trans':
                arrival_time_sum += self.send_trans(R)
            elif data == 'block':
                arrival_time_sum += self.send_block(R)
            elif data == 'sign':
                arrival_time_sum += self.send_sign(R)
        self.sendqueue.append(data)
        self.queuetime.append(arrival_time_sum)
        #print("数据和时间分别是", data, arrival_time_sum)
    
    # 将接收消息添加到队列
    def add_receivequeue(self, data):
        print("添加接收消息")
    
    # 信道忙碌 R 是信道速率
    def channel_busy(self, R):
        # 将退避时间与等待时间相加，重设等待时间
        self.channelstate += 1
        # 队列中最前的时间是最小的时间 CW = 10
        backoff_time = self.queuetime[0] + (random.randint(0,10) * (pow(2, self.channelstate) - 1))* 512/float(R)
        # 对于队列中的时间，如果回退时间大于队列时间，则重置队列时间
        for i in range(len(self.queuetime)):
            if backoff_time >= self.queuetime[i]:
                self.queuetime[i] = backoff_time
            else:
                break

    # 发送消息
    def send_message(self):
        collections.deque(self.queuetime)# 先入先出处理消息
        collections.deque(self.sendqueue)
        self.channel_busy = 0

# 创建节点：N节点数量，A是节点平均包到达率， D是邻节点的距离
def create_nodes(N):
    nodes = []
    for i in range(0, N):
        nodes.append(Node(i))
    for node in nodes:
        datas = ['trans', 'block', 'sign']
        for j in range(5):
            data = random.choice(datas)
            node.add_sendqueue(data, R)
    return nodes

""" nodes = create_nodes(2)
for node in nodes:
    print("Node:", node.nodeid)
    print("Send data", node.sendqueue)
    print("Send time", node.queuetime)
    print("Receive data", node.receivequeue) """

def transmission(N):
    curr_time = 0   #当前时间
    nodes = create_nodes(N)
    for node in nodes:
        print("Node:", node.nodeid)
        print("Send data", node.sendqueue)
        print("Send time", node.queuetime)
        print("Receive data", node.receivequeue)
    
    while curr_time < maxSimulationTime:
    # Step 1: 从所有节点中选择最小的时间
        nodes.sort(key = operator.attrgetter('queuetime'))
        print("排序后")
        for node in nodes:
            print("Node:", node.nodeid)
            print("Send data", node.sendqueue)
            print("Send time", node.queuetime)
            print("Receive data", node.receivequeue)
        min_node = Node(None)  # 随机临时节点
        min_node.queuetime = [float("infinity")] # 输出是 inf
        for node in nodes:
            if len(node.queuetime) > 0:
                min_node = min_node if min_node.queuetime[0] < node.queuetime[0] else node
        print("临时节点", min_node.nodeid)
        # 如果不再发送消息，则终止
        if min_node.nodeid is None:  
            print("消息已经发送完了")
            break
        # 最小时间节点发送一个消息，记录当前时间
        curr_time = min_node.queuetime[0]
        print("当前时间",curr_time)
        # Step 2:检查信道是否忙碌
        # 计算节点传输时间和数据发送时间
        
        for node in nodes:
            if node.nodeid != min_node.nodeid and len(node.queuetime) > 0:
                t_prop = 0
                if min_node.sendqueue[0] == 'trans':
                    t_prop = 512*8/float(R) # 512是交易的长度， R是信道速率bps 交易发送时间
                elif min_node.sendqueue[0] == 'block':
                    t_prop = (pow(2,20)*8)/float(R) # 512是交易的长度， R是信道速率bps 交易发送时间
                elif min_node.sendqueue[0] == 'trans':
                    t_prop = 512*8/float(R) # 512是交易的长度， R是信道速率bps 交易发送时间
                print("传输时间：", t_prop)
                # 节点在数据传输的过程中感知未来信道是忙碌
                will_busy = True if node.queuetime[0] <= (curr_time + t_prop) else False
                # 所有的队列数据包将要在此期间发送的将时间往后推迟，否则不需要做出更改
                if curr_time < node.queuetime[0] < (curr_time + t_prop):
                    for i in range(len(node.queuetime)):
                        if (curr_time) < node.queuetime[i] < (curr_time + t_prop):
                            node.queuetime[i] = (curr_time + t_prop)
                        else:
                            break
                if will_busy:
                    print("信道繁忙")
                    node.channel_busy(R)
        # Step 3: 更新所有节点的最新数据包到达时间，并继续下一个数据
        
        data = min_node.sendqueue[0]
        for node in nodes:
            if node.nodeid == min_node.nodeid:
                node.send_message()
            node.receivequeue.append(data)
    print("完成传输之后")
    for node in nodes:
        print("Node:", node.nodeid)
        print("Send data", node.sendqueue)
        print("Send time", node.queuetime)
        print("Receive data", node.receivequeue)

transmission(2)




