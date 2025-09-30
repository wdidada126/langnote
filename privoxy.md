# privoxy
curl -x http://127.0.0.1:10801 http://httpbin.org/ip

https://www.privoxy.org/

https://www.privoxy.org/user-manual/index.html

https://github.com/shadowsocks/ShadowsocksX-NG
用了


源代码和安装文件
https://sourceforge.net/projects/ijbswa/files/Win32/3.0.34%20%28stable%29/


## source code 源代码
git clone https://www.privoxy.org/git/privoxy.git
cd privoxy
autoheader
autoconf
./configure      # (--help to see options)
make             # (the make from GNU, sometimes called gmake)
su               # Possibly required
make -n install  # (to see where all the files will go)
make -s install  # (to really install, -s to silence output)

git clone https://www.privoxy.org/git/privoxy.git
cd privoxy
autoheader
autoconf
./configure
make -j4
sudo make -n install

## win10配置
cd D:\dev_tools\privoxy_3.0.34
privoxy.exe --no-daemon config.txt

$env:HTTP_PROXY="http://127.0.0.1:8118"
$env:HTTPS_PROXY="https://127.0.0.1:8118"

## mac
brew info privoxy
/usr/local/etc/privoxy/config


你已经通过 Homebrew 成功安装了 `privoxy`，并且能看到：

```bash
/usr/local/Cellar/privoxy/3.0.33/homebrew.mxcl.privoxy.plist
```

这个文件就是 macOS Launch Agent 的服务配置文件，用于让 `privoxy` 作为后台服务运行并支持开机自启。

现在你只需要将这个 `.plist` 文件“链接”到用户级服务目录，并用 `launchd` 加载它。

##  目标：设置 Privoxy 开机自启 + 后台自动运行

### 手动使用 `launchctl`（适用于 `brew services` 不可用）


#### 1. 复制 plist 文件到用户 LaunchAgents 目录

```bash
cp /usr/local/Cellar/privoxy/3.0.33/homebrew.mxcl.privoxy.plist ~/Library/LaunchAgents/
```

#### 2. 加载并启动服务（立即运行 + 开机自启）

```bash
launchctl load ~/Library/LaunchAgents/homebrew.mxcl.privoxy.plist
launchctl start homebrew.mxcl.privoxy
```

>  `load` 表示注册为开机自启  
>  `start` 表示立即启动（如果不加，下次重启才生效）

#### 3. 验证是否运行

```bash
ps aux | grep privoxy
```

你应该看到类似：

```
privoxy   12345   0.0  0.1  1234567  89012   ??  Ss    10:30AM   0:00.12 /usr/local/sbin/privoxy /usr/local/etc/privoxy/config
```

###  方法三：设置为系统级服务（可选，不推荐普通用户）

如果你想让 Privoxy 在所有用户登录前就运行（如共享代理），可以放到 `/Library/LaunchDaemons/`（需要 `sudo`）：

```bash
sudo cp /usr/local/Cellar/privoxy/3.0.33/homebrew.mxcl.privoxy.plist /Library/LaunchDaemons/
sudo launchctl load /Library/LaunchDaemons/homebrew.mxcl.privoxy.plist
sudo launchctl start homebrew.mxcl.privoxy
```

>  注意：需要管理员权限，且配置文件路径要确保可读。


##  如何停止或卸载服务？

### 停止服务（临时）

```bash
launchctl stop homebrew.mxcl.privoxy
launchctl unload ~/Library/LaunchAgents/homebrew.mxcl.privoxy.plist
```

### 取消开机自启

只需 `unload` 即可：

```bash
launchctl unload ~/Library/LaunchAgents/homebrew.mxcl.privoxy.plist
```

文件可以保留，下次再 `load` 就能恢复。

##  验证 Privoxy 是否正常工作

1. 检查监听端口（默认 `8118`）：

```bash
grep "listen-address" /usr/local/etc/privoxy/config
```

2. 测试代理是否响应：

```bash
curl -x http://127.0.0.1:10801 http://httpbin.org/ip
```

应返回你的IP（通过 Privoxy 转发）。

##  总结：推荐操作流程

```bash
# 1. 确保 services 扩展存在
brew tap homebrew/services

# 2. 启动并设置开机自启（自动管理）
brew services start privoxy

# 3. 验证
brew services list | grep privoxy
ps aux | grep privoxy
```

>  这样就实现了：Privoxy 开机自动启动 + 后台运行 + 易于管理

 关键点：
- `homebrew.mxcl.privoxy.plist` 是服务配置模板，必须被 `launchctl` 加载。
- `brew services start privoxy` 是最简洁、最标准的方式。
- 手动 `launchctl` 是备选方案，适合调试或旧版 Homebrew。

你现在完全可以使用 `brew services start privoxy` 实现自动化管理
