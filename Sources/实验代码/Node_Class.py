import operator
from re import X
from time import time  #导入operator 包,pip install operator
from Crypto.Signature import pkcs1_15
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
import random
import collections


class Node:
    def __init__(self, nodeID, x, y, radius, privatekey, publickey):
         self.nodeID = nodeID           # 节点的ID
         self.x = x                     # 节点的经度
         self.y = y                     # 节点的纬度
         self.radius = radius           # 节点的通信半径
         self.transactions = []         # 存储交易
         self.blockchain = []           # 存储区块链
         self.nodelist = []             # 存储所有在线邻节点信息
         self.sendqueue = []            # 记录发送消息的队列——先进先出原则
         self.queuetime = []            # 记录各个消息的发送时间队列——先进先出原则
         self.receivequeue = []         # 记录接收消息的队列——先进先出原则
         self.busy = 0                  # 记录信道忙碌状态
         self.sendnode = None
         self.maxbusy = 10              # 最大忙碌
         self.lifetime = 0              # 存储节点的寿命
         self.numblocks = 0             # 存储生成出块节点的数量
         self.privatekey = privatekey   # 存储私钥
         self.publickey = publickey     # 存储公钥
    
    # 生成一个交易
    def Create_Trans(ID):
        return {'Trans_ID: ': ID}   # 交易ID
    
    # 生成一个区块
    def create_Block(self, previous_hash, leaderID, current_transactions):
        block ={
            # 区块ID(Height)
            'ID':len(self.blockchain)+1,
            # 上一块区块的hash
            'previous_hash':previous_hash,
            # 出块节点
            'leaderID':leaderID,
            # 区块的hash
            'Hash': None,
            # 区块最终签名（区块 + 区块Hash + 签名）
            'final_signature': None,
            # 交易账本
            'transactions': current_transactions
        }
        return block
    
    # 对消息签名
    def RSA_Signature(self, data):
        # 获取 数据消息 的HASH值，摘要算法MD5，验证时也必须用MD5
        digest = MD5.new(data.encode('utf-8'))
         # 使创建 私钥 签名工具, 并用私钥对HASH值进行签名
        signature = pkcs1_15.new(self.privatekey).sign(digest)
        return signature

    # 验证签名
    def RSA_Verifier(public_key,data, signature):
        # 获取 数据消息 的HASH值，签名时采用摘要算法MD5，验证时也必须用MD5
        digest = MD5.new(data.encode('utf-8'))
        # 使用Crypto.Signature 中 公钥 验签工具 对 数据和签名 进行验签
        verify_result = pkcs1_15.new(public_key).verify(digest, signature)
        return verify_result
    
    # 验证区块的有效性
    def Verify_Block(self, block, leaderID):
         # 验证出块节点的合法性
        if block.leaderID != leaderID:
            verify_result = False
         # 验证区块高度的有效性
        elif block.ID != len(self.blockchain)+1:
            verify_result = False
         # 验证父区块hash的有效性
        elif block.previous_hash != self.blockchain[-1].hash:
            verify_result = False
         # 验证交易的有效性
        for tx in block.transactions:
            for bc in self.blockchain:
                if tx in bc.transactions:
                    verify_result = False
        else:
            verify_result = True
        return verify_result

    # 首领选举
    # 计算节点的稳定度
    def Caculate_Stability(self, K, alpha, beta):
        sum_time = 0.0
        # 计算所有节点的剩余时间和
        for node in self.nodelist:
            sum_time = sum_time + node.lifetime
        # 计算每个节点的稳定度
        for node in self.nodelist:
            bratio = round(node.bnum/K, 4)
            tratio =  round(node.lifetime/sum_time, 4)
            node.stability =  round(alpha * tratio +  (1- alpha) * bratio, 4)

    # 构建轮盘并选举首领
    def Leader_Election(self):
        # 按照节点的ID进行排序
        self.nodelist.sort(key = operator.attrgetter('nodeID')) 
        sum_stability = 0
        probs = []
        # 计算所有节点的稳定度之和
        for node in self.nodelist:
            sum_stability = sum_stability + node.stability
        # 计算各个节点被选中的概率
        for node in self.nodelist:
            prob = round(node.stability/sum_stability, 4)
            probs.append(prob)
        #构建轮盘
        Disk = [0]
        sum_p = 0
        for prob in probs:
            sum_p = round(sum_p + prob, 4)
            Disk.append(sum_p)
        # 根据区块链最新确认的区块hash选举首领节点
        seed = self.blockchain[-1].hash
        probability = seed/2^(len(seed))
        for k in range(len(probs)):
                if probability >= Disk[k] and probability < Disk[k+1]: # 判定随机数是否在节点k的区间中
                    leaderID = k
                    break
        return leaderID
    
    # 同步交易
    def Synchronous_Transaction(self, block):
        for tx in block.transactions:
            if tx in self.transactions:
                self.transactions.remove(tx)

    # 同步区块
    def Synchronous_Block(self, block):
        self.blockchain.append(block)

    # 同步系统信息
    def Synchronous_Information(self, leaderID, K):
        # 更新节点信息，包括节点数量、节点ID，节点稳定度（剩余活动时间和共识区块数量）
        for node in self.nodelist:
            if node.lifetime == 0:
                self.nodelist.remove(node)
            if node.nodeID == leaderID:
                node.numblocks = node.numblocks + 1
            if node.nodeID ==  node.blockchain[-K].leaderID:
                node.numblocks = node.numblocks - 1
    
    # 注册新节点
    def Regist_Node(self, node):
        if node in self.nodelist:
            print("The node has been there!")
        else:
            self.nodelist.append(node)
            print("Add new node successfully!")

    def add_sendqueue(self, data, current_time):
        self.sendqueue.append(data)
        self.queuetime.append(current_time)
    #print("数据和时间分别是", data, arrival_time_sum)
    
    # 计算两个节点同步他们连接的边（信道）发送数据所需要的时间
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
            t_trans = pow(2, 11) /float(R)
        return t_trans
    
    # # 信道忙碌时，随机退避一段时间 R 是信道速率
    def channel_busy(self, R):
        # 将退避时间与等待时间相加，重设等待时间
        if len(self.queuetime) > 0:
            self.busy += 1
            #print("信道忙碌", self. nodeID, self.busy)
            if self.busy < self.maxbusy:
                # 队列中最前的时间是最小的时间 CW = 10
                CW = random.randint(0,10)
                backoff_time = self.queuetime[0] + CW* (pow(2, self.busy)-1) * 512/float(R) 
                # 对于队列中的时间，如果回退时间大于队列时间，则重置队列时间
                for i in range(len(self.queuetime)):
                    if backoff_time > self.queuetime[i]:
                        self.queuetime[i] = backoff_time
                    else:
                        break
            else:
                # 丢弃数据
                self.queuetime = collections.deque(self.queuetime)# 先入先出处理消息
                self.queuetime.popleft()
                self.sendqueue = collections.deque(self.sendqueue)
                self.sendqueue.popleft()
                self.busy = 0
    
    # 传输消息成功之后更新本地信息
    def update_information(self, curr_time, timeslot, R):
        data = self.sendqueue[0]
        t_prop = self.send_message(R)
        t_trans =  t_prop  + self.queuetime[0] + random.uniform(0, 0.01536)
        for i in range(len(self.queuetime)):
            if self.queuetime[i] <= t_trans:
                self.queuetime[i] = t_trans
            else:
                break
        for node in self.nodelist:
            node.receivequeue.append(data)
            for i in range(len(node.queuetime)):
                r_trans = curr_time + timeslot
                if node.queuetime[0] <= r_trans:
                    node.queuetime[i] = r_trans
                else:
                    break
            node.busy = 0
        self.busy = 0
        self.queuetime = collections.deque(self.queuetime)
        self.sendqueue = collections.deque(self.sendqueue)
        self.queuetime.popleft()
        self.sendqueue.popleft()

    def print_node(self):
        print("Node:", self.nodeID)
        print("Location, radius", self.x, self.y, self.radius)
        print("Send data", self.sendqueue)
        print("Send time", self.queuetime)
        print("Neighbers", len(self.nodelist))
        print("Receive data", self.receivequeue)
        
    
