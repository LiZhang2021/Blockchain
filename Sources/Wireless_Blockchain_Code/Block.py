import datetime     # 导入日期时间库
import hashlib      # 导入哈希函数库
import time         # 导入时间库

# 构建区块类
class Block:
    # 初始化一个区块
    def __init__(self, index, previoushash, leaderID):
        self.index = index                             # 区块的索引
        self.transactionslist = []                   #存储区块中的交易
        self.timestamp = datetime.datetime.now()    # 区块生成时间
        self.hash = None                            # 区块哈希
        self.previoushash = previoushash  # 前一个区块的哈希
        self.currentNodes = set()               # 存储生成这个区块时的系统中节点的信息
        self.leaderID = leaderID                       # 存储区块的出块节点信息
    
    # 计算块的哈希
    def set_hash(self):
        combination = str(self.index) + str(self.timestamp) + str(self.previoushash) + str(self.leader)
        for trans in self.transactionlist:
            combination = combination + str(trans)
        self.hash = hashlib.sha256( combination.encode("utf-8")).hexdigest()
    # 表示区块中的信息
    def __repr__(self):
        return "\nblock PreviouHash: " + str(self.previoushash) + "\nblock Transactionlist: " + str(len(self.transactionlist)) \
               + "\nblock TimeStamp: " + str(self.timestamp) + "\nblock Hash: " + str(self.hash) + "\nblock Difficulty: " \
               + str(self.difficulty) + "\nblock Nonce: " + str(self.nonce) + "\n"