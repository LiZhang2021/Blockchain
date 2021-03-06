# -*- coding: utf-8 -*-
"""
节点类
1. 生成交易
2. 生成有效区块
3. 生成空区块
4. 生成签名
5. 生成最终签名
6. 验证区块
7. 发送消息
8. 接收消息
9. 同步交易
10. 同步区块链
11. 
Created on Sun Apr 18 2022
@author: shally, ZHANG
"""


import operator  #导入operator 包,pip install operator
import Crypto.PublicKey.RSA
import Crypto.Signature.PKCS1_v1_5
import Crypto.Hash.SHA256
import random
import collections
import hashlib
from finalsign import Finalsign
import numpy as np

from block import Block
from transaction import Transaction
from sign import Sign

# 计算节点成功接收消息的参数
PL = 20*np.log10(0.125/(4*np.pi))
beta = 2
Pt = 100
Pn=pow(10, 9)

class Node(object):
    def __init__(self, node_id, x, y, radius):
         self.node_id =  node_id  # 节点id
         self.x = x  # 经度
         self.y = y  # 纬度
         self.radius = radius  # 通信半径
         self.tx_pool = None  # 交易池
         self.blockchain = None  # 区块链
         self.neighbors = None  # 存储所有在线邻节点信息
         self.channel_state = 0  # 信道状态（空闲0/发送1/接收2）
         self.transmission_node = None  # 传输节点信息(如果节点信道状态是1则记录该节点发送消息的所有目标节点，信道是2则记录该节点接收消息的源节点)
         self.send_queue = None  # 发送消息的队列
         self.send_time = 0  # 节点消息的发送时间
         self.psigns = None
         self.csigns = None
         self.current_sign = None  # 当前区块的签名
         self.current_block = None  # 正在确认的区块
         self.count_votes = 0  # 投票计数
         self.current_leader_id = None  # 当前区块的出块节点id
         self.sybil = 0  # 标记女巫节点
        #  self.timeout = 0  # 超时
         self.send_prop = 0.0125  # 发送概率
         self.prob_suc = 0  # 从其他节点接收消息成功的概率（传输消息成功的时候计算）
    # 定义输出
    def __str__(self):
        str_fmt = "node_id:{}, lifetime:{}, recent_gen_blocks:{}, neighbors:{}, stability:{}\n" +\
            "channel_state: {}, transmission_node: {}, current_block: {}, current_leaderid:{}"
        return str_fmt.format(self.node_id, self.lifetime, self.recent_gen_blocks, len(self.neighbors), 
                              self.stability, self.channel_state, self.transmission_node, 
                              self.current_block, self.current_leader_id) 

    # 生成一个交易
    def gen_trans(self, current_time):
        tx_id = str(self.node_id) + ":" + str(current_time)
        tx = Transaction(tx_id)
        if not self.tx_pool:
            self.tx_pool = [tx]
        else:
            self.tx_pool.append(tx)
        if not self.send_queue:
            self.send_queue = [tx]
        else:
            self.send_queue.append(tx)
    
    # 生成一个有效区块
    def gen_valid_block(self, min_tx_num, current_time):      
        if self.tx_pool and len(self.tx_pool) >= min_tx_num:
            block_id, pre_hash = 0, 0        
            if self.blockchain:
                # print("首领节点", self.node_id, self.blockchain[-1].hash)
                block_id = len(self.blockchain)
                pre_hash = self.blockchain[-1].hash
            tx_arr = self.tx_pool[:min_tx_num]
            block = Block(block_id, self.node_id, pre_hash, tx_arr)
            block_content = str(block.block_id) + str(block.leader_id) +\
                str(block.pre_hash) + "".join([str(tx) for tx in block.tx_arr])
            block.hash = hashlib.sha256(block_content.encode("utf-8")).hexdigest()
            self.current_block = block
            self.send_prop = 1
            for rnode in self.neighbors:
                rnode.send_prop = 0
            # self.send_time = current_time + 1
            print("节点生成区块",self.node_id, block.block_id, len(block.tx_arr), self.channel_state)
            if not self.send_queue:
                self.send_queue = [block]
            else:
                if self.channel_state == 1:
                    self.send_queue.insert(1, block)
                else:
                    self.send_queue.insert(0, block)
            # print("首领的发送时间",  self.send_time)
            # print("当前时间",  current_time)
            # file_begin_time = open("Jamming_Begin_time.txt","a")
            # if self.node_id == 0:
            #     file_begin_time.writelines(["LEADER_ID\t", "0", "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
            # else:
            #     file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
            # file_begin_time.close() 
            # file_begin_time = open("Adversary_Begin_time_PBFT.txt","a")
            # if self.node_id == 0:
            #     file_begin_time.writelines(["LEADER_ID\t", "0", "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
            # else:
            #     file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
            # file_begin_time.close() 
            # file_begin_time = open("Sybil_Begin_time.txt","a")
            # if self.node_id == 0:
            #     file_begin_time.writelines(["LEADER_ID\t", "0", "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
            # else:
            #     file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
            # file_begin_time.close() 
            # file_begin_time = open("Begin_time_blocksize(PBFT).txt","a")
            # if self.node_id == 0:
            #     file_begin_time.writelines(["LEADER_ID\t", "0", "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
            # else:
            #     file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])            
            # file_begin_time.close()    
            # file_begin_time = open("Begin_time_nodes(PBFT).txt","a")
            # if self.node_id == 0:
            #     file_begin_time.writelines(["LEADER_ID\t", "0", "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
            # else:
            #     file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"]) 
            # file_begin_time.close()
            file_begin_time = open("Begin_time_propagation(PBFT).txt","a")
            if self.node_id == 0:
                file_begin_time.writelines(["LEADER_ID\t", "0", "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
            else:
                file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
            file_begin_time.close()  
            # file_begin_time = open("Adversary_Begin_time_PBFT.txt","a")
            # if self.node_id == 0:
            #     file_begin_time.writelines(["LEADER_ID\t", "0", "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
            # else:
            #     file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
            # file_begin_time.close() 
        else:
            self.gen_trans(current_time)

    # 生成一个空区块
    def gen_empty_block(self, current_time): 
        block_id, pre_hash = 0, 0            
        if self.blockchain:
            block_id = len(self.blockchain)
            pre_hash = self.blockchain[-1].hash
        tx_arr = None
        block = Block(block_id, self.node_id, pre_hash, tx_arr)
        block_content = str(block.block_id) + str(block.leader_id) +\
            str(block.pre_hash) + "None"
        block.hash = hashlib.sha256(block_content.encode("utf-8")).hexdigest()
        self.current_block = block
        self.send_prop = self.send_prop*(1 + 0.1)
        if self.send_prop > 1:
            self.send_prop = 1
        print("生成一个空区块")
        if not self.send_queue:
            self.send_queue = [block]
        else:
            if self.channel_state > 0:
                self.send_queue.insert(1, block)
            else:
                self.send_queue.insert(0, block)
        # file_begin_time = open("Sybil_Begin_time.txt","a")
        # if self.node_id == 0:
        #     if not tx_arr:
        #         file_begin_time.writelines(["LEADER_ID\t", "0", "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", "0", "\n"])
        #     else:
        #         file_begin_time.writelines(["LEADER_ID\t", "0", "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
        # else:
        #     if not tx_arr:
        #         file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", "0", "\n"])
        #     else:
        #         file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
        # file_begin_time.close() 

        # file_begin_time = open("Adversary_Begin_time_PBFT.txt","a")
        # if self.node_id == 0:
        #     file_begin_time.writelines(["LEADER_ID\t", "0", "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(0), "\n"])
        # else:
        #     file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(0), "\n"])
        # file_begin_time.close() 
        file_begin_time = open("Begin_time_propagation(PBFT).txt","a")
        if self.node_id == 0:
            file_begin_time.writelines(["LEADER_ID\t", "0", "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(0), "\n"])
        else:
            file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(0), "\n"])
        file_begin_time.close() 
        if not self.tx_pool:
            self.gen_trans(current_time)
        else:
            if len(self.tx_pool) < 5000:
                self.gen_trans(current_time)
        
    # 生成Pre-prepare消息
    def gen_pre_pre_msg(self):
        tsign = 'Pre-prepare Message'
        self.current_sign = tsign
        # self.send_prop = 0.0125
        # if not self.send_queue:
        #     self.send_queue = [tsign]
        # else:
        #     if self.channel_state == 1:
        #         self.send_queue.insert(1, tsign)
        #     else:
        #         self.send_queue.insert(0, tsign)
        # print("节点生成签名",self.node_id)
    # 生成Prepared 消息
    def gen_prepared_msg(self):
        tsign = 'Prepared Message'
        self.current_sign = tsign
        self.send_prop = 0.0125
        if not self.psigns:
            self.psigns = [tsign]
        else:
            self.psigns.append(tsign)
        if not self.send_queue:
            self.send_queue = [tsign]
        else:
            if self.channel_state > 0:
                if self.send_queue and len(self.send_queue) >1 and isinstance(self.send_queue[1], Transaction):
                    self.send_queue.insert(1, tsign)
                elif self.send_queue and len(self.send_queue) >2 and isinstance(self.send_queue[1], Transaction):
                    self.send_queue.insert(2, tsign)
            else:
                if isinstance(self.send_queue[0], Transaction):
                    self.send_queue.insert(0, tsign)
                else:
                    self.send_queue.insert(1, tsign)
    
    # 生成Prepared 消息
    def gen_commit_msg(self):
        tsign = 'Commit Message'
        self.current_sign = tsign
        self.send_prop = 0.0125
        if not self.csigns:
            self.csigns = [tsign]
        else:
            self.csigns.append(tsign)
        if not self.send_queue:
            self.send_queue = [tsign]
        else:
            if self.channel_state > 0:
                if self.send_queue and len(self.send_queue) >1 and isinstance(self.send_queue[1], Transaction):
                    self.send_queue.insert(1, tsign)
                elif self.send_queue and len(self.send_queue) >2 and isinstance(self.send_queue[1], Transaction):
                    self.send_queue.insert(2, tsign)
            else:
                if isinstance(self.send_queue[0], Transaction):
                    self.send_queue.insert(0, tsign)
                else:
                    self.send_queue.insert(1, tsign)

    # 验证区块的有效性
    def verify_block(self):
        test_block_id, test_pre_hash = 0, 0
        if self.blockchain:
            test_block_id = len(self.blockchain)
            test_pre_hash = self.blockchain[-1].hash
         # 验证出块节点的合法性
        if self.current_block.leader_id != self.current_leader_id:
            print("出块节点失败")
            verify_result = False
         # 验证区块高度的有效性
        elif self.current_block.block_id != test_block_id:
            print("区块ID失败")
            verify_result = False
         # 验证父区块hash的有效性
        elif self.current_block.pre_hash != test_pre_hash:
            print("父区块哈希验证失败", self.current_block.pre_hash, test_pre_hash)
            verify_result = False
         # 验证交易的有效性
        else:
            verify_result = True
        return verify_result
    
    # 同步交易
    def update_transactions(self):
        if self.current_block and self.current_block.tx_arr:
            self.tx_pool = list(set(self.tx_pool) - set(self.current_block.tx_arr))

    # 节点同步最新区块链
    def synchronous_blockchain(self):
        for node in self.neighbors:
            if len(self.blockchain) < len(node.blockchain):
                self.blockchain = node.blockchain
        
    # 计算节点发送数据所需要的时间
    def commpute_trans_time0(self, data, trans_rate):
        # 如果是交易数据， 一个交易的大小设为512B
        if isinstance(data, Transaction):
            t_trans = pow(2, 9)*8 /float(trans_rate)
        # 如果是区块数据，一个区块的大小设为1MB
        elif isinstance(data, Block):
            if not data.tx_arr:
                t_trans = pow(2, 11)*8 /float(trans_rate)
            else:
                t_trans = len(data.tx_arr) * pow(2, 9)*8 /float(trans_rate) + pow(2, 11)*8 /float(trans_rate)
        # 如果是签名数据，一个签名的大小设为2048bit 
        elif isinstance(data, Sign):
            t_trans = pow(2, 11) /float(trans_rate)
        elif isinstance(data, Finalsign):
            t_trans = pow(2, 11) /float(trans_rate)
        else:
            t_trans = 0
        return t_trans

# 计算节点发送数据所需要的时间
    def commpute_trans_time(self, data, trans_rate):
        # 如果是交易数据， 一个交易的大小设为512B
        if isinstance(data, Transaction):
            t_trans = 4  # 512*8/2048
        # 如果是区块数据，一个区块的大小设为1MB
        elif isinstance(data, Block):
            if not data.tx_arr:
                t_trans = 16  # 8*pow(2, 11) /2048
            else:
                t_trans = len(data.tx_arr) * 4 + 16
        # 如果是签名数据，一个签名的大小设为2048bit 
        elif data == 'Pre-prepare Message':
            t_trans = 2
        elif data == 'Prepared Message':
            t_trans = 2
        elif data == 'Commit Message':
            t_trans = 2
        else:
            t_trans = 0
        return t_trans

   
    # 计算节点接收成功的概率
    def compute_trans_prob(self, sendnode):
        # 计算节点之间的距离
        d = np.sqrt((pow(self.x - sendnode.x, 2)) + (pow(self.y - sendnode.y, 2)))
        if d < 1:
            d=1
        ev = pow(10, 0.1 *PL)*beta*Pn*Pt*pow(d, -3)
        self.prob_suc = 1-pow(np.e,-ev)

    # 传输消息成功之后更新本地信息
    def update_sendnode_info(self, data, slot, trans_rate, current_time):
        if self.sybil == 1 and self.current_block:
            self.send_prop = 0
        t_trans = self.commpute_trans_time(data, trans_rate)
        t_prop =  t_trans  + self.send_time + slot
        # 更新消息传输完成后发送节点的区块状态
        if isinstance(data, Block):
            if data.leader_id == self.current_leader_id: 
               self.current_block = data
               self.send_prop = 0
            #    print("传输区块成功", self.node_id)
        elif data == 'Prepared Message':
            self.send_prop = 0
            # print("传输Prepared Message成功", self.node_id, len(self.psigns))
        elif data == 'Commit Message':
            self.send_prop = 0
            # print("传输Commit Message成功",self.node_id, self.current_sign, len(self.csigns))
            if self.send_queue and self.send_queue[0] == 'Prepared Message':
                del self.send_queue[0]
            if self.send_queue and len(self.send_queue) >1 and self.send_queue[1] == 'Prepared Message':
                del self.send_queue[1]
            if self.send_queue and len(self.send_queue) >2 and self.send_queue[2] == 'Prepared Message':
                del self.send_queue[2]
        elif data == 'Pre-prepare Message':
            # print("传输Pre-prepare Message成功", self.node_id)
            if self.send_queue and self.send_queue[0] == 'Commit Message':
                del self.send_queue[0]
            if self.send_queue and len(self.send_queue) >1 and self.send_queue[1] == 'Commit Message':
                del self.send_queue[1]
            if self.send_queue and len(self.send_queue) >2 and self.send_queue[2] == 'Commit Message':
                del self.send_queue[2]
        # elif isinstance(data, Transaction):
        #     print("传输交易成功", self.node_id)
            
        # 更新发送节点传输完成之后消息队列时间
        self.send_time = current_time + slot
        self.channel_state = 0
        self.transmission_node = None
        self.send_queue = collections.deque(self.send_queue)
        self.send_queue.popleft()
        # print("下一个数据类型", self.node_id, type(self.send_queue[0]))
        # print("节点的传输时间", self.node_id, self.send_time)

    # 接收消息成功后，更新本地消息
    def update_receivenode_info(self, data, current_time, slot, trans_rate, prob_suc):
        if self.sybil == 1 and isinstance(data, Block):
            self.send_prop = 0
        if self.sybil == 1 and self.current_block:
            self.send_prop = 0
        # 判定节点是否接收成功
        rdm = random.uniform(0,1)
        snode = self.transmission_node[0]
        self.compute_trans_prob(snode)
        if rdm <= prob_suc:
            # print("接收消息成功", self.node_id, self.transmission_node[0].node_id)
            # 更新消息传输完成后接收节点的状态
            if isinstance(data, Block):
                if not self.current_block and data.leader_id == self.current_leader_id: 
                    self.current_block = data
                    # print("接收区块成功",self.node_id)
            elif data == 'Prepared Message':
                if not self.psigns:
                    self.psigns = [data]
                else:
                    self.psigns.append(data)
                # print("接收Prepared Message成功", self.node_id, len(self.psigns))
            elif data == 'Commit Message':
                if not self.csigns:
                    self.csigns = [data]
                else:
                    self.csigns.append(data)
                if self.send_queue and self.send_queue[0] == 'Prepared Message':
                    del self.send_queue[0]
                if self.send_queue and len(self.send_queue) >1 and self.send_queue[1] == 'Prepared Message':
                    del self.send_queue[1]
                if self.send_queue and len(self.send_queue) >2 and self.send_queue[2] == 'Prepared Message':
                    del self.send_queue[2]
                # print("接收Commit Message成功", self.node_id, len(self.csigns))
            elif data == 'Pre-prepare Message':
                self.current_sign = 'Pre-prepare Message'
                # self.send_prop = 0.0125
                # print("接收Pre-prepare Message成功", self.node_id, self.current_sign)
                if self.send_queue and self.send_queue[0] == 'Commit Message':
                    del self.send_queue[0]
                if self.send_queue and self.send_queue[1] == 'Commit Message':
                    del self.send_queue[1]
                if self.send_queue and self.send_queue[2] == 'Commit Message':
                    del self.send_queue[2]
            elif isinstance(data, Transaction):
                if not self.tx_pool:
                    self.tx_pool = [data]
                else:
                    if data not in self.tx_pool:
                    #     print("已经在交易池中")
                    # else:
                        # print("接收交易成功", self.node_id)
                        self.tx_pool.append(data)
            # 更新所有接收节点发送队列的时间和信道状态       
            self.send_time = current_time + slot
            self.channel_state = 0
            self.transmission_node = None
        else:
        # 更新所有接收节点发送队列的时间和信道状态    
            # print("接收消息失败", self.node_id)   
            self.send_time = current_time + slot 
            self.channel_state = 0
            self.transmission_node = None
        # print("节点的传输时间", self.node_id, self.send_time)
    
    # 接收消息成功后，更新本地消息
    def update_receivenode_info0(self, data, current_time, slot, trans_rate):
        # 判定节点是否接收成功
        if isinstance(data, Block):
            self.send_prop = 0
        rdm = random.uniform(0,1)
        snode = self.transmission_node[0]
        self.compute_trans_prob(snode)
        if rdm <= 1:
            # print("接收消息成功", self.node_id, self.transmission_node[0].node_id)
            # 更新消息传输完成后接收节点的状态
            if isinstance(data, Block):
                if not self.current_block and data.leader_id == self.current_leader_id: 
                    self.current_block = data
                    # print("接收区块成功",self.node_id, self.send_prop)
                    # if self.sybil == 1:
                    #     self.send_prop = 0.0025
            elif data == 'Prepared Message':
                if not self.psigns:
                    self.psigns = [data]
                else:
                    self.psigns.append(data)
                # print("接收Prepared Message成功", self.node_id, len(self.psigns), self.sybil, self.send_prop)
            elif data == 'Commit Message':
                if not self.csigns:
                    self.csigns = [data]
                else:
                    self.csigns.append(data)
                if self.send_queue and self.send_queue[0] == 'Prepared Message':
                    del self.send_queue[0]
                if self.send_queue and len(self.send_queue)>1 and self.send_queue[1] == 'Prepared Message':
                    del self.send_queue[1]
                if self.send_queue and len(self.send_queue)>2 and self.send_queue[2] == 'Prepared Message':
                    del self.send_queue[2]
                # print("接收Commit Message成功", self.node_id, len(self.csigns), self.sybil, self.send_prop)
            elif data == 'Pre-prepare Message':
                self.current_sign = 'Pre-prepare Message'
                # print("接收Pre-prepare Message成功", self.node_id, self.current_sign)
                if self.send_queue and self.send_queue[0] == 'Commit Message':
                    del self.send_queue[0]
                if self.send_queue and self.send_queue[1] == 'Commit Message':
                    del self.send_queue[1]
                if self.send_queue and self.send_queue[2] == 'Commit Message':
                    del self.send_queue[2]
            elif isinstance(data, Transaction):
                if not self.tx_pool:
                    self.tx_pool = [data]
                else:
                    if data not in self.tx_pool:
                    #     print("已经在交易池中")
                    # else:
                        # print("接收交易成功", self.node_id)
                        self.tx_pool.append(data)
            # 更新所有接收节点发送队列的时间和信道状态       
            self.send_time = current_time + slot
            self.channel_state = 0
            self.transmission_node = None
        else:
        # 更新所有接收节点发送队列的时间和信道状态    
            # print("接收消息失败", self.node_id)   
            self.send_time = current_time + slot 
            self.channel_state = 0
            self.transmission_node = None
        # print("节点的传输时间", self.node_id, self.send_time)

if __name__ == "__main__":
    from block import Block
    from transaction import Transaction
    from sign import Sign
    from finalsign import Finalsign
    # tx = Transaction(1)
    node = Node(12, 23, 34, 200)
    node.gen_trans(1308)
    tx = node.send_queue[-1]
    print("输出交易")
    print(tx)
    node.gen_empty_block()
    block = node.send_queue[0]
    print("输出区块")
    print(block)
    node.current_block = block
    node.gen_sign()
    sign = node.send_queue[0]
    print("输出签名")
    print(sign)
    node.signs = [sign]
    node.gen_final_sign(1)
    fsign = node.send_queue[0]
    print("输出最终签名")
    print(fsign)
    fsign = Finalsign("shally0", block.hash, 30)
    node.final_sign = fsign
    print("输出节点")
    print(node)
    pass


"""
TODO
1. 改进区块的输出格式(完成)

LOG:
# 2022/4/18
1. 

"""
