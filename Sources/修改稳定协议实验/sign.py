# -*- coding: utf-8 -*-
"""
区块类

Created on Sun Apr 18 11:37:47 2022
@author: shally, ZHANG
"""

class Sign(object):
    def __init__(self, signer_id, sign_content):
        self.signer_id = signer_id  # 签名节点的id
        self.sign_content = sign_content  # 签名内容
        self.signature = self.set_sign() # 签名
    
    def set_sign(self):
        signature = str(self.signer_id) + " signs " + str(self.sign_content)
        return signature
    
    def __str__(self):
        str_fmt = "signer_id:{}, sign_content:{}\n" + "signature:{}"
        return str_fmt.format(self.signer_id, self.sign_content, self.signature) 
                

if __name__ == "__main__":
    from block import Block
    from transaction import Transaction
    tx = Transaction(1)
    block = Block(0,0,0,[tx])
    block.hash = "shally"
    # print(block)
    sign = Sign("shally0", block.hash)
    print(sign)
    pass


"""
TODO
1. 改进区块的输出格式(完成)

LOG:
# 2022/4/18
1. 

"""
