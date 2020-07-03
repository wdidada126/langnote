- 《HTTPS权威指南》
- 《openssl攻略》

crt格式的证书详解：
版本
有V1，V2，V3
公钥
RSA 一大串字符
指纹
一串字符

CipherSuite.TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256

加密套件，签名方式 公钥加密方式 对称加密方式 摘要方式
RSA可以用于加密解密，也可以用于数字签名
RSA非对称加密
ECDHE 数字签名 椭圆曲线 DH

tls协议格式
头部
内容类型（Client Hello，Server Hello, Certificate）
版本
长度
消息体



 - 使用非对称加密协商加密算法
 - 使用对称加密方式传输数据
 - 使用第三方机构签发的证书，来加密公钥，用于公钥的安全传输、防止被中间人串改。


