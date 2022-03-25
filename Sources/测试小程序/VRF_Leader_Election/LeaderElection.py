from re import S
import VRF_Func

from VRF_Func import VRF, VRF_verify
N = 100
prob = []   # 记录所有共识节点被选中的概率

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

# 节点输入出块节点公钥、值、证明和种子，判定出块节点的合法性
def VerifyLeader(pk, value, proof, nodeID, seed):
    result = VRF_verify(pk, seed, proof)
    low_value = sum(prob[:nodeID])
    high_value = sum(prob[:nodeID + 1])
    if result == False or low_value > value/pow(2, len(value)) or value/pow(2, len(value)) > high_value:
        return False
    else:
        return True