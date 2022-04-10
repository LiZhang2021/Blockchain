import random
import math

from Crypto.Signature import pkcs1_15
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
import hashlib


from network import Network

NUM_NODES = 5          # 节点数量
CONFIRM_THRESHOLD = 5  # 区块确认阈值
RADIUS = 200                  # 节点的通信半径
TRANSMISSION_RATE = 1*pow(10, 6)            # 信道传输速率
MAX_SIMULATIOND_TIME = 10 # 仿真时间
SLOT = 512/float(TRANSMISSION_RATE) # 一个包大小为512bit，在当前传输速率下时隙长度
NUM_BLOCKS = 10             # 计算共识比的区块数量
ALPHA = 0.9                         # 稳定度

N1 = Network()
N1.create_nodes(NUM_NODES, RADIUS)
N1.create_genesis_block()
N1.find_adjacent_nodes(RADIUS)

Current_Time = 0
Num_Slots = 0
print("当前时间", Current_Time)
while Current_Time < MAX_SIMULATIOND_TIME:
    Num_Slots += 1
    # 每个节点都会生成一个交易
    while Num_Slots == 4:
        Num_Slots = 0
        for node in N1.nodes:
            tx_ID = Current_Time + node.nodeID
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
                node.queuetime.append(Current_Time)
            else:
                node.queuetime.append(Current_Time)
            if node.queuedata == None:
                node.queuedata = []
                node.queuedata.append(temp_tx)
            else:
                node.queuedata.append(temp_tx)
    # 计算当前完成区块确认的节点数量
    count = 0
    for node in N1.nodes:
        if node.currentleader == None and node.currentblock == None and node.finalsign == None:
            count += 1
    if count == len(N1.nodes):
        print('所有节点完成了一次区块确认')
        N1.leader = None
        N1.leaderID = None
        probability = random.uniform(0,1)
    N1.handle_event(probability, Current_Time, NUM_BLOCKS , ALPHA, CONFIRM_THRESHOLD)
    N1.transmission(Current_Time, SLOT, TRANSMISSION_RATE)
    Current_Time += SLOT

for node in N1.nodes:
    print("输出节点信息", node.nodeID, len(node.blockchain))

for b in N1.nodes[0].blockchain:
    b.print_block()
