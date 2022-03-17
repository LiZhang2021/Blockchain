import datetime
import math
import random
import numpy
import time

import matplotlib.pyplot as plt
import numpy as np

# 可调参数
N =20 # 节点个数
seed = datetime.datetime.now() # 点产生的随机种子
p = 0.2 # 某一时间点发送信号的概率
radius = 10 # 广播半径

plt.ion() # 循环开始
plt.show()

# 构造节点，全部存入一个列表
x_all = np.random.rand(N)
y_all = np.random.rand(N)

list_node_broadcast = []
list_node_receipt = []
list_node_conflict = []

for _ in range(50):
    # 结果参数
    num_node_broadcast = 0 # 正在广播的节点的个数
    num_node_receipt = 0 # 有效接收的节点的个数
    num_node_conflict = 0 # 发生冲突的节点个数

    for each_index in range(len(x_all)):
        randonX = random.uniform(-0.1, 0.1)
        x_all[each_index] += randonX
        randonY = random.uniform(-0.1, 0.1)
        y_all[each_index] += randonY

    # 依概率构造广播节点和接收节点
    node_broadcast = [] # 广播节点
    node_receipt = [] # 接收节点
    for i in range(len(x_all)):
        random_pro = random.uniform(0, 1)
        if random_pro <= 0.2:
            node_broadcast.append([x_all[i], y_all[i]])
            num_node_broadcast += 1
        else:
            node_receipt.append([x_all[i], y_all[i]])
    list_node_broadcast.append(num_node_broadcast) # 记录一次循环的广播节点个数

    # 计算有效的接收节点
    effective_receipt_node = []
    conflict_receipt_node = []
    for each_receipt in node_receipt:
        flag = 0 # 该变量用来指示某个接收节点是否处于多个广播节点的广播范围之内，0表示0个，1表示1个...以此类推
        for each_broadcast in node_broadcast:
            if math.sqrt((each_receipt[0]-each_broadcast[0])**2 + (each_receipt[1]-each_broadcast[1])**2) < radius:
                flag += 1
        if flag > 1:
            num_node_conflict += 1
            conflict_receipt_node.append(each_receipt)
        if flag == 1:
            effective_receipt_node.append(each_receipt)
            num_node_receipt += 1
    list_node_receipt.append(num_node_receipt) # 记录一次循环的有效节点接收个数
    list_node_conflict.append(num_node_conflict) # 记录一次循环的冲突节点个数

    # 提取广播节点、接收节点、有效接收节点的坐标
    broadcast_x = [i[0] for i in node_broadcast]
    broadcast_y = [i[1] for i in node_broadcast]
    receipt_x = [i[0] for i in node_receipt]
    receipt_y = [i[1] for i in node_receipt]
    effective_receipt_x = [[i[0] for i in effective_receipt_node]]
    effective_receipt_y = [[i[1] for i in effective_receipt_node]]
    conflict_receipt_x = [[i[0] for i in conflict_receipt_node]]
    conflict_receipt_y = [[i[1] for i in conflict_receipt_node]]

    plt.cla()  # 清除当前绘图

    # 绘制散点图
    plt.scatter(broadcast_x, broadcast_y, s=1000, c='#ffffff', edgecolors='#000000', label='broadcast') # 绘制广播节点
    plt.scatter(receipt_x, receipt_y, s=10, c='#000000', edgecolors='#000000', label='receipt') # 绘制全部接收节点
    plt.scatter(effective_receipt_x, effective_receipt_y, s=10, c='#32b16c', edgecolors='#32b16c', label='effective receipt') # 绘制有效接收节点
    plt.scatter(conflict_receipt_x, conflict_receipt_y, s=10, c='#e60012', edgecolors='#e60012', label='conflict receipt') # 绘制冲突接收节点

    # 图中的文字说明
    plt.text(0.5, 0.05, 'number of all node: %d' % N, fontdict={'size': 10, 'color': 'red'})
    plt.text(0.5, 0, 'number of broadcast node: %d (%0.2f)' % (num_node_broadcast, num_node_broadcast/N), fontdict={'size':10, 'color':'red'})
    plt.text(0.5, -0.05, 'number of effective receipt node: %d (%0.2f)' % (num_node_receipt, num_node_receipt), fontdict={'size':10, 'color':'red'})
    plt.text(0.5, -0.1, 'number of conflict receipt node: %d (%0.2f)' % (num_node_conflict, num_node_conflict), fontdict={'size':10, 'color':'red'})

    plt.axis('off')
    plt.xlim(-0.1, 1.5)
    plt.ylim(-0.1, 1.5)
    plt.style.use('ggplot')
    plt.legend(loc='lower left')
    plt.pause(2)  # 保留绘图2s

plt.ioff() # 循环结束
plt.show()

print("有效发送" + str(numpy.mean(list_node_broadcast)))
print("有效接收" + str(numpy.mean(list_node_receipt)))
print("冲突" + str(numpy.mean(list_node_conflict)))
print("Sy" + str(numpy.mean(list_node_conflict)/numpy.mean(list_node_broadcast)))

x_axis = [str(i)+"t" for i in range(50)]

fig = plt.figure(figsize=(12,4))
plt.axis('on')
plt.subplot(facecolor='w')
plt.plot(x_axis, list_node_broadcast, color='black', linewidth=1.0, linestyle='-', label='广播节点')
plt.plot(x_axis, list_node_receipt, color='green', linewidth=1.0, linestyle='-', label='接收节点')
plt.plot(x_axis, list_node_conflict, color='red', linewidth=1.0, linestyle='-', label='冲突节点')

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.xticks(rotation=-60)
plt.legend(loc='upper left')
plt.grid(axis="both")
# plt.show()
