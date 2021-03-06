# -*- coding: utf-8 -*-
"""
交易类

Created on Sun Apr 17 10:37:47 2022
@author: shally, ZHANG
"""

class Transaction(object):
    def __init__(self, tx_id):
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

    pass

"""
TODO:
1. 

LOG:
# 2022/4/18
1. 暂时仅使用交易tx_id属性（为了追溯交易）
2. 
"""