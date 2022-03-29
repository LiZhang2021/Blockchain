import Crypto.PublicKey.RSA
import Crypto.Signature.PKCS1_v1_5
import Crypto.Hash.SHA256


""" 1. 生成秘钥对, 创建 公钥/私钥 对象 """

# 生成一对长度为 2048 位的 RSA 秘钥对
key = Crypto.PublicKey.RSA.generate(2048)

# 从秘钥对中获取 公钥 对象, 返回类型为: <class 'Crypto.PublicKey.RSA.RsaKey'>
public_key = key.publickey()

# 秘钥对本身就是 私钥 对象, 类型为:    <class 'Crypto.PublicKey.RSA.RsaKey'>
private_key = key


""" 2. 数据内容 """

# 要签名的数据内容（bytes类型）
data_content = "Hello World".encode()


""" 3. 创建 私钥 签名工具: 签名 """

# 创建 私钥 签名工具, 返回类型为: <class 'Crypto.Signature.pkcs1_15.PKCS115_SigScheme'>
pri_signer = Crypto.Signature.PKCS1_v1_5.new(private_key)

# 创建 Hash 对象（使用 SHA256 算法）, 返回类型为: <class 'Crypto.Hash.SHA256.SHA256Hash'>
msg_hash = Crypto.Hash.SHA256.new()
# 对 数据内容 进行 Hash
msg_hash.update(data_content)

# 使用 私钥 签名工具 对 数据 进行签名, 返回签名结果（bytes类型）
signature_result = pri_signer.sign(msg_hash)


""" 4. 创建 公钥 验签工具: 验签 """

# 创建 公钥 验签工具, 返回类型为: <class 'Crypto.Signature.pkcs1_15.PKCS115_SigScheme'>
pub_signer = Crypto.Signature.PKCS1_v1_5.new(public_key)

# 创建 Hash 对象（使用 SHA256 算法）, 返回类型为: <class 'Crypto.Hash.SHA256.SHA256Hash'>
msg_hash = Crypto.Hash.SHA256.new()
# 对 数据内容 进行 Hash
msg_hash.update(data_content)

# 使用公钥 验签工具 对 数据和签名 进行验签, 返回 True/False
verify = pub_signer.verify(msg_hash, signature_result)

# 校验结果为 True 表示通过验签
print(verify)


# 验签: 
#    验证「数据」、「签名」、「公钥」 三个可公开的数据是否匹配。
#    如果匹配，说明该「签名」是该「公钥」对应的「私钥」对该「数据」进行的正确签名；
#    如果不匹配，说明可能该「数据」被篡改。
#    如此可以用来验证公开发布的「数据」是否是官方（即「私钥」）发布的。
