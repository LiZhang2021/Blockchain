import random
import math
from time import sleep
from Crypto.Signature import pkcs1_15
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA

from cv2 import sqrt
from Node_Class import Node

trans_nodes = []

class Network:
    def __init__(self):
        self.nodes = []     # 记录网络中所有节点
    
    # 创建节点
    def create_nodes(self, Num_nodes, radius):
        for i in range(Num_nodes):
            temp_x = random.randint(0, 100)
            temp_y = random.randint(0, 100)
            key = RSA.generate(2048)
            temp_privatekey = key.export_key("PEM")
            temp_publickey = key.publickey().export_key("PEM")
            node = Node(i, temp_x, temp_y, radius, temp_privatekey, temp_publickey)
            self.nodes.append(node)

    
    # 根据节点的位置确定所有节点的邻节点
    def find_adjacent_nodes(self, radius):
        for inode in self.nodes:
            for jnode in self.nodes:
                if inode.nodeID != jnode.nodeID:
                    dis = (pow(inode.x - jnode.x, 2)) + (pow(inode.y - jnode.y, 2))
                    if dis <= pow(radius,2):
                        inode.nodelist.append(jnode)
    
     # 传输消息
    def transmission(self, curr_time, timeslot, R):
        for node in self.nodes:
            # 如果信道忙，找到发送节点，判定是否在当前时隙传输消息完成
            if node.busy > 0:
                if node.sendnode == None:
                    # 如果是传输节点，则需要判定当前时间是否传输完数据
                    t_trans = node.send_message(R) + node.queuetime[0]
                    if curr_time <= t_trans <= (curr_time + timeslot):
                        print("传输完成的时间是", t_trans)
                        node.update_information(curr_time, timeslot, R)
                        node.print_node()
                        for knode in node.nodelist:
                            knode.sendnode = None
                            knode.print_node()
                elif node.sendnode != None and (curr_time <= node.queuetime[0] < (curr_time + timeslot)) and len(node.queuetime) > 0:
                    node.channel_busy(R)
            
            else:
                # 如果节点认为信道为空，查看自己是否需要发送数据
                if len(node.queuetime) > 0:
                    if curr_time <= node.queuetime[0] < (curr_time + timeslot):
                        sum_busy = 0
                        for rnode in node.nodelist:
                            sum_busy += rnode.busy
                        if  sum_busy > 0:
                            print("有其他节点在传输，信道忙")
                            node.channel_busy(R)
                        else:
                            # 节点可以传输消息
                            node.busy = 1
                            node.sendnode = None
                            for rnode in node.nodelist:
                                rnode.sendnode = node
                                rnode.channel_busy(R)
                else:
                    print("节点没有消息要发送", node.nodeID)



    # 事件处理
    def handle_event(self, curr_time, timeslot):
        # 每个时隙每个节点都会生成一个交易
        # 每个时隙
        print("节点处理事件")




            


        