import random
import math
from time import sleep
import Crypto.PublicKey.RSA
import Crypto.Signature.PKCS1_v1_5
import Crypto.Hash.SHA256
import hashlib


from cv2 import sqrt
from Node_Class import Node
from Block_Class import Block

threshold1 = 2
probability = 0.5

class Network:
    def __init__(self):
        self.nodes = []     # 记录网络中所有节点
    
    # 创建节点
    def create_nodes(self, Num_nodes, radius):
        for i in range(Num_nodes):
            temp_x = random.randint(0, 100)
            temp_y = random.randint(0, 100)
            key = Crypto.PublicKey.RSA.generate(2048)
            temp_privatekey = key
            temp_publickey = key.publickey()
            node = Node(i, temp_x, temp_y, radius, temp_privatekey, temp_publickey)
            node.lifetime = random.randint(10, 400)
            self.nodes.append(node)

    # 生成一个创世区块
    def Create_GenesisBlock(self):
        geneblock = Block(0, 0, None, None)
        combination = str(geneblock.ID) + str(geneblock.previous_hash) + str(geneblock.leaderID)
        geneblock.Hash = hashlib.sha256( combination.encode("utf-8")).hexdigest()
        for node in self.nodes:
            node.blockchain.append(geneblock)
    
    # 根据节点的位置确定所有节点的邻节点
    def find_adjacent_nodes(self, radius):
        for inode in self.nodes:
            for jnode in self.nodes:
                if inode.nodeID != jnode.nodeID:
                    dis = (pow(inode.x - jnode.x, 2)) + (pow(inode.y - jnode.y, 2))
                    if dis <= pow(radius,2):
                        inode.nodelist.append(jnode)
    
     # 传输消息
    def transmission(self, curr_time, timeslot, R):
        for node in self.nodes:
            # 如果信道忙，找到发送节点，判定是否在当前时隙传输消息完成
            if node.busy > 0:
                if node.sendnode == None:
                    # 如果是传输节点，则需要判定当前时间是否传输完数据
                    t_trans = node.send_message(R) + node.queuetime[0]
                    if curr_time <= t_trans <= (curr_time + timeslot):
                        print("传输完成的时间是", t_trans)
                        node.update_information(curr_time, timeslot, R)
                        node.print_node()
                        for knode in node.nodelist:
                            knode.sendnode = None
                            knode.print_node()
                elif node.sendnode != None and (curr_time <= node.queuetime[0] < (curr_time + timeslot)) and len(node.queuetime) > 0:
                    node.channel_busy(R)
            
            else:
                # 如果节点认为信道为空，查看自己是否需要发送数据
                if len(node.queuetime) > 0:
                    if curr_time <= node.queuetime[0] < (curr_time + timeslot):
                        sum_busy = 0
                        for rnode in node.nodelist:
                            sum_busy += rnode.busy
                        if  sum_busy > 0:
                            print("有其他节点在传输，信道忙")
                            node.channel_busy(R)
                        else:
                            # 节点可以传输消息
                            node.busy = 1
                            node.sendnode = None
                            for rnode in node.nodelist:
                                rnode.sendnode = node
                                rnode.channel_busy(R)
                else:
                    print("节点没有消息要发送", node.nodeID)
    # 传输消息
    def transmission1(self, curr_time, timeslot, R):
        for node in self.nodes:
            """ if node.nodeID == node.currentleader and node.sendqueue[0] == 'block' and node.sendnode != None:
                node.busy = 1
                node.sendnode = None
                node.queuetime[0] = curr_time
                for rnode in node.nodelist:
                    rnode.busy = 1
                    rnode.sendnode = node """
            if len(node.queuetime) > 0 and curr_time <= node.queuetime[0] <= curr_time + timeslot:
                sum_busy = node.busy
                for rnode in node.nodelist:
                    sum_busy += rnode.busy
                if sum_busy > 0:
                    # print('有其他节点在传输数据，信道忙', node.nodeID)
                    node.channel_busy(R)
                else:
                    # print("信道空闲，开始发送信道变得忙碌", node.nodeID)
                    node.busy = 1
                    node.sendnode = None
                    for rnode in node.nodelist:
                        rnode.sendnode = node
                        rnode.busy = 1
            elif node.busy > 0 and node.sendnode == None:
                # 找到正在传输的发送节点，计算当前时间是否能够传输完成
                if node.nodeID == node.currentleader:
                    print("首领节点传输数据", node.nodeID)
                t_trans = node.send_message(R) + node.queuetime[0]
                if curr_time <= t_trans <= (curr_time + timeslot):
                    print("当前节点发送完成，时间是", t_trans)
                    node.update_information(curr_time, timeslot, R)
                    # node.print_node()
                    node.busy = 0
                    for knode in node.nodelist:
                        knode.sendnode = None
                        # knode.print_node() 
                        node.busy = 0 
            elif len(node.queuetime) == 0:
                print("节点没有消息要发送", node.nodeID)
    
    # 事件处理
    def handle_event(self, curr_time, K, alpha):
        # 每个时隙每个节点都会生成一个交易，并且将交易添加到交易池和发送队列中
        for node in self.nodes:
            tx_ID = curr_time + node.nodeID
            temp_tx = node.Create_Trans(tx_ID)
            node.transactions.append(temp_tx)
            node.sendqueue.append('trans')
            node.queuetime.append(curr_time)
            node.queuedata.append(temp_tx)
        # 判定当前是否已经存在首领节点
        for node in self.nodes:
            if node.currentleader == None and node.currentblock == None:
                # 没有首领节点和正在处理的区块，需要先确定当前轮的首领节点
                node.Caculate_Stability(K, alpha)
                LeaderID = node.Leader_Election(probability)
                node.currentleader = LeaderID
                print("节点选出的首领节点是", node.nodeID, LeaderID)
            if node.currentleader != None and node.currentblock == None:
                # 首领节点创建区块
                if node.nodeID == node.currentleader :
                    # 交易池中最多取2000个交易，生成区块
                    if  10<= len(node.transactions) < 2000:
                        current_transactions = node.transactions
                    else:
                        current_transactions = node.transactions[:2000]
                    curr_block = node.Create_Block(node.blockchain[-1].Hash, node.currentleader , current_transactions)
                    node.Set_BlockHash(curr_block)
                    node.currentblock = curr_block
                    # node.receivequeue.append(curr_block)
                    # 将生成的区块放入发送队列中，优先级最高
                    node.sendqueue.insert(0, 'block')
                    node.queuetime.insert(0, curr_time)
                    node.queuedata.insert(0, curr_block)
                    # 将生成的区块Hash签名放入发送队列中，优先级次高
                    block_hash_sign= node.RSA_Signature(curr_block.Hash)
                    node.currentsign = block_hash_sign
                    node.receivequeue.append(block_hash_sign)
                    node.sendqueue.insert(1, 'sign')
                    node.queuetime.insert(1, curr_time)
                    node.queuedata.insert(1, block_hash_sign)
                    for i in range(len(node.queuetime)):
                        if node.queuetime[i] < curr_time:
                            node.queuetime[i] = curr_time
                    node.busy = 1
                    node.sendnode = None
                    for rnode in node.nodelist:
                        rnode.busy = 1
                        rnode.sendnode = node
                        for i in range(len(rnode.queuetime)):
                            if rnode.queuetime[i] < curr_time:
                                rnode.queuetime[i] = curr_time
            if node.currentleader != None and node.currentblock != None:
                # 如果有正在处理的区块，首先需要判定是否接收到该区块的最终签名
                if node.finalsign != None:
                    # 接收到最终签名则将区块添加到区块链上，并删除节点交易池中已经上链的交易
                    node.blockchain.append(node.receivequeue[0])
                    node.Synchronous_Transaction(node.receivequeue[0])
                    if node.nodeID == node.currentleader:
                        node.numblocks = node.numblocks + 1
                    if node.nodeID == node.blockchain[-(K+1)].leaderID:
                        node.numblocks = node.numblocks -1
                    node.receivequeue = []
                    node.final_signature = None
                    node.currentsign = None
                    node.currentblock = None
                    node.currentleader = None
                else:     
                # 节点需要判定区块的签名数量是否达到阈值，如果达到阈值，则生成最终签名
                    if len(node.receivequeue) >= threshold1:
                        # 节点收集签名的数量达到阈值，则生成当前区块的最终签名
                        combination_sign = node.currentblock.Hash + str(2)
                        node.finalsign = node.RSA_Signature(combination_sign)
                        node.sendqueue.insert(0, 'finalsign')
                        node.queuetime.insert(0, curr_time)
                        node.queuedata.insert(0, node.finalsign)
                    else:
                        # 节点收集签名的数量不够且未曾签名，验证区块的有效性成功之后签名
                        if node.currentsign == None:
                            if node.Verify_Block(node.currentblock):
                                node.currentsign = node.RSA_Signature(curr_block.Hash)
                                node.receivequeue.append(node.currentsign)
                                node.sendqueue.append( 'sign')
                                node.queuetime.append( curr_time)
                                node.queuedata.append(1, node.currentsign)
                            




            


        