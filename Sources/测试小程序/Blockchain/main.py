from asyncio.base_events import _ProtocolFactory
from inspect import signature
from unittest import result
from cv2 import threshold

# 节点输入私钥和种子，判定自己是否成为首领
def LeaderElection(sk, seed):
    (value, pi) = VRF(sk, seed) # 随机可验证函数
    if (value == interval):# 判断节点是否被选中成为首领
        result= True
    else:
        result = False
    return value, pi, result

# 验证出块节点的合法性
def VerifyLeader(pk, value, pi):
    if (VerifyVRF(pk, value, pi, seed) == 0):
        return 0
    else:
        return 1

# 计算所有节点的稳定度
def caculate_stability(Nodelist):
    alpha = 0.5
    beta = 0.5
    for node in Nodelist:
        node.currentStability = alpha * node.currentLifetime + beta * node.ratio

# 计算所有节点被选中的概率
def caculate_probability(Nodelist):
    prob = []
    sum_stability = 0
    for node in Nodelist:
        sum_stability = sum_stability + node.currentStability
    for node in Nodelist:
        temp = node.currentStability/sum_stability
        prob.append(temp)
    return prob


# 计算区块哈希
def caculate_hash(inBlock):
    combination = str(inBlock.index) + str(inBlock.timestamp) + str(inBlock.previoushash) + str(inBlock.leader)
    for trans in inBlock.transactionlist:
        combination = combination + str(trans)
    return hashlib.sha256( combination.encode("utf-8")).hexdigest()

# 创建一个新区块
def CreateBlock():
    prevHash = chain[-1].hash   # 节点获取区块链最后一个区块的哈希
    index = len(chain)+1
    newBlock = Block(index, prevHash, nodeID)
    newBlock.transactions = currenttransactions
    newBlock.leaderID = nodeID
    return newBlock

# 检查区块的有效性
def checkBlock(newBlock):
    lastBlock = chain[-1]
    if  lastBlock.index + 1 != newBlock.index:
        result = False
    if lastBlock.hash != newBlock.previoushash:
        result = False
    if caculate_hash(newBlock) != newBlock.hash:
        result = False
    result = True
    return result

# 生成最终签名
def createFinalSig(signatures):
    if len(signatures) > threshold:
        result = Finalsig
    else:
        result = None
    return result

# 添加区块到区块链
def appendBlock(newBlock):
    chain.append(newBlock) 

# RSA算法
# 生成密钥对
def gnerateKeys():
    return sk, pv

# 生成签名
def createSignature(sk, m):
    return sig
# 检查签名
def checkSignature(sig, pv):
    return result

# 随机可验证函数
def VRF(sk, seed):

    return value, proof

# 验证随机结果
def VerifyVRF(pk, value, proof, seed):
    return result

# 广播区块信息
#def broadcastBlock(Block, sig):

# 广播签名信息
#def broadcastSignatue(sig)

# 接收区块信息
#def receiveBlock(Block, sig):

# 接收签名信息
#def receiveSignature(sig):