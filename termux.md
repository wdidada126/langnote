# termux



只能在termux中操作ssh登陆相关的文件

然后复制到笔记本上



https://www.jianshu.com/p/5c8678cef499



android c开发

clang



apt

清华源





https://www.jianshu.com/p/5c8678cef499



ssh 公钥那段可以开个 netcat -l port 外部传过去



Termux终端中sshd只支持密钥验证？No。现在可以这样：
1. 获取用户名：在termux输入whoami
2. 重置密码：在termux输入passwd
3. 打开sshd服务之后用前两步的用户名和密码登录


1）在termux 里安装openssh， 命令 pkg install openssh
2）将其他设备的指纹通过其他方式导入到 .ssh/authorized_keys
3） 在termux里启动ssh服务，命令 sshd
4）其他设备通过ssh登录, 使用8022端口

假设你termux设备ip为192.168.0.111，那么在其他设备上通过 ssh -p8022 192.168.0.111 登录termux 设备。设备指纹通过 cat ~/.ssh/id_rsa.pub 查看