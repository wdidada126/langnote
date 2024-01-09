# paramiko
The leading native Python SSHv2 protocol library.

pip install paramiko

https://github.com/paramiko/paramiko

http://paramiko.org/

```python
import paramiko

def scp_upload(local_file, remote_file, hostname, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)

    sftp = ssh.open_sftp()
    sftp.put(local_file, remote_file)
    sftp.close()

    ssh.close()

# 示例用法
local_file = '本地文件路径'
remote_file = '远程文件路径'
hostname = '主机名或IP地址'
port = 22  # SSH端口，默认为22
username = '用户名'
password = '密码'

scp_upload(local_file, remote_file, hostname, port, username, password)
```


