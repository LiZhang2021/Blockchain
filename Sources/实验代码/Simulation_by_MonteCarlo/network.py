import random
import math
import Crypto.PublicKey.RSA
import Crypto.Signature.PKCS1_v1_5
import Crypto.Hash.SHA256
import hashlib
import operator


from node import Node
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
SLOT = 512/float(TRANSMISSION_RATE) # 一个包大小为512bit，在当前传输速率下时隙长度
NUM_BLOCKS = 10             # 计算共识比的区块数量
ALPHA = 0.5                         # 稳定度

class Network(object):
    def __init__(self):
        self.nodes = []         # 网络中所有节点
        self.leader_id = None    # 当前的出块节点id
        self.leader = None      # 当前首领节点
    
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
                self.nodes[i].lifetime = 500
                self.nodes[i].recent_gen_blocks = 120
            if i % 4 == 1:
                self.nodes[i].lifetime = 1000
                self.nodes[i].recent_gen_blocks = 120
            if i % 4 == 2:
                self.nodes[i].lifetime = 500
                self.nodes[i].recent_gen_blocks = 360
            if i % 4 == 3:
                self.nodes[i].lifetime = 1000
                self.nodes[i].recent_gen_blocks = 360
    
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
    def caculate_stability(self, block_threshold, alpha):
        # 对网络中的节点按照节点ID排序
        self.nodes.sort(key = operator.attrgetter('node_id'))
        sum_time = 0.0
        # 计算所有节点的剩余时间和
        for node in self.nodes:
            sum_time +=  node.lifetime
        # 计算每个节点的稳定度
        for node in self.nodes:
            # 计算共识比
            bratio = round(node.recent_gen_blocks/block_threshold, 4)
            # 计算时间比
            tratio =  round(node.lifetime/sum_time, 4)
            # 计算稳定度
            node.stability =  round(alpha * tratio +  (1- alpha) * bratio, 4)
            # print("节点稳定度", node.node_id, node.lifetime, node.recent_gen_blocks, node.stability)

    # 构建轮盘并选举首领
    def leader_election(self, prob, block_threshold, alpha):
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
            sum_i = sum(probs[:i+1])
            Disk.insert(i+1, sum_i)
        # print("轮盘", Disk )
        # 根据区块链最新确认的区块hash选举首领节点
        for node_id in range(len(probs)):
                if prob >= Disk[node_id] and prob < Disk[node_id+1]: # 判定随机数是否在节点k的区间中
                    self.leader_id = node_id
                    break

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
    def transmission(self, curr_time, slot, trans_rate):
        for node in self.nodes:
            if node.channel_state == 0 and node.send_queue:
                # 找到当前时隙所有要传输的节点
                temp_nodes = [node]
                for tnode in node.neighbors:
                    if tnode.channel_state == 0 and curr_time <= tnode.send_time <= (curr_time + slot):
                        temp_nodes.append(tnode)    
                snode = random.choice(temp_nodes)
                # print("节点开始传输数据", snode.node_id, type(snode.send_queue[0]), snode.send_time) 
                snode.channel_state = 1
                # print("发送节点状态", snode.node_id, snode.channel_state)
                for rnode in snode.neighbors:
                    if rnode.channel_state == 0:
                        rnode.channel_state = 2
                        # print("接收节点状态", rnode.node_id, rnode.channel_state)
                        rnode.transmission_node = [snode]
                        if not snode.transmission_node:
                            snode.transmission_node = [rnode]
                        else:
                            snode.transmission_node.append(rnode)
            elif node.channel_state == 1 and node.send_queue: # 节点发送消息
                # 查看节点发送消息是否结束
                data = node.send_queue[0]
                t_trans = node.commpute_trans_time(data, trans_rate) + node.send_time
                # print("节点开始传输的时间", curr_time, t_trans, curr_time + slot)
                if curr_time <= t_trans < curr_time + slot and node.transmission_node and node.transmission_node[0].send_queue:
                    # 传输完成，更新发送节点信息
                    # print("节点在当前时隙传输完成", node.node_id, (curr_time + slot))                    
                    for rnode in node.transmission_node:
                        rnode.update_receivenode_info(data, curr_time,slot, trans_rate)
                        # print("节点的交易池",rnode.node_id, len(rnode.tx_pool))
                    # print("发送节点", node.node_id, len(node.tx_pool))
                    node.update_sendnode_info(data, slot, trans_rate)
                

    # 事件处理
    def handle_event(self, curr_time, slot, min_tx_num, signs_threshold):
        for node in self.nodes:
            if node.node_id == self.leader_id:  # 首领节点的操作
                if not node.current_block:
                    # print("节点要生成区块", node.node_id)
                    # 如果还没有生成区块，则需要生成区块和区块Hash的签名
                    node.gen_valid_block(min_tx_num, curr_time)
                    node.gen_sign()
                    # print("首领生成签名成功了", node.node_id)
                else:
                    # 已经生成区块之后，判定区块是否被确认
                    if not node.final_sign:
                        if node.signs and len(node.signs) >= signs_threshold:
                            # print("节点生成最终签名了", node.node_id)
                            node.gen_final_sign(signs_threshold)
                        else:
                            # if not node.signs:
                            #     print("节点收集的签名还不够", node.node_id, 0)
                            # else:
                            #     print("节点收集的签名还不够", node.node_id, len(node.signs))
                            if not node.current_sign:
                                node.gen_sign()
                                # print("首领节点生成签名成功了", node.node_id)
                            # else:
                            #     print("节点已经生成签名了，只能等待接收",node.node_id)
                    # node.gen_trans(curr_time)
            else:  # 非首领节点的操作
                # 如果有正在处理的区块，就需要对区块进行验证确认，否则就生成交易和传输交易
                if node.current_block:
                    # 判断是否已经生成当前区块的最终签名
                    if not node.final_sign:
                        if node.signs:
                            if len(node.signs) >= signs_threshold:
                                node.gen_final_sign(signs_threshold)
                                # print("节点生成最终签名了", node.node_id)
                        else:
                            # print("节点收集的签名还不够")
                            if not node.current_sign:
                                node.gen_sign()
                                # print("普通节点生成签名成功了", node.node_id)
                                # print("节点额发送队列", type(node.send_queue[0]))
                            # else:
                            #     print("节点已经生成签名了，只能等待接收",node.node_id)
                else:
                    if not node.tx_pool:
                        node.gen_trans(curr_time)
                    else:
                        if len(node.tx_pool) < 5000:
                            node.gen_trans(curr_time)
   
    # 设置女巫节点
    def set_sybil_nodes(self, gamma):
        # 设置女巫节点，gamma 是女巫节点所占系统的比例
        candidate = []
        for node in self.nodes:
            if node.lifetime <= 500:
                candidate.append(node)
        num_sybil = int(gamma*len(self.nodes))
        print("女巫节点的数量", num_sybil)
        print("候选节点数量", len(candidate))
        for i in range(num_sybil):
            sybil_node = random.choice(candidate)
            sybil_node.sybil = 1
            candidate.remove(sybil_node)

    # 女巫节点事件处理
    def Sybil_event(self, curr_time, slot, min_tx_num, signs_threshold):
        for node in self.nodes:
            if node.node_id == self.leader_id:  # 首领节点的操作
                if not node.current_block:                   
                    # 如果首领节点是女巫节点
                    if node.sybil == 1:
                        node.timeout += slot
                        if node.timeout >= 10*slot: # 70*slot
                            node.gen_empty_block(curr_time)
                            node.timeout = 0
                        else:
                            node.gen_trans(curr_time)
                    else:
                        # 首领节点不是女巫节点
                        # print("节点要生成区块", node.node_id)
                        # 如果还没有生成区块，则需要生成区块和区块Hash的签名
                        node.gen_valid_block(min_tx_num, curr_time)
                        node.gen_sign()
                        # print("首领生成签名成功了", node.node_id)
                else:
                    if node.sybil == 0:
                        # 已经生成区块之后，判定区块是否被确认
                        if not node.final_sign:
                            if node.signs and len(node.signs) >= signs_threshold:
                                # print("节点生成最终签名了", node.node_id)
                                node.gen_final_sign(signs_threshold)
                            else:
                                if not node.current_sign:
                                    node.gen_sign()
            else:  # 非首领节点的操作
                # 如果有正在处理的区块，就需要对区块进行验证确认，否则就生成交易和传输交易
                if node.current_block and node.sybil == 0:
                    # 判断是否已经生成当前区块的最终签名
                    if not node.final_sign:
                        if node.signs:
                            if len(node.signs) >= signs_threshold:
                                node.gen_final_sign(signs_threshold)
                                # print("节点生成最终签名了", node.node_id)
                        else:
                            # print("节点收集的签名还不够")
                            if not node.current_sign:
                                node.gen_sign()
                                # print("普通节点生成签名成功了", node.node_id)
                                # print("节点额发送队列", type(node.send_queue[0]))
                            # else:
                            #     print("节点已经生成签名了，只能等待接收",node.node_id)
                else:
                    if not node.tx_pool:
                        node.gen_trans(curr_time)
                    else:
                        if len(node.tx_pool) < 5000:
                            node.gen_trans(curr_time)

    def run(self):
        # 创建节点和创世区块，并且找到所有节点的邻居节点
        self.create_nodes(NUM_NODES, RADIUS)
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
                print('所有节点完成了一次区块确认', current_time, self.nodes[0].blockchain[-1].blockID)
            self.handle_event(current_time, NUM_BLOCKS , ALPHA, CONFIRM_THRESHOLD)
            self.transmission(current_time, SLOT, TRANSMISSION_RATE)
            current_time += SLOT
        for node in self.nodes:
            print("输出节点信息", node.nodeID, len(node.blockchain))
        # for b in self.nodes[0].blockchain:
        #     b.print_block()

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
            N1.leader_election(prob, block_threshold, alpha)
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


        