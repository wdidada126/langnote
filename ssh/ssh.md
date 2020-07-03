# 生成密钥

`ssh-keygen -t rsa -C "XXX@xx.com.cn" -f finename`

ssh-keygen -t rsa -C "sandisks555@gmail.com" -f id_rsa_sandisks_gitlab



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





<<<<<<< HEAD
**ssh 免密登录失败**



-vvv可以调试



=======
>>>>>>> afe522da082020e5ece0b75c43067644b2edb768
