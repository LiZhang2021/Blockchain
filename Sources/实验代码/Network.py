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

threshold1 = 25
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
                if jnode.nodeID != inode.nodeID:
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
            if node.busy > 0:
                if node.sendnode == None:
                    # 如果是传输节点，则需要判定当前时间是否传输完数据
                    t_trans = node.send_message(R) + node.queuetime[0]
                    if curr_time <= t_trans <= (curr_time + timeslot):
                        # print("传输完成的时间是", node.nodeID, node.sendqueue[0], t_trans)
                        node.busy = 0
                        node.sendnode = None
                        node.update_information(timeslot, R)
                        for knode in node.nodelist:
                            knode.sendnode = None
                            knode.busy = 0
                else:
                    if len(node.queuetime) > 0 and curr_time <= node.queuetime[0] < (curr_time + timeslot):
                        node.channel_busy(R)
                        # print("信道忙", node.nodeID, node.queuetime[0], node.sendnode.nodeID)
            else:
                # 如果节点认为信道为空，查看自己是否需要发送数据
                if len(node.queuetime) > 0:
                    if curr_time <= node.queuetime[0] < (curr_time + timeslot):
                        sum_busy = 0 + node.busy
                        for rnode in node.nodelist:
                            sum_busy += rnode.busy
                        if sum_busy == 0:
                            # print("节点开始传输消息", node.nodeID, node.sendqueue[0])
                            # if node.sendqueue[0]=='block':
                                # print("正在传输区块中交易数量为", len(node.queuedata[0].transactions))
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
    def handle_event0(self, curr_time, K, alpha):
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
                node.currentleader = node.Leader_Election(probability, K, alpha)
                if node.nodeID == node.currentleader:
                    # print("生成区块成功", node.nodeID)
                    # 节点直到自己成为首领节点就打包交易生成区块
                    # 交易池中最多取2000个交易，生成区块
                    if len(node.transactions) < 200:
                        current_transactions = node.transactions[:len(node.transactions)+1]# (有语法问题)
                    else:
                        current_transactions = node.transactions[:200]
                    curr_block = node.Create_Block(node.blockchain[-1].Hash, node.currentleader , current_transactions)
                    node.Set_BlockHash(curr_block)
                    node.currentblock = curr_block
                    # curr_block.print_block()
                    # node.receivequeue.append(curr_block)
                    # 将生成的区块放入发送队列中，优先级最高
                    node.sendqueue.insert(1, 'block')
                    node.queuetime.insert(1, curr_time)
                    node.queuedata.insert(1, curr_block)
                    # 将生成的区块Hash签名放入发送队列中，优先级次高
                    block_hash_sign= node.RSA_Signature(curr_block.Hash)
                    node.currentsign = block_hash_sign
                    node.receivequeue.append(block_hash_sign)
                    node.sendqueue.insert(2, 'sign')
                    node.queuetime.insert(2, curr_time)
                    node.queuedata.insert(2, block_hash_sign)
                    for i in range(0, len(node.queuetime)):
                        if node.queuetime[i] < curr_time:
                            node.queuetime[i] = curr_time
                    # if node.sendqueue[1] == 'block':
                        # print("节点将区块放入队列成功")
            elif node.currentleader != None and node.currentblock != None:
                # 如果有正在处理的区块，首先需要判定是否接收到该区块的最终签名
                if node.finalsign != None:
                    print("添加区块到链", node.nodeID, node.currentblock.ID)
                    # 接收到最终签名则将区块添加到区块链上，并删除节点交易池中已经上链的交易
                    node.currentblock.final_signature = node.finalsign
                    node.Synchronous_Block(node.currentblock)
                    node.Synchronous_Transaction(node.currentblock)
                    # 同步系统信息放在网络中统一做
                    if node.nodeID == node.currentleader:
                        node.numblocks = node.numblocks + 1
                    if node.nodeID == node.blockchain[-(K+1)].leaderID:
                        node.numblocks = node.numblocks - 1
                    node.receivequeue = []
                    node.finalsign = None
                    node.currentsign = None
                    node.currentblock = None
                    node.currentleader = None
                else:
                # 节点需要判定区块的签名数量是否达到阈值，如果达到阈值，则生成最终签名
                    if len(node.receivequeue) >= threshold1:
                        # 节点收集签名的数量达到阈值，则生成当前区块的最终签名
                        # combination_sign = node.currentblock.Hash + str(2)
                        # temp_finalsign = node.RSA_Signature(combination_sign)
                        # print("生成最终签名成功, 且一致")
                        temp_finalsign = 'final signature successful'
                        node.currentblock.final_signature = temp_finalsign
                        node.finalsign = temp_finalsign
                        node.sendqueue.insert(1, 'finalsign')
                        node.queuetime.insert(1, curr_time)
                        node.queuedata.insert(1, node.finalsign)
                        for i in range(0, len(node.queuetime)):
                            if node.queuetime[i] < curr_time:
                                node.queuetime[i] = curr_time
                    else:
                        # 节点收集签名的数量不够且未曾签名，验证区块的有效性成功之后签名
                        if node.currentsign == None:
                            if node.currentblock != None and node.Verify_Block(node.currentblock):
                                node.currentsign = node.RSA_Signature(node.currentblock.Hash)
                                # print("生成签名成功")
                                node.receivequeue.append(node.currentsign)
                                node.sendqueue.insert(1, 'sign')
                                node.queuetime.insert(1, curr_time)
                                node.queuedata.insert(1, node.currentsign)
                                for i in range(0, len(node.queuetime)):
                                    if node.queuetime[i] < curr_time:
                                        node.queuetime[i] = curr_time

    
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
            if node.currentleader == None:
                # 没有首领节点和正在处理的区块，需要先确定当前轮的首领节点
                currentleader = node.Leader_Election(probability, K, alpha)
                node.currentleader = currentleader
                if node.nodeID == node.currentleader:
                    # 节点直到自己成为首领节点就打包交易生成区块
                    # 交易池中最多取2000个交易，生成区块
                    if len(node.transactions) < 200:
                        current_transactions = node.transactions[:len(node.transactions)+1]
                    else:
                        current_transactions = node.transactions[:200]
                    curr_block = node.Create_Block(node.blockchain[-1].Hash, node.currentleader , current_transactions)
                    node.Set_BlockHash(curr_block)
                    node.currentblock = curr_block
                    # print("节点的首领节点是1", node.nodeID, node.currentblock.ID)
                    # curr_block.print_block()
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
                    for i in range(0, len(node.queuetime)):
                        if node.queuetime[i] < curr_time:
                            node.queuetime[i] = curr_time   
            else:             
                if node.currentblock != None:
                    # if node.nodeID == node.currentleader:
                        # print("节点的首领节点是有当前区块的", node.nodeID, node.finalsign)
                # 如果节点没有受到来自首领的区块就等，直到收到来自首领的区块
                # 如果有正在处理的区块，首先需要判定是否接收到该区块的最终签名
                    if node.currentblock.final_signature != None:
                        # 收到最终签名则需要将签名添加到区块中，并且将区块添加到区块链
                        # print("添加区块到链", node.nodeID, node.currentblock.ID)
                        # 接收到最终签名则将区块添加到区块链上，并删除节点交易池中已经上链的交易
                        # node.currentblock.final_signature = node.finalsign
                        node.Synchronous_Block(node.currentblock)
                        node.Synchronous_Transaction(node.currentblock)
                        # 同步系统信息放在网络中统一做
                        if node.nodeID == node.currentleader:
                            node.numblocks = node.numblocks + 1
                        if node.nodeID == node.blockchain[-(K+1)].leaderID:
                            node.numblocks = node.numblocks - 1
                        node.receivequeue = []
                        node.finalsign = None
                        node.currentsign = None
                        node.currentblock = None
                        node.currentleader = None
                    else:
                    # 节点需要判定区块的签名数量是否达到阈值，如果达到阈值，则生成最终签名
                        if len(node.receivequeue) >= threshold1:
                            # 节点收集签名的数量达到阈值，则生成当前区块的最终签名
                            # combination_sign = node.currentblock.Hash + str(2)
                            # temp_finalsign = node.RSA_Signature(combination_sign)
                            # print("生成最终签名成功, 且一致", node.nodeID)
                            temp_finalsign = 'final signature successful'
                            node.currentblock.final_signature = temp_finalsign
                            # node.finalsign = temp_finalsign
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
                            for i in range(0, len(node.queuetime)):
                                if node.queuetime[i] < curr_time:
                                    node.queuetime[i] = curr_time
                        else:
                            # 节点收集签名的数量不够且未曾签名，验证区块的有效性成功之后签名
                            if node.currentsign == None:
                                if node.currentblock != None and node.Verify_Block(node.currentblock):
                                    # node.currentsign = node.RSA_Signature(node.currentblock.Hash)
                                    # print("生成签名成功")
                                    node.currentsign = str(node.nodeID) + '签名区块' + str(node.currentblock.ID) +'成功'
                                    node.receivequeue.append(node.currentsign)
                                    node.sendqueue.insert(1, 'sign')
                                    node.queuetime.insert(1, curr_time)
                                    node.queuedata.insert(1, node.currentsign)
                                    for i in range(0, len(node.queuetime)):
                                        if node.queuetime[i] < curr_time:
                                            node.queuetime[i] = curr_time

    def run(self):
        pass 



            


        