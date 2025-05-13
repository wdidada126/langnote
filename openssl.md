# openssl
https://www.openssl.org/

OpenSSL 是一个开源的工具包，用于实现安全套接字层（SSL）和传输层安全（TLS）协议，同时提供通用的加密库。它广泛应用于各种应用程序中，以确保数据传输的安全性和完整性。以下是 OpenSSL 库的主要功能：
1. SSL/TLS 支持
OpenSSL 提供了完整的 SSL/TLS 协议实现，支持客户端和服务器之间的安全通信。主要功能包括：
证书管理：生成、验证和管理 SSL/TLS 证书。
密钥交换：支持多种密钥交换算法，如 RSA、Diffie-Hellman 等。
加密和解密：使用对称和非对称加密算法保护数据传输。
身份验证：验证通信双方的身份，确保数据的完整性和机密性。
2. 加密算法
OpenSSL 提供了广泛的加密算法，包括：
对称加密：如 AES、DES、Blowfish 等。
非对称加密：如 RSA、DSA、ECDSA 等。
哈希函数：如 MD5、SHA-1、SHA-256 等。
消息认证码：如 HMAC、CMAC 等。
3. 证书和密钥管理
OpenSSL 提供了强大的工具和库函数，用于生成、管理和验证证书和密钥：
生成密钥：生成 RSA、DSA、ECDSA 等密钥对。
生成证书签名请求（CSR）：生成证书签名请求，用于向证书颁发机构（CA）申请证书。
自签名证书：生成自签名证书，适用于测试和内部使用。
证书验证：验证证书的有效性，包括证书链验证、吊销列表检查等。
证书吊销列表（CRL）：管理和验证证书吊销列表。
4. 密码学工具
OpenSSL 提供了一系列密码学工具，用于各种安全操作：
数据加密和解密：使用对称和非对称加密算法对数据进行加密和解密。
数字签名：生成和验证数字签名，确保数据的完整性和身份认证。
随机数生成：生成高质量的随机数，用于密钥生成和其他安全操作。
密钥派生：从密码或密钥材料派生出加密密钥。
5. 命令行工具
OpenSSL 提供了一个功能强大的命令行工具，用于执行各种安全操作：
证书生成和管理：生成证书、密钥、CSR 等。
数据加密和解密：对文件进行加密和解密。
证书验证：验证证书的有效性。
密钥转换：将密钥从一种格式转换为另一种格式。
哈希计算：计算文件的哈希值。
6. 库函数
OpenSSL 提供了丰富的库函数，供应用程序开发者使用：
SSL/TLS 库：提供 SSL/TLS 协议的实现，支持客户端和服务器端的通信。
加密库：提供各种加密算法的实现，包括对称加密、非对称加密、哈希函数等。
X.509 证书库：提供证书和密钥的管理功能，包括证书生成、验证、吊销等。
随机数生成器：提供高质量的随机数生成功能。
7. 支持多种平台
OpenSSL 支持多种操作系统和平台，包括：
Linux
Windows
macOS
Unix
8. 应用示例
以下是一些使用 OpenSSL 的常见应用示例：
生成密钥和证书
sh复制
# 生成 RSA 密钥
openssl genpkey -algorithm RSA -out private.key -pkeyopt rsa_keygen_bits:2048

# 生成证书签名请求 (CSR)
openssl req -new -key private.key -out csr.csr

# 生成自签名证书
openssl req -x509 -days 365 -key private.key -in csr.csr -out certificate.crt
数据加密和解密
sh复制
# 使用 AES 加密文件
openssl enc -aes-256-cbc -in plaintext.txt -out encrypted.bin -k secret

# 使用 AES 解密文件
openssl enc -aes-256-cbc -d -in encrypted.bin -out decrypted.txt -k secret
证书验证
sh复制
# 验证证书
openssl verify -CAfile ca.crt certificate.crt
生成哈希值
sh复制
# 计算文件的 SHA-256 哈希值
openssl dgst -sha256 plaintext.txt
总结
OpenSSL 是一个功能强大的工具包，广泛应用于各种应用程序中，以确保数据传输的安全性和完整性。它提供了 SSL/TLS 支持、多种加密算法、证书和密钥管理、密码学工具、命令行工具和库函数，支持多种平台，是开发安全应用程序的必备工具。

使用 openssl 验证 SHA512 校验值：

openssl dgst -r -sha512 xxx.tar.xz

D:\git\github\vcpkg\buildtrees\openssl\x64-windows-dbg\apps\openssl.exe

## 版本

conan search openssl
conancenter
  openssl
    openssl/1.0.2s
    openssl/1.0.2t
    openssl/1.0.2u
    openssl/1.1.0k
    openssl/1.1.0l
    openssl/1.1.1c
    openssl/1.1.1d
    openssl/1.1.1e
    openssl/1.1.1f
    openssl/1.1.1g
    openssl/1.1.1h
    openssl/1.1.1i
    openssl/1.1.1j
    openssl/1.1.1k
    openssl/1.1.1l
    openssl/1.1.1m
    openssl/1.1.1n
    openssl/1.1.1o
    openssl/1.1.1p
    openssl/1.1.1q
    openssl/1.1.1s
    openssl/1.1.1t
    openssl/1.1.1u
    openssl/1.1.1v
    openssl/1.1.1w
    openssl/3.0.0
    openssl/3.0.1
    openssl/3.0.2
    openssl/3.0.3
    openssl/3.0.4
    openssl/3.0.5
    openssl/3.0.7
    openssl/3.0.8
    openssl/3.0.9
    openssl/3.0.10
    openssl/3.0.11
    openssl/3.0.12
    openssl/3.1.0
    openssl/3.1.1
    openssl/3.1.2
    openssl/3.1.3
    openssl/3.1.4
    openssl/3.2.0
    openssl/3.3.0

https://www.jianshu.com/p/fad5276a70e0

## repo
https://github.com/openssl/openssl


## 编译

centos 7.6，升级过程中估计会有如下报错，


Can’t locate IPC/Cmd.pm in @INC 
……
Can't locate Data/Dumper.pm in @INC 
……
Can't locate Test/More.pm in @INC 
……




安装必备包：
yum install perl-IPC-Cmd perl-Data-Dumper perl-Test-Taint

## 源代码仓库

要在Ubuntu 20上编译OpenSSL 1.1.1o版本，请按照以下步骤操作：

1. 首先，确保已经安装了必要的依赖项。在终端中运行以下命令：

```bash
sudo apt-get update
sudo apt-get install -y build-essential libssl-dev zlib1g-dev libreadline-dev libyaml-dev libsqlite3-dev llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
```

2. 接下来，从GitHub上克隆OpenSSL源代码仓库：

```bash
git clone https://github.com/openssl/openssl.git
cd openssl
```

3. 检出所需的版本（例如，1.1.1o）：

```bash
git checkout OpenSSL_1_1_1o
```

4. 配置并编译OpenSSL：

```bash
./config --prefix=/usr/local/openssl --openssldir=/usr/local/openssl shared zlib enable-camellia enable-idea enable-seed enable-sm2 enable-sm4 enable-tls13 enable-weak-ssl-ciphers no-comp no-dso no-hw no-mdc2 no-rc5 no-rfc3779 no-sctp no-ssl-trace no-zlib no-tests
make
```

5. 安装编译好的OpenSSL：

```bash
sudo make install
```

6. 更新系统库路径：

```bash
sudo ldconfig
```

现在，您已经在Ubuntu 20上成功编译了OpenSSL 1.1.1o版本。

### mac
git clone https://gitee.com/cbsync/openssl.git

git clone https://github.com/openssl/openssl.git
cd openssl
git submodule update --init --recursive
./Configure
make
make test
sudo make install

### 编译产物

lcrypto_a
libcrypto.a ?

## doc

https://docs.openssl.org/3.0/man7/migration_guide/

https://docs.openssl.org/master/man7/ossl-guide-libcrypto-introduction
