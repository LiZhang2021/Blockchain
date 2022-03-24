# VRF Algorithm

**证明人**: 持有VRF公私钥的人就可以成为证明人
**验证者**: 只持有VRF公钥的人就可以成为验证人

# 基本符号
* SK：VRF私钥
* PK：VRF公钥
* Alpha: VRF输入，将对其进行哈希
* Beta: VRF哈希输出
* Pi: VRF证明

VRF基本算法：
* step 1: 有一个密钥对生成算法生成VRF所需的公私钥对；
* step 2: 证明人计算值 Beta = VRF_Hash(SK, Alpha)；
* step 3: 证明人还需要用私钥及输入计算一个证明 Pi = VRF_prove(SK, Alpha)；
* step 4: 验证人通过对应的公钥可以验证结果的正确性 VRF_verify(PK, Alpha, Pi)

step 2和 step 3可以合并为 (Beta,Pi) = VRF(SK,Alpha)