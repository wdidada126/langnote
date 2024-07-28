# openssh

## mail list
https://www.openssh.com/list.html
sandisks gmail

You can also make such adjustments via email by sending a message to:

  openssh-unix-dev-request@mindrot.org

with the word `help' in the subject or body (don't include the
quotes), and you will get back a message with instructions.

## windows
C:\Windows\System32\OpenSSH

scp.exe
sftp.exe
ssh-add.exe
ssh-agent.exe
ssh-keygen.exe
ssh-keyscan.exe
ssh.exe

## ubuntu 20
sudo apt install openssh-server -y
sudo lsof -i:22
不是lsof -i:22

OpenSSH服务器的配置文件位于`/etc/ssh/sshd_config`。你可以使用文本编辑器（如nano或vim）打开该文件并编辑它，以更改OpenSSH服务器的配置选项。

例如，要更改SSH服务器监听的端口号，可以按照以下步骤操作：

1. 打开终端（Ctrl+Alt+T）。
2. 输入以下命令以使用nano编辑器打开sshd_config文件：

```bash
sudo nano /etc/ssh/sshd_config
```

3. 找到以下行：

```bash
#Port 22
```

4. 取消注释并将端口号更改为所需的值，例如：

```bash
Port 2222
```

5. 保存文件并退出nano编辑器（按Ctrl+X，然后按Y，最后按Enter）。
6. 重启SSH服务以使更改生效：

```bash
sudo systemctl restart ssh
```

现在，SSH服务器将监听新的端口号。


ubuntu 20主机 openssh开启，现在要ssh登录，为什么是能public key，不能username password
在Ubuntu 20主机上，如果已经开启了OpenSSH服务并且配置了公钥认证方式，那么默认情况下将不允许使用用户名和密码进行登录。这是因为OpenSSH的默认配置是使用公钥认证方式，这种方式比传统的用户名和密码认证方式更加安全。

如果你希望使用用户名和密码进行登录，可以按照以下步骤修改OpenSSH服务器的配置文件：

1. 打开终端（Ctrl+Alt+T）。
2. 输入以下命令以编辑sshd_config文件：

```bash
sudo vim /etc/ssh/sshd_config
```

3. 找到以下行：

```bash
#PasswordAuthentication yes
```

4. 取消注释并将值更改为yes：

```bash
PasswordAuthentication yes
```

5. 保存文件并退出nano编辑器（按Ctrl+X，然后按Y，最后按Enter）。

6. 重启SSH服务以使更改生效：

```bash
sudo systemctl restart ssh
```

现在，你应该可以使用用户名和密码进行SSH登录了。请注意，使用用户名和密码认证方式可能会降低系统的安全性，因此建议尽可能使用公钥认证方式。

开机启动
sudo systemctl enable ssh
Synchronizing state of ssh.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable ssh