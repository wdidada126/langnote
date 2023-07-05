# wireshark


https://www.cnblogs.com/softidea/p/10446388.html

SSLKEYLOGFILE

filtter

ip.dst==60.205.225.118

ip.dst==60.205.225.118
ip.dst==47.94.136.171
ip.dst==67.209.189.193

192.168.1.228

route add 192.168.1.228 mask 255.255.255.255 192.168.0.254
route delete 192.168.1.228 mask 255.255.255.255 192.168.0.254


ip.addr == 172.19.6.206

ip.dst == 172.19.6.206

ip.src == 172.19.6.206



wireshark https解密
步骤:
1. 获取网站的 SSL 证书:
- 从浏览器导入证书。在 Chrome 浏览器中,访问该网站,然后点击锁图标 -> 证书 -> 详情。将证书导出为 PFX 或者 CER 格式,再导入到 Wireshark。
- 使用 OpenSSL 从网站抓取证书。运行以下命令获取证书:
```
openssl s_client -connect example.com:443
```
它会显示证书信息,复制整个证书部分保存成PEM文件,文件名例如:example.com.pem
2. 在 Wireshark 中导入证书。打开 Wireshark 的 Preferences > Protocols > SSL > RSA Keys List > Add,选择刚才保存的 PEM 证书文件。
3. 过滤 HTTPS 数据包。在 Wireshark 过滤器中输入 tcp.port == 443 只抓取 443 端口的 HTTPS 数据包。
4. 解密数据包。右键选择要解密的HTTPS数据包 > Decryption > Decrypt SSL Session。
5. 选择刚才导入的证书进行解密。如果提示"No RSA Keys found for decryption",说明还没有导入证书。 
6. 解密成功后,HTTPS 数据包内容将显示为明文,可以查看里面的 HTTP 请求和响应。
7. 如果网站证书更新了,需要再次获取新的证书,重复上述步骤进行解密。
希望这个过程可以帮助你使用 Wireshark 解密 HTTPS 数据包!

