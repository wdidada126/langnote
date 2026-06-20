# wireshark


tshark抓包
tcpdump抓包及tshark解包方法介绍

tshark是wireshark的命令行工具，通过shell命令抓取、解析报文。tcpdump是Linux系统下的抓包工具。wireshark和tcpdump都共同使用 libpcap作为其底层抓包的库，tshark也可以抓取报文。

备注郑芳老师在上计算机网络课程的时候说了，这一点

## 实现原理
pcap

https://www.winpcap.org/install/

https://www.tcpdump.org/manpages/pcap.3pcap.html

Wireshark和pcap（Packet Capture）之间存在密切的关系。简单来说，pcap是一种用于捕获网络数据包的技术，而Wireshark则是一个广泛使用的网络封包分析软件，它使用pcap技术来捕获和分析网络数据包。

以下是关于Wireshark和pcap的详细解释：

pcap（Packet Capture）：
pcap是一种捕获代理网络数据包的技术，它基于操作系统内核层的实现来进行数据包的捕获。
pcap技术可以捕获数据包并进行多种操作，如过滤、深度分析等，从而帮助管理员、开发人员进行网络故障诊断与分析。
pcap通常用于抓取广域网（WAN）或局域网（LAN）上的数据包，并且支持多种操作系统和编程语言。
Wireshark（前称Ethereal）：
Wireshark是一个开源的网络封包分析软件，它使用pcap技术来捕获和分析网络数据包。
Wireshark可以截取网络封包，并尽可能显示出最为详细的网络封包资料，包括源地址、目的地址、协议类型、数据内容等。
Wireshark适用于各种网络环境，如以太网、WiFi、蓝牙等，并支持多种网络协议，如TCP、UDP、HTTP、FTP等。
Wireshark的使用者包括网络管理员、网络安全工程师、开发者等，他们可以使用Wireshark来检测网络问题、检查信息安全问题、为新的通讯协定除错等。
在Wireshark中，pcap文件（通常以.pcap、.cap或.dmp为扩展名）是用来存储捕获到的网络数据包的。这些文件可以在Wireshark中打开并进行分析，从而帮助用户了解网络行为、诊断网络问题等。同时，Wireshark也支持使用捕获过滤器来只捕获符合特定条件的网络数据包，以便更精确地分析网络流量。

总之，pcap是一种捕获网络数据包的技术，而Wireshark则是一个使用pcap技术来捕获和分析网络数据包的软件工具。它们在网络故障诊断、网络安全分析等领域发挥着重要作用。

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

