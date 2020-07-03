# sed



```shell
sed -i "s/192.168.2.131/123.12.12.12/g" `grep 192.168.2.131 -rl ./*`
sed -i "s/3.0.0-beta/3.0.0-canary/g" `grep 3.0.0-beta -rl ./*`
```

-i ：直接修改读取的文件内容，而不是输出到终端。

[sed -i命令详解](https://www.cnblogs.com/ev-zhk/p/4277023.html)

Chrome Canary、Dev、Beta 的区别是什么？





ripgrep

命令行工具



