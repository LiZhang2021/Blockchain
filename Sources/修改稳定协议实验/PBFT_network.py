import random
import math
import Crypto.PublicKey.RSA
import Crypto.Signature.PKCS1_v1_5
import Crypto.Hash.SHA256
import hashlib
import operator

import numpy


from PBFT_node import Node
from block import Block
from transaction import Transaction
from sign import Sign
from finalsign import Finalsign

NUM_NODES = 100          # 节点数量
CONFIRM_THRESHOLD = 51  # 区块确认阈值
RADIUS = 200                  # 节点的通信半径
TRANSMISSION_RATE = 1*pow(10, 7)  # 信道传输速率
MAX_SIMULATIOND_TIME = 100 # 仿真时间
MAX_TRANSACTIONS = 2000
# SLOT = 512/float(TRANSMISSION_RATE) # 一个包大小为512bit，在当前传输速率下时隙长度
SLOT = 1
NUM_BLOCKS = 10             # 计算共识比的区块数量
ALPHA = 0.7                         # 稳定度

class Network(object):
    def __init__(self):
        self.nodes = []         # 网络中所有节点
        self.leader_id = None    # 当前的出块节点id
        self.leader = None      # 当前首领节点
        self.current_time = 0
    
    def __str__(self):
        if not self.nodes:
            str_fmt = "Network_number_of_Nodes:{}\n" + "leader:{}, nodes:{}"
            return str_fmt.format(len(self.nodes), self.leader_id, "None")
        else:
            str_fmt = "Network_number_of_Nodes:{}\n" + "leader:{}, nodes:{}"
            return str_fmt.format(len(self.nodes), self.leader_id, [str(node) for node in self.nodes])
    
    # 创建节点
    def create_nodes(self, num_nodes, radius):
        for i in range(num_nodes):
            temp_x = random.randint(0, 100)
            temp_y = random.randint(0, 100)
            node = Node(i, temp_x, temp_y, radius)
            self.nodes.append(node)
    
    # 给网络设置初始活动时间和提出区块数量
    def set_basic_info(self):
        for i in range(len(self.nodes)):
            if i % 4 == 0:
                self.nodes[i].lifetime = 20
                self.nodes[i].recent_gen_blocks = 30
            if i % 4 == 1:
                self.nodes[i].lifetime = 100
                self.nodes[i].recent_gen_blocks = 30
            if i % 4 == 2:
                self.nodes[i].lifetime = 20
                self.nodes[i].recent_gen_blocks = 90
            if i % 4 == 3:
                self.nodes[i].lifetime = 100
                self.nodes[i].recent_gen_blocks = 90
    
    # 根据节点的位置和通信半径确定所有节点的邻节点
    def find_adjacent_nodes(self):
        for inode in self.nodes:
            for jnode in self.nodes:
                if jnode.node_id != inode.node_id:
                    dis = (pow(inode.x - jnode.x, 2)) + (pow(inode.y - jnode.y, 2))
                    if dis <= pow(inode.radius,2):
                        if not inode.neighbors:
                            inode.neighbors = [jnode]
                        else:
                            inode.neighbors.append(jnode)

    # 首领选举
    # 计算节点的稳定度
    def caculate_stability(self, alpha):
        # 对网络中的节点按照节点ID排序
        self.nodes.sort(key = operator.attrgetter('node_id'))
        sum_time = 0.0
        # 计算所有节点的剩余时间和
        for node in self.nodes:
            sum_time +=  node.lifetime
        # 计算所有节点的近期生成区块数量
        sum_block = 0
        for node in self.nodes:
            sum_block += node.recent_gen_blocks
        # 计算每个节点的稳定度
        for node in self.nodes:
            # 计算共识比
            bratio = node.recent_gen_blocks/sum_block
            # 计算时间比
            tratio = node.lifetime/sum_time
            # 计算稳定度
            node.stability =  (alpha * tratio +  (1- alpha) * bratio)
            # print("节点稳定度", node.node_id, node.lifetime, node.recent_gen_blocks, node.stability)

    # 构建轮盘并选举首领
    def leader_election(self, prob, alpha):
        # 计算所有节点的稳定度
        self.caculate_stability(alpha)
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
            sum_i = sum(probs[:i+1])
            Disk.insert(i+1, sum_i)
        # print("轮盘", Disk )
        # 根据区块链最新确认的区块hash选举首领节点
        for node_id in range(len(probs)):
                if prob >= Disk[node_id] and prob < Disk[node_id+1]: # 判定随机数是否在节点k的区间中
                    self.leader_id = node_id
                    break
        if self.leader_id == None:
            self.leader_id = 0

    # 完成区块确认之后，网络需要更新最新信息
    def update_information(self):
        # 更新节点信息，包括节点数量、节点ID，节点稳定度（剩余活动时间和共识区块数量）
        for node in self.nodes:
            # 节点的活动时间递减
            node.lifetime -= 1
            # 共识比窗口前移
            # if len(node.blockchain) > block_threshold:
            if node.node_id == self.leader_id:
                node.recent_gen_blocks += 1
            # if node.node_id == node.blockchain[-(block_threshold+1)].leaderID:
        dnode = random.choice(self.nodes)
        dnode.recent_gen_blocks -= 1

 # 传输消息
    def transmission(self, slot, trans_rate, prob_suc):
        for node in self.nodes:
            if node.channel_state == 0 and node.send_queue and self.current_time <= node.send_time < (self.current_time + slot):
                # 节点确定是否要发送消息
                p_send = random.uniform(0,1)
                if p_send <= node.send_prop:
                    temp_sender = [node]
                else:
                    temp_sender = []
                    for tnode in node.neighbors:
                        if tnode.channel_state == 0 and self.current_time <= tnode.send_time < (self.current_time + slot):
                            p_send = random.uniform(0,1)
                            if p_send <= tnode.send_prop:
                                temp_sender.append(tnode)
                if not temp_sender:
                    # print("当前时隙为空",self.current_time)
                    for node in self.nodes:
                        # print("节点信息", node.node_id, node.channel_state, node.send_prop)
                        node.channel_state = 0
                        node.transmission_node = None
                        # node.empty_slots += slot
                        node.send_time = self.current_time + slot
                    break
                elif len(temp_sender)>1:
                     # print("当前时隙信道忙碌",self.current_time)
                    for node in self.nodes:
                        # print("节点信息", node.node_id, node.channel_state, node.send_prop)
                        node.channel_state = 0
                        node.transmission_node = None
                        # node.empty_slots += slot
                        node.send_time = self.current_time + slot
                    break
                else:
                    snode = random.choice(temp_sender)
                    snode.channel_state = 1
                    # 确定接收节点集合
                    for rnode in snode.neighbors:
                        # 空闲接收节点决定是否接收该节点的消息
                        if rnode.channel_state == 0:                           
                            rnode.channel_state = 2
                            rnode.transmission_node = [snode]
                            if not snode.transmission_node:
                                snode.transmission_node = [rnode]
                            else:
                                snode.transmission_node.append(rnode)
            elif node.channel_state == 1 and node.send_queue: # 节点发送消息
                data = node.send_queue[0]
                t_trans = node.commpute_trans_time(data, trans_rate) + node.send_time
                # print("节点开始传输的时间和结束的时间", node.node_id, node.send_time , t_trans)
                if self.current_time <= t_trans < self.current_time + slot:
                    # 传输完成，更新发送节点信息
                    # print("节点在当前时隙传输完成", node.node_id, (self.current_time + slot))                    
                    for rnode in node.transmission_node:
                        rnode.update_receivenode_info(data, self.current_time,slot, trans_rate,prob_suc)
                        # print("节点的交易池",rnode.node_id, len(rnode.tx_pool))
                    # print("发送节点", node.node_id, len(node.tx_pool))
                    node.update_sendnode_info(data, slot, trans_rate, self.current_time)
     # 传输消息
    def transmission0(self, slot, trans_rate, prob_suc):
        for node in self.nodes:
            if node.channel_state == 0 and node.send_queue and self.current_time <= node.send_time < (self.current_time + slot):
                # 节点确定是否要发送消息
                p_send = random.uniform(0,1)
                if p_send <= node.send_prop:
                    temp_sender = [node]
                else:
                    temp_sender = []
                    for tnode in node.neighbors:
                        if tnode.channel_state == 0 and self.current_time <= tnode.send_time < (self.current_time + slot):
                            p_send = random.uniform(0,1)
                            if p_send <= tnode.send_prop:
                                temp_sender.append(tnode)
                if not temp_sender:
                    # print("当前时隙为空",self.current_time)
                    for node in self.nodes:
                        # print("节点信息", node.node_id, node.channel_state, node.send_prop)
                        node.channel_state = 0
                        node.transmission_node = None
                        # node.empty_slots += slot
                        node.send_time = self.current_time + slot
                    break
                elif len(temp_sender)>1:
                     # print("当前时隙信道忙碌",self.current_time)
                    for node in self.nodes:
                        # print("节点信息", node.node_id, node.channel_state, node.send_prop)
                        node.channel_state = 0
                        node.transmission_node = None
                        # node.empty_slots += slot
                        node.send_time = self.current_time + slot
                    break
                else:
                    snode = random.choice(temp_sender)
                    snode.channel_state = 1
                    # 确定接收节点集合
                    for rnode in snode.neighbors:
                        # 空闲接收节点决定是否接收该节点的消息
                        if rnode.channel_state == 0:                           
                            rnode.channel_state = 2
                            rnode.transmission_node = [snode]
                            if not snode.transmission_node:
                                snode.transmission_node = [rnode]
                            else:
                                snode.transmission_node.append(rnode)
            elif node.channel_state == 1 and node.send_queue: # 节点发送消息
                data = node.send_queue[0]
                t_trans = node.commpute_trans_time(data, trans_rate) + node.send_time
                # print("节点开始传输的时间和结束的时间", node.node_id, node.send_time , t_trans)
                if self.current_time <= t_trans < self.current_time + slot:
                    # 传输完成，更新发送节点信息
                    # print("节点在当前时隙传输完成", node.node_id, (self.current_time + slot))                    
                    for rnode in node.transmission_node:
                        rnode.update_receivenode_info(data, self.current_time,slot, trans_rate,prob_suc)
                        # print("节点的交易池",rnode.node_id, len(rnode.tx_pool))
                    # print("发送节点", node.node_id, len(node.tx_pool))
                    node.update_sendnode_info(data, slot, trans_rate, self.current_time)

     # 事件处理
    def handle_event(self, min_tx_num, signs_threshold):
        # print("当前时间", self.current_time)
        for node in self.nodes:
            if node.node_id == self.leader_id:  # 首领节点的操作
                if not node.current_block:
                    # 如果还没有生成区块，则需要生成区块和区块Hash的签名
                    node.gen_valid_block(min_tx_num, self.current_time)
                else:
                    if node.current_block and node.current_sign and node.psigns and len(node.psigns) >= signs_threshold:
                        node.gen_commit_msg()
                        print("生成Commit message", node.node_id)
                    elif node.current_block and node.current_sign == 'Commit Message' and node.csigns and len(node.csigns) >= signs_threshold:
                        node.gen_pre_pre_msg()
                            # print("生成Pre-Prepare message", node.node_id)
            else:  # 非首领节点的操作
                # 如果有正在处理的区块，就需要对区块进行验证确认，否则就生成交易和传输交易
                if node.current_block:
                    # print("接收节点信息", node.node_id, node.current_sign, node.psigns)
                    if node.current_block and not node.current_sign:
                        # 还没有传输prepared 消息
                        node.gen_prepared_msg()
                        # print("生成Prepared message", node.node_id)
                    elif node.current_block and node.current_sign == 'Prepared Message' and node.psigns and len(node.psigns) >= signs_threshold:
                            node.gen_commit_msg()    
                            # print("生成Commit message", node.node_id)    
                    elif node.current_block and node.current_sign == 'Commit Message' and node.csigns and len(node.csigns) >= signs_threshold:
                            node.gen_pre_pre_msg()
                else:
                    # print("还没有收到区块")
                    if not node.tx_pool:
                        node.gen_trans(self.current_time)
                    else:
                        if len(node.tx_pool) < 10000:
                            node.gen_trans(self.current_time)

    # 设置故障节点
    def set_aversary(self, gamma):
        # 设置故障节点，gamma 是故障节点所占系统的比例
        num_adversary = int(gamma*len(self.nodes))
        print("故障节点的数量", num_adversary)
        t = 0
        for node in self.nodes:
            if node.sybil == 0 and node.node_id % 2==0 and t < num_adversary:
                node.sybil = 1
                node.lifetime = 15
                node.recent_gen_blocks = 10
                # print("节点被设置为故障节点", node.node_id, t)
                t = t + 1
                # print("t=", t)
                if t >=num_adversary:
                    break

                    # 故障节点事件处理
    def Adversary_event(self, min_tx_num, signs_threshold):
        # print("当前时间", self.current_time)
        for node in self.nodes:
            if node.node_id == self.leader_id:  # 首领节点的操作
                if not node.current_block:                   
                    node.gen_valid_block(min_tx_num, self.current_time)
                    # node.gen_sign()
                    # print("首领生成签名成功了", node.node_id)
                else:
                    if node.sybil == 0:
                        if not node.current_sign and node.psigns and len(node.psigns) >= signs_threshold:
                            node.gen_commit_msg()
                            # print("生成Commit message", node.node_id)
                        elif node.current_sign == 'Commit Message' and node.csigns and len(node.csigns) >= signs_threshold:
                                node.gen_pre_pre_msg()
            else:  # 非首领节点的操作
                # 如果有正在处理的区块，就需要对区块进行验证确认，否则就生成交易和传输交易
                if node.current_block and node.sybil == 0:
                    # print("接收节点信息", node.node_id, node.current_sign, node.psigns)
                    if not node.current_sign and node.current_block:
                        # 还没有传输prepared 消息
                        node.gen_prepared_msg()
                        node.send_prop = 0.0125
                        # print("生成Prepared message", node.node_id)
                    elif node.current_sign == 'Prepared Message' and node.psigns and len(node.psigns) >= signs_threshold:
                            node.gen_commit_msg()    
                            node.send_prop = 0.0125
                            # print("生成Commit message", node.node_id)    
                    elif node.current_sign == 'Commit Message' and node.csigns and len(node.csigns) >= signs_threshold:
                            node.gen_pre_pre_msg()
                else:
                    if not node.tx_pool:
                        node.gen_trans(self.current_time)
                    else:
                        if len(node.tx_pool) < 10000:
                            node.gen_trans(self.current_time)

     # 故障传输消息
    def transmission_Adversary(self, slot, trans_rate):
        for node in self.nodes:
            if node.channel_state == 0 and node.send_queue and self.current_time <= node.send_time < (self.current_time + slot):
                # 节点确定是否要发送消息
                p_send = random.uniform(0,1)
                if p_send <= node.send_prop:
                    temp_sender = [node]
                else:
                    temp_sender = []
                    for tnode in node.neighbors:
                        if tnode.channel_state == 0 and self.current_time <= tnode.send_time < (self.current_time + slot):
                            p_send = random.uniform(0,1)
                            if p_send <= tnode.send_prop:
                                temp_sender.append(tnode)
                if not temp_sender:
                    # print("当前时隙为空",self.current_time)
                    for node in self.nodes:
                        # print("节点信息", node.node_id, node.channel_state, node.send_prop)
                        node.channel_state = 0
                        node.transmission_node = None
                        node.send_time = self.current_time + slot
                    break
                elif len(temp_sender) > 1:
                    print("当前时隙信道忙碌",self.current_time)
                    for node in self.nodes:
                        # print("节点信息", node.node_id, node.channel_state, node.send_prop)
                        node.channel_state = 0
                        node.transmission_node = None
                        node.send_time = self.current_time + slot
                    break
                else:
                    snode = temp_sender[0]
                    snode.channel_state = 1
                    # 确定接收节点集合
                    for rnode in snode.neighbors:
                        # 空闲接收节点决定是否接收该节点的消息
                        if rnode.channel_state == 0:                           
                            rnode.channel_state = 2
                            rnode.transmission_node = [snode]
                            if not snode.transmission_node:
                                snode.transmission_node = [rnode]
                            else:
                                snode.transmission_node.append(rnode)
            elif node.channel_state == 1 and node.send_queue: # 节点发送消息
                data = node.send_queue[0]
                t_trans = node.commpute_trans_time(data, trans_rate) + node.send_time
                # print("节点开始传输的时间和结束的时间", node.node_id, node.send_time , t_trans)
                if self.current_time <= t_trans < self.current_time + slot:
                    # 传输完成，更新发送节点信息
                    # print("节点在当前时隙传输完成", node.node_id, (self.current_time + slot))                    
                    for rnode in node.transmission_node:
                        rnode.update_receivenode_info0(data, self.current_time,slot, trans_rate)
                        # rnode.update_receivenode_info(data, self.current_time,slot, trans_rate, prob_suc)# print("节点的交易池",rnode.node_id, len(rnode.tx_pool))
                    # print("发送节点", node.node_id, len(node.tx_pool))
                    node.update_sendnode_info(data, slot, trans_rate, self.current_time)
        

    
if __name__== '__main__':
    N1 = Network()
    NUM_NODES= 500
    signs_threshold = int(NUM_NODES/2) + 1
    print("所需签名数量", signs_threshold)
    min_tx_num = 20
    N1.create_nodes(NUM_NODES, 200)
    N1.set_basic_info()
    N1.find_adjacent_nodes()
    # print(N1) 
    block_threshold = 960*(int(NUM_NODES/4))
    alpha = 0.5
    prob = 0.01
    current_time = 0
    print("当前时间", current_time)
    while current_time < 3:
        # 确定当前是否有首领节点
        if not N1.leader_id: 
        # 确定当前的首领
            N1.leader_election(prob, alpha)
            print("首领节点是", N1.leader_id)
            for node in N1.nodes:
                node.current_leader_id = N1.leader_id
                if node.node_id == N1.leader_id:
                    N1.leader = node
            prob += 0.1
    # 计算当前完成区块确认的节点数量
        count = 0
        for node in N1.nodes:
            if node.current_leader_id and node.current_block and node.current_block.final_sig:
                count += 1
        if count >= int(len(N1.nodes)/2):
            # N1.update_information()
            for node in N1.nodes:
                if not node.blockchain:
                    node.blockchain = [node.current_block]
                else:
                    node.blockchain.append(node.current_block)
                # 更新交易池中的信息
                node.update_transactions()
                if node.node_id == N1.leader_id:
                    node.recent_gen_blocks += 1
                node.signs = None
                node.final_sign = None
                node.current_sign = None
                node.current_block = None
                node.current_leader_id = None
            dnode = random.choice(N1.nodes)
            dnode.recent_gen_blocks -= 1
            N1.leader_id = None
            N1.Leader = None
            print("当前时间", current_time)
            print('所有节点完成了一次区块确认', current_time, N1.nodes[0].blockchain[-1].block_id)
        N1.handle_event(current_time, SLOT, min_tx_num, signs_threshold)
        N1.transmission(current_time, SLOT, TRANSMISSION_RATE)
        # print("首领节点信息", N1.nodes[2].send_queue[0])
        current_time += SLOT
    # for node in N1.nodes:
    #     print("区块数量", node.node_id, len(node.blockchain))  


        