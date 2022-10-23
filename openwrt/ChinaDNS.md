# ChinaDNS

https://github.com/shadowsocks/ChinaDNS


src/chinadns -m -c chnroute.txt


ChinaDNS-ng


https://www.itgeeker.net/openwrt-chinadns-configration-by-itgeeker-net/

Dnsmaq 接收来自局域网的 DNS 请求后直接转发给 ChinaDNS 处理；ChinaDNS通过上级服务器（Upstream Servers）进行DNS查询。


wget -O /tmp/delegated-apnic-latest 'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest' && awk -F\| '/CN\|ipv4/ { printf("%s/%d\n", $4, 32-log($5)/log(2)) }' /tmp/delegated-apnic-latest > /etc/chinadns_chnroute.txt

CHNRoute File


ChinaDNS 组件来解决。

另外，也可以采用重构优化的 ChinaDNS-NG 来替代。二者主要区别：

ChinaDNS 安装简单、使用稳定可靠，但最近一次更新是 2015 年；
ChinaDNS-NG 是新近的项目，需要自行编译，稳定性还需要验证；
ChinaDNS 无法显式定义可信 DNS 和 国内 DNS，而是根据 IP 地址自动判断；
ChinaDNS 也无法显式定义具体域名的解析行为，譬如指定域名使用可信 DNS（或国内 DNS）解析。