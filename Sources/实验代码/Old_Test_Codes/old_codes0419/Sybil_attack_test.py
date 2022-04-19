import random
import math
import Crypto.PublicKey.RSA
import Crypto.Signature.PKCS1_v1_5
import Crypto.Hash.SHA256
import hashlib
import operator

import matplotlib.pyplot as plt
import matplotlib.pyplot as mp

import numpy


from node import Node
from block import Block
from transaction import Transaction

NUM_NODES = 100          # 节点数量
CONFIRM_THRESHOLD = 51  # 区块确认阈值
RADIUS = 200                  # 节点的通信半径
TRANSMISSION_RATE = 1*pow(10, 6)            # 信道传输速率
MAX_SIMULATIOND_TIME = 50 # 仿真时间
MAX_TRANSACTIONS = 2000
SLOT = 512/float(TRANSMISSION_RATE) # 一个包大小为512bit，在当前传输速率下时隙长度
NUM_BLOCKS = 10             # 计算共识比的区块数量
ALPHA = 0.5                         # 稳定度
TIME_OUT = 5
# CONSENSUS_BEGIN_TIME = []
# CONSENSUS_END_TIME = []
# NUM_TRANSACTIONS = []
class Network:
    def __init__(self):
        self.nodes = []         # 记录网络中所有节点
        self.leaderID = None    # 记录当前的首领节点ID
        self.leader = None      # 记录当前首领节点
        self.timeout = 0        # 记录超时
    
    # 创建节点：输入节点数量和通信半径
    def create_nodes(self, num_nodes, radius):
        for i in range(num_nodes):
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
    # 生成一个空区块
    def creat_empty_block(self):
        blockID = len(self.nodes[0].blockchain)
        previous_hash = self.nodes[0].blockchain[-1].Hash
        leaderID = self.leaderID
        current_transactions = None
        empty_block = Block(blockID, previous_hash, leaderID, current_transactions)
        combination = str(empty_block) + str(empty_block.previous_hash) + str(empty_block.leaderID)
        empty_block.Hash = hashlib.sha256( combination.encode("utf-8")).hexdigest()
        return empty_block

    # 根据节点的位置和通信半径确定所有节点的邻节点
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
    def caculate_stability(self, block_threshold, alpha):
        # 对网络中的节点按照节点ID排序
        self.nodes.sort(key = operator.attrgetter('nodeID'))
        # 节点的区块数量大于 K 时，稳定度计算需要活动时间比和共识比；否则稳定度就是节点活动时间比
        if len(self.nodes[0].blockchain) > block_threshold:
            sum_time = 0.0
            # 计算所有节点的剩余时间和
            for node in self.nodes:
                sum_time = sum_time + node.lifetime
            # 计算每个节点的稳定度
            for node in self.nodes:
                bratio = round(node.numblocks/block_threshold, 4)
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
    def leader_election(self, probability, block_threshold, alpha):
        # 计算所有节点的稳定度
        self.caculate_stability(block_threshold, alpha)
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
    def update_information(self, block_threshold):
        # 更新节点信息，包括节点数量、节点ID，节点稳定度（剩余活动时间和共识区块数量）
        for node in self.nodes:
            # 节点的活动时间递减
            node.lifetime -= 1
            # 共识比窗口前移
            if len(node.blockchain) > block_threshold:
                if node.nodeID == node.blockchain[-1].leaderID:
                    node.numblocks += 1
                if node.nodeID == node.blockchain[-(block_threshold+1)].leaderID:
                    node.numblocks -= 1
    # 设置女巫节点的数量
    def set_sybil_nodes(self, gamma):
        num_sybil = len(self.nodes) * gamma
        print("设置女巫节点", num_sybil, gamma)
        for i in range(int(num_sybil)):
            t = random.randint(0,len(self.nodes)-1)
            self.nodes[t].sybil = 1 # 设置为女巫节点
            # print("女巫节点",self.nodes[t].nodeID, self.nodes[t].sybil)
            
     # 传输消息
    def transmission(self, curr_time, slot, trans_rate):
        for node in self.nodes:
            # 查看节点信道是否忙碌
            if node.busy > 0:
                # 查看节点是否是正在传输消息的节点
                if node.sendnode == None:
                    # 如果是传输节点，则需要判定当前时间是否传输完数据
                    t_trans = node.commpute_trans_time(trans_rate) + node.queuetime[0]
                    if curr_time <= t_trans <= (curr_time + slot):
                        # print("传输完成的时间是", node.nodeID, node.sendqueue[0], t_trans)
                        node.busy = 0
                        node.sendnode = None
                        node.update_information(slot, trans_rate)
                        for knode in node.nodelist:
                            knode.sendnode = None
                            knode.busy = 0
                else:
                    if len(node.queuetime) > 0 and curr_time <= node.queuetime[0] < (curr_time + slot):
                        node.channel_busy(trans_rate)
            else:
                # 如果节点认为信道为空，查看自己是否需要发送数据
                if node.queuetime != None:
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
                            node.channel_busy(trans_rate)
                            
                # else:
                    # print("节点没有消息要发送", node.nodeID)

    # 事件处理
    def handle_event(self, curr_time, block_threshold, alpha, confirm_threshold, max_transactions, consensus_begin_time, num_transactions):
        # 确定当前是否有首领节点
        if self.leaderID == None: 
            # 确定当前的首领
            probability = random.uniform(0,1)
            currentleader = self.leader_election(probability, block_threshold, alpha)
            for node in self.nodes:
                node.currentleader = currentleader
                if node.nodeID == currentleader:
                    self.leader = node
            self.leaderID = currentleader
            # print("首领节点是", self.leaderID)
        else:
            # 确定首领之后，看是否生成区块
            if self.leader.currentblock == None:
                if self.leader.sybil == 1:
                    if self.leader.queuetime == None:
                        self.leader.timeout = 0
                    else:
                        self.timeout += SLOT
                    # print("发送时间", self.timeout) 
                    # 诚实节点超时未收到区块，则会创建一个空区块
                    if self.timeout > TIME_OUT:
                        # print("出块节点是女巫节点，生成空区块")
                        # 生成一个空区块
                        curr_block = self.creat_empty_block()
                        self.leader.currentblock = curr_block
                        consensus_begin_time.append(curr_time - TIME_OUT)
                        self.timeout = 0
                        num_transactions.append(0)
                        # print("首领生成区块成功, 交易数量为", self.leader.nodeID, len(current_transactions), curr_time)
                        # 将生成的区块放入发送队列中，优先级最高
                        if self.leader.busy > 0 and self.leader.sendnode == None:
                            self.leader.sendqueue.insert(1, 'block')
                            self.leader.queuetime.insert(1, curr_time)
                            self.leader.queuedata.insert(1, curr_block)
                        else:
                            self.leader.sendqueue.insert(0, 'block')
                            self.leader.queuetime.insert(0, curr_time)
                            self.leader.queuedata.insert(0, curr_block)
                    # 调整所有的消息发送时间
                        for i in range(len(self.leader.queuetime)):
                            if self.leader.queuetime[i] < curr_time:
                                self.leader.queuetime[i] = curr_time                     
                else:
                    # print("出块节点不是女巫节点，生成有效区块")
                    # 查看交易数量是否超过最低阈值
                    if self.leader.transactions!= None and len(self.leader.transactions) >= max_transactions:
                        # 交易池中最多取200个交易，生成区块
                        ntransactions = list(self.leader.transactions)
                        if len(self.leader.transactions) < max_transactions:
                            current_transactions = ntransactions[:len(self.leader.transactions)]
                        else:
                            current_transactions = ntransactions[:max_transactions]
                        curr_block = self.leader.create_block(self.leader.blockchain[-1].Hash, self.leader.currentleader , current_transactions)
                        self.leader.currentblock = curr_block
                        consensus_begin_time.append(curr_time)
                        num_transactions.append(len(current_transactions))
                        # print("首领生成区块成功, 交易数量为", self.leader.nodeID, len(current_transactions), curr_time)
                        # 将生成的区块放入发送队列中，优先级最高
                        # 将生成的区块Hash签名放入发送队列中，优先级次高
                        leader_sign = str(self.leader.nodeID) + '签名区块' + str(self.leader.currentblock.blockID) +'成功'
                        self.leader.currentsign = leader_sign
                        # print("首领生成签名")
                        if self.leader.currentsigns == None:
                            self.leader.currentsigns = []
                            self.leader.currentsigns.append(leader_sign)
                        else:
                            self.leader.currentsigns.append(leader_sign)
                        if self.leader.busy >0 and self.leader.sendnode == None:
                            self.leader.sendqueue.insert(1, 'block')
                            self.leader.queuetime.insert(1, curr_time)
                            self.leader.queuedata.insert(1, curr_block)
                            self.leader.sendqueue.insert(2, 'sign')
                            self.leader.queuetime.insert(2, curr_time)
                            self.leader.queuedata.insert(2, str(self.leader.nodeID) + ' sign')
                        else:
                            self.leader.sendqueue.insert(0, 'block')
                            self.leader.queuetime.insert(0, curr_time)
                            self.leader.queuedata.insert(0, curr_block)
                            self.leader.sendqueue.insert(1, 'sign')
                            self.leader.queuetime.insert(1, curr_time)
                            self.leader.queuedata.insert(1, str(self.leader.nodeID) + ' sign')
                    # 调整所有的消息发送时间
                        for i in range(len(self.leader.queuetime)):
                            if self.leader.queuetime[i] < curr_time:
                                self.leader.queuetime[i] = curr_time  
            else:
                #首领节点已经生成区块了
                # 如果有正在处理的区块，首先需要判定是否有节点接收到该区块的最终签名
                for node in self.nodes:
                    if node.currentblock != None:
                        # 节点接收区块成功之后，开始确认区块
                        if node.finalsign==None:
                        # 节点需要判定区块的签名数量是否达到阈值，如果达到阈值，则生成最终签名
                            if node.currentsigns == None:
                                # print("节点还没有收到任何签名", node.nodeID)
                                node.currentsigns = []
                            else:
                                if len(node.currentsigns) >= confirm_threshold:
                                    # print("节点可以生成最终签名啦", node.nodeID, node.currentleader)
                                    # 节点收集签名的数量达到阈值，则生成当前区块的最终签名
                                    temp_finalsign = 'final signature successful'
                                    node.finalsign = temp_finalsign
                                    if node.sendnode == None and node.busy >0 :
                                        node.sendqueue.insert(1, 'finalsign')
                                        node.queuetime.insert(1, curr_time)
                                        node.queuedata.insert(1, temp_finalsign)
                                        for i in range(len(node.queuetime)):
                                            if node.queuetime[i] < curr_time:
                                                node.queuetime[i] = curr_time
                                    else:
                                        node.sendqueue.insert(0, 'finalsign')
                                        node.queuetime.insert(0, curr_time)
                                        node.queuedata.insert(0, temp_finalsign)
                                        for i in range(len(node.queuetime)):
                                            if node.queuetime[i] < curr_time:
                                                node.queuetime[i] = curr_time
                                else:
                                    # 节点收集签名的数量不够且未曾签名，验证区块的有效性成功之后签名
                                    if node.currentsign == None and node.sybil == 0:
                                            # print("有效区块进行签名")
                                            if node.currentblock != None and node.verify_block(node.currentblock):
                                                if node.sybil == 0:
                                                    # print("生成有效块签名", node.nodeID)
                                                    node.currentsign = str(node.nodeID) + '签名区块' + str(node.currentblock.blockID) +'成功'
                                                    node.currentsigns.append(node.currentsign)
                                                    if node.sendnode == None and node.busy > 0:
                                                        node.sendqueue.insert(1, 'sign')
                                                        node.queuetime.insert(1, curr_time)
                                                        node.queuedata.insert(1, node.currentsign)
                                                    else:
                                                        node.sendqueue.insert(0, 'sign')
                                                        node.queuetime.insert(0, curr_time)
                                                        node.queuedata.insert(0, node.currentsign)
                                                    for i in range(len(node.queuetime)):
                                                        if node.queuetime[i] < curr_time:
                                                            node.queuetime[i] = curr_time
                                            else:
                                                print("节点已经生成签名了或者节点是女巫节点", node.nodeID, node.sybil)

    def run(self, max_transactions, consensus_begin_time, consensus_end_time, num_transactions, num_nodes, confirm_threshold, gamma):
        # 创建节点和创世区块，并且找到所有节点的邻居节点
        self.create_nodes(num_nodes, RADIUS)
        self.set_sybil_nodes(gamma)
        self.create_genesis_block()
        self.find_adjacent_nodes(RADIUS)
        current_time = 0
        num_slots = 0
        print("当前时间", current_time)
        while current_time < MAX_SIMULATIOND_TIME:
            num_slots += 1
            # 每个节点都会生成一个交易
            while num_slots == 4:
                num_slots = 0
                for node in self.nodes:
                    tx_ID = current_time + node.nodeID
                    temp_tx = node.create_trans(tx_ID)
                    if node.transactions == None:
                        node.transactions = set()
                        node.transactions.add(temp_tx)
                    else:
                        node.transactions.add(temp_tx)
                    if node.sendqueue == None:
                        node.sendqueue = []
                        node.sendqueue.append('trans')
                    else:
                        node.sendqueue.append('trans')
                    if node.queuetime == None:
                        node.queuetime = []
                        node.queuetime.append(current_time)
                    else:
                        node.queuetime.append(current_time)
                    if node.queuedata == None:
                        node.queuedata = []
                        node.queuedata.append(temp_tx)
                    else:
                        node.queuedata.append(temp_tx)
            # 计算当前完成区块确认的节点数量
            count = 0
            for node in self.nodes:
                if node.currentleader != None and node.currentblock != None and node.finalsign != None:
                    count += 1
            if count == len(self.nodes):
                if self.leader.sybil == 1:
                    print('所有节点完成了一次空区块确认', current_time, self.nodes[0].blockchain[-1].blockID)
                else:
                    print('所有节点完成了一次有效区块确认', current_time, self.nodes[0].blockchain[-1].blockID)
                self.leader = None
                self.leaderID = None
                self.update_information(NUM_BLOCKS)
                for node in self.nodes:
                    node.blockchain.append(node.currentblock)
                    # 更新交易池中的信息
                    node.update_transactions(node.currentblock)
                    node.currentsigns = None
                    node.finalsign = None
                    node.currentsign = None
                    node.currentblock = None
                    node.currentleader = None
                consensus_end_time.append(current_time)
                # print("当前共识完成时间", consensus_end_time)
            self.handle_event(current_time, NUM_BLOCKS , ALPHA, confirm_threshold, max_transactions, consensus_begin_time, num_transactions)
            self.transmission(current_time, SLOT, TRANSMISSION_RATE)
            current_time += SLOT
        # for node in self.nodes:
        #     print("输出节点信息", node.nodeID, len(node.blockchain))
        # for b in self.nodes[0].blockchain:
        #     b.print_block()

if __name__== '__main__':
    # gammas = [0.1, 0.2, 0.3, 0.4, 0.49]
    gammas = numpy.arange(0.01, 0.50, 0.01)
    latency = []
    throughput = []
    NUM_NODES = 100
    confirm_threshold = int(NUM_NODES/2) + 1
    MAX_TRANSACTIONS = 1024
    for gamma in gammas: 
        gamma = round(gamma,2)    
        N1 = Network()
        CONSENSUS_BEGIN_TIME = []
        CONSENSUS_END_TIME = []
        NUM_TRANSACTIONS = []
        N1.run(MAX_TRANSACTIONS, CONSENSUS_BEGIN_TIME, CONSENSUS_END_TIME, NUM_TRANSACTIONS, NUM_NODES, confirm_threshold, gamma)
        CONSENSUS_LATENCY = list(map(lambda x: x[0]-x[1], zip( CONSENSUS_END_TIME, CONSENSUS_BEGIN_TIME)))
        CONSENSUS_AVERAGE = numpy.mean(CONSENSUS_LATENCY)
        TRANSACTION_AVERAGE = numpy.mean(NUM_TRANSACTIONS)
        # print("开始时间",CONSENSUS_BEGIN_TIME)
        # print("结束时间", CONSENSUS_END_TIME)
        # print("共识时延", CONSENSUS_LATENCY)
        # print("交易数量", NUM_TRANSACTIONS)
        print("节点数量", NUM_NODES)
        print("平均共识时延", CONSENSUS_AVERAGE)
        print("交易数量", TRANSACTION_AVERAGE)
        latency.append(CONSENSUS_AVERAGE)
        throughput.append(round(TRANSACTION_AVERAGE/CONSENSUS_AVERAGE, 4))
    print("女巫节点数量", gammas)
    print("时延数据", latency)
    print("吞吐量数据", throughput)
 
    # 写入数据
    file = open('test_sybil.txt', 'a')
    mid = str(gammas).replace('[', '').replace(']', '')
    # 删除单引号并用字符空格代替逗号
    mid = mid.replace("'", '').replace(',', '') + '\n'
    file.write(mid)
    file.close()

    file = open('test_sybil.txt', 'a')
    mid = str(latency).replace('[', '').replace(']', '')
    # 删除单引号并用字符空格代替逗号
    mid = mid.replace("'", '').replace(',', '') + '\n'
    file.write(mid)
    file.close()

    file = open('test_sybil.txt', 'a')
    mid = str(throughput).replace('[', '').replace(']', '')
    # 删除单引号并用字符空格代替逗号
    mid = mid.replace("'", '').replace(',', '') + '\n'
    file.write(mid)
    file.close()

    # 绘图
    mp.gcf().set_facecolor(numpy.ones(3) * 240/255)#设置背景色
    fig, ax1 = plt.subplots() # 使用subplots()创建窗口
    # 绘制折线图像1, 标签，线宽
    ax1.plot(gammas, latency, c='orangered', label='Latency', linewidth = 1) 
    mp.legend(loc=2)
    ax2 = ax1.twinx() # 创建第二个坐标轴
    ax2.plot(gammas, throughput, c='blue', label='Throughput', linewidth = 1) #同上, 'o-'
    mp.legend(loc=4)
    plt.grid(True)  # 样式风格：网格型
    # ax1.set_title("Double Y axis",size=22)  # 大标题
    ax1.set_xlabel('Number of Nodes',size=18)  
    ax1.set_ylabel('Latency',size=18)
    ax2.set_ylabel('Throughput',size=18)
    # mp.gcf().autofmt_xdate() # 自动适应刻度线密度，包括x轴，y轴
    plt.show()
            


        