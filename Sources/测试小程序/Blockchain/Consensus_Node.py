import datetime
import math
import random
from cv2 import threshold
import numpy
import time

import matplotlib.pyplot as plt
import numpy as np

# 节点的类
class Node:
    def __init__(self, index, x, y, radius):
        self.index = index          # 节点的编号
        self.x = x                  # 节点的经度
        self.y = y                  # 节点的维度
        self.radius = radius        # 节点的通信半径
        self.state = 0              # 节点的状态
        self.nodeslist = []         # 存储当前参与共识的所有节点
        self.currentLifetime = 0    # 记录节点的生存时间
        self.currentratio = 0       # 记录节点的共识比
        self.currentStability = 0   # 记录节点当前的稳定度
        self.chain = []             # 记录区块链信息

    # 查看自己是否成为出块节点
    def is_leader(self):
        if 


    # 验证出块节点的有效性

    def is_valid_leader(leader):
        if 


    # 表示一个节点的信息
    def __repr__(self):
        return "Node index: " + str(self.index) + " State: " + str(self.state) \
               + " x: " + str(self.x) + " y: " + str(self.y) \
               + " Radius: " + str(self.radius)+ " Stability: " + str(self.currentStability) \
               + " Lifetime: " + str(self.lifetime) +  "\n"


# 构造节点网络类
class Nodenet:
    # 初始化网络
    def __init__(self):
        self.NodeList = []                # 网络中的节点
        self.CurrentConsensusNodes = []   # 网络中当前共识的节点

    # 生成节点
    def GenerateNode(self, index, x, y, speed, radius, lifetime):
        Gnode = Node(index, x, y, speed, radius)
        self.NodeList.append(Gnode)

    # 计算所有节点的当前稳定度
    def caculate_currentstability(self):
        alpha = 0.95
        beta = 0.05
        threshold = 100
        for node in self.CurrentConsensusNodes:
            if len(node.chain) > threshold: 
                for b_temp in node.chain[-threshold:]:
                    bcount = 0                      # 统最新的Threahold个区块中，节点生成区块的数量
                    if b_temp.leaderID == node.index:
                        bcount = bcount + 1
                ratio = bcount/ threshold           # 计算节点的共识比
                node.currentStability = alpha * node.currentLifetime + beta * ratio
            else:
                node.currentStability = node.currentLifetime

    # 选举出块节点成为leader
    def Winner(self):
        

    #   计算所有节点的邻居节点
    def calculate_all_neiborNodes(self):
        for fnum in range(0, len(self.NodeList)):
            for snum in range(fnum + 1, len(self.NodeList)):
                R = pow((self.NodeList[fnum].x - self.NodeList[snum].x), 2) + pow(
                    (self.NodeList[fnum].y - self.NodeList[snum].y), 2)
                if R <= pow(self.NodeList[fnum].radius, 2):
                    self.NodeList[fnum].neiborlist.append(self.NodeList[snum])
                    self.NodeList[snum].neiborlist.append(self.NodeList[fnum])

if __name__ == '__main__':
    # 初始化一个网络
    Net0 = Nodenet()
     # 网络生成20个节点
    num_node = 0
    while num_node < 200:
        x = random.randint(0,200)
        y = random.randint(0,200)
        speed = 0
        radius = 300
        Net0.GenerateNode(num_node,x,y,speed,radius)
        num_node = num_node + 1

#    for node in Net0.NodeList:
#        node.__repr__()
    list_node_broadcast = []
    list_node_receipt = []
    list_node_conflict = []

# 成功接收消息的节点数量
# 广播节点的数量
    for _ in range(100):
        num_node_broadcast = 0 # 正在广播的节点的个数
        num_node_receipt = 0 # 有效接收的节点的个数
        num_node_conflict = 0 # 发生冲突的节点个数

    # 依概率构造广播节点和接收节点

        node_broadcast = [] # 广播节点
        node_receipt = [] # 接收节点

        # 选出广播节点
        index= random.randint(0, 200)
        for node in Net0.NodeList:
            random_pro = random.uniform(0, 1)
            if (node.index == index) & (random_pro <= 0.5):
                node_broadcast.append(node)
                num_node_broadcast += 1
            else:
                node_receipt.append(node)
        list_node_broadcast.append(num_node_broadcast) # 记录一次循环的广播节点个数
        

    # 计算有效的接收节点
        effective_receipt_node = []
        conflict_receipt_node = []
        for rnode in node_receipt:
            flag = 0 # 该变量用来指示某个接收节点是否处于多个广播节点的广播范围之内，0表示0个，1表示1个...以此类推
            for bnode in node_broadcast:
                if math.sqrt((rnode.x - bnode.x)**2 + (rnode.y- bnode.y)**2) < 300.0:
                    flag += 1
            if flag > 1:
                num_node_conflict += 1
                conflict_receipt_node.append(rnode)
            if flag == 1:
                effective_receipt_node.append(rnode)
                num_node_receipt += 1
        list_node_receipt.append(num_node_receipt) # 记录一次循环的有效节点接收个数
        list_node_conflict.append(num_node_conflict) # 记录一次循环的冲突节点个数
    print('接收节点数量')
    for i in list_node_receipt:
        print(i)
    print("有效发送" + str(numpy.mean(list_node_broadcast)))
    print("有效接收" + str(numpy.mean(list_node_receipt)))
    print("冲突" + str(numpy.mean(list_node_conflict)))
    print("Sy " + str(numpy.mean(list_node_conflict)/numpy.mean(list_node_broadcast)))

'''     # 提取广播节点、接收节点、有效接收节点的坐标
        broadcast_x = [i.x for i in node_broadcast]
        broadcast_y = [i.y for i in node_broadcast]
        receipt_x = [i.x for i in node_receipt]
        receipt_y = [i.y for i in node_receipt]
        effective_receipt_x = [[i.x for i in effective_receipt_node]]
        effective_receipt_y = [[i.y for i in effective_receipt_node]]
        conflict_receipt_x = [[i.x for i in conflict_receipt_node]]
        conflict_receipt_y = [[i.y for i in conflict_receipt_node]]
    
        plt.cla()  # 清除当前绘图
        # 绘制散点图
        plt.scatter(broadcast_x, broadcast_y, s=500, c='#ffffff', edgecolors='#000000', label='broadcast') # 绘制广播节点
        plt.scatter(receipt_x, receipt_y, s=10, c='#000000', edgecolors='#000000', label='receipt') # 绘制全部接收节点
        plt.scatter(effective_receipt_x, effective_receipt_y, s=10, c='#32b16c', edgecolors='#32b16c', label='effective receipt') # 绘制有效接收节点
        plt.scatter(conflict_receipt_x, conflict_receipt_y, s=10, c='#e60012', edgecolors='#e60012', label='conflict receipt') # 绘制冲突接收节点
        plt.show()'''
    
    
    