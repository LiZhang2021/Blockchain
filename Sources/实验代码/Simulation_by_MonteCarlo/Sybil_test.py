# -*- coding: utf-8 -*-
"""
测试节点数量对于时延和吞吐量的影响
参数设置：
0. 区块头大小: 1MB = 1024B
1. 交易大小: 512B = 0.5KB = 4096 bit
2. 节点数量: 500
3.概率 p = numpy.arange(0, 1, 0.01)
4. 假设每次区块都能打包满区块
5. 时隙大小设为512 bit的传输时间
需要记录的数据：
1. 记录每次选中节点的稳定度、当前的最大稳定度、最小稳定度和平均稳定度
2. 记录共识的时延:测试10次共识过程并记录所有的数据
3. 记录交易数量:记录10次共识过程中生成区块的所有交易
变量：
1. 女巫节点的比例: 0 ~ 49%

Created on Sun Apr 19 2022
@author: shally, ZHANG
"""
from random import random
import numpy as np
import random


if __name__== '__main__':
    from transaction import Transaction
    from block import Block
    from sign import Sign
    from finalsign import Finalsign
    from node import Node
    from network import Network

    BLOCK_SIZE = 1024  # 区块大小设置1MB = 1024KB
    NUM_NODES= 300  # 节点的数量
    TRANSMISSION_RATE = 35*pow(2, 20)  # 信道传输速率
    SLOT = 512/float(TRANSMISSION_RATE) # 时隙大小
    print("时隙", SLOT)
    MAX_SIMULATIOND_TIME = 10000 # 仿真时间
    ALPHA = 0.5
    # gammas = np.arange(0.45, 0.50, 0.01)
    gammas = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.49]
    # gammas = [0.35, 0.4, 0.45, 0.49]
    signs_threshold = int(NUM_NODES/2) + 1  # 确认阈值
    print("所需签名数", signs_threshold)
    block_threshold = 960*(NUM_NODES/4)
    for gamma in gammas:
        gamma = round(gamma,2)
        print("女巫节点占比", str(gamma))
        file_begin_time = open("Sybil_Begin_time.txt","a")
        file_begin_time.writelines(["Sybil_percentage\t", str(gamma), "\tSybil_num_nodes\t", str(gamma * NUM_NODES), "\n"])
        file_begin_time.close()
        file_end_time = open("Sybil_End_time.txt","a")
        file_end_time.writelines(["Sybil_percentage\t", str(gamma), "\tSybil_num_nodes\t", str(gamma * NUM_NODES), "\n"])
        file_end_time.close()
        file_stability = open("Sybil_Stability.txt","a")
        file_stability.writelines(["Sybil_percentage\t", str(gamma), "\tSybil_num_nodes\t", str(gamma * NUM_NODES), "\n"])
        file_stability.close()
        min_tx_num = int((BLOCK_SIZE * 1024 - 256)/512)  # 交易数量
        N1 = Network()
        N1.create_nodes(NUM_NODES, 200)
        N1.set_basic_info()
        N1.find_adjacent_nodes()
        N1.set_sybil_nodes(gamma)
        N1.current_time = 0
        cblocks = 0 # 当前共识的次数
        while N1.current_time < MAX_SIMULATIOND_TIME and cblocks < 10:
            # 确定当前是否有首领节点
            if not N1.leader: 
                # 确定当前的首领   
                # prob = random.uniform(0, 1)
                prob = cblocks/10.0
                N1.leader_election(prob, ALPHA)
                print("首领节点是", N1.leader_id)
                file_stability = open("Sybil_Stability.txt","a")
                for node in N1.nodes:
                    file_stability.writelines(["NODE_STABILITY\t Node_id\t", str(node.node_id), "\t Stability\t", str(node.stability), "\t\n"])
                    node.current_leader_id = N1.leader_id
                    if node.node_id == N1.leader_id:
                        N1.leader = node  
                        # 提升出块节点传输概率
                        node.send_prop = (1+0.1) * node.send_prop
                        if node.send_prop > 0.9:
                            node.send_prop = 0.9
                    else:
                        # 降低普通节点传输概率
                        node.send_prop = node.send_prop/(1+0.1)
                if N1.leader_id == 0:            
                    file_stability.writelines(["LEADER_STABILITY\t", "0", "\tLEADER_ID_type\t", str(N1.leader.sybil), "\tStability\t", str(N1.leader.stability), "\t\n"])
                else:
                    file_stability.writelines(["LEADER_STABILITY\t", str(N1.leader.node_id), "\tLEADER_ID_type\t", str(N1.leader.sybil), "\tStability\t", str(N1.leader.stability), "\t\n"])
                file_stability.close()
            # 计算当前完成区块确认的节点数量
            count = 0
            for node in N1.nodes:
                if N1.leader and node.current_block and node.current_block.final_sig:
                    count += 1
            if count >= int(NUM_NODES/2):
                for node in N1.nodes:
                    if not node.blockchain:
                        node.blockchain = [node.current_block]
                    else:
                        node.blockchain.append(node.current_block)
                    # 更新交易池中的信息
                    node.update_transactions()
                    node.signs = None
                    node.final_sign = None
                    node.current_sign = None
                    node.current_block = None
                    node.current_leader_id = None
                    node.send_prop = 0.5
                    node.time_window = 10
                    node.recent_receive_data = None
                N1.update_information()               
                file_end_time = open("Sybil_End_time.txt","a")
                if N1.leader.node_id == 0:
                    if not N1.leader.blockchain[-1].tx_arr:
                        file_end_time.writelines(["LEADER_ID\t", "0", "\tLEADER_ID_type\t", str(N1.leader.sybil), "\tBLOCK_ID\t", str(N1.leader.blockchain[-1].block_id), "\tEnd_TIME\t", str(N1.current_time), "\t NUM_TXS\t", "0", "\n"])
                    else:
                        file_end_time.writelines(["LEADER_ID\t", "0", "\tLEADER_ID_type\t", str(N1.leader.sybil), "\tBLOCK_ID\t", str(N1.leader.blockchain[-1].block_id), "\tEnd_TIME\t", str(N1.current_time), "\t NUM_TXS\t", str(len(N1.leader.blockchain[-1].tx_arr)), "\n"])
                else:
                    if not N1.leader.blockchain[-1].tx_arr:
                        file_end_time.writelines(["LEADER_ID\t", str(N1.leader.node_id), "\tLEADER_ID_type\t", str(N1.leader.sybil), "\tBLOCK_ID\t", str(N1.leader.blockchain[-1].block_id), "\tEnd_TIME\t", str(N1.current_time), "\t NUM_TXS\t", "0", "\n"])
                    else:
                        file_end_time.writelines(["LEADER_ID\t", str(N1.leader.node_id), "\tLEADER_ID_type\t", str(N1.leader.sybil), "\tBLOCK_ID\t", str(N1.leader.blockchain[-1].block_id), "\tEnd_TIME\t", str(N1.current_time), "\t NUM_TXS\t", str(len(N1.leader.blockchain[-1].tx_arr)), "\n"])
                file_end_time.close()
                N1.leader_id = None
                N1.leader = None
                print('所有节点完成了一次区块确认', N1.current_time, N1.nodes[0].blockchain[-1].block_id)
                cblocks +=1
            N1.Sybil_event(min_tx_num, signs_threshold)
            N1.transmission(SLOT, TRANSMISSION_RATE)
            N1.current_time += SLOT