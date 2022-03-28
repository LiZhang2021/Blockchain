

# 节点的类
class Node:
    def __init__(self, index, x, y, radius):
        self.index = index          # 节点的编号
        self.x = x                  # 节点的经度
        self.y = y                  # 节点的纬度
        self.radius = radius        # 节点的通信半径
        self.keys = []              # 节点的密钥对
        self.publickeys = []        # 存储其他节点的公钥
        self.state = 0              # 节点的状态
        self.nodeslist = []         # 存储当前参与共识的所有节点
        self.currentLifetime = 0    # 记录节点的生存时间
        self.currentratio = 0       # 记录节点的共识比
        self.currentStability = 0   # 记录节点当前的稳定度
        self.chain = []             # 记录区块链信息
    
    # 节点输入私钥和种子，判定自己是否成为首领
    def LeaderElection(self, sk, seed):
    (value, pi) = VRF(sk, seed) # 随机可验证函数
    ID = 0
    for i in range(N):
        low_value = sum(prob[:i])
        high_value = sum(prob[:i+1])
        if low_value > value/pow(2, len(value)) or value/pow(2, len(value)) > high_value:# 判断节点是否被选中成为首领
            ID = ID + 1
    if ID == self.NodeID:
        result= True
    else:
        result = False
    return value, pi, result

