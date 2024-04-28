# netcat

nc — arbitrary TCP and UDP connections and listens

我是在测试sparkStreaming时候用到


https://netcat.sourceforge.net/

wget -O netcat-0.7.1.tar.gz https://zenlayer.dl.sourceforge.net/project/netcat/netcat/0.7.1/netcat-0.7.1.tar.gz?viasf=1

## netcat
在CentOS和Ubuntu上，可以使用系统自带的包管理工具来安装Netcat。

在CentOS上，可以使用以下命令安装Netcat：

```bash
sudo yum install nc -y
```

在Ubuntu上，可以使用以下命令安装Netcat：

```bash
sudo apt-get update  
sudo apt-get install netcat -y
```
完成安装后，就可以使用Netcat命令执行各种网络任务了，如建立TCP或UDP连接、端口扫描、文件传输等。

请注意，具体的安装命令可能会因操作系统版本或发行版的不同而有所差异。如果上述命令无法正常工作，建议查阅相关操作系统的文档或在线资源，以获取更准确的安装方法。

另外，Netcat是一个功能强大的工具，使用时需要谨慎操作，避免对网络安全造成潜在威胁。请确保在合法和安全的范围内使用Netcat，并遵循相关的网络安全规定和最佳实践。

nc -L -p 9999 

netcat-win32-1.12.zip


nc -vz 192.168.1.2 8080


PS C:\Users\edidada> nc -vz 127.0.0.1 8199
www.sublimetext.com [127.0.0.1] 8199 (?) open
PS C:\Users\edidada> nc -vz localhost 8199
DNS fwd/rev mismatch: Wdidada != www.sublimetext.com
Wdidada [127.0.0.1] 8199 (?) open

https://zhuanlan.zhihu.com/p/83959309



#### 传输测试

你在配置 iptable 或者安全组策略，禁止了所有端口，但是仅仅开放了 8080 端口，你想测试一下该设置成功与否怎么测试？安装个 nginx 改下端口，外面再用 chrome 访问下或者 telnet/curl 测试下？？还是 python -m 启动简单 http 服务 ？其实不用那么麻烦，在需要测试的 A 主机上：
nc -l -p 8080
这样就监听了 8080 端口，然后在 B 主机上连接过去：
nc 192.168.1.2 8080
PS C:\Users\edidada> nc  localhost 8199
ii
ii