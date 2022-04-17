# -*- coding: utf-8 -*-
"""
区块类

Created on Sun Apr 17 10:37:47 2022
@author: shally, ZHANG
"""
MAX_BLOCK_NUM = 100000000000  # 区块中交易个数的上限 
MIN_BLOCK_NUM = 1000  # 区块中交易个数的下线

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
        str_fmt = "leader_id:{}, block_id:{}, pre_hash:{}, block_hash:{}\n" + "TX: {}"
        return str_fmt.format(self.leader_id, self.block_id, self.pre_hash, 
                              self.block_hash, self.tx_arr)  # TODO


if __name__ == "__main__":
    from transaction import Transaction
    tx1 = Transaction(0)
    tx2 = Transaction(1)
    block = Block(0,0,0,[tx1, tx2])
    print(block)
    pass


"""
TODO
1. 改进区块的输出格式

LOG:
# 2022/4/17
1. 调整代码结构

"""
    
    
    