import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline

K = 5000

# 声明节点的类
class Node:
    def __init__(self, index, ttime, bnum):
        self.index = index          # 节点的编号
        self.prob = 0               # 记录节点被选中的概率
        self.ttime = ttime          # 记录节点剩余时间
        self.bnum = bnum            # 记录节点共识区块数量
        self.tratio = 0             # 记录节点剩余时间比
        self.bratio = 0             # 记录节点共识比
        self.stability = 0          # 记录节点稳定度
# 计算节点共识比
def caculate_bratio(NodeList):
    bratio_list = []
    for node in NodeList:
        node.bratio = node.bnum/K
        bratio_list.append(node.bratio)
    bthreshold = np.mean(bratio_list)
    return bthreshold

# 计算所有节点剩余时间比
def caculate_tratio(NodeList):
    sum_time = 0
    tratio_list = []
    for node in NodeList:
        sum_time = sum_time + node.ttime
    for node in NodeList:
        node.tratio = node.ttime/sum_time
        tratio_list.append(node.tratio)
    tthreshold = np.mean(tratio_list)
    return tthreshold

# 计算节点稳定度
def caculate_stability(NodeList, alpha):
    stability_list = []
    for node in NodeList:
        node.stability = alpha * node.tratio + (1 - alpha) * node.bratio
        stability_list.append(node.stability)
    Mstability = max(stability_list)
    return Mstability
# 计算所有节点被选中的概率，并构建轮盘
def caculate_prob(NodeList):
    sum_stability = 0
    probs = []
    for node in NodeList:
        sum_stability = sum_stability + node.stability

    for node in NodeList:
        tprob = node.stability/sum_stability
        node.prob = round(tprob,4)
        probs.append(tprob)
    return probs

if __name__ == '__main__':
    x = []
    y = []
    alphas = np.arange(0, 1.1, 0.1)
    num_consensus = 100
    #alphas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    for alpha in alphas:
        # 随机生成两百个节点，并赋予不同的时间和共识区块
        num_nodes = 500
        NodeList = []
        temp_K = K
        for i in range(num_nodes):
            ttime = np.random.uniform(0, 1000)
            bnum = random.randint(0, temp_K)
            temp_K = temp_K - bnum
            TNode = Node(i, ttime, bnum)
            NodeList.append(TNode)
        if temp_K > 0:
            node = random.choice(NodeList)
            node.bnum = node.bnum + temp_K
        bthreshold = caculate_bratio(NodeList)
        tthreshold = caculate_tratio(NodeList)
        Mstability = caculate_stability(NodeList,alpha)

        # 计算10次共识过程中优质节点选中共识比
        num_best = 0.0  # 记录优质节点被选中的次数
        for node in NodeList:
            if node.stability == Mstability:
                #print("节点的时间比和共识比分别为：", node.tratio, node.bratio)
                if node.tratio > tthreshold  and node.bratio > bthreshold:
                    num_best = num_best + 1
        
        #print("优质节点数量：", num_best)
        #print("alpha为:", alphas)
        bp = num_best/num_consensus
        #print("优质节点比为：", bp)
        x. append(alpha)
        y. append(bp)
    y_smooth = savgol_filter(y,15,3, mode= 'nearest')
    plt.plot(x, y_smooth)
    plt.show()


