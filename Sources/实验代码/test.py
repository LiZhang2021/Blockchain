import random
import math

from Crypto.Signature import pkcs1_15
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
import hashlib


from network import Network

Num_nodes = 3          # 节点数量
radius = 200                  # 节点的通信半径
R = 1*pow(10, 6)            # 信道传输速率
maxSimulationTime = 5 # 仿真时间
timeslot = 512/float(R) # 一个包大小为512bit，在当前传输速率下时隙长度
K = 1
alpha = 0.9

N1 = Network()
N1.create_nodes(Num_nodes, radius)
N1.create_genesis_block()
N1.find_adjacent_nodes(radius)

curr_time = 0
print("当前时间", curr_time)
while curr_time < maxSimulationTime:
    # 每个节点都会生成一个交易
    for node in N1.nodes:
        tx_ID = curr_time + node.nodeID
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
            node.queuetime.append(curr_time)
        else:
            node.queuetime.append(curr_time)
        if node.queuedata == None:
            node.queuedata = []
            node.queuedata.append(temp_tx)
        else:
            node.queuedata.append(temp_tx)
        

    N1.handle_event(curr_time, K, alpha)
    N1.transmission(curr_time, timeslot, R)
    # curr_time += 0.1
    curr_time += timeslot

for node in N1.nodes:
    print("输出节点信息", node.nodeID, len(node.blockchain))
