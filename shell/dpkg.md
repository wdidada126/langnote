# dpkg

man dpkg

要查看通过apt安装的库文件所在路径，可以使用以下命令：
dpkg - package manager for Debian
dpkg -L libprotobuf-dev

查看/usr/include/linux/sysctl.h属于哪个包？

dpkg -S /usr/include/linux/sysctl.h
linux-libc-dev:amd64: /usr/include/linux/sysctl.h

# 1. 查看当前安装的 Boost 版本
dpkg -l | grep boost

