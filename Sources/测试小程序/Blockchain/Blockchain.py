import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
from Block import Block
from Transaction import Transaction
 
 
class Blockchain(object):
    # 区块链初始化
    def __init__(self, ID):
        self.chain = []  # 此列表表示区块链对象本身。
        self.currentTransactions = []  # 此列表用于记录目前在区块链网络中已经经矿工确认合法的交易信息，等待写入新区块中的交易信息。
        self.nodes = set()  # 建立一个无序元素集合。此集合用于存储区块链网络中已发现的所有节点信息
        self.set_nodeID(ID) # 记录维护区块的节点ID
    
    # 维护区块链节点的ID
    def set_nodeID(self, node_id):
        self.nodeID = node_id

    # 创建创世区块
    def create_genesis_block(self):
        Genesis = Block(0, 1, -1)
        self.chain.append(Genesis)

    # 注册节点
    def Register_node(self, node):
        self.nodes.add(node)

    # 生成新区块
    def New_block(self, index, previous_hash, NodeID ):
        newBlock = Block(index, previous_hash, NodeID)
        newBlock.transactionslist = self.currentTransactions
        newBlock.leaderID = self.nodeID
        return newBlock
 
    # 创建新交易
    def new_Transaction(self, index, payer, recer, count):
        newTransaction = Transaction(index, payer, recer, count)
        return newTransaction

    # 获取区块链最后一个区块
    def last_Block(self):
        return self.chain[-1] 
    
    # 计算区块的哈希
    def caculate_hash(self, inBlock):
        combination = str(inBlock.index) + str(inBlock.timestamp) + str(inBlock.previoushash) + str(inBlock.leader)
        for trans in inBlock.transactionlist:
            combination = combination + str(trans)
        return hashlib.sha256( combination.encode("utf-8")).hexdigest()

    # 判定区块的有效性
    def is_block_valid(self, newBlock):
        lastBlock = self.chain[-1]
        if  lastBlock.index + 1 != newBlock.index:
            return False
        if lastBlock.hash != newBlock.previoushash:
            return False
        if self.caculate_hash(newBlock) != newBlock.hash:
            return False
        return True
 