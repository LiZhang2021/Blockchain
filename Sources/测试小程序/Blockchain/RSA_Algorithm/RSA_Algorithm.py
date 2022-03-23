# 利用pycrypto实现RSA算法生成公私钥对,
# 实现加密解密、签名解签等功能

from Crypto import Random
from Crypto.PublicKey import RSA
 from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Sig_pk
import base64
from Crypto.Hash import SHA


# 加密解密：公钥加密，私钥解密
# 签名验签：私钥签名，公钥解签

# 生成公私钥对
def generate_keys():
    # 利用伪随机数来生成私钥和公钥
    random_generator = Random.new().read
    rsa_obj = RSA.generate(1024, random_generator) # 生成长度为1024的私钥
    private_pem = rsa_obj.exportKey() #pem格式输出私钥
    public_key = rsa_obj.publickey()
    public_pem = public_key.exportKey() #pem格式输出公钥
    print(private_pem, public_pem)
    return private_pem, public_pem

# 利用公钥对消息加密
def rsa_encrypt(public_key, message):
    message_bype = message.encode(encoding="utf-8") # 消息编码
    cipher = Cipher_pkcs1_v1_5.new(public_key)  # 创建用于执行PKCS#1 v1.5加密或解密的密码
    dd=cipher.encrypt(message_bype) # 对需要加密的消息进行PKCS#1 v1.5加密
    cipher_text = base64.b64encode(dd)  # 使用Base64对类似字节的对象进行编码
    return cipher_text
 
# 利用私钥解密
def rsa_decrypt(private_key, encrypt_text):
    cipher = Cipher_pkcs1_v1_5.new(private_key) # 创建用于执行PKCS#1 v1.5加密或解密的密码
    plain_text = cipher.decrypt(base64.b64decode(encrypt_text), '') # 对需要加密的消息进行PKCS#1 v1.5加密，再使用Base64对类似字节的对象进行解码。
    return plain_text
 
# 利用私钥签名
def rsa_sign(private_key, msg):
    # 根据sha算法处理签名内容
    sign_data = SHA.new(msg.encode())
    # 私钥进行签名
    sig_pk = Sig_pk.new(private_key)
    sign_m = sig_pk.sign(sign_data)
    # 将签名后的内容，转换为base64编码
    result = base64.b64encode(sign_m)
    # 签名结果转换成字符串
    data = result.decode()
    return data

# 利用公钥解签
def rsa_signoff(public_key, sign_data, msg):
    # base64解码
    sign_data = base64.b64decode(sign_data)
    # 将签名之前的内容进行hash处理
    sha_msg = SHA.new(msg.encode())
    # 验证签名
    signer = Sig_pk.new(public_key)
    result = signer.verify(sha_msg, sign_data)
    return result

# 测试加密解密
def test_keys(request):
    # 生成密钥
    rsa_obj = RSA.generate(1024)
    private_pem = rsa_obj.exportKey()  # pem格式输出私钥
    public_key = rsa_obj.publickey()
    public_pem = public_key.exportKey()  # 将公钥输出成pem格式
    print("公钥",public_pem)
    msg = 'hello world' 
    encrypt_text = rsa_encrypt(public_key,msg)  #公钥加密
    print("公钥加密",encrypt_text)
    text = rsa_decrypt(rsa_obj, encrypt_text)  #私钥解密
    print("私钥解密",text)
 
    msg="大家好，我们是超级市场"
    encrypt_text = rsa_encrypt(public_key, msg)  # 公钥加密
    print("公钥加密0", encrypt_text)
    text = rsa_decrypt(rsa_obj, encrypt_text)  # 私钥解密
    print("私钥解密0", text.decode('utf-8'))

# 测试签名解签
def test_sign():
    # 生成密钥
    rsa_obj = RSA.generate(1024)
    private_pem = rsa_obj.exportKey()  # pem格式输出私钥
    public_key = rsa_obj.publickey()
    public_pem = public_key.exportKey()  # 将公钥输出成pem格式
    print("公钥",public_pem)
    msg = 'hello world'
    print(msg)
    # 私钥签名
    private_key = RSA.importKey(private_pem)
    sign_data = rsa_sign(private_key, msg)
    print("签名", sign_data)
    # 公钥解签
    public_key = RSA.importKey(public_pem)
    result = rsa_signoff(public_key, sign_data, msg)
    print("解签", result)
