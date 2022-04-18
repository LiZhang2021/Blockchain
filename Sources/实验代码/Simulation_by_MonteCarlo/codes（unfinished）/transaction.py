# -*- coding: utf-8 -*-
"""
交易类

Created on Sun Apr 18 11:35:47 2022
@author: shally, ZHANG
"""

from turtle import isvisible


class Transaction(object):
    def __init__(self, tx_id=0):
        self.tx_id = tx_id  # 交易id
        self.payer = "shally"  # 付款人
        self.payee = None  # 收款人
        self.content = None  # 交易内容    
    
    def __str__(self):
        str_fmt = "tx_id: {}, payer: {}, payee: {}\n" + "content: {}"
        return str_fmt.format(self.tx_id, self.payer, self.payee,
                              self.content)


if __name__ == "__main__":
    tx = Transaction(0)
    print(tx)
    print(isinstance(tx, Transaction))

    pass


"""
TODO:
1.

LOG:
# 2022/4/17
1. 暂时仅使用交易ID（为了追溯交易）
2. 
"""