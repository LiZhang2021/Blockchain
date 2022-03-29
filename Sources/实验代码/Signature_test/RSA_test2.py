from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


""" 1. 读取 秘钥对, 创建 公钥/私钥 对象 """

# 从 PEM 格式的 公钥 文件中读取数据
with open("public_key.pem", "rb") as pubfile:
    pub_bytes = pubfile.read()
# 导入读取到的公钥数据, 生成公钥对象, 返回类型为: <class 'Crypto.PublicKey.RSA.RsaKey'>
public_key = RSA.import_key(pub_bytes)


# 从 PEM 格式的 私钥 文件中读取数据
with open("private_key.pem", "rb") as prifile:
    pri_bytes = prifile.read()
# 导入读取到的私钥数据, 生成 私钥对象, 返回类型为: <class 'Crypto.PublicKey.RSA.RsaKey'>
private_key = RSA.import_key(pri_bytes)


# 私钥中包含了公钥, 公钥也可以从私钥中获取（PS: 公钥中不包含私钥）
# public_key = private_key.publickey()


""" 2. 创建密码器, 加密/解密 """

# 创建 公钥 密码器, 返回类型为: <class 'Crypto.Cipher.PKCS1_v1_5.PKCS115_Cipher'>
pub_cipher = PKCS1_v1_5.new(public_key)
# 加密内容(bytes), 返回加密后的密文（bytes类型）
ciphertext = pub_cipher.encrypt("Hello World".encode())

# print("ciphertext", ciphertext)

# 创建 私钥 密码器, 返回类型为: <class 'Crypto.Cipher.PKCS1_v1_5.PKCS115_Cipher'>
pri_cipher = PKCS1_v1_5.new(private_key)
# 解密密文(bytes), 返回解密后的明文（bytes类型）
plaintext = pri_cipher.decrypt(ciphertext, sentinel=None)


""" 3. 查看结果 """

# 输出解密后的明文, 结果为: "Hello World"
# print(plaintext)    # 输出结果为 b'Hello World'
print(plaintext.decode())
