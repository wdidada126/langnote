# wget

wget --no-check-certificate https://dlcdn.apache.org/geode/1.14.4/apache-geode-1.14.4.tgz



该错误表明wget无法信任dlcdn.apache.org的SSL证书。

可以用以下方法解决:

1. 使用--no-check-certificate参数忽略证书检查:

```bash
wget --no-check-certificate <url> 
```

2. 手动安装dlcdn.apache.org的SSL证书,让wget能正确验证:

```bash 
wget <url> 
# 下载dlcdn.apache.org的证书
openssl s_client -showcerts -connect dlcdn.apache.org:443 </dev/null 2>/dev/null|openssl x509 -outform PEM > cert.pem

# 通过 --ca-certificate 指定证书路径
wget --ca-certificate=cert.pem <url>
```

3. 使用CA根证书,让wget信任dlcdn.apache.org的证书:

```bash
wget --ca-certificate=/etc/ssl/certs/ca-certificates.crt <url>
```

或者更新wget的CA证书列表:

```bash
wget http://curl.haxx.se/ca/cacert.pem -O /etc/ssl/certs/ca-certificates.crt
```

然后再使用`--ca-certificate`参数。

以上方法都可以解决wget无法信任证书的问题。建议选择第一种或第三种,第二种方法最繁琐。



wget -O



Wget url -O大写



下载到一半，停止





curl -o xxxfilename url

--no-check-certificate
https不检测tls证书

## 源代码 source code

https://www.gnu.org/software/wget/

https://www.gnu.org/software/wget/manual/

https://mirrors.ustc.edu.cn/gnu/wget/


### 编译脚本

wget https://mirrors.ustc.edu.cn/gnu/wget/wget2-2.1.0.tar.gz -O wget2-2.1.0.tar.gz
tar -zxvf wget2-2.1.0.tar.gz
ls
cd wget2-2*
cd +x configure
./configure
make -j4
sudo make install


报错：
ssl_openssl.c:1625:26: error: 'X509_CHECK_FLAG_NEVER_CHECK_SUBJECT' undeclared (first use in this function); did you mean 'X509_CHECK_FLAG_ALWAYS_CHECK_SUBJECT'?
   SSL_set_hostflags(ssl, X509_CHECK_FLAG_NEVER_CHECK_SUBJECT);

初步判断原因：wget对