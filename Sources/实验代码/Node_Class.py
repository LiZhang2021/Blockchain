from calendar import c
import operator
from re import X
from time import time  #导入operator 包,pip install operator
import Crypto.PublicKey.RSA
import Crypto.Signature.PKCS1_v1_5
import Crypto.Hash.SHA256
import random
import collections
import hashlib

from Block_Class import Block
from Trans_Class import Trans


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
         self.queuedata = []            # 记录各个数据的具体信息队列——先进先出原则
         self.receivequeue = []         # 记录接收消息的队列——先进先出原则
         self.busy = 0                  # 记录信道忙碌状态
         self.sendnode = None
         self.maxbusy = 100              # 最大忙碌
         self.lifetime = 0              # 存储节点的寿命
         self.numblocks = 0             # 存储生成出块节点的数量
         self.stability = 0
         self.privatekey = privatekey   # 存储私钥
         self.publickey = publickey     # 存储公钥
         self.finalsign = None          # 记录最终签名
         self.currentsign = None        # 记录对当前区块的签名
         self.currentblock = None       # 记录正在处理的区块
         self.currentleader = None       # 记录当前处理区块的首领节点
    
    # 生成一个交易
    def Create_Trans(self, ID):
        return Trans(ID)   # 交易ID
    
    # 生成一个区块
    def Create_Block(self, previous_hash, leaderID, current_transactions):
        block = Block(len(self.blockchain), previous_hash, leaderID, current_transactions)
        return block
    
    # 计算块的哈希
    def Set_BlockHash(self, block):
        combination = str(block.ID) + str(block.previous_hash) + str(block.leaderID)
        for trans in block.transactions:
            combination = combination + str(trans)
        block.Hash = hashlib.sha256( combination.encode("utf-8")).hexdigest()

    # 对消息签名
    def RSA_Signature(self, data):
        # 获取 数据消息 的HASH值，摘要算法MD5，验证时也必须用MD5
        data = data.encode()
        digest = Crypto.Hash.SHA256.new()
        digest.update(data)
         # 使创建 私钥 签名工具, 并用私钥对HASH值进行签名
        signature = Crypto.Signature.PKCS1_v1_5.new(self.privatekey).sign(digest)
        return signature

    # 验证签名
    def RSA_Verifier(public_key,data, signature):
        # 获取 数据消息 的HASH值，签名时采用摘要算法MD5，验证时也必须用MD5
        digest = Crypto.Hash.SHA256.new()
        digest.update(data.encode())
        # 使用Crypto.Signature 中 公钥 验签工具 对 数据和签名 进行验签
        verify_result = Crypto.Signature.PKCS1_v1_5.new(public_key).verify(digest, signature)
        return verify_result
    
    # 验证区块的有效性
    def Verify_Block(self, block):
        self.blockchain.sort(key = operator.attrgetter('ID'))
         # 验证出块节点的合法性
        if block.leaderID != self.currentleader:
            print("出块节点失败")
            verify_result = False
         # 验证区块高度的有效性
        elif block.ID != len(self.blockchain):
            print("区块ID失败", self.nodeID, block.ID, len(self.blockchain))
            verify_result = False
         # 验证父区块hash的有效性
        elif block.previous_hash != self.blockchain[-1].Hash:
            print("父区块哈希失败")
            verify_result = False
         # 验证交易的有效性
        else:
            verify_result = True
        return verify_result

    # 首领选举
    # 计算节点的稳定度
    def Caculate_Stability(self, K, alpha):
        temp_nodes = self.nodelist
        temp_nodes.append(self)
        temp_nodes.sort(key = operator.attrgetter('nodeID'))
        
        if len(self.blockchain) > K:
            sum_time = 0.0
            # 计算所有节点的剩余时间和
            for node in temp_nodes:
                sum_time = sum_time + node.lifetime
            # 计算每个节点的稳定度
            for node in temp_nodes:
                bratio = round(node.numblocks/K, 4)
                tratio =  round(node.lifetime/sum_time, 4)
                node.stability =  round(alpha * tratio +  (1- alpha) * bratio, 4)
        else:
            sum_time = 0.0
            # 计算所有节点的剩余时间和
            for node in temp_nodes:
                sum_time = sum_time + node.lifetime
            # 计算每个节点的稳定度
            for node in temp_nodes:
                tratio =  round(node.lifetime/sum_time, 4)
                node.stability =  tratio 
        for node in temp_nodes:
            print("节点的剩余时间分别是", node.stability)

    # 构建轮盘并选举首领
    def Leader_Election(self, probability, K, alpha):
        # 计算所有节点的稳定度
        temp_nodes = []
        for rnode in self.nodelist:
            temp_nodes.append(rnode)
        temp_nodes.append(self)
        temp_nodes.sort(key = operator.attrgetter('nodeID'))
        if len(self.blockchain) > K:
            sum_time = 0.0
            # 计算所有节点的剩余时间和
            for node in temp_nodes:
                sum_time = sum_time + node.lifetime
            # 计算每个节点的稳定度
            for node in temp_nodes:
                bratio = round(node.numblocks/K, 4)
                tratio =  round(node.lifetime/sum_time, 4)
                node.stability =  round(alpha * tratio +  (1- alpha) * bratio, 4)
        else:
            sum_time = 0.0
            # 计算所有节点的剩余时间和
            for node in temp_nodes:
                sum_time = sum_time + node.lifetime
            # 计算每个节点的稳定度
            for node in temp_nodes:
                tratio =  round(node.lifetime/sum_time, 4)
                node.stability =  tratio
        # 计算各个节点被选中的概率
        sum_stability = 0
        probs = []
        # 计算所有节点的稳定度之和
        for node in temp_nodes:
            sum_stability = sum_stability + node.stability
        # 计算各个节点被选中的概率
        for node in temp_nodes:
            prob = round(node.stability/sum_stability, 4)
            probs.append(prob)
        # print("概率分别为", probs)
        #构建轮盘
        Disk = [0]
        for i in range(0,len(probs)):
            sum_p = sum(probs[:i+1])
            Disk.insert(i+1, sum_p)
        # print("轮盘为",Disk)
        # 根据区块链最新确认的区块hash选举首领节点
        # seed = self.blockchain[-1].Hash
        # probability = int(seed)/2^(len(seed))
        for lk in range(0, len(probs)):
                if probability >= Disk[lk] and probability < Disk[lk+1]: # 判定随机数是否在节点k的区间中
                    leaderID = lk
                    break
        return leaderID
    
    # 同步交易
    def Synchronous_Transaction(self, block):
        for tx in block.transactions:
            if tx in self.transactions:
                self.transactions.remove(tx)
                # print("删除交易")

    # 同步区块
    def Synchronous_Block(self, block):
        self.blockchain.append(block)

    # 同步系统信息
    def Synchronous_Information(self, leaderID, K):
        # 更新节点信息，包括节点数量、节点ID，节点稳定度（剩余活动时间和共识区块数量）
        if self.nodeID == self.currentblock.leaderID:
            self.numblocks = self.numblocks + 1
        if node.nodeID == node.blockchain[-(K+1)].leaderID:
            node.numblocks = node.numblocks - 1
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
        cdata = self.queuedata[0]
        # 如果是交易数据， 一个交易的大小设为512B
        if data == 'trans':
            t_prop = pow(2, 9)*8 /float(R)
        # 如果是区块数据，一个区块的大小设为1MB
        elif data == 'block':
            num_trans = len(cdata.transactions)
            t_prop = num_trans * pow(2, 9)*8 /float(R)
        # 如果是签名数据，一个签名的大小设为1024bit 
        elif data == 'sign':
            t_prop = pow(2, 11) /float(R)
        elif data == 'finalsign':
            t_prop = pow(2, 11) /float(R)
        return t_prop
    
    # # 信道忙碌时，随机退避一段时间 R 是信道速率
    def channel_busy0(self, R):
        # 将退避时间与等待时间相加，重设等待时间
        if len(self.queuetime) > 0:
            self.busy += 1
            #print("信道忙碌", self. nodeID, self.busy)
            if self.busy < self.maxbusy:
                # 队列中最前的时间是最小的时间 CW = 20
                CW = 10
                backoff_time = self.queuetime[0] + CW * self.busy * 512/float(R) + random.uniform(0, 0.00512)
                # 对于队列中的时间，如果回退时间大于队列时间，则重置队列时间
                for i in range(0, len(self.queuetime)):
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
                self.busy = 1
    # # 信道忙碌时，随机退避一段时间 R 是信道速率
    def channel_busy(self, R):
        # 将退避时间与等待时间相加，重设等待时间
        if len(self.queuetime) > 0:
            self.busy += 1
            #print("信道忙碌", self. nodeID, self.busy)
            # 队列中最前的时间是最小的时间 CW = 20
            CW = 10
            backoff_time = self.queuetime[0] + CW * self.busy * 512/float(R) + random.uniform(0, 0.00512)
            # 对于队列中的时间，如果回退时间大于队列时间，则重置队列时间
            for i in range(0, len(self.queuetime)):
                if backoff_time > self.queuetime[i]:
                    self.queuetime[i] = backoff_time
                else:
                    break
    
    # 传输消息成功之后更新本地信息
    def update_information(self, timeslot, R):
        data = self.sendqueue[0]
        cdata = self.queuedata[0]
        t_prop = self.send_message(R)
        t_trans =  t_prop  + self.queuetime[0] + random.uniform(0, 0.1536)
        # 更新发送节点传输完成之后消息队列时间
        for i in range(0, len(self.queuetime)):
            if self.queuetime[i] <= t_trans:
                self.queuetime[i] = t_trans
            else:
                break
        # 根据接收节点接收消息的类型更新节点的状态
        for node in self.nodelist:
            if data == 'trans':
                if cdata in node.transactions:
                    break
                else:
                    node.transactions.append(cdata)
            elif data == 'block':
                if node.currentblock == None:
                    node.currentblock = cdata
            elif data == 'sign':
                if cdata in node.receivequeue:
                    break
                else:
                    node.receivequeue.append(cdata)
            elif data == 'finalsign':
                    node.finalsign = cdata
                    node.currentblock.final_signature = cdata
                    # print("添加最终签名", node.nodeID)
            else:
                break
            
            # 更新所有接收节点发送队列的时间和信道状态
            for i in range(0,len(node.queuetime)):
                r_trans = t_prop + node.queuetime[0] + timeslot
                if node.queuetime[0] <= r_trans:
                    node.queuetime[i] = r_trans
                else:
                    break
            node.busy = 0
            node.sendnode = None
        # 更新发送节点信道状态和发送队列
        self.busy = 0
        self.queuetime = collections.deque(self.queuetime)
        self.sendqueue = collections.deque(self.sendqueue)
        self.queuedata = collections.deque(self.queuedata)
        self.queuetime.popleft()
        self.sendqueue.popleft()
        self.queuedata.popleft()

    def print_node(self):
        print("Node:", self.nodeID)
        print("Location, radius", self.x, self.y, self.radius)
        print("Send data", len(self.sendqueue))
        print("Send time", len(self.queuetime))
        print("Neighbers", len(self.nodelist))
        print("Receive data", len(self.receivequeue))
        
    
