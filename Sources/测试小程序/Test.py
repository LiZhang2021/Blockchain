import random
import collections

list = ['1', '2', '3']
list = collections.deque(list)
print(list)
list.popleft()
print(list)