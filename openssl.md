# openssl

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

https://www.jianshu.com/p/fad5276a70e0


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
