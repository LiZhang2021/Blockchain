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
    NUM_NODES= 100  # 节点的数量
    TRANSMISSION_RATE = 35*pow(2, 20)  # 信道传输速率
    # SLOT = 512/float(TRANSMISSION_RATE) # 时隙大小
    SLOT= 1
    print("时隙", SLOT)
    MAX_SIMULATIOND_TIME = 100000000 # 仿真时间
    ALPHA = 0.7
    # p_success = np.arange(0.0, 1, 0.05)
    # p_success = [0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35]
    # p_success =[0.75, 0.8, 0.85, 0.9, 0.95]
    # F_ratios = np.arange(0, 0.5, 0.03)
    # F_ratios = np.arange(0.42, 0.5, 0.03)
    signs_threshold = int(NUM_NODES/2) + 1  # 确认阈值
    print("所需签名数", signs_threshold)
    retransis = np.arange(2, 21, 1)
    # retransis = [2]
    # for gamma in F_ratios:
        # ps = 0.8
        # gamma = round(gamma,2)
        # print("故障节点占比", str(gamma))
    for retrans in retransis:
        ps = 0.2
        print("重传次数", str(retrans))
        TIMEOUT = 10000 + retrans * 5000
    # for ps in p_success:
    #     ps = round(ps,2)
    #     print("传输成功概率", str(ps))
        # file_begin_time = open("propagation_Begin_time.txt","a")
        # file_begin_time.writelines(["propagation success probability\t", str(ps), "\n"])
        # file_begin_time.close()
        # file_end_time = open("propagation_End_time.txt","a")
        # file_end_time.writelines(["propagation success probability\t", str(ps), "\n"])
        # file_end_time.close()
        # file_begin_time = open("propagation_Begin_time.txt","a")
        # file_begin_time.writelines(["propagation success probability\t", str(gamma), "\n"])
        # file_begin_time.close()
        # file_end_time = open("propagation_End_time.txt","a")
        # file_end_time.writelines(["propagation success probability\t", str(gamma), "\n"])
        # file_end_time.close()
        file_begin_time = open("propagation_Begin_time.txt","a")
        file_begin_time.writelines(["Retransmission Times\t", str(retrans), "\n"])
        file_begin_time.close()
        file_end_time = open("propagation_End_time.txt","a")
        file_end_time.writelines(["Retransmission Times\t", str(retrans), "\n"])
        file_end_time.close()
        min_tx_num = int((BLOCK_SIZE * 1024 - 256)/512)  # 交易数量
        N1 = Network()
        N1.create_nodes(NUM_NODES, 200)
        N1.set_basic_info()
        # N1.set_sybil_nodes(gamma)
        N1.find_adjacent_nodes()
        N1.current_time = 0
        cblocks = 0 # 当前共识的次数
        fail_times = 0  # 共识失败次数
        # x_trans = np.log(-np.log(0.95)/(len(N1.nodes)-np.log(0.95)))/np.log(1-ps)
        # print("x_trans=", x_trans)
        print("TIMEOUT=", TIMEOUT)
        while N1.current_time < MAX_SIMULATIOND_TIME and cblocks < 100:
            # 确定当前是否有首领节点
            if not N1.leader: 
                # 确定当前的首领   
                # prob = random.uniform(0, 1)
                prob = cblocks/100.0
                # prob = 0
                N1.leader_election(prob, ALPHA)
                print("首领节点是", N1.leader_id)
                for node in N1.nodes:
                    node.current_leader_id = N1.leader_id
                    if node.node_id == N1.leader_id:
                        N1.leader = node
                if N1.leader.sybil == 1:
                    for node in N1.nodes:
                        node.send_time += 4100
                        node.channel_state = 0
                begin_time = N1.current_time
                print("开始时间", begin_time)
                for node in N1.nodes:
                    # print("节点信息",node.node_id, node.lifetime, node.recent_gen_blocks, node.send_prop, node.time_window)
                    node.current_leader_id = N1.leader_id
                    if node.node_id == N1.leader_id:
                        N1.leader = node 
            # 计算当前完成区块确认的节点数量
            count = 0
            for node in N1.nodes:
                if N1.leader and node.current_block and node.current_block.final_sig:
                    count += 1
            # print("当前时间成功接收最终签名节点的数量", N1.current_time, count)
            # if count >= int(NUM_NODES/2):
            if count >= 1:
                insert_block = N1.leader.current_block
                for node in N1.nodes:
                    if not node.blockchain:
                        node.blockchain = [insert_block]
                    else:
                        node.blockchain.append(insert_block)
                    # 更新交易池中的信息
                    node.update_transactions()
                    node.send_queue = None
                    # node.tx_pool = None
                    node.channel_state = 0
                    node.transmission_node = None
                    node.send_queue = None
                    node.send_time = N1.current_time + SLOT
                    node.signs = None
                    node.final_sign = None
                    node.current_sign = None
                    node.current_block = None
                    node.current_leader_id = None
                    node.recent_receive_data = None
                    # node.send_prop = 0.2
                    # node.time_window = 100
                # N1.update_information()               
                file_end_time = open("propagation_End_time.txt","a")
                if N1.leader.node_id == 0:
                    if not N1.leader.blockchain[-1].tx_arr:
                        file_end_time.writelines(["LEADER_ID\t", "0",  "\tBLOCK_ID\t", str(N1.leader.blockchain[-1].block_id), "\tEnd_TIME\t", str(N1.current_time), "\t NUM_TXS\t", "0", "\n"])
                    else:
                        file_end_time.writelines(["LEADER_ID\t", "0",  "\tBLOCK_ID\t", str(N1.leader.blockchain[-1].block_id), "\tEnd_TIME\t", str(N1.current_time), "\t NUM_TXS\t", str(len(N1.leader.blockchain[-1].tx_arr)), "\n"])
                else:
                    if not N1.leader.blockchain[-1].tx_arr:
                        file_end_time.writelines(["LEADER_ID\t", str(N1.leader.node_id),  "\tBLOCK_ID\t", str(N1.leader.blockchain[-1].block_id), "\tEnd_TIME\t", str(N1.current_time), "\t NUM_TXS\t", "0", "\n"])
                    else:
                        file_end_time.writelines(["LEADER_ID\t", str(N1.leader.node_id),  "\tBLOCK_ID\t", str(N1.leader.blockchain[-1].block_id), "\tEnd_TIME\t", str(N1.current_time), "\t NUM_TXS\t", str(len(N1.leader.blockchain[-1].tx_arr)), "\n"])
                file_end_time.close()
                N1.leader_id = None
                N1.leader = None
                
                print('所有节点完成了一次区块确认', N1.current_time, N1.nodes[0].blockchain[-1].block_id)
                cblocks +=1
            if ((N1.current_time - begin_time) == TIMEOUT) and cblocks <100:
                print("共识失败", fail_times)
                for node in N1.nodes:
                    node.send_queue = None
                    node.tx_pool = None
                    node.channel_state = 0
                    node.transmission_node = None
                    node.send_queue = None
                    node.send_time = N1.current_time + SLOT
                    node.signs = None
                    node.final_sign = None
                    node.current_sign = None
                    node.current_block = None
                    node.current_leader_id = None
                    node.recent_receive_data = None
                    # node.send_prop = 0.2
                    # node.time_window = 100
                # N1.update_information()               
                file_end_time = open("propagation_End_time.txt","a")
                if N1.leader.node_id == 0:
                    if not N1.leader.blockchain:
                        file_end_time.writelines(["LEADER_ID\t", "0",  "\tFailed to generate the first block\t", "\tEnd_TIME\t", str(N1.current_time), "\n"])
                    else:
                        if N1.leader.blockchain[-1].tx_arr:
                            file_end_time.writelines(["LEADER_ID\t", "0",  "\tBLOCK_ID\t", str(N1.leader.blockchain[-1].block_id), "\tEnd_TIME\t", str(N1.current_time), "\t NUM_TXS\t", "0", "\n"])
                        else:
                            file_end_time.writelines(["LEADER_ID\t", "0",  "\tBLOCK_ID\t", str(N1.leader.blockchain[-1].block_id), "\tEnd_TIME\t", str(N1.current_time), "\t NUM_TXS\t", str(len(N1.leader.blockchain[-1].tx_arr)), "\n"])
                else:
                    if not N1.leader.blockchain:
                        file_end_time.writelines(["LEADER_ID\t", "0",  "\tFailed to generate the first block\t", "\tEnd_TIME\t", str(N1.current_time), "\n"])
                    
                    else:
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
            # print("当前时间", N1.current_time)    
            # N1.handle_event(min_tx_num, signs_threshold)
            # N1.transmission1(SLOT, TRANSMISSION_RATE,ps)
            N1.Adversary_event(min_tx_num, signs_threshold)
            # N1.transmission_Adversary1(SLOT, TRANSMISSION_RATE, ps)
            N1.transmission_Adversary1(SLOT, TRANSMISSION_RATE, ps, retrans)
            N1.current_time += SLOT
        # file_end_time = open("summary_message_loss.txt","a")
        # file_end_time.writelines(["Propagation success probability\t", str(ps), "\t Consensus times\t", str(cblocks), "\t Failed times\t", str(fail_times), "\n"])
        # file_end_time.close()    
        # file_end_time = open("summary_faulty_nodes_ratio.txt","a")
        # file_end_time.writelines(["Faulty Nodes ratio\t", str(gamma), "\t Consensus times\t", str(cblocks), "\t Failed times\t", str(fail_times), "\n"])
        # file_end_time.close()
        file_end_time = open("summary_retrans_times.txt","a")
        file_end_time.writelines(["retranssation times\t", str(retrans), "\t Consensus times\t", str(cblocks), "\t Failed times\t", str(fail_times), "\n"])
        file_end_time.close()