# scp

两台通过联网的主机，复制文件
`
scp -P 27795  root@67.209.189.193:/root/mactex-20200407.pkg  ~
`

scp
usage: scp [-12346BCpqrv] [-c cipher] [-F ssh_config] [-i identity_file]
           [-l limit] [-o ssh_option] [-P port] [-S program]
           [[user@]host1:]file1 ... [[user@]host2:]file2


scp是Linux系统下的一个用于远程复制文件的命令。其基本语法如下：
scp [参数选项] [源文件] [目标地址]
其中，参数选项和源文件都是可选的，目标地址是必须的。

以下是一些常用的参数选项：

-r：递归复制整个目录。
-P：指定端口号。
-C：开启压缩传输。
-v：显示详细的传输过程。

以下是一些常用的示例：

1. 从本地复制文件到远程服务器：

`scp /path/to/local/file user@remote_server:/path/to/remote/directory`

这将把本地的文件复制到远程服务器的指定目录。

2. 从远程服务器复制文件到本地：

`scp user@remote_server:/path/to/remote/file /path/to/local/directory`

这将从远程服务器的指定文件复制到本地的指定目录。

3. 递归复制整个目录：

`scp -r /path/to/local/directory user@remote_server:/path/to/remote/directory`

这将递归复制本地的整个目录到远程服务器的指定目录。

4. 使用端口号进行传输：

`scp -P 22 user@remote_server:/path/to/remote/file /path/to/local/directory`

这将使用SSH端口22进行文件传输。

请注意，在使用scp命令时，需要确保目标地址和源文件的路径正确，并且需要提供目标服务器的用户名和密码（如果需要的话）。


`scp` 是用于在本地和远程计算机之间安全复制文件的命令。它基于 SSH（Secure Shell）协议，因此需要确保本地和远程计算机之间的网络连接是安全的。

以下是使用 `scp` 命令复制文件的基本语法：

```bash
scp [选项] [源文件路径] [目标文件路径]
```

其中，`[选项]` 可以是以下选项之一：

- `-P`：指定远程主机的端口号。
- `-r`：递归复制目录及其内容。
- `-p`：保留文件属性（如时间戳、权限等）。
- `-q`：静默模式，不显示传输过程中的信息。

例如，要将本地文件 `file.txt` 复制到远程主机 `example.com` 的 `/home/user` 目录下，可以使用以下命令：

```bash
scp -P 22 file.txt user@example.com:/home/user/
```

请根据实际情况替换 `22` 为远程主机的端口号，以及 `user` 为目标主机上的用户名。


## scp，如何把公钥放到对方计算机上
要将公钥放到对方计算机上，你可以使用SCP命令。首先，你需要在本地计算机上生成一对公钥和私钥。然后，将公钥上传到远程服务器。当需要从远程服务器下载文件时，可以使用SCP命令并指定私钥进行身份验证。

具体操作步骤如下：
1. 打开目标主机的authorized_keys文件：`vim ~/.ssh/authorized_keys`
2. 查看源主机公钥：一般在源主机上执行`cat ~/.ssh/id_rsa.pub`命令即可
3. 将源主机公钥追加到文件中：将公钥内容复制，然后在authorized_keys文件的最后一行粘贴并保存退出。

sshpass
仅仅支持linux
askpass支持windows
