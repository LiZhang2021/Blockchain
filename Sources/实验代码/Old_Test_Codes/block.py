class Block:
    def __init__(self, blockID, previous_hash, leaderID, current_transactions):
        self.blockID = blockID
        self.previous_hash = previous_hash
        self.leaderID = leaderID
        self.Hash = None
        self.final_signature = None
        self.transactions = current_transactions
    
    def print_block(self):
        print("区块ID", self.blockID)
        print("区块previous_hash", self.previous_hash)
        print("区块LeaderID", self.leaderID)
        print("区块Hash", self.Hash)
        print("区块final_signature", self.final_signature)
        if self.transactions == None:
            print("区块交易数量", 0)
        else:
            print("区块交易数量",len(self.transactions))