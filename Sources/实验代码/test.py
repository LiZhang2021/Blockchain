import random
import math
from time import sleep
from Crypto.Signature import pkcs1_15
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
import hashlib

from cv2 import sqrt
from Node_Class import Node
from Network import Network

Num_nodes = 3          # 节点数量
radius = 200                  # 节点的通信半径
R = 1*pow(10, 6)            # 信道传输速率
maxSimulationTime = 10 # 仿真时间
timeslot = 512/float(R) # 一个包大小为512bit，在当前传输速率下时隙长度
K = 1
alpha = 0.9

N1 = Network()
N1.create_nodes(Num_nodes, radius)
N1.Create_GenesisBlock()
N1.find_adjacent_nodes(radius)


curr_time = 0
print("当前时间", curr_time)
while curr_time < maxSimulationTime:
    # 每个节点都会生成一个交易
    # print("当前时间", curr_time)
    N1.handle_event(curr_time, K, alpha)
    N1.transmission1(curr_time, timeslot, R)
    # curr_time += 0.1
    curr_time += timeslot

for node in N1.nodes:
    print("节点的区块数量", node.nodeID, len(node.blockchain))

    


