import random
import collections

# 边的类
class Edge:
    def __init__(self, sender, receiver, R):
        self.sendnode = sender      # 记录发送节点
        self.receivennode = receiver# 记录接收节点
        self.sendmsg = 0            # 记录信道发送状态
        self.receivemsg = 0         # 记录信道接收状态
        self.collision = 0          # 记录信道冲突状态
        self.busy = 0               # 记录信道忙碌状态
        self.rate = R               # R是信道速率bps
    
    # 计算两个节点同步他们连接的边（信道）发送数据所需要的时间
    def send_message(self):
        data = self.sendqueue[0]
        # 如果是交易数据， 一个交易的大小设为512B
        if data == 'trans':
            t_trans = pow(2, 9)*8 /float(self.R)
        # 如果是区块数据，一个区块的大小设为1MB
        elif data == 'block':
            t_trans = pow(2, 20)*8 /float(self.R)
        # 如果是签名数据，一个签名的大小设为1024bit 
        elif data == 'sign':
            t_trans = pow(2, 11) /float(self.R)
        return t_trans
    
    # # 信道忙碌时，随机退避一段时间 R 是信道速率
    def channel_busy(self):
        # 将退避时间与等待时间相加，重设等待时间
        self.busy += 1
        print("信道忙碌", self.busy)
        # 队列中最前的时间是最小的时间 CW = 10
        CW = random.randint(0,10)
        backoff_time = self.queuetime[0] + CW* pow(2, self.busy) * 512/float(self.R)
        # 对于队列中的时间，如果回退时间大于队列时间，则重置队列时间
        for i in range(len(self.queuetime)):
            if backoff_time > self.queuetime[i]:
                self.queuetime[i] = backoff_time
            else:
                break
        print("回退后时间：", self.queuetime)
    
    # 信道冲突时，将在传输结束之后重传数据 R 是信道速率
    def channel_collision(self):
        self.collision += 1
        print("节点接收消息冲突", self.receivennode.nodeID, self.collision)
        t_trans = self.send_message()
        t_time = self.sendnode.queuetime[0] + t_trans
        # 对于队列中的时间，如果传输时间大于队列时间，则重置队列时间
        for i in range(len(self.sendenode.queuetime)):
            if t_time > self.sendenode.queuetime[i]:
                self.sendenode.queuetime[i] = t_time
            else:
                break
        print("冲突后时间：", self.sendnode.queuetime)
    
    # 传输消息成功之后更新本地信息
    def update_information(self):
        data = self.sendenode.sendqueue[0]
        self.sendenode.queuetime = collections.deque(self.sendenode.queuetime)# 先入先出处理消息
        self.sendenode.queuetime.popleft()
        self.sendenode.sendqueue = collections.deque(self.sendenode.sendqueue)
        self.sendenode.sendqueue.popleft()
        self.receivennode.receivequeue.append(data)
        self.collision = 0
        self.busy = 0

        