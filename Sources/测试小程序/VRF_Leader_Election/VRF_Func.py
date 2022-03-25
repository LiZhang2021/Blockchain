import math
import struct
import hashlib
import binascii

from Crypto.PublicKey import RSA


# SK：VRF私钥
# PK：VRF公钥
# Alpha: VRF输入，将对其进行哈希
# Beta: VRF哈希输出
# Pi: VRF证明
# Prover: 持有VRF公私钥的人就可以成为证明人
# Verifier: 只持有VRF公钥的人就可以成为验证人

# VRF基本算法：
# step 1:有一个密钥对生成算法生成VRF所需的公私钥对；
# step 2:证明人计算值 Beta = VRF_Hash(SK, Alpha)；
# step 3:证明人还需要用私钥及输入计算一个证明 Pi = VRF_prove(SK, Alpha)；
# step 4:验证人通过对应的公钥可以验证结果的正确性 VRF_verify(PK, Alpha, Pi)
# step 2和 step 3可以合并为 (Beta,Pi) = VRF(SK,Alpha)

# RSA签名算法
def RSA_sign(SK, m):
    # 如果消息长度不在范围之内则报错
    if not (0 <= m <= SK['n']-1):
        raise Exception("message representative out of range")
    # 返回由私钥的签名
    sign = pow(m, SK['d'], SK['n']) # m^(SK['d'])%SK['n]
    return sign

# RSA解签算法
def RSA_verify(PK, sign):
    if not (0 <= sign <= PK['n']-1):
        raise Exception("message representative out of range")
    verify_sign = pow(sign, PK['e'], PK['n']) 
    return  verify_sign

# 非负整数转化成字符串
def Int_to_OString(x):
    try:
        return struct.pack('I',x)
    except:
        Ostring =  binascii.unhexlify( len(hex(x)[2:])%2*'0' + hex(x)[2:])
        return Ostring

# 字符串转化成非负整数
def OString_to_Int(x):
    Toint = int(binascii.hexlify(x), 16)
    return Toint

# 基于散列函数的掩码生成函数
# gmseed：掩码生成操作的目标字符串
# maskLen：生成掩码长度，最多 2^{32}
# 输出：maskLen长度的掩码
def Generate_Mask(gm_seed, mask_len, Hash=hashlib.sha1):
    T = b''
    for i in range(math.ceil(mask_len/Hash().digest_size)):
        C = Int_to_OString(i)
        T = T + Hash(gm_seed.encode() + C).digest()
    return T[:mask_len]

# 生成哈希值和证明
# SK:私钥
# Alpha: VRF哈希输入
def VRF(SK, Alpha, Hash=hashlib.sha1):
    k = hashlib.sha1().digest_size
    encode_msg = Generate_Mask(Alpha, k-1) # 生成输入哈希的掩码
    m = OString_to_Int(encode_msg) 
    sign = RSA_sign(SK, m)  # 用私钥签名
    Pi = Int_to_OString(sign)  # 生成证明
    Beta = Hash(Pi).digest()    # 生成证明的哈希
    return Beta, Pi

# VRF证明验证函数
def VRF_verify(PK, Alpha, Pi):
    k = hashlib.sha1().digest_size
    sign = OString_to_Int(Pi)   
    m = RSA_verify(PK, sign)    # 用公钥解签
    encode_msg1 = Int_to_OString(m)
    encode_msg = Generate_Mask(Alpha, k-1) # 生成输入哈希的掩码
    if encode_msg1 == encode_msg:
        return True
    else:
        return False

alpha1 = 'hellow'
alpha2 = "hello"
rsa = RSA.generate(1024) # RSA(n, e, d)
K = {'e':rsa.e, 'n':rsa.n, 'd':rsa.d}# 公钥(n, e)，私钥(nd)
Beta, Pi = VRF(K, alpha1)
result = VRF_verify(K, alpha2, Pi)
print(result)