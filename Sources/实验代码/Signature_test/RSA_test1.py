
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


""" 1. 生成秘钥对, 创建 公钥/私钥 对象 """

# 生成一对长度为 2048 位的 RSA 秘钥对
key = RSA.generate(2048)

# 从秘钥对中获取 公钥 对象, 返回类型为: <class 'Crypto.PublicKey.RSA.RsaKey'>
public_key = key.publickey()

# 秘钥对本身就是 私钥 对象, 类型为:    <class 'Crypto.PublicKey.RSA.RsaKey'>
private_key = key


""" 2. 创建密码器, 加密/解密 """

# 创建 公钥 密码器, 返回类型为: <class 'Crypto.Cipher.PKCS1_v1_5.PKCS115_Cipher'>
pub_cipher = PKCS1_v1_5.new(public_key)
# 加密内容(bytes), 返回加密后的密文（bytes类型）
ciphertext = pub_cipher.encrypt("Hello World".encode())


# 创建 私钥 密码器, 返回类型为: <class 'Crypto.Cipher.PKCS1_v1_5.PKCS115_Cipher'>
pri_cipher = PKCS1_v1_5.new(private_key)
# 解密密文(bytes), 返回解密后的明文（bytes类型）
plaintext = pri_cipher.decrypt(ciphertext, sentinel=None)


""" 3. 查看结果 """

# 输出解密后的明文, 结果为: "Hello World"
print(plaintext.decode())
