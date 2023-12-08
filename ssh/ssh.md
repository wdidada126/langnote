# ssh

测试一下该SSH key
在git Bash 中输入以下代码

$ ssh -T git@github.com


ssh git@bitbucket.org host_key_info

## 生成密钥
Windows 用户建议使用 Windows PowerShell 或者 Git Bash，在 命令提示符 下无 cat 和 ls 命令。


ssh-keygen -t ed25519 -C "1664884095@qq.com"

`ssh-keygen -t rsa -C "XXX@xx.com.cn" -f finename`

ssh-keygen -t rsa -C "sandisks555@gmail.com" -f id_rsa_sandisks_gitlab
ssh-keygen -t rsa -C "sandisks555@gmail.com" -f id_rsa_edidada_github

ssh-keygen -t rsa -C "1664884095@qq.com" -f id_rsa_166_gitee

ssh-keygen -m PEM -t rsa -b 4096 -C "wc@eteng.cn" -f id_rsa_coding_eteng

ssh-keygen -m PEM -t rsa -b 4096 -C "1664884095@qq.com" -f id_rsa_coding_166

C:\Users\edida/.ssh/id_rsa_coding_166
C:\Users\edida/.ssh/id_rsa_coding_eteng

```
git config user.name "edidada"
git config user.email "1664884095@qq.com"
```

### 生成的文件名和文件位置

使用 `ssh-kengen` 会在~/.ssh/目录下生成两个文件，不指定文件名和密钥类型的时候，默认生成的两个文件是：

- `id_rsa`
- `id_rsa.pub`

第一个是私钥文件，第二个是公钥文件。

生成ssh key的时候，可以通过 `-f` 选项指定生成文件的文件名，如下:

```bash
[huqiu@101 .ssh]$ ssh-keygen -f test   -C "test key"
                             ~~文件名   ~~~~ 备注
```

如果没有指定文件名，会询问你输入文件名:

免密登陆

文件 .ssh authorized_keys权限不对

ssh -vvv -i ~/.ssh/id_rsa_termux 

ssh-copy-id

ssh-add

ssh-agent 导入本机的私钥

要登录多个机器,github也是用ssh的

ssh 免密登录失败
-vvv可以调试

## ssh client
C:\Windows\System32\OpenSSH\ssh.exe

ssh-keyscan github.com >> /c/Users/edida/.ssh/known_hosts

git pull -S /c/Users/edida/.ssh/id_rsa_edidada_github origin master

git pull -S c/Users/edida/.ssh/id_rsa_edidada_github origin master


当你使用 SSH 进行远程连接时，通常需要提供身份验证信息来验证你的身份。传统的身份验证方式包括使用密码进行身份验证或使用 SSH 密钥对进行身份验证。

SSH 密钥对由两部分组成：私钥（private key）和公钥（public key）。私钥保存在你的本地计算机上，而公钥则被添加到远程服务器上的授权文件中。在进行 SSH 连接时，你的本地计算机使用私钥进行身份验证，而远程服务器使用公钥验证你的身份。

SSH 代理（SSH Agent）是一个在后台运行的程序，它可以管理你的私钥，并在需要时自动提供身份验证，而无需每次都输入密码或密钥的密码。`ssh-add` 命令用于将私钥添加到 SSH 代理中。

使用 `ssh-add` 命令的一些常见用法和注意事项包括：

1. 添加私钥到 SSH 代理：使用 `ssh-add` 命令，可以将私钥添加到 SSH 代理中，例如：

   ````
   ssh-add ~/.ssh/id_rsa
   ```

   这将把 `~/.ssh/id_rsa` 私钥添加到 SSH 代理中。

2. 查看已添加的私钥：可以使用 `ssh-add -l` 命令查看当前 SSH 代理中已添加的私钥列表。

3. 删除已添加的私钥：使用 `ssh-add -d` 命令可以从 SSH 代理中删除指定的私钥，例如：

   ````
   ssh-add -d ~/.ssh/id_rsa
   ```

   这将从 SSH 代理中删除 `~/.ssh/id_rsa` 私钥。

4. 持久性添加私钥：默认情况下，通过 `ssh-add` 添加的私钥在注销或重新启动计算机后会被移除。如果希望私钥在重启后仍然保持添加状态，可以使用 `-K` 参数，例如：

   ````
   ssh-add -K ~/.ssh/id_rsa
   ```

   这将持久性地将 `~/.ssh/id_rsa` 私钥添加到 SSH 代理中。

使用 SSH 代理和 `ssh-add` 命令可以帮助简化 SSH 连接的过程，提高安全性，并避免重复输入密码或密钥的密码。你可以根据需要管理和操作 SSH 代理中的私钥，并根据具体情况配置持久性添加私钥。



在 Windows 10 上，`~/.ssh/config` 文件实际上位于用户目录下的 `.ssh` 文件夹中。你可以按照以下步骤创建该文件：

1. 打开 Windows 资源管理器并导航到你的用户目录。通常情况下，这个目录的路径是 `C:\Users\YourUsername`，其中 `YourUsername` 是你的 Windows 用户名。

2. 在用户目录中，查找名为 `.ssh` 的文件夹。如果没有该文件夹，可以创建一个新的文件夹并命名为 `.ssh`。

3. 在 `.ssh` 文件夹中，右键单击空白区域，并选择 "新建" -> "文本文档"。

4. 将新创建的文本文档重命名为 `config`，确保没有任何后缀名。

5. 右键单击 `config` 文件，选择 "编辑" 或 "使用默认程序打开"。

6. 在文本编辑器中，按照以下格式添加 SSH 配置信息：

   ````
   Host github.com
     IdentityFile /path/to/private_key
     User your_github_username
   ```

   将 `/path/to/private_key` 替换为你生成的私钥文件的实际路径，并将 `your_github_username` 替换为你的 GitHub 用户名。

7. 保存并关闭文件。

现在，你已经成功创建了 `~/.ssh/config` 文件。请确保将其中的路径和用户名替换为你自己的实际信息。记住，在 Windows 上，该文件在用户目录的 `.ssh` 文件夹中，而不是直接位于 `C:\` 目录下。

