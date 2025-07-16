# proxy windows

Windows命令行代理

假设你已经使用了SS客户端，本地socks5代理为127.0.0.1:1080

在CMD窗口输入如下指令设置代理：

set http_proxy=socks5://127.0.0.1:1080

set https_proxy=socks5://127.0.0.1:1080

set ftp_proxy=socks5://127.0.0.1:1080

在Windows PowerShell中，您可以使用以下命令来设置HTTP代理：

```powershell
$env:http_proxy="http://127.0.0.1:20800"
```

这个命令会将`http_proxy`环境变量设置为`http://127.0.0.1:10800`，指定了HTTP代理的地址和端口。

如果您需要同时设置HTTPS代理，可以使用以下命令：

```powershell
$env:https_proxy="http://127.0.0.1:20800"
```

```powershell
$env:http_proxy="http://127.0.0.1:20800"
$env:https_proxy="http://127.0.0.1:20800"
```

java代码不支持http设置socks5

```powershell
$env:http_proxy="socks5://127.0.0.1:7890"
$env:https_proxy="socks5://127.0.0.1:7890"
```

```powershell
$env:http_proxy="http://127.0.0.1:20801"
$env:https_proxy="http://127.0.0.1:20801"
```

```cmd
set http_proxy=http://127.0.0.1:20800
set https_proxy=http://127.0.0.1:20800
echo %http_proxy%
echo %https_proxy%
```

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

