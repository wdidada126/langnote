# binutils

GNU Binutils（全称：Binary Utilities）是一组用于处理目标文件、汇编代码和链接的开发工具集合。这些工具是构建 C/C++ 程序的重要组成部分，尤其在 Linux 和类 Unix 系统中广泛使用。

### Binutils 官网地址：

https://www.gnu.org/software/binutils/

这是 GNU 项目对 Binutils 的官方介绍页面。

```shell
rpm -ql devtoolset-7-binutils 
/opt/rh/devtoolset-7/root/usr/bin/addr2line
/opt/rh/devtoolset-7/root/usr/bin/ar
/opt/rh/devtoolset-7/root/usr/bin/as
/opt/rh/devtoolset-7/root/usr/bin/c++filt
/opt/rh/devtoolset-7/root/usr/bin/dwp
/opt/rh/devtoolset-7/root/usr/bin/elfedit
/opt/rh/devtoolset-7/root/usr/bin/gprof
/opt/rh/devtoolset-7/root/usr/bin/ld
/opt/rh/devtoolset-7/root/usr/bin/ld.bfd
/opt/rh/devtoolset-7/root/usr/bin/ld.gold
/opt/rh/devtoolset-7/root/usr/bin/nm
/opt/rh/devtoolset-7/root/usr/bin/objcopy
/opt/rh/devtoolset-7/root/usr/bin/objdump
/opt/rh/devtoolset-7/root/usr/bin/ranlib
/opt/rh/devtoolset-7/root/usr/bin/readelf
/opt/rh/devtoolset-7/root/usr/bin/size
/opt/rh/devtoolset-7/root/usr/bin/strings
/opt/rh/devtoolset-7/root/usr/bin/strip
```

addr2line
ar
as
c++filt
dwp
elfedit
gold
gprof
ld
ld.bfd
ld.gold
nm
objcopy
objdump
ranlib
readelf
size
strings
strip


```shell
dpkg -L binutils
/.
/usr
/usr/bin
/usr/lib
/usr/lib/compat-ld
/usr/lib/gold-ld
/usr/lib/x86_64-linux-gnu
/usr/share
/usr/share/bug
/usr/share/bug/binutils
/usr/share/bug/binutils/presubj
/usr/share/doc
/usr/share/doc/binutils
/usr/share/doc/binutils/copyright
/usr/share/lintian
/usr/share/lintian/overrides
/usr/share/lintian/overrides/binutils
/usr/share/man
/usr/bin/addr2line
/usr/bin/ar
/usr/bin/as
/usr/bin/c++filt
/usr/bin/dwp
/usr/bin/elfedit
/usr/bin/gold
/usr/bin/gprof
/usr/bin/ld
/usr/bin/ld.bfd
/usr/bin/ld.gold
/usr/bin/nm
/usr/bin/objcopy
/usr/bin/objdump
/usr/bin/ranlib
/usr/bin/readelf
/usr/bin/size
/usr/bin/strings
/usr/bin/strip
/usr/lib/compat-ld/ld
/usr/lib/gold-ld/ld
/usr/share/doc/binutils/changelog.Debian.gz

```