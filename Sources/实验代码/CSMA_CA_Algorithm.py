import random
import math
import collections
import operator  #导入operator 包,pip install operator

maxSimulationTime = 50
R = pow(10, 6)

class Node:
    def __init__(self,ID):
        self.nodeid = ID
        self.sendqueue = []         # 记录发送消息的队列——先进先出原则
        self.queuetime = []         # 记录各个消息的发送时间队列
        self.receivequeue = []      # 记录接收消息的队列——先进先出原则
        self.channelstate = 0       # 信道的状态，空闲或者忙碌
    
        # 将发送消息添加到队列，消息可能是交易、区块、签名
    def add_sendqueue(self, data, current_time):
        self.sendqueue.append(data)
        self.queuetime.append(current_time)
        #print("数据和时间分别是", data, arrival_time_sum)

    # 发送交易消息所需要的时间， R是信道速率bps
    def send_message(self, R):
        data = self.sendqueue[0]
        # 如果是交易数据， 一个交易的大小设为512B
        if data == 'trans':
            t_trans = pow(2, 9)*8 /float(R)
        # 如果是区块数据，一个区块的大小设为1MB
        elif data == 'block':
            t_trans = pow(2, 20)*8 /float(R)
        # 如果是签名数据，一个签名的大小设为1024bit 
        elif data == 'sign':
            t_trans = pow(2, 10) /float(R)
        return t_trans
    
    # 信道忙碌 R 是信道速率
    def channel_busy(self, R):
        # 将退避时间与等待时间相加，重设等待时间
        self.channelstate += 1
        print("信道状态", self.channelstate)
        # 队列中最前的时间是最小的时间 CW = 10
        CW = random.randint(0,10)
        backoff_time = self.queuetime[0] + CW* pow(2, self.channelstate) * 512/float(R)
        # 对于队列中的时间，如果回退时间大于队列时间，则重置队列时间
        for i in range(len(self.queuetime)):
            if backoff_time > self.queuetime[i]:
                self.queuetime[i] = backoff_time
            else:
                break
        print("回退后时间：", self.queuetime)

    # 发送消息成功之后更新本地信息
    def update_information(self):
        self.queuetime = collections.deque(self.queuetime)# 先入先出处理消息
        self.queuetime.popleft()
        self.sendqueue = collections.deque(self.sendqueue)
        self.sendqueue.popleft()
        self.channelstate = 0

# 创建节点：N节点数量，A是节点平均包到达率， D是邻节点的距离
def create_nodes(N):
    nodes = []
    for i in range(N):
        nodes.append(Node(i)) 
    return nodes

def transmission(N):
    curr_time = 0   #当前时间
    nodes = create_nodes(N)
    # 添加发送消息
    for node in nodes:
        datas = ['trans', 'block', 'sign']
        for j in range(5):
            data = random.choice(datas)
            node.add_sendqueue(data, curr_time)
    print("传输之前", curr_time)
    for node in nodes:
        print("Node:", node.nodeid)
        print("Send data", node.sendqueue)
        print("Send time", node.queuetime)
        print("Receive data", node.receivequeue) 
    # 传输数据
    while curr_time < maxSimulationTime:
    # Step 1: 从所有节点中选择最小的时间
        min_node = Node(None)  # 随机临时节点
        min_node.queuetime = [float("infinity")] # 输出是 inf
        for node in nodes:
            if len(node.queuetime) > 0:
                min_node = min_node if min_node.queuetime[0] < node.queuetime[0] else node
        print("传输节点", min_node.nodeid)
        # 如果不再发送消息，则终止
        if min_node.nodeid is None:  
            print("消息已经发送完了")
            break
        # 最小时间节点发送一个消息，记录当前时间
        curr_time = min_node.queuetime[0]
        print("当前传输时间",curr_time)
    # Step 2:检查信道是否忙碌
        # 计算节点传输时间和数据发送时间
        for node in nodes:
            # 计算消息传输时间
            t_prop = min_node.send_message(R)
            # 非传输节点在数据传输的过程中感知未来信道是忙碌
            if node.nodeid != min_node.nodeid:
                if len(node.queuetime) > 0:
                    will_busy = True if node.queuetime[0] <= (curr_time + t_prop) else False
                    if will_busy:
                        print("信道繁忙")
                        node.channel_busy(R)
            else:
                # 所有的队列数据包将要在此期间发送的将时间往后推迟，否则不需要做出更改
                for i in range(1,len(node.queuetime)):
                    if (curr_time) <= node.queuetime[i] <= (curr_time + t_prop):
                        node.queuetime[i] = (curr_time + t_prop)
                    else:
                        break
                
    # Step 3: 更新所有节点的最新数据包到达时间，并继续下一个数据
        data = min_node.sendqueue[0]
        #curr_time += maxSimulationTime
        # 发送节点将发送消息队列中的最早的元素删除
        # 接收节点将消息存入接收消息队列中
        for node in nodes:
            if node.nodeid == min_node.nodeid:
                node.update_information()
            else:
                node.receivequeue.append(data)
        # 更新当前的时间
        curr_time += t_prop

    # step 4:传输完成之后输出
    print("完成传输之后", curr_time)
    for node in nodes:
        print("Node:", node.nodeid)
        print("Send data", node.sendqueue)
        print("Send time", node.queuetime)
        print("Receive data", node.receivequeue) 

transmission(10) 




