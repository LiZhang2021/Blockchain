
num_nodes = 800
K = 144

# 声明节点的类
class Node:
    def __init__(self, index, rho, r):
        self.index = index          # 节点的编号
        self.currentratio = r       # 记录节点的共识比
        self.currtentimeratio = rho   # 记录节点的剩余活动时间比
        self.currentStability = 0   # 记录节点当前的稳定度

    # 计算节点稳定度
    def Caculate_Stability(self, alpha, beta):
        self.currentStability = alpha & self.currtentimeratio + beta * self.currentratio

# 生成两百个节点
