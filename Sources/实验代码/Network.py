import random
import math
from time import sleep
import Crypto.PublicKey.RSA
import Crypto.Signature.PKCS1_v1_5
import Crypto.Hash.SHA256
import hashlib
import operator


from node import Node
from block import Block
from transaction import Transaction

threshold_signs = 2
probability = 0.5

class Network:
    def __init__(self):
        self.nodes = []         # 记录网络中所有节点
        self.leaderID = None    # 记录当前的首领节点ID
        self.leader = None      # 记录当前首领节点
    
    # 创建节点
    def create_nodes(self, Num_nodes, radius):
        for i in range(Num_nodes):
            temp_x = random.randint(0, 100)
            temp_y = random.randint(0, 100)
            node = Node(i, temp_x, temp_y, radius)
            node.lifetime = random.randint(10, 400)
            self.nodes.append(node)
    # 生成一个创世区块
    def create_genesis_block(self):
        geneblock = Block(0, 0, None, None)
        combination = str(geneblock.blockID) + str(geneblock.previous_hash) + str(geneblock.leaderID)
        geneblock.Hash = hashlib.sha256( combination.encode("utf-8")).hexdigest()
        for node in self.nodes:
            if node.blockchain == None:
                node.blockchain = []
                node.blockchain.append(geneblock)
            else:
                node.blockchain.append(geneblock)
    
    # 根据节点的位置确定所有节点的邻节点
    def find_adjacent_nodes(self, radius):
        for inode in self.nodes:
            for jnode in self.nodes:
                if jnode.nodeID != inode.nodeID:
                    dis = (pow(inode.x - jnode.x, 2)) + (pow(inode.y - jnode.y, 2))
                    if dis <= pow(radius,2):
                        if inode.nodelist == None:
                            inode.nodelist = []
                            inode.nodelist.append(jnode)
                        else:
                            inode.nodelist.append(jnode)
    # 添加新节点
    def regist_node(self, node):
        if node in self.nodes:
            print("The node has been there!")
        else:
            self.nodes(node)
            print("Add new node successfully!")

    # 首领选举
    # 计算节点的稳定度
    def caculate_stability(self, K, alpha):
        # 对网络中的节点按照节点ID排序
        self.nodes.sort(key = operator.attrgetter('nodeID'))
        # 节点的区块数量大于 K 时，稳定度计算需要活动时间比和共识比；否则稳定度就是节点活动时间比
        if len(self.nodes[0].blockchain) > K:
            sum_time = 0.0
            # 计算所有节点的剩余时间和
            for node in self.nodes:
                sum_time = sum_time + node.lifetime
            # 计算每个节点的稳定度
            for node in self.nodes:
                bratio = round(node.numblocks/K, 4)
                tratio =  round(node.lifetime/sum_time, 4)
                node.stability =  round(alpha * tratio +  (1- alpha) * bratio, 4)
        else:
            sum_time = 0.0
            # 计算所有节点的剩余时间和
            for node in self.nodes:
                sum_time = sum_time + node.lifetime
            # 计算每个节点的稳定度
            for node in self.nodes:
                node.stability =  round(node.lifetime/sum_time, 4) 

    # 构建轮盘并选举首领
    def leader_election(self, probability, K, alpha):
        # 计算所有节点的稳定度
        self.caculate_stability(K, alpha)
        # 根据节点的稳定度计算节点被选中的概率
        sum_stability = 0
        probs = []
        # 计算所有节点的稳定度之和
        for node in self.nodes:
            sum_stability +=  node.stability
        # 计算各个节点被选中的概率
        for node in self.nodes:
            probs.append(round(node.stability/sum_stability, 4))
        #构建轮盘
        Disk = [0]
        for i in range(len(probs)):
            sum_p = sum(probs[:i+1])
            Disk.insert(i+1, sum_p)
        # 根据区块链最新确认的区块hash选举首领节点
        for ID in range(len(probs)):
                if probability >= Disk[ID] and probability < Disk[ID+1]: # 判定随机数是否在节点k的区间中
                    leaderID = ID
                    break
        return leaderID

    # 完成区块确认之后，网络需要更新最新信息
    def upload_information(self, K):
        # 更新节点信息，包括节点数量、节点ID，节点稳定度（剩余活动时间和共识区块数量）
        for node in self.nodes:
            # 节点的活动时间递减
            node.lifetime -= 1
            # 共识比窗口前移
            if node.nodeID == self.currentblock.leaderID:
                self.numblocks += 1
            if node.nodeID == node.blockchain[-(K+1)].leaderID:
                node.numblocks -= 1

     # 传输消息
    def transmission(self, curr_time, slot, R):
        for node in self.nodes:
            # 查看节点信道是否忙碌
            if node.busy > 0:
                # 查看节点是否是正在传输消息的节点
                if node.sendnode == None:
                    # 如果是传输节点，则需要判定当前时间是否传输完数据
                    t_trans = node.commpute_trans_time(R) + node.queuetime[0]
                    if curr_time <= t_trans <= (curr_time + slot):
                        # print("传输完成的时间是", node.nodeID, node.sendqueue[0], t_trans)
                        node.busy = 0
                        node.sendnode = None
                        node.update_information(slot, R)
                        for knode in node.nodelist:
                            knode.sendnode = None
                            knode.busy = 0
                else:
                    if len(node.queuetime) > 0 and curr_time <= node.queuetime[0] < (curr_time + slot):
                        node.channel_busy(R)
            else:
                # 如果节点认为信道为空，查看自己是否需要发送数据
                if len(node.queuetime) > 0:
                    if curr_time <= node.queuetime[0] < (curr_time + slot):
                        sum_busy = 0
                        for rnode in node.nodelist:
                            sum_busy += rnode.busy
                        if sum_busy == 0:
                            # 节点开始传输消息
                            # print('节点传输消息',node.nodeID, node.sendqueue[0])
                            node.sendnode = None
                            node.busy = 1
                            for rnode in node.nodelist:
                                rnode.busy = 1
                                rnode.sendnode = node
                        else:
                            print("有其他节点在传输，信道忙")
                            node.channel_busy(R)
                            
                else:
                    print("节点没有消息要发送", node.nodeID)
    
    # 事件处理
    def handle_event(self, curr_time, K, alpha):
        # 确定当前是否有首领节点
        if self.leaderID == None: 
            # 确定当前的首领
            currentleader = self.leader_election(probability, K, alpha)
            for node in self.nodes:
                node.currentleader = currentleader
                if node.nodeID == currentleader:
                    self.leader = node
            self.leaderID = currentleader
        else:
            # 确定首领之后，看是否生成区块
            if self.leader.currentblock == None:
                # 查看交易数量是否超过最低阈值
                if len(self.leader.transactions) >= 10:
                    # 交易池中最多取200个交易，生成区块
                    ntransactions = list(self.leader.transactions)
                    if len(self.leader.transactions) < 200:
                        current_transactions = ntransactions[:len(self.leader.transactions)]
                    else:
                        current_transactions = ntransactions[:200]
                    curr_block = self.leader.create_block(self.leader.blockchain[-1].Hash, self.leader.currentleader , current_transactions)
                    self.leader.currentblock = curr_block
                    print("首领生成区块成功", self.leader.nodeID)
                    # 将生成的区块放入发送队列中，优先级最高
                    self.leader.sendqueue.insert(0, 'block')
                    self.leader.queuetime.insert(0, curr_time)
                    self.leader.queuedata.insert(0, curr_block)
                    # 将生成的区块Hash签名放入发送队列中，优先级次高
                    leader_sign = str(self.leader.nodeID) + '签名区块' + str(self.leader.currentblock.blockID) +'成功'
                    self.leader.currentsign = leader_sign
                    # print("首领生成签名")
                    if self.leader.currentsigns == None:
                        self.leader.currentsigns = []
                        self.leader.currentsigns.append(leader_sign)
                    else:
                        self.leader.currentsigns.append(leader_sign)
                    self.leader.sendqueue.insert(1, 'sign')
                    self.leader.queuetime.insert(1, curr_time)
                    self.leader.queuedata.insert(1, str(self.leader.nodeID) + ' sign')
                    for i in range(len(self.leader.queuetime)):
                        if self.leader.queuetime[i] < curr_time:
                            self.leader.queuetime[i] = curr_time  
                else:
                    print("交易数量不够，首领节点需要等待...")
            else:
                # 如果有正在处理的区块，首先需要判定是否有节点接收到该区块的最终签名
                for node in self.nodes:
                    if node.currentblock != None:
                        # print("节点还未收到区块")
                    # else:
                        # print('节点收到区块了')
                        if node.currentblock.final_signature != None:
                            print("节点已经确认区块啦", node.nodeID, node.currentblock.blockID)
                            # 如果，则需要将区块添加到本地链上
                            node.blockchain.append(node.currentblock)
                            # 更新交易池中的信息
                            node.update_transactions(node.currentblock)
                            node.currentsigns = None
                            node.finalsign = None
                            node.currentsign = None
                            node.currentblock = None
                            node.currentleader = None
                        else:
                        # 节点需要判定区块的签名数量是否达到阈值，如果达到阈值，则生成最终签名
                            if node.currentsigns == None:
                                # print("节点还没有生成签名")
                                node.currentsigns = []
                            else:
                                if len(node.currentsigns) >= threshold_signs:
                                    print("节点可以生成最终签名啦")
                                    # 节点收集签名的数量达到阈值，则生成当前区块的最终签名
                                    temp_finalsign = 'final signature successful'
                                    node.currentblock.final_signature = temp_finalsign
                                    if node.sendqueue[0] == 'sign':
                                        del node.sendqueue[0]
                                        del node.queuetime[0]
                                        del node.queuedata[0]
                                    if node.sendqueue[1] == 'sign':
                                        del node.sendqueue[1]
                                        del node.queuetime[1]
                                        del node.queuedata[1]
                                    node.sendqueue.insert(1, 'finalsign')
                                    node.queuetime.insert(1, curr_time)
                                    node.queuedata.insert(1, node.finalsign)
                                    for i in range(len(node.queuetime)):
                                        if node.queuetime[i] < curr_time:
                                            node.queuetime[i] = curr_time
                                else:
                                    # 节点收集签名的数量不够且未曾签名，验证区块的有效性成功之后签名
                                    if node.currentsign == None:
                                        # print('节点生成签名了', node.nodeID)
                                        if node.currentblock != None and node.verify_block(node.currentblock):
                                            node.currentsign = str(node.nodeID) + '签名区块' + str(node.currentblock.blockID) +'成功'
                                            node.currentsigns.append(node.currentsign)
                                            node.sendqueue.insert(1, 'sign')
                                            node.queuetime.insert(1, curr_time)
                                            node.queuedata.insert(1, node.currentsign)
                                            for i in range(len(node.queuetime)):
                                                if node.queuetime[i] < curr_time:
                                                    node.queuetime[i] = curr_time

    def run(self):
        pass 



            


        