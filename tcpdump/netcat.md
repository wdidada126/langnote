# netcat

我是在测试sparkStreaming时候用到


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