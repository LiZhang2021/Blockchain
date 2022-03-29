from Crypto.Signature import pkcs1_15
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA

# 对数据文件中的数据进行签名
with open("data.txt","r") as datafile:
    data = datafile.read()

# print(data)


""" Step 2：定义签名函数，能够使用指定的私钥对数据文件进行签名，并将签名结果输出到文件返回 """
def RSA_Signaturer(private_key,data):
    # 获取 数据消息 的HASH值，摘要算法MD5，验证时也必须用MD5
    """ # 也可以使用 SHA256 算法，验证时也必须用SHA256，
    返回类型为: <class 'Crypto.Hash.SHA256.SHA256Hash'>
    msg_hash = Crypto.Hash.SHA256.new()
    # 对 数据内容 进行 Hash
    msg_hash.update(data_content) """
    digest = MD5.new(data.encode('utf-8'))
    # 使创建 私钥 签名工具, 并用私钥对HASH值进行签名
    signature = pkcs1_15.new(private_key).sign(digest)
    # 将签名结果写入文件
    sig_results = open("sig_results.txt","wb")
    sig_results.write(signature)
    sig_results.close()
    return sig_results


""" step 3：定义签名验证函数，能够使用指定的公钥对 step 2中的签名文件进行验证，返回验证结果 """
def RSA_Verifier(public_key,data,signature):
    # 获取 数据消息 的HASH值，签名时采用摘要算法MD5，验证时也必须用MD5
    digest = MD5.new(data.encode('utf-8'))
    try:
        # 使用Crypto.Signature 中 公钥 验签工具 对 数据和签名 进行验签
        pkcs1_15.new(public_key).verify(digest, signature)
        print("验证成功！！！")
    except:
        print("签名无效！！！")

        
# step 4：利用 step 1中的文件对 step 2 和 step 3 中的函数进行测试。

# 打开私钥文件和数据文件，读取 私钥 和 数据 信息
with open('private_key.pem') as prifile,\
    open('data.txt') as datafile:
    private_key = RSA.import_key(prifile.read())
    data = datafile.read()

    # 利用 私钥 对 数据 进行签名
    RSA_Signaturer(private_key,data)

# 打开公钥文件、数据文件和签名结果文件，读取 公钥、数据和签名结果
with open('public_key.pem') as pubfile,\
    open('data.txt') as datafile,\
    open('sig_results.txt','rb') as sigfile:
    public_key = RSA.import_key(pubfile.read())
    data = datafile.read()
    signature = sigfile.read()

    # 验证 数据 和 签名 的正确性
    RSA_Verifier(public_key,data,signature)

