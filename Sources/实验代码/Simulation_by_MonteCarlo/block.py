# -*- coding: utf-8 -*-
"""
区块类

Created on Sun Apr 18 11:37:47 2022
@author: shally, ZHANG
"""

class Block(object):
    def __init__(self, block_id, leader_id, pre_hash, tx_arr):
        self.block_id = block_id  # 区块id / 区块高度
        self.leader_id = leader_id  # 出块节点（首领）id
        self.pre_hash = pre_hash  # 前一个区块（所有内容的id）
        self.hash = None  # 区块hash
        self.block_sig = None  # （出块节点的）区块签名
        self.final_sig = None  # 区块hash最终签名 
        self.tx_arr = tx_arr  # 区块打包的交易列表
    
    def __str__(self):
        if not self.tx_arr:
            str_fmt = "block_id:{}, leader_id:{}, pre_hash:{}, block_hash:{}, TX is None"
            return str_fmt.format(self.block_id, self.leader_id, self.pre_hash, 
                              self.hash) 
        else:
            str_fmt = "block_id:{}, leader_id:{}, pre_hash:{}, block_hash:{}\n" + "TX: {}"
            return str_fmt.format(self.block_id, self.leader_id, self.pre_hash, 
                                self.hash, [str(tx) for tx in self.tx_arr]) 
                

if __name__ == "__main__":
    from transaction import Transaction
    tx1 = Transaction(0)
    tx2 = Transaction(1)
    block = Block(0,0,0,[tx1, tx2])
    print(block)
    pass


"""
TODO
1. 改进区块的输出格式(完成)

LOG:
# 2022/4/17
1. 调整代码结构

"""

