node = [1, 2, 3]
node1 = [4,5,6]
node2 = [7, 8, 9]
file = open('data.txt', 'a')
mid = str(node).replace('[', '').replace(']', '')
# 删除单引号并用字符空格代替逗号
mid = mid.replace("'", '').replace(',', '') + '\n'
file.write(mid)
file.close()

file = open('data.txt', 'a')
mid = str(node1).replace('[', '').replace(']', '')
# 删除单引号并用字符空格代替逗号
mid = mid.replace("'", '').replace(',', '') + '\n'
file.write(mid)
file.close()

file = open('data.txt', 'a')
mid = str(node2).replace('[', '').replace(']', '')
# 删除单引号并用字符空格代替逗号
mid = mid.replace("'", '').replace(',', '') + '\n'
file.write(mid)
file.close()
