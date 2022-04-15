import random
from xml.dom.minicompat import NodeList
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

# 计算所有节点共识比
def caculate_bratio(NodeList, K):
    bratio_list = []
    # 计算每个节点的共识比，K可以是固定的也可以是可变的
    for node in NodeList:
        node.bratio = node.bnum/K
        node.bratio = round(node.bratio, 4)
    return NodeList

# 计算所有节点剩余时间比
def caculate_tratio(NodeList):
    sum_time = 0.0
    # 计算所有节点的剩余时间和
    for node in NodeList:
        sum_time = sum_time + node.ttime
    # 计算每个节点的剩余时间比
    for node in NodeList:
        if sum_time > 0:
            node.tratio = node.ttime/sum_time
            node.tratio = round(node.tratio, 4)
        else:
            node.tratio = 0
    return NodeList

# 计算所有节点稳定度
def caculate_stability(NodeList, K, alpha):
    sum_time = 0.0
    # 计算所有节点的剩余时间和
    for node in NodeList:
        sum_time = sum_time + node.ttime
    # 计算每个节点的剩余时间比和共识比
    for node in NodeList:
        if sum_time > 0:
            node.tratio = node.ttime/sum_time
            node.tratio = round(node.tratio, 4)
        else:
            node.tratio = 0     
        node.bratio = node.bnum/K
        node.bratio = round(node.bratio, 4)
    stability_list = []
    # 计算所有节点的稳定度
    for node in NodeList:
        node.stability = alpha * node.tratio +  (1- alpha) * node.bratio
        node.stability = round(node.stability, 4)


# 计算所有节点被选中的概率，并构建轮盘
def caculate_prob(NodeList, K, alpha):
    sum_time = 0.0
    # 计算所有节点的剩余时间和
    for node in NodeList:
        sum_time = sum_time + node.ttime
    # 计算每个节点的剩余时间比和共识比
    for node in NodeList:
        if sum_time > 0:
            node.tratio = node.ttime/sum_time
            node.tratio = round(node.tratio, 4)
        else:
            node.tratio = 0     
        node.bratio = node.bnum/K
        node.bratio = round(node.bratio, 4)
    # 计算所有节点的稳定度
    for node in NodeList:
        node.stability = alpha * node.tratio +  (1- alpha) * node.bratio
        node.stability = round(node.stability, 4)
    # 计算节点被选中的概率
    sum_stability = 0.0
    probs = []
    # 计算所有节点的稳定度之和
    for node in NodeList:
        sum_stability += node.stability
    # 计算各个节点被选中的概率
    for node in NodeList:
        tprob = node.stability/sum_stability
        node.prob = round(tprob,4)
        probs.append(tprob)
    #构建轮盘
    Disk = [0]
    sum_p = 0
    for p in probs:
        sum_p = sum_p + p
        sum_p = round(sum_p, 4)
        Disk.append(sum_p)
    return Disk

# 创建不同数量的优质节点，并均匀分布
def create_nodes(num_nodes):
    NodeList = []
    for j in range(num_nodes):
        if j % 4 == 0:
            ttime = 250
            bnum = 12
        elif j % 4 == 1:
            ttime = 500
            bnum = 12
        elif j % 4 == 2:
            ttime = 250
            bnum = 36 
        else:
            ttime = 500
            bnum = 36
        TNode = Node(j, ttime, bnum)
        NodeList.append(TNode)
    return NodeList

if __name__ == '__main__':
    # 全局变量
    x = []
    y = []
    num_consensus = 499     # 共识次数
    num_nodes = 500         # 节点数量
    K = 12000
    NodeList = create_nodes(num_nodes)
    # timelist = []
    # blocklist = []
    # for node in NodeList:
    #     timelist.append(node.ttime)
    #     blocklist.append(node.bnum)
    # tt = np.var(timelist)
    # ttf = np.sqrt(tt)
    # bn = np.var(blocklist)
    # bnf = np.sqrt(bn)
    # print("时间和区块的方差分别是", ttf, bnf, ttf/(ttf+bnf))
    #     print("节点", node.index, node. ttime, node.bnum)
    # 测试不同alpha值时，优质节点被选中的概率
    alphas = np.arange(0, 1.1, 0.1)
    #alphas = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
    for alpha in alphas:
        alpha = round(alpha, 4)
        print("alpha为:", alpha)
        temp_nodelist = create_nodes(num_nodes)
        # print("临时节点数量",len(temp_nodelist), temp_nodelist[5].index, temp_nodelist[5].ttime, temp_nodelist[5].bnum)
        num_best = 0.0  # 记录在不同的alpha下优质节点被选中的次数

        # 测试num_consensus 次数时，优质节点被选中的次数
        for nc in range(num_consensus):
            # 根据所有节点的稳定度绘制轮盘赌
            Disk = caculate_prob(temp_nodelist, K, alpha)
            # 生成出块节点选举的值
            p = nc/50.0
            # 确定出块节点（根据轮盘赌）
            temp = 0
            for t in range(num_nodes):
                if p >= Disk[t] and p < Disk[t+1]: # 判定随机数是否在节点k的区间中
                    temp = t
                    break
            
            # print("选中节点的下标是", temp)
            # 判定出块节点是否是优质节点
            for node in temp_nodelist:
                if node.index == temp:
                    # print("优质节点的信息", node.index, node. ttime, node.bnum)
                    # 更新节点的共识区块数量
                    node.bnum = node.bnum + 1
                    if (node.ttime > 400)  and (node.bnum > 20):
                        num_best = num_best + 1
                        #print("优质节点计数：", num_best)
            d = random.randint(0,num_nodes-1)
            temp_nodelist[nc].bnum -= 1
            # 更新所有节点的剩余活动时间
            for node in temp_nodelist:
                node.ttime = node.ttime - 1

        #计算选中优质节点次数与总共识次数占比
        bp = num_best/num_consensus
        #print("优质节点比为：", bp)
        # 添加对应的alpha和优质节点选中次数占比到数组中
        x. append(alpha)
        y. append(bp)
    
    # 绘图
    y = savgol_filter(y,15, 3,  mode= 'nearest')
    plt.plot(x, y)
    #设置横纵坐标字体大小
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    #标签设置字体大小设置
    plt.xlabel('alpha',fontsize=14)
    plt.ylabel('best_ratio',fontsize=14)
    plt.show()

# 结论
# 1. 选择中位数和均值作为优质节点的判定阈值可以选取到更多的优质节点
# 2. 选择最大值和最小值的平均数作为优质节点的判定阈值选取到较少的优质节点
# 3. 随着alpha的增加，共识中优质节点比呈下降趋势，因此alpha在条件允许的范围内可以设置比较大一点

