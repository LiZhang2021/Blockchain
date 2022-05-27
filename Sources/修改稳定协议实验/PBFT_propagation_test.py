# -*- coding: utf-8 -*-
"""
测试节点数量对于时延和吞吐量的影响
参数设置：
0. 区块头大小: 1MB = 1024KB
1. 交易大小: 512B = 0.5KB = 4096 bit
2. 带宽:35Mbps = 35*pow(2, 20)
3. 概率 p = numpy.arange(0, 1, 0.01)
5. 假设每次区块都能打包满区块
6. 时隙大小设为512 bit的传输时间
需要记录的数据：
1. 记录每次选中节点的稳定度、当前的最大稳定度、最小稳定度和平均稳定度
2. 记录共识的时延:测试10次共识过程并记录所有的数据
3. 记录交易数量:记录10次共识过程中生成区块的所有交易
变量：
1. 生成节点数量: 10~1000

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
    from PBFT_node import Node
    from PBFT_network import Network

    BLOCK_SIZE = 1024  # 区块大小设置1MB = 1024KB
    prob_sucs = np.arange(0.1, 1, 0.1)  # 区块大小设置
    # prob_sucs = [1]

    NUM_NODES= 100  # 节点的数量
    TRANSMISSION_RATE = 35*pow(2, 20)  # 信道传输速率
    # SLOT = 512/float(TRANSMISSION_RATE) # 时隙大小
    SLOT = 1
    print("时隙", SLOT)
    MAX_SIMULATIOND_TIME = 100000000 # 仿真时间
    ALPHA = 0.7
    signs_threshold = int(2*NUM_NODES/3) + 1  # 确认阈值
    print("所需签名数", signs_threshold)
    for ps in prob_sucs:
        print("传输成功率", ps)
        file_begin_time = open("Begin_time_propagation(PBFT).txt","a")
        file_begin_time.writelines(["propagation success probability\t", str(ps), "\n"])
        file_begin_time.close()
        file_end_time = open("End_time_propagation(PBFT).txt","a")
        file_end_time.writelines(["propagation success probability\t", str(ps), "\n"])
        file_end_time.close()
        min_tx_num = int((BLOCK_SIZE * 1024 - 256)/512)  # 交易数量
        N1 = Network()
        N1.create_nodes(NUM_NODES, 200)
        # N1.set_basic_info()
        N1.find_adjacent_nodes()
        N1.current_time = 0
        cblocks = 0 # 当前共识的次数
        fail_times = 0  # 共识失败的次数
        while N1.current_time < MAX_SIMULATIOND_TIME and cblocks < 100:
            # 确定当前是否有首领节点
            if not N1.leader: 
                # 确定当前的首领   
                # leader = random.choice(N1.nodes)
                rdm_leader = random.uniform(0,1)
                begin_time = N1.current_time
                print("开始时间", begin_time)
                if rdm_leader <0.67:
                    begin_time = N1.current_time
                    leader = N1.nodes[0]
                    N1.leader = leader
                    N1.leader_id = leader.node_id
                    print("首领节点是", N1.leader_id)
                    for node in N1.nodes:
                        node.current_leader_id = N1.leader_id
                        # if node.node_id == N1.leader_id:
                        #     N1.leader = node    
                else:
                    print("首领节点故障，当前轮共识失败", cblocks)
                    N1.current_time += 25000
                    print("结束时间", N1.current_time)
                    fail_times +=1
                    cblocks +=1
            # 计算当前完成区块确认的节点数量
            count = 0
            for node in N1.nodes:
                if N1.leader and node.current_block and node.current_sign == 'Pre-prepare Message':
                    count += 1
            if count >= int(2*NUM_NODES/3):
                for node in N1.nodes:
                    if not node.blockchain:
                        node.blockchain = [node.current_block]
                    else:
                        node.blockchain.append(node.current_block)
                    # 更新交易池中的信息
                    # node.update_transactions()   
                    node.send_queue = None
                    node.tx_pool = None
                    node.channel_state = 0
                    node.transmission_node = None
                    node.send_queue = None
                    node.send_time = N1.current_time + SLOT
                    node.psigns = None
                    node.csigns = None
                    node.current_sign = None
                    node.current_block = None
                    node.current_leader_id = None
                file_end_time = open("End_time_propagation(PBFT).txt","a")
                if N1.leader.node_id == 0:
                    file_end_time.writelines(["LEADER_ID\t", "0", "\tBLOCK_ID\t", str(N1.leader.blockchain[-1].block_id), "\tEnd_TIME\t", str(N1.current_time), "\t NUM_TXS\t", str(len(N1.leader.blockchain[-1].tx_arr)), "\n"])
                else:
                    file_end_time.writelines(["LEADER_ID\t", str(N1.leader_id), "\tBLOCK_ID\t", str(N1.leader.blockchain[-1].block_id), "\tEnd_TIME\t", str(N1.current_time), "\t NUM_TXS\t", str(len(N1.leader.blockchain[-1].tx_arr)), "\n"])
                file_end_time.close()
                N1.leader_id = None
                N1.leader = None
                print('所有节点完成了一次区块确认', N1.current_time, N1.nodes[0].blockchain[-1].block_id)
                cblocks +=1
            if ((N1.current_time - begin_time) == 30000) and cblocks <100:
                print("共识失败", cblocks)
                for node in N1.nodes:
                    node.send_queue = None
                    node.tx_pool = None
                    node.channel_state = 0
                    node.transmission_node = None
                    node.send_time = N1.current_time + SLOT
                    node.psigns = None
                    node.csigns = None
                    node.current_sign = None
                    node.current_block = None
                    node.current_leader_id = None
                    file_end_time = open("End_time_propagation(PBFT).txt","a")
                if N1.leader and N1.leader.node_id == 0:
                    if not N1.leader.blockchain:
                        file_end_time.writelines(["LEADER_ID\t", "0",  "\tFailed to generate the first block\t", "\tEnd_TIME\t", str(N1.current_time), "\n"])
                    else:
                        if N1.leader.blockchain[-1].tx_arr:
                            file_end_time.writelines(["LEADER_ID\t", "0",  "\tBLOCK_ID\t", str(N1.leader.blockchain[-1].block_id), "\tEnd_TIME\t", str(N1.current_time), "\t NUM_TXS\t", "0", "\n"])
                        else:
                            file_end_time.writelines(["LEADER_ID\t", "0",  "\tBLOCK_ID\t", str(N1.leader.blockchain[-1].block_id), "\tEnd_TIME\t", str(N1.current_time), "\t NUM_TXS\t", str(len(N1.leader.blockchain[-1].tx_arr)), "\n"])
                elif N1.leader and N1.leader.node_id > 0:
                    if not N1.leader.blockchain[-1].tx_arr:
                        file_end_time.writelines(["LEADER_ID\t", str(N1.leader.node_id),  "\tBLOCK_ID\t", str(N1.leader.blockchain[-1].block_id), "\tEnd_TIME\t", str(N1.current_time), "\t NUM_TXS\t", "0", "\n"])
                    else:
                        file_end_time.writelines(["LEADER_ID\t", str(N1.leader.node_id),  "\tBLOCK_ID\t", str(N1.leader.blockchain[-1].block_id), "\tEnd_TIME\t", str(N1.current_time), "\t NUM_TXS\t", str(len(N1.leader.blockchain[-1].tx_arr)), "\n"])
                file_end_time.close()
                print("结束时间", N1.current_time)
                N1.leader_id = None
                N1.leader = None
                fail_times +=1
                cblocks +=1
            N1.handle_event(min_tx_num, signs_threshold)
            N1.transmission(SLOT, TRANSMISSION_RATE, ps)
            N1.current_time += SLOT
        
        file_end_time = open("summary_propagation_End_time(PBFT).txt","a")
        file_end_time.writelines(["propagation success probability\t", str(ps), "\t Consensus times\t", str(cblocks), "\t Failed times\t", str(fail_times), "\n"])
        file_end_time.close()