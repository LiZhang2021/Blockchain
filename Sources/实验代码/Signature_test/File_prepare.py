from Crypto.PublicKey import RSA

'''step 1：准备私钥文件、公钥文件和据文件'''

# 生成一对长度为 2048位的 RSA 秘钥对, 使用默认的随机数生成函数
# 也可以指定一个随机数生成函数: randfunc=Crypto.Random.new().read
key = RSA.generate(2048)

# print(key)          # Private RSA key at 0x1AB1D68FDC0
# print(type(key))    # <class 'Crypto.PublicKey.RSA.RsaKey'>


# 导出私钥, "PEM" 表示使用文本编码输出, 返回的是 bytes 类型, 格式如下:
# b'-----BEGIN RSA PRIVATE KEY-----\n{Base64Text}\n-----END RSA PRIVATE KEY-----'
# 输出格式可选: "PEM", "DER", "OpenSSH"
private_key = key.export_key("PEM")

# 导出公钥, "PEM" 表示使用文本编码输出, 返回的是 bytes 类型, 格式如下:
# b'-----BEGIN PUBLIC KEY-----\n{Base64Text}\n-----END PUBLIC KEY-----'
public_key = key.publickey().export_key("PEM")
# 转换为文本打印输出公钥和私钥，格式: Base64Text
# print(private_key.decode())
# print(public_key.decode())

## 把数据、公钥和私钥保存到文件
data = "I love you"
with open("private_key.pem", "wb") as prifile,\
    open("public_key.pem", "wb") as pubfile,\
    open("data.txt","a") as datafile:
    prifile.write(private_key)
    pubfile.write(public_key)
    datafile.write(data)

