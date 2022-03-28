import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline


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
    bthreshold = np.median(bratio_list)
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
    tthreshold = np.median(tratio_list)
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
    # 全局变量
    x = []
    y = []
    alphas = np.arange(0, 1.1, 0.1)
    num_consensus = 10
    num_nodes = 500
    #alphas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    for alpha in alphas:
        alpha = round(alpha, 4)
        print("alpha为:", alpha)
        K = 1000
        print("区块数量：", K)
        num_best = 0.0  # 记录在不同的alpha下优质节点被选中的次数
        for i in range(num_consensus):
            # 随机生成节点并赋予不同的时间和共识区块
            NodeList = []
            temp_K = K
            for j in range(num_nodes):
                ttime = np.random.uniform(0, 1000)
                bnum = random.randint(0, temp_K)
                temp_K = temp_K - bnum
                TNode = Node(j, ttime, bnum)
                NodeList.append(TNode)
            if temp_K > 0:
                node = random.choice(NodeList)
                node.bnum = node.bnum + temp_K
            # 计算所有节点的时间比、共识比和稳定度
            bthreshold = caculate_bratio(NodeList)
            tthreshold = caculate_tratio(NodeList)
            Mstability = caculate_stability(NodeList,alpha)
            # print("最大稳定度：",Mstability)

            # 根据所有节点的稳定度绘制轮盘赌
            probs = caculate_prob(NodeList)
            # p = np.random.uniform(0,1) # 随机生成出块节点选举的值
            p = random.random()
            p = round(p,4)
            #print("概率值：", p)
            for k in range(num_nodes):
                temp = 0
                low = sum(probs[:k])
                high = sum(probs[:k+1])
                if p >= low and p< high: # 判定随机数是否在节点k的区间中
                    temp = k
                    break
            for node in NodeList:
                if node.index == temp:
                    if node.tratio > tthreshold  and node.bratio > bthreshold:
                        num_best = num_best + 1
                        print("优质节点计数：", num_best)
                        #print("节点的时间比和共识比分别为：", node.tratio, node.bratio)
        
        
        
        print("优质节点数量：", num_best)
        bp = num_best/num_consensus
        #print("优质节点比为：", bp)
        x. append(alpha)
        y. append(bp)
    y = savgol_filter(y,25,3,  mode= 'nearest')
    plt.plot(x, y)
    plt.show()


