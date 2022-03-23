# VRF Algorithm

这个算法涉及七个函数：$RSA_FDH_VRF()$
* $(proof) = RSA_VRF_prove(private_key, seed)$
  * private_key：
* $(T) = MGF1(mgfseed, maskLen)$：基于散列函数的掩码生成函数
  * mgfseed：掩码生成操作的目标字符串
  * maskLen：生成掩码长度，最多 $2^{32}$
  * 输出：maskLen长度的掩码
* $i2osp(x)$：非负整数转化成字符串
* $os2ip(x)$：字符串转化成非负整数
* $RSASP1()$：RSA签名算法
* $RSAVP1()$：RSA验证签名算法

证明生成过程：$pi = RSAFDHVRF_prove(private_key, seed(alpha))$，其中 $pi$ 是长度为 $k$ 的证明字符串。主要执行过程：
* one_string = i2osp(1，1)
* em = MGF1()
* m = os2ip1(em)
* s = RSASP1(K, m)
* pi_string = i2OSP(s, k)

证明验证过程：RSA_FDH_VRFVerify()
参数：
* public_key：公钥
* seed

