import operator  #导入operator 包,pip install operator
from Crypto.Signature import pkcs1_15
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA


class Node:
    def __init__(self, nodeID, privatekey, public_key):
         self.nodeID = nodeID
         self.transactions = []     # 存储交易
         self.blockchain = []       # 存储区块链
         self.nodelist = []            # 存储所有节点信息
         self.lifetime = 0             # 存储节点的寿命
         self.numblocks = 0        # 存储生成出块节点的数量
         self.privatekey = privatekey   # 存储私钥
         self.publickey = public_key    # 存储公钥
    
    # 生成一个交易
    def Create_Trans(ID):
        return {'Trans_ID: ': ID}   # 交易ID
    
    # 生成一个区块
    def create_Block(self, previous_hash, leaderID, current_transactions):
        block ={
            # 区块ID(Height)
            'ID':len(self.blockchain)+1,
            # 上一块区块的hash
            'previous_hash':previous_hash,
            # 出块节点
            'leaderID':leaderID,
            # 区块的hash
            'Hash': None,
            # 区块最终签名（区块 + 区块Hash + 签名）
            'final_signature': None,
            # 交易账本
            'transactions': current_transactions
        }
        return block
    
    # 对消息签名
    def RSA_Signature(self, data):
        # 获取 数据消息 的HASH值，摘要算法MD5，验证时也必须用MD5
        digest = MD5.new(data.encode('utf-8'))
         # 使创建 私钥 签名工具, 并用私钥对HASH值进行签名
        signature = pkcs1_15.new(self.privatekey).sign(digest)
        return signature

    # 验证签名
    def RSA_Verifier(public_key,data, signature):
        # 获取 数据消息 的HASH值，签名时采用摘要算法MD5，验证时也必须用MD5
        digest = MD5.new(data.encode('utf-8'))
        # 使用Crypto.Signature 中 公钥 验签工具 对 数据和签名 进行验签
        verify_result = pkcs1_15.new(public_key).verify(digest, signature)
        return verify_result
    
    # 验证区块的有效性
    def Verify_Block(self, block, leaderID):
         # 验证出块节点的合法性
        if block.leaderID != leaderID:
            verify_result = False
         # 验证区块高度的有效性
        elif block.ID != len(self.blockchain)+1:
            verify_result = False
         # 验证父区块hash的有效性
        elif block.previous_hash != self.blockchain[-1].hash:
            verify_result = False
         # 验证交易的有效性
        for tx in block.transactions:
            for bc in self.blockchain:
                if tx in bc.transactions:
                    verify_result = False
        else:
            verify_result = True
        return verify_result

    # 首领选举
    # 计算节点的稳定度
    def Caculate_Stability(self, K, alpha, beta):
        sum_time = 0.0
        # 计算所有节点的剩余时间和
        for node in self.nodelist:
            sum_time = sum_time + node.lifetime
        # 计算每个节点的稳定度
        for node in self.nodelist:
            bratio = round(node.bnum/K, 4)
            tratio =  round(node.lifetime/sum_time, 4)
            node.stability =  round(alpha * tratio +  (1- alpha) * bratio, 4)

    # 构建轮盘并选举首领
    def Leader_Election(self):
        # 按照节点的ID进行排序
        self.nodelist.sort(key = operator.attrgetter('nodeID')) 
        sum_stability = 0
        probs = []
        # 计算所有节点的稳定度之和
        for node in self.nodelist:
            sum_stability = sum_stability + node.stability
        # 计算各个节点被选中的概率
        for node in self.nodelist:
            prob = round(node.stability/sum_stability, 4)
            probs.append(prob)
        #构建轮盘
        Disk = [0]
        sum_p = 0
        for prob in probs:
            sum_p = round(sum_p + prob, 4)
            Disk.append(sum_p)
        # 根据区块链最新确认的区块hash选举首领节点
        seed = self.blockchain[-1].hash
        probability = seed/2^(len(seed))
        for k in range(len(probs)):
                if probability >= Disk[k] and probability < Disk[k+1]: # 判定随机数是否在节点k的区间中
                    leaderID = k
                    break
        return leaderID
    
    # 同步交易
    def Synchronous_Transaction(self, block):
        for tx in block.transactions:
            if tx in self.transactions:
                self.transactions.remove(tx)

    # 同步区块
    def Synchronous_Block(self, block):
        self.blockchain.append(block)

    # 同步系统信息
    def Synchronous_Information(self, leaderID, K):
        # 更新节点信息，包括节点数量、节点ID，节点稳定度（剩余活动时间和共识区块数量）
        for node in self.nodelist:
            if node.lifetime == 0:
                self.nodelist.remove(node)
            if node.nodeID == leaderID:
                node.numblocks = node.numblocks + 1
            if node.nodeID ==  node.blockchain[-K].leaderID:
                node.numblocks = node.numblocks - 1
    
    # 注册新节点
    def Regist_Node(self, node):
        if node in self.nodelist:
            print("The node has been there!")
        else:
            self.nodelist.append(node)
            print("Add new node successfully!")

        
    
