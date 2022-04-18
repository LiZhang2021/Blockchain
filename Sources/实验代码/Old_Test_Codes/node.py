from ast import NotIn
from calendar import c
import operator
from time import time  #导入operator 包,pip install operator
import Crypto.PublicKey.RSA
import Crypto.Signature.PKCS1_v1_5
import Crypto.Hash.SHA256
import random
import collections
import hashlib

from block import Block
from transaction import Transaction


class Node:
    def __init__(self, nodeID, x, y, radius):
         self.nodeID =  nodeID               # 节点的ID
         self.x = x                     # 节点的经度
         self.y = y                     # 节点的纬度
         self.radius = radius           # 节点的通信半径
         self.transactions = None       # 存储交易
         self.blockchain = None         # 存储区块链
         self.nodelist = None           # 存储所有在线邻节点信息
         self.lifetime = 0              # 存储节点的寿命
         self.numblocks = 0             # 存储生成出块节点的数量
         self.stability = 0             # 存储节点的稳定度
         self.busy = 0                  # 记录信道忙碌状态
         self.sendnode = None           # 记录当前发送消息的节点
         self.sendqueue = None          # 记录发送消息的队列——先进先出原则
         self.queuetime = None          # 记录各个消息的发送时间队列——先进先出原则
         self.queuedata = None          # 记录各个数据的具体信息队列——先进先出原则
         self.currentsigns = None       # 记录接收消息的队列——先进先出原则
         self.finalsign = None          # 记录最终签名
         self.currentsign = None        # 记录对当前区块的签名
         self.currentblock = None       # 记录正在处理的区块
         self.currentleader = None      # 记录当前处理区块的首领节点
         self.sybil = 0                 # 记录节点是否是女巫节点
         self.timeout = 0               # 记录出块节点的超时

    # 生成一个交易
    def create_trans(self, ID):
        return Transaction(ID)   # 交易ID
    
    # 生成一个有效区块
    def create_block(self, previous_hash, leaderID, current_transactions):
        block = Block(len(self.blockchain), previous_hash, leaderID, current_transactions)
        combination = str(block.blockID) + str(block.previous_hash) + str(block.leaderID)
        for trans in block.transactions:
            combination = combination + str(trans)
        block.Hash = hashlib.sha256( combination.encode("utf-8")).hexdigest()
        return block

    # 对消息签名
    def RSA_signature(self, data):
        # 获取 数据消息 的HASH值，摘要算法MD5，验证时也必须用MD5
        data = data.encode()
        digest = Crypto.Hash.SHA256.new()
        digest.update(data)
         # 使创建 私钥 签名工具, 并用私钥对HASH值进行签名
        signature = Crypto.Signature.PKCS1_v1_5.new(self.privatekey).sign(digest)
        return signature

    # 验证签名
    def RSA_verifier(public_key,data, signature):
        # 获取 数据消息 的HASH值，签名时采用摘要算法MD5，验证时也必须用MD5
        digest = Crypto.Hash.SHA256.new()
        digest.update(data.encode())
        # 使用Crypto.Signature 中 公钥 验签工具 对 数据和签名 进行验签
        verify_result = Crypto.Signature.PKCS1_v1_5.new(public_key).verify(digest, signature)
        return verify_result
    
    # 验证区块的有效性
    def verify_block(self, block):
        self.blockchain.sort(key = operator.attrgetter('blockID'))
         # 验证出块节点的合法性
        if block.leaderID != self.currentleader:
            print("出块节点失败")
            verify_result = False
         # 验证区块高度的有效性
        elif block.blockID != len(self.blockchain):
            print("区块ID失败")
            verify_result = False
         # 验证父区块hash的有效性
        elif block.previous_hash != self.blockchain[-1].Hash:
            print("父区块哈希失败")
            verify_result = False
         # 验证交易的有效性
        else:
            verify_result = True
        return verify_result
    
    # 同步交易
    def update_transactions(self, block):
        if block.transactions != None:
            btransactions = set(block.transactions)
            # self.transactions = set(self.transactions)
            self.transactions = self.transactions - btransactions

    # 节点同步最新区块链
    def synchronous_blockchain(self, node):
        if len(self.blockchain) < len(node.blockchain):
            self.blockchain = node.blockchain
    
    # 计算节点发送数据所需要的时间
    def commpute_trans_time(self, trans_rate):
        data_type = self.sendqueue[0]
        data = self.queuedata[0]
        # 如果是交易数据， 一个交易的大小设为512B
        if data_type == 'trans':
            t_trans = pow(2, 9)*8 /float(trans_rate)
        # 如果是区块数据，一个区块的大小设为1MB
        elif data_type == 'block':
            if data.transactions == None:
                num_trans = 0
            else:
                num_trans = len(data.transactions)
            t_trans = num_trans * pow(2, 9)*8 /float(trans_rate) + pow(2, 11) /float(trans_rate)
        # 如果是签名数据，一个签名的大小设为1024bit 
        elif data_type == 'sign':
            t_trans = pow(2, 11) /float(trans_rate)
        elif data_type == 'finalsign':
            t_trans = pow(2, 11) /float(trans_rate)
        else:
            t_trans = 0
        return t_trans
    
    # 节点将要发送的消息类型、时间和数据存放到队列中
    def add_trans_message(self, data_type, data, current_time):
        # 存放消息类型
        self.sendqueue.append(data_type)
        # 存放发送消息的时间
        self.queuetime.append(current_time)
        # 存放具体的数据
        self.queuedata.append(data)

    # # 信道忙碌时，随机退避一段时间 R 是信道速率
    def channel_busy(self, trans_rate):
        # 将退避时间与等待时间相加，重设等待时间
        # if len(self.queuetime) > 0:
        # 信道忙碌计数增加
        self.busy += 1
        CW = 10
        backoff_time = self.queuetime[0] + CW * self.busy * 512/float(trans_rate) + random.uniform(0, 0.00512)
        # 对于队列中的时间，如果回退时间大于队列时间，则重置队列时间
        for i in range(len(self.queuetime)):
            if backoff_time > self.queuetime[i]:
                self.queuetime[i] = backoff_time
            else:
                break
    
    # 传输消息成功之后更新本地信息
    def update_information(self, slot, trans_rate):
        # print("传输完成，更新消息")
        # 获取传输消息的信息，并计算传输消息的时间
        data_type = self.sendqueue[0]
        data = self.queuedata[0]
        t_trans = self.commpute_trans_time(trans_rate)
        t_prop =  t_trans  + self.queuetime[0] + random.uniform(0, 0.1536)
        # 更新消息传输完成后发送节点的区块状态
        if data_type == 'finalsign':
            if self.currentleader!= None and self.currentblock != None:
                # self.finalsign = data
                self.currentblock.final_signature = data
                if self.sendqueue[1] == 'sign':
                    del self.sendqueue[1]
                    del self.queuetime[1]
                    del self.queuedata[1]
        # 更新发送节点传输完成之后消息队列时间
        for i in range(len(self.queuetime)):
            if self.queuetime[i] <= t_prop:
                self.queuetime[i] = t_prop
            else:
                break
        # 更新消息传输完成后接收节点的区块状态
        for node in self.nodelist:
            if data_type == 'trans':
                if data in node.transactions:
                    print("已经在交易池中",node.nodeID)
                else:
                    # print("添加交易到交易池中", node.nodeID)
                    node.transactions.add(data)
            elif data_type == 'block':
                if node.currentblock == None:
                    # print("节点接收区块成功", node.nodeID)
                    node.currentblock = data
            elif data_type == 'sign':
                if node.currentsigns == None:
                    node.currentsigns = []
                    node.currentsigns.append(data)
                    # print('第一次接收添加签名成功',node.nodeID)
                else:
                    if data in node.currentsigns:
                        print("已经在签名集合中")
                    else:
                        # print("添加签名到签名池中",node.nodeID)
                        node.currentsigns.append(data)
            elif data_type == 'finalsign':
                if node.currentblock != None:
                    node.finalsign = data
                    node.currentblock.final_signature = data
                    if node.sendqueue[0] == 'finalsign':
                        del node.sendqueue[0]
                        del node.queuetime[0]
                        del node.queuedata[0]
                    if node.sendqueue[1] == 'finalsign':
                        del node.sendqueue[1]
                        del node.queuetime[1]
                        del node.queuedata[1]
                    if node.sendqueue[0] == 'sign':
                        del node.sendqueue[0]
                        del node.queuetime[0]
                        del node.queuedata[0]
                    if node.sendqueue[1] == 'sign':
                        del node.sendqueue[1]
                        del node.queuetime[1]
                        del node.queuedata[1]
            # 更新所有接收节点发送队列的时间和信道状态
            for i in range(len(node.queuetime)):
                r_prop = t_trans + node.queuetime[0] + slot
                if node.queuetime[i] <= r_prop:
                    node.queuetime[i] = r_prop
                else:
                    break
            node.busy = 0
            node.sendnode = None
        # 更新发送节点信道状态和发送队列将已经发送了的消息从列表中删除
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
        
    
