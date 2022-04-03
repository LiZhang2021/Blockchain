
# 边的类
class Edge:
    def __init__(self):
        self.sendnode = None
        self.receivennode = None
        self.sendmsg = 0    # 记录信道发送状态
        self.receivemsg = 0 # 记录信道接收状态
        self.collisions = 0 # 记录信道冲突状态
    
    # 信道冲突
    def collision_occured(self, R):

    def Send_Message(self, send_vertex, receive_vertex, message):
        self.envertex = receive_vertex
        self.outvertex = send_vertex
        self.state = self.state + 1

    def Receive_Message(self, entry_vertex, outgoing_vertex, message):

        