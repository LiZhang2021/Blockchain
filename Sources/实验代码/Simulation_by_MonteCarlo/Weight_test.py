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


# 计算所有节点稳定度
def caculate_stability(NodeList, alpha):
    # 计算所有节点的稳定度
    sum_time = 0
    sum_block = 0
    for node in NodeList:
        sum_time += node.ttime
        sum_block += node.bnum
    for node in NodeList:
        node.tratio = node.ttime/sum_time
        node.bratio = node.bnum/sum_block
        node.stability = alpha * node.tratio +  (1- alpha) * node.bratio

# 计算所有节点被选中的概率，并构建轮盘
def caculate_prob(NodeList, alpha):
    caculate_stability(NodeList, alpha)
    sum_stability = 0
    probs = []
    # 计算所有节点的稳定度之和
    for node in NodeList:
        sum_stability += node.stability
    # 计算各个节点被选中的概率
    for node in NodeList:
        tprob = node.stability/sum_stability
        probs.append(tprob)
    #构建轮盘
    Disk = [0]
    sum_p = 0
    # for i in range(len(probs)):
    #     sum_i = sum(probs[:i+1])
    #     Disk.insert(i+1, sum_i)
    for p in probs:
        sum_p = sum_p + p
        Disk.append(sum_p)
    return Disk

if __name__ == '__main__':
    # 全局变量
    x = []
    y = []
    num_consensus = 100     # 共识次数
    num_nodes = 100         # 节点数量

    # 随机生成节点并赋予不同的时间和共识区块

    # 测试不同alpha值时，优质节点被选中的概率
    alphas = np.arange(0, 1.1, 0.1)
    for alpha in alphas:
        alpha = round(alpha, 4)
        print("alpha为:", alpha)
        NodeList = []
        for j in range(num_nodes):
            if j%4 == 0:
                TNode = Node(j, 100, 50)
                NodeList.append(TNode)
            elif j%4 == 1:
                TNode = Node(j, 200, 50)
                NodeList.append(TNode)
            elif j%4 == 2:
                TNode = Node(j, 500, 50)
                NodeList.append(TNode)
            elif j%4 == 3:
                TNode = Node(j, 200, 50)
                NodeList.append(TNode)
        temp_nodelist = NodeList
        num_best = 0.0  # 记录在不同的alpha下优质节点被选中的次数
        # for node in temp_nodelist:
        #     print("节点", node.index, node.ttime,node.bnum)
        # 测试num_consensus 次数时，优质节点被选中的次数
        for nc in range(num_consensus):
            # for node in temp_nodelist:
            #     print("节点", node.index, node.ttime,node.bnum)
            # 根据所有节点的稳定度绘制轮盘赌
            Disk = caculate_prob(temp_nodelist, alpha)
            # 随机生成出块节点选举的值
            # p = np.random.uniform(0,1) 
            p = nc/(num_consensus+1.0)
            # 确定出块节点（根据轮盘赌）
            for k in range(num_nodes):
                if p >= Disk[k] and p < Disk[k+1]: # 判定随机数是否在节点k的区间中
                    temp = k
                    break            
            # 判定出块节点是否是优质节点
            sum_time = 0
            sum_block = 0
            for node in temp_nodelist:
                sum_time += node.ttime
                sum_block += node.bnum
            ave_time = sum_time/num_nodes
            ave_block = sum_block/num_nodes
            print("均值", ave_time, ave_block)
            for node in temp_nodelist:
                if node.index == temp:
                    print("节点的信息", node.index, node.ttime, node.bnum)
                    if (node.ttime >= ave_time)  and (node.bnum >= ave_block):
                        num_best = num_best + 1
                        #print("优质节点计数：", num_best)
                    # 更新节点的共识区块数量
                    node.bnum = node.bnum + 1
            # 更新所有节点的剩余活动时间
            m = random.randint(0,num_nodes)
            for node in temp_nodelist:
                node.ttime = node.ttime - 1
                if node.index == m:
                    node.bnum = node.bnum - 1
        #计算选中优质节点次数与总共识次数占比
        bp = num_best/num_consensus
        print("优质节点比为：", bp)
        # file_stability = open("Stability.txt","a")
        # file_stability.writelines(["alpha\t", str(alpha), "\tconsensus ratio\t", str(bp), "\n"])
        # file_stability.close()
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

