# proxy windows

Windows命令行代理

假设你已经使用了SS客户端，本地socks5代理为127.0.0.1:1080

在CMD窗口输入如下指令设置代理：

set http_proxy=socks5://127.0.0.1:1080

set https_proxy=socks5://127.0.0.1:1080

set ftp_proxy=socks5://127.0.0.1:1080

172.18.176.1

ubuntu用export
export http_proxy=socks5://127.0.0.1:20800
export https_proxy=socks5://127.0.0.1:20800

export http_proxy=http://172.18.176.1:20800
export https_proxy=https://172.18.176.1:20800

core.net.http:proxies={"http" : "PROTOCOL://IP:PORT/", "https" : "PROTOCOL://IP:PORT/"}

https://requests.readthedocs.io/en/latest/user/advanced/#proxies

export http_proxy=socks5://172.18.176.1:7890
export https_proxy=socks5://172.18.176.1:7890

