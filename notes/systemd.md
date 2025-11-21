# systemd



ubuntu从16.04开始不再使用initd管理系统,改用systemd。然而systemd很难用,刚开始接触有点烦,改变太大,跟之前的完全不同



systemd

exec 



[Systemd 入门教程：实战篇](https://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-part-two.html)



```shell script


systemctl cat sshd.service

[Unit]
Description=OpenSSH server daemon
Documentation=man:sshd(8) man:sshd_config(5)
After=network.target sshd-keygen.service
Wants=sshd-keygen.service

[Service]
EnvironmentFile=/etc/sysconfig/sshd
ExecStart=/usr/sbin/sshd -D $OPTIONS
ExecReload=/bin/kill -HUP $MAINPID
Type=simple
KillMode=process
Restart=on-failure
RestartSec=42s

[Install]
WantedBy=multi-user.target
```



配置文件,centos 7在

/usr/lib/systemd/system

ubuntu 16 tls不在，在
/etc/systemd/system


https://www.centosdoc.com/system/201.html
