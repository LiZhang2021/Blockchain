class Block:
    def __init__(self, blockID, previous_hash, leaderID, current_transactions):
        self.ID = blockID
        self.previous_hash = previous_hash
        self.leaderID = leaderID
        self.Hash = None
        self.final_signature = None
        self.transactions = current_transactions