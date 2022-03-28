import datetime
#构造交易类
class Transaction:
    # 初始化一笔交易
    def __init__(self, index, payer, recer, count):
        self.index = index  # 交易的索引
        self.payer = payer  # 付款方
        self.recer = recer  # 收款方
        self.count = count  # 额度
        self.timestamp = datetime.datetime.now()  # 当前交易块时间
    # 表示交易的信息
    def __repr__(self):
        return str(self.payer) + " pay " + str(self.recer) + " " + str(self.count)