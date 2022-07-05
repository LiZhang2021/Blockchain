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
beta = 10
Pt = pow(10, -2)
Pn=pow(10, -9)

class Node(object):
    def __init__(self, node_id, x, y, radius):
         self.node_id =  node_id  # 节点id
         self.x = x  # 经度
         self.y = y  # 纬度
         self.radius = radius  # 通信半径
         self.tx_pool = None  # 交易池
         self.blockchain = None  # 区块链
         self.neighbors = None  # 存储所有在线邻节点信息
         self.lifetime = 0  # 剩余寿命
         self.recent_gen_blocks = 0   # 最近生成的区块数量
         self.stability = 0  # 稳定度
         self.channel_state = 0  # 信道状态（空闲0/发送1/接收2）
         self.transmission_node = None  # 传输节点信息(如果节点信道状态是1则记录该节点发送消息的所有目标节点，信道是2则记录该节点接收消息的源节点)
         self.send_queue = None  # 发送消息的队列
         self.send_time = 0  # 节点消息的发送时间
         self.signs = None  # 部分签名
         self.final_sign = None  # 最终签名
         self.current_sign = None  # 当前区块的签名
         self.current_block = None  # 正在确认的区块
         self.current_leader_id = None  # 当前区块的出块节点id
         self.sybil = 0  # 标记女巫节点
         self.timeout = 0  # 超时
         self.send_prop = 0.0125  # 发送概率
         self.time_window = 100  # 敌手攻击窗口
         self.count_slots = 0  # 时间窗口计数
         self.recent_receive_data = None  # 近期接收敌手窗口大小的数据
         self.jamming = 0  # Jamming 节点状态(不发起攻击0/发起攻击1)
         self.prob_suc = 0  # 从其他节点接收消息成功的概率（传输消息成功的时候计算）
         self.empty_slots = 0 # 记录以及传输过区块的节点
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
            print("节点生成区块",self.node_id, block.block_id, len(block.tx_arr), self.channel_state, self.send_time)
            if not self.send_queue:
                self.send_queue = [block]
            else:
                if self.channel_state == 1:
                    self.send_queue.insert(1, block)
                else:
                    self.send_queue.insert(0, block)
            # print("首领的发送时间",  self.send_time)
            # print("当前时间",  current_time)
            file_begin_time = open("propagation_Begin_time.txt","a")
            if self.node_id == 0:
                file_begin_time.writelines(["LEADER_ID\t", "0", "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
            else:
                file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
            file_begin_time.close() 
            # file_begin_time = open("Jamming_Begin_time.txt","a")
            # if self.node_id == 0:
            #     file_begin_time.writelines(["LEADER_ID\t", "0", "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
            # else:
            #     file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
            # file_begin_time.close() 
            # file_begin_time = open("Adversary_Begin_time.txt","a")
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
            # file_begin_time = open("Begin_time_blocksize.txt","a")
            # if self.node_id == 0:
            #     file_begin_time.writelines(["LEADER_ID\t", "0", "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
            # else:
            #     file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])            
            # file_begin_time.close()    
            # file_begin_time = open("Begin_time_nodes.txt","a")
            # if self.node_id == 0:
            #     file_begin_time.writelines(["LEADER_ID\t", "0", "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
            # else:
            #     file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
            # file_begin_time.close()    
            # file_begin_time = open("Begin_time_bandwidth.txt","a")
            # if self.node_id == 0:
            #     file_begin_time.writelines(["LEADER_ID\t", "0", "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
            # else:
            #     file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])    
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
        self.send_prop = 1
        for rnode in self.neighbors:
            rnode.send_prop = 0
        print("生成一个空区块", self.node_id, self.send_prop, self.channel_state)
        if not self.send_queue:
            self.send_queue = [block]
        else:
            if self.channel_state == 1:
                self.send_queue.insert(1, block)
            else:
                self.send_queue.insert(0, block)
        # print("首领的发送时间",  self.send_time)
        # print("当前时间",  current_time)
        # file_begin_time = open("propagation_Begin_time.txt","a")
        # if self.node_id == 0:
        #     file_begin_time.writelines(["LEADER_ID\t", "0", "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
        # else:
        #     file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
        # file_begin_time.close() 
        # file_begin_time = open("Jamming_Begin_time.txt","a")
        # if self.node_id == 0:
        #     file_begin_time.writelines(["LEADER_ID\t", "0", "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
        # else:
        #     file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
        # file_begin_time.close() 
        # file_begin_time = open("Adversary_Begin_time.txt","a")
        # if self.node_id == 0:
        #     file_begin_time.writelines(["LEADER_ID\t", "0", "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time-20000), "\tNUM_TXS\t", str(0), "\n"])
        # else:
        #     file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time-20000), "\tNUM_TXS\t", str(0), "\n"])
        # file_begin_time.close() 
        file_begin_time = open("propagation_Begin_time.txt","a")
        if self.node_id == 0:
            file_begin_time.writelines(["LEADER_ID\t", "0", "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(0), "\n"])
        else:
            file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(0), "\n"])
        file_begin_time.close() 
        # file_begin_time = open("Sybil_Begin_time.txt","a")
        # if self.node_id == 0:
        #     file_begin_time.writelines(["LEADER_ID\t", "0", "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(0), "\n"])
        # else:
        #     file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tLEADER_ID_type\t", str(self.sybil), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(0), "\n"])
        # file_begin_time.close() 
        # file_begin_time = open("Begin_time_blocksize.txt","a")
        # if self.node_id == 0:
        #     file_begin_time.writelines(["LEADER_ID\t", "0", "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
        # else:
        #     file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])            
        # file_begin_time.close()    
        # file_begin_time = open("Begin_time_nodes.txt","a")
        # if self.node_id == 0:
        #     file_begin_time.writelines(["LEADER_ID\t", "0", "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
        # else:
        #     file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
        # file_begin_time.close()    
        # file_begin_time = open("Begin_time_bandwidth.txt","a")
        # if self.node_id == 0:
        #     file_begin_time.writelines(["LEADER_ID\t", "0", "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])
        # else:
        #     file_begin_time.writelines(["LEADER_ID\t", str(self.node_id), "\tBLOCK_ID\t", str(block.block_id), "\tBEGIN_TIME\t", str(current_time), "\tNUM_TXS\t", str(len(tx_arr)), "\n"])    
        # file_begin_time.close() 
        if not self.tx_pool:
            self.gen_trans(current_time)
        else:
            if len(self.tx_pool) < 5000:
                self.gen_trans(current_time)
        
    # 生成部分签名
    def gen_sign(self):
        self.send_prop = 0.0125
        if not self.current_sign and self.current_block and self.verify_block():
            tsign = Sign(self.node_id, self.current_block.hash)
            self.current_sign = tsign
            # 添加签名到签名列表中
            if not self.signs:
                self.signs = [tsign]
            else:
                self.signs.append(tsign)
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
            # print("节点生成签名",self.node_id)
    # 生成最终签名
    def gen_final_sign(self, sign_threshold):
        self.send_prop = 0.0125
        if not self.final_sign:
            if self.current_block and self.current_leader_id == self.current_block.leader_id and self.signs and len(self.signs) >= sign_threshold:
                fsign = Finalsign(self.node_id, self.current_block.hash, sign_threshold)
                self.final_sign = fsign
                # # 提升节点传输概率
                # self.send_prop = self.send_prop*(1 + 0.1)
                # if self.send_prop > 1:
                #     self.send_prop = 1
                # 添加最终签名到发送列表中
                if not self.send_queue:
                    self.send_queue = [fsign]
                else:
                    if self.channel_state == 1:
                        self.send_queue.insert(1, fsign)
                    else:
                        self.send_queue.insert(0, fsign)

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
        elif isinstance(data, Sign):
            t_trans = 2
        elif isinstance(data, Finalsign):
            t_trans = 2
        else:
            t_trans = 0
        return t_trans

    # 信道忙碌时，随机退避一段时间 trans_rate 是信道速率
    def channel_busy(self, trans_rate):
        # 将退避时间与等待时间相加，重设等待时间
        self.busy += 1
        time_window = 10
        self.send_time += time_window * self.busy * 512/float(trans_rate) + random.uniform(0, 0.00512)
    
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
        # 获取传输消息的信息，并计算传输消息的时间
        t_trans = self.commpute_trans_time(data, trans_rate)
        t_prop =  t_trans  + self.send_time + slot
        # 更新消息传输完成后发送节点的区块状态
        if isinstance(data, Finalsign):
            # self.send_prop = 0.0125
            if self.current_block and self.current_block.hash == data.sign_content:
                self.current_block.final_sig = data
                # print("传输最终签名成功", self.node_id)
                if self.send_queue and len(self.send_queue) >=2 and isinstance(self.send_queue[1], Sign):
                    del self.send_queue[1]
        elif isinstance(data, Block):
            self.send_prop = 0
            if data.leader_id == self.current_leader_id: 
               self.current_block = data
               print("传输区块成功", self.node_id)
               self.transmited_block =1
        elif isinstance(data, Sign):
            if data not in self.signs:
                self.signs.append(data)
            # print("传输签名成功", self.node_id, self.send_prop, len(self.signs))
            self.send_prop = 0
        # elif isinstance(data, Transaction):
            # print("传输交易成功", self.node_id)
            
        # 更新发送节点传输完成之后消息队列时间
        self.send_time = current_time + slot
        self.channel_state = 0
        self.transmission_node = None
        self.send_queue = collections.deque(self.send_queue)
        self.send_queue.popleft()
        # print("节点的传输时间", self.node_id, self.send_time)

    # 接收消息成功后，更新本地消息
    def update_receivenode_info(self, data, current_time, slot, trans_rate, prob_suc):      
        # 判定节点是否接收成功
        if isinstance(data, Block):
            self.send_prop = 0
        rdm = random.uniform(0,1)
        snode = self.transmission_node[0]
        self.compute_trans_prob(snode)
        # if isinstance(data, Block):
        #     temp_prob = 1
        # else:
        #     temp_prob = prob_suc
        temp_prob = prob_suc
        if rdm <= temp_prob :
            # print("接收消息成功", self.node_id, self.transmission_node[0].node_id)
            # 更新消息传输完成后接收节点的状态
            if isinstance(data, Finalsign):
                if self.current_block and self.current_block.hash == data.sign_content:
                    self.current_block.final_sig = data
                    self.final_sign = data
                    # print("接收最终签名成功", self.node_id)
                    if self.send_queue and isinstance(self.send_queue[0], Finalsign):
                        del self.send_queue[0]
                    if self.send_queue and len(self.send_queue) >1 and isinstance(self.send_queue[1], Finalsign):
                        del self.send_queue[1]
                    if self.send_queue and isinstance(self.send_queue[0], Sign):
                        del self.send_queue[0]
                    if self.send_queue and len(self.send_queue)>1 and  isinstance(self.send_queue[1], Sign):
                        del self.send_queue[1]
                    if self.send_queue and len(self.send_queue)>2 and  isinstance(self.send_queue[2], Sign):
                        del self.send_queue[2]
            elif isinstance(data, Block):
                if not self.current_block and data.leader_id == self.current_leader_id: 
                    self.current_block = data
            elif isinstance(data, Sign):
                if not self.signs:
                    self.signs = [data]
                else:
                    if data not in self.signs:
                    #     print("已经在签名集合中", self.node_id, len(self.signs))
                    # else:
                        self.signs.append(data)
                        # print("节点接收签名成功", self.node_id, len(self.signs))
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

    def update_receivenode_info0(self, data, current_time, slot, trans_rate):     
        if isinstance(data, Block):
            self.send_prop = 0
        # if self.sybil == 1 and isinstance(data, Sign):
        #     self.send_prop = 0.0125
        # 判定节点是否接收成功  
        rdm = random.uniform(0,1)
        snode = self.transmission_node[0]
        self.compute_trans_prob(snode)
        temp_prob = 1
        if rdm <= temp_prob :
            # print("接收消息成功", self.node_id, self.transmission_node[0].node_id)
            # 更新消息传输完成后接收节点的状态
            if isinstance(data, Finalsign):
                if self.current_block and self.current_block.hash == data.sign_content:
                    self.current_block.final_sig = data
                    self.final_sign = data
                    # print("接收最终签名成功", self.node_id)
                    if self.send_queue and isinstance(self.send_queue[0], Finalsign):
                        del self.send_queue[0]
                    if self.send_queue and len(self.send_queue) >1 and isinstance(self.send_queue[1], Finalsign):
                        del self.send_queue[1]
                    if self.send_queue and isinstance(self.send_queue[0], Sign):
                        del self.send_queue[0]
                    if self.send_queue and len(self.send_queue)>1 and  isinstance(self.send_queue[1], Sign):
                        del self.send_queue[1]
                    if self.send_queue and len(self.send_queue)>2 and  isinstance(self.send_queue[2], Sign):
                        del self.send_queue[2]
            elif isinstance(data, Block):
                if not self.current_block and data.leader_id == self.current_leader_id: 
                    self.current_block = data
                    # print("节点接收区块成功", self.node_id)
            elif isinstance(data, Sign):
                if not self.signs:
                    self.signs = [data]
                else:
                    if data not in self.signs:
                    #     print("已经在签名集合中", self.node_id, len(self.signs))
                    # else:
                        self.signs.append(data)
                        # print("节点接收签名成功", self.node_id, len(self.signs))
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
    


# 传输消息成功之后更新本地信息
    def update_sendnode_info_jammer(self, data, slot, trans_rate):
        # 获取传输消息的信息，并计算传输消息的时间
        t_trans = self.commpute_trans_time(data, trans_rate)
        t_prop =  t_trans  + self.send_time + slot
        # 更新消息传输完成后发送节点的区块状态
        if isinstance(data, Finalsign):
            if self.current_block and self.current_block.hash == data.sign_content:
                self.current_block.final_sig = data
                # print("传输最终签名成功", self.node_id)
                if isinstance(self.send_queue[1], Sign):
                    del self.send_queue[1]
        elif isinstance(data, Block):
            if data.leader_id == self.current_leader_id: 
               self.current_block = data
               print("传输区块成功", self.node_id)
        # elif isinstance(data, Sign):
        #     print("传输签名成功", self.node_id, len(self.signs))
        # elif isinstance(data, Transaction):
        #     print("传输交易成功", self.node_id)
        # 更新发送节点传输完成之后消息队列时间
        self.send_time = t_prop
        self.channel_state = 0
        self.transmission_node = None
        self.send_queue = collections.deque(self.send_queue)
        self.send_queue.popleft()
        

    # 接收消息成功后，更新本地消息
    def update_receivenode_info_jammer(self, data, current_time, slot):
                    
        rdm = random.uniform(0,1)
        snode = self.transmission_node[0]
        self.compute_trans_prob(snode)
        if rdm <= self.prob_suc :
            # print("接收消息成功", self.node_id, self.transmission_node[0].node_id)
            # 更新消息传输完成后接收节点的状态
            if isinstance(data, Finalsign):
                if self.current_block and self.current_block.hash == data.sign_content:
                    self.current_block.final_sig = data
                    self.final_sign = data
                    # print("接收最终签名成功", self.node_id)
                    if isinstance(self.send_queue[0], Finalsign):
                        del self.send_queue[0]
                    if len(self.send_queue) >1 and isinstance(self.send_queue[1], Finalsign):
                        del self.send_queue[1]
                    if isinstance(self.send_queue[0], Sign):
                        del self.send_queue[0]
                    if len(self.send_queue)>1 and  isinstance(self.send_queue[1], Sign):
                        del self.send_queue[1]
                    if len(self.send_queue)>2 and  isinstance(self.send_queue[2], Sign):
                        del self.send_queue[2]
            elif isinstance(data, Block):
                if not self.current_block and data.leader_id == self.current_leader_id: 
                    self.current_block = data
                    # print("接收区块成功",self.node_id)
                    # if self.current_sign in self.send_queue:
                    #     self.send_prop = self.send_prop*(1+0.1)
                    #     if self.send_prop > 0.9:
                    #         self.send_prop = 0.9
                    # else:
                    #     self.send_prop = self.send_prop/(1+0.1)
                    #     if self.send_prop <0.1:
                    #         self.send_prop = 0.1
            elif isinstance(data, Sign):
                if not self.signs:
                    self.signs = [data]
                else:
                    if data not in self.signs:
                    #     print("已经在签名集合中", self.node_id, len(self.signs))
                    # else:
                        self.signs.append(data)
                        # print("节点接收签名成功", self.node_id, len(self.signs))
                # if self.current_sign in self.send_queue:
                #     self.send_prop = self.send_prop*(1+0.1)
                #     if self.send_prop > 0.9:
                #         self.send_prop = 0.9
                # else:
                #     self.send_prop = self.send_prop/(1+0.1)
                #     if self.send_prop <0.1:
                #         self.send_prop = 0.1
            elif isinstance(data, Transaction):
                if not self.tx_pool:
                    self.tx_pool = [data]
                else:
                    if data not in self.tx_pool:
                    #     print("已经在交易池中")
                    # else:
                        # print("接收交易成功", self.node_id)
                        self.tx_pool.append(data)
                # if self.current_sign in self.send_queue:
                #     self.send_prop = self.send_prop*(1+0.1)
                #     if self.send_prop > 0.9:
                #         self.send_prop = 0.9
                # else:
                #     self.send_prop = self.send_prop/(1+0.1)
                #     if self.send_prop <0.1:
                #         self.send_prop = 0.1
            # 更新所有接收节点发送队列的时间和信道状态       
            self.send_time = current_time + slot
            self.channel_state = 0
            self.transmission_node = None
        else:
        # 更新所有接收节点发送队列的时间和信道状态    
            print("接收消息失败", self.node_id)   
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
