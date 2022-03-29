# RSA加密、解密、签名和验证签名

## RSA_test

RSA_test1.py 生成密钥对进行加密解密测试；
RSA_test2.py 从文件中读取密钥对进行加密解密测试
RSA_sigtest.py 生成密钥对进行数据签名和验证签名

## Signature_test

利用python的标准库实现数字签名生成和验证过程：
* File_prepare.py: step 1  准备私钥文件private_key.pem、公钥文件public_key.pem和数据文件data.txt；
* sig_results.txt step 2: 定义签名函数（能够使用指定的私钥对数据文件进行签 名，并将签名结果输出到文件返回）；
* step 3: 定义签名验证函数（能够使用指定的公钥对 step 2 中的签名文件进行验证，返回验证结果）；
* Signature.pystep 4: 利用 step 1 中的文件对 step 2和step 3中的函数进行测试。