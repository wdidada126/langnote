# systemctl


启动服务：systemctl start vsftpd.service

关闭服务：systemctl stop vsftpd.service

重启服务：systemctl restart vsftpd.service

显示服务的状态：systemctl status vsftpd.service

在开机时启用服务：systemctl enable vsftpd.service

在开机时禁用服务：systemctl disable vsftpd.service

查看服务是否开机启动：systemctl is-enabled vsftpd.service

查看已启动的服务列表：systemctl list-unit-files|grep enabled

查看启动失败的服务列表：systemctl --failed



```shell
systemctl status redis.service
● redis.service - Redis persistent key-value database
   Loaded: loaded (/usr/lib/systemd/system/redis.service; disabled; vendor preset: disabled)
  Drop-In: /etc/systemd/system/redis.service.d
           └─limit.conf
   Active: failed (Result: exit-code) since Tue 2021-03-02 09:45:17 CST; 24h ago
 Main PID: 12998 (code=exited, status=1/FAILURE)

Mar 02 09:45:17 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: Starting Redis persistent key-value database...
Mar 02 09:45:17 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: redis.service: main process exited, code=exited, status=1/FAILURE
Mar 02 09:45:17 iZ2ze9f7g12pq4tby7ewz2Z redis-shutdown[12999]: Could not connect to Redis at 127.0.0.1:6379: Connection refused
Mar 02 09:45:17 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: redis.service: control process exited, code=exited status=1
Mar 02 09:45:17 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: Failed to start Redis persistent key-value database.
Mar 02 09:45:17 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: Unit redis.service entered failed state.
Mar 02 09:45:17 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: redis.service failed.
```

```shell
systemctl --version
systemd 219
+PAM +AUDIT +SELINUX +IMA -APPARMOR +SMACK +SYSVINIT +UTMP +LIBCRYPTSETUP +GCRYPT +GNUTLS +ACL +XZ +LZ4 -SECCOMP +BLKID +ELFUTILS +KMOD +IDN
```


https://www.cnblogs.com/sun77/p/13969027.html

```shell
systemctl list-unit-files | grep redis
redis-sentinel.service                        disabled
redis.service                                 disabled
```


