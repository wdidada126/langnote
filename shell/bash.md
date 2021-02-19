# bash

升级gclic

```shell
unlink /lib64/libc.so.6
ln -s libc-2.14.so /lib64/libc.so.6
ll libc.so.6
strings /lib64/libc.so.6 |grep GLIBC_
```
