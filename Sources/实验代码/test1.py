import math

k = [1, 2, '5', 7]

t = '5'
for i in range(0, len(k)):
    if t == k[i]:
        print(i)
        break

k.pop(i)
print(k)
# 初始化guests列表
guests=['Zhang san','Li si','Wang wu','Zhao liu']
# 将列表中的`Zhang san`删除
del guests[0]
# 输出新的guests列表
print(guests)

