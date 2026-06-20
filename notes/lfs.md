# LFS（英文 Linux From Scratch 的缩写）

LFS-BOOK-8.3.pdf
https://lctt.github.io/LFS-BOOK/
http://www.linuxfromscratch.org/lfs/


中文释意为“从零开始构建的 Linux”

https://zhuanlan.zhihu.com/p/51992113
http://www.linuxfromscratch.org/lfs/


/usr/include/asm/*.h
Linux API ASM 头文件
/usr/include/asm-generic/*.h
Linux API ASM 通用头文件
/usr/include/drm/*.h
Linux API DRM 头文件
/usr/include/linux/*.h
Linux API Linux 头文件
/usr/include/mtd/*.h
Linux API MTD 头文件
/usr/include/rdma/*.h
Linux API RDMA 头文件
/usr/include/scsi/*.h
Linux API SCSI 头文件
/usr/include/sound/*.h
Linux API 音频头文件
/usr/include/video/*.h
Linux API 视频头文件
/usr/include/xen/*.h
Linux API Xen 头文件	


gcc需要的GMP、MPFR、MPC三个库

man 手册
描述 C 编程语言函数，重要的设备文件，以及主要的配置文件

binutils
https://blog.csdn.net/zqixiao_09/article/details/50783007
https://www.gnu.org/software/binutils/


addr2line,ar,as,c++filt,elfedit,gprof,ld,ld.bfd,nm,objcopy,objdump,ranlib,readelf,size,strings,和strip


GMP GNU多精度算术库
GMP(The GNU Multiple Precision Arithmetic Library)又叫GNU多精度算术库
https://blog.csdn.net/CherylNatsu/article/details/6405714

GNU MPFR
GNU MPFR (GNU Multiple Precision Floating-Point Reliably

https://en.wikipedia.org/wiki/GNU_MPFR


MPC 软件包包含一个能以任意高精度进行复数数值计算和对结果进行正确四舍五入的库































c++
C++ 编译器
cc
C 编译器
cpp
C 预处理器；编译器用来扩展源文件中 #include、#define 以及类似语句
g++
C++ 编译器
gcc
C 编译器
gcc-ar
增加插件到命令行的 ar 的封装。这个程序只用于添加 "链接时间优化"，在使用默认编译选项时不起作用
gcc-nm
增加插件到命令行的 nm 的封装。这个程序只用于添加 "链接时间优化"，在使用默认编译选项时不起作用
gcc-ranlib
增加插件到命令行的 ranlib 的封装。这个程序只用于添加 "链接时间优化"，在使用默认编译选项时不起作用
gcov
一个覆盖测试工具；用于分析程序以决定在哪里进行优化有最大的效果
libasan
Address Sanitizer（译者注：地址消毒剂，可以查看：Wiki）运行时库。
libgcc
包含用于 gcc 的运行时支持
libgcov
当指示 GCC 启用分析时该库会被链接到程序中
libgomp
用于 C/C++、Fortran 语言的多平台共享内存并行编程的 OpenMP API 的 GNU 实现
libiberty
包含多种 GNU 程序所使用的例程，包括 getopt, obstack, strerror, strtol, 和 strtoul
liblto_plugin
GCC 的链接时间优化插件，允许 GCC 跨编译单元进行优化
libquadmath
GCC 四精度数学库 API
libssp
包含支持 GCC 堆栈溢出保护功能的例程
libstdc++
标准 C++ 库
libsupc++
为 C++ 编程语言提供支持例程
libtsan
Thread Sanitizer（译者注：数据速率检测工具，包括一个编译器指令模块和运行时库） 运行时库












Bzip2 软件包包含压缩和解压缩的程序。用 bzip2 压缩文本文件能获得比传统的 gzip 更好的压缩比。
bunzip2
解压 bzip 压缩的文件
bzcat
解压到标准输出
bzcmp
对 bzip 压缩的文件运行 cmp 命令
bzdiff
对 bzip 压缩的文件运行 diff 命令
bzegrep
对 bzip 压缩的文件运行 egrep 命令
bzfgrep
对 bzip 压缩的文件运行 fgrep 命令
bzgrep
对 bzip 压缩的文件运行 grep 命令
bzip2
使用哈夫曼编码的 Burrows-Wheeler 块排序文本压缩算法压缩文件；压缩率比传统的用 “Lempel-Ziv” 算法的压缩器要好，比如 gzip。
bzip2recover
尝试从损坏的 bzip 压缩文件中恢复数据
bzless
对 bzip 压缩的文件运行 less 命令
bzmore
对 bzip 压缩的文件运行 more 命令
libbz2
用 Burrows-Wheeler 算法实现的无损的块排序数据压缩库


















pkg-config 软件包包含一个在配置和 make 文件运行时把 include 路径和库路径传递给编译工具的工具。


Ncurses 软件包包含用于不依赖于特定终端的字符屏幕处理的库。


captoinfo
转换 termcap 描述为 terminfo 描述
clear
如果可以的话清空屏幕
infocmp
比较或输出 terminfo 描述
infotocap
转换 terminfo 描述为 termcap 描述
ncursesw5-config
为 ncurses 提供配置信息
reset
重新初始化终端为默认设置
tabs
清空终端并设置制表符长度
tic
将 terminfo 文件从源文件格式转换到二进制格式的 terminfo 条目描述编译器需要 ncurses 例程 [terminfo 文件包含特定终端的功能信息]
toe
列出所有可用的终端类型，给出每个主名称和描述
tput
可以在 shell 中使用终端特定的功能值；也可用来重置或初始化终端或者报告它的完整名称
tset
可以用来初始化终端
libcursesw
到 libncursesw 的链接。
libncursesw
包含在一个终端屏幕以多种复杂方式显示文本的函数；使用这些功能的一个好的例子是内核 make menuconfig 时的菜单显示
libformw
包含实现表单的函数
libmenuw
包含实现菜单的函数
libpanelw
包含实现面板的函数

attr 软件包包含管理文件系统对象的扩展属性的工具。
attr
扩展文件系统对象的属性
getfattr
获取文件系统对象的扩展属性
setattr
设置文件系统对象的扩展属性
libattr
包含管理扩展属性的库函数

Acl软件包包含管理访问控制列表的工具，访问控制列表用于定义文件和目录更细粒度的自定义访问权限。
chacl
更改文件或目录的访问控制列表
getfacl
获取文件访问控制列表
setacl
设置文件访问控制列表
libacl
包括用于管理访问控制列表的库函数

Libcap 软件包实现了可用在 Linux 内核上的对 POSIX 1003.1e 功能的用户空间接口。 这些功能将所有强大 root 权限划分为不同的权限组合。
capsh
使用和控制功能支持的 shell 封装
getcap
检查文件功能
getpcaps
显示查询进程的功能
libcap
包括用于管理 POSIX 1003.1e 功能的库函数

Sed 软件包包含一个流编辑器。
Shadow 软件包包含以安全方式处理密码的程序。
chage
用来更改强制性密码更新的最大天数
chfn
用来更改用户的全名以及其它信息
chgpasswd
用来以批处理模式更新组密码
chpasswd
用来以批处理模式更新用户密码
chsh
用来更改用户登录时默认使用的 shell
expiry
检查并强制执行当前密码过期策略
faillog
用来检查登录失败的日志文件，设置锁定用户的最大失败次数，或者重置失败次数
gpasswd
用来给组增加、删除成员以及管理员
groupadd
用指定的名称创建组
groupdel
用指定的名称删除组
groupmems
允许用户管理他/她自己的组成员列表而不需要超级用户权限。
groupmod
用于更改指定组的名称或 GID
grpck
验证组文件 /etc/group 和 /etc/gshadow 的完整性
grpconv
从普通组文件创建或升级为 shadow 组文件
grpunconv
从 /etc/gshadow 更新到 /etc/group 然后删除前者
lastlog
报告所有用户或指定用户的最近一次登录
login
用于系统让用户登录进来
logoutd
用于强制限制登录时间和端口的守护进程
newgrp
用于在一次登录会话中更改当前 GID
newusers
用于批量创建或更新用户账户
nologin
显示一个账户不可用的信息；它用于来作为不可登录的账户的默认 shell
passwd
用来更改用户或组账户的密码
pwck
验证密码文件 /etc/passwd 和 /etc/shadow 的完整性
pwconv
从普通密码文件创建或升级 shadow 密码文件
pwunconv
从 /etc/shadow 更新到 /etc/passwd 然后删除前者
sg
当用户的 GID 被设置为指定组的 GID 时执行一个特定命令
su
用替换的用户和组 ID 运行 Shell
useradd
用指定的名称新建用户或更新新用户的默认信息
userdel
删除指定的用户账户
usermod
用于更改指定用户的登录名称、UID、shell、初始组、home 目录，等
vigr
编辑 /etc/group 或 /etc/gshadow 文件
vipw
编辑 /etc/passwd 或 /etc/shadow 文件

https://linux.cn/lfs/LFS-BOOK-7.7-systemd/chapter06/procps-ng.html

ext2
适用于那些分区容量不是太大，更新也不频繁的情况，例如 /boot 分区。
ext3
是 ext2 的改进版本，其支持日志功能，能够帮助系统从非正常关机导致的异常中恢复。它通常被用作通用的文件系统。
ext4
是 ext 文件系统的最新版。提供了很多新的特性，包括纳秒级时间戳、创建和使用巨型文件(16TB)、以及速度的提升。

mkfs -v -t ext4 /dev/<xxx>
mkswap /dev/<yyy>

mkswap，swapon, swapoff命令:创建交换分区
http://blog.51cto.com/leomars/522768

笔者作为linux运维，玩Linux From Scratch 玩了很多年。说实话，你从头到尾玩一遍，边学边解决问题，一般参考国内金步国的内核调试指南，一边结合自己的硬件进行定制和调试，你能学通很多东西，运维gentoo和arch就不在话下了，因为从无到有藏着很多最基础的认知，你必须从头到尾做完一遍才行，人无法想象理解自己没有做过的事，没有玩过LFS的，听不懂我在说什么，不会知道金步国三个字的含金量。：）
Linux From Scratch（LFS）项目提供了从源代码构建定制 Linux 系统的逐步指南。
项目提供了 System V 和 systemd 两个版本，允许用户选择不同的初始化系统。现在 LFS 项目宣布将不再提供 System V 版本，第一个理由是工作量太大，项目志愿者们不堪重负。LFS 包含 88 个软件包，Beyond Linux From Scratch(BLFS) 包含逾 1000 个软件包，更新软件包需要同时检查与 System V 和 systemd 的兼容性；第二个原因是桌面环境 GNOME 和 KDE Plasma 未来都只支持 systemd 了。预计2026年 3 月开始，释出的 LFS 13.0 将只有 systemd 版本。
老实说，我对这个消息既不意外也不难过，但是还是感到唏嘘。因为老古董slackware都吸纳了滚动版本的特性，开始滚动更新，也早就拥抱 systemd了。
从项目维护的角度来看，这似乎是不可避免的宿命。
LFS 放弃 System V 版本，标志着 Linux 社区中初始化系统之争在一个最具教学意义的阵地落下了帷幕。对于关注 Linux 内核社区和底层架构的开发者来说，这一转变背后有几个深层逻辑。
1. 维护负担和代价
正如公告所言，LFS 核心虽然只有 88 个包，但 BLFS（Beyond LFS）才是真正的挑战。在现代发行版中，软件依赖已经形成了一个复杂的网状结构。为两套截然不同的初始化系统维护兼容脚本（System V 的initscripts vs systemd 的 unit files），其工作量不是翻倍，而是呈几何倍数增长。
新一代社区志愿者的大量流失。现在的花花世界，诱惑太多，愿意并有能力手工编写符合 LFS 标准的 SysV 启动脚本的开发者越来越少，人才断层让项目难以为继。
2. 桌面环境纷纷倒戈胁迫
在linux桌面阵营，GNOME 与 KDE 均支持systemd，这可能是压死骆驼的最后一根稻草。由于现代桌面环境高度依赖 logind、timedated 等 systemd 组件来实现电源管理、多用户会话隔离和硬件热插拔，剥离 systemd 变得异常困难。
如果 LFS 坚持 SysV，那么它的用户将很难体验到现代化的图形界面，这会使 LFS 的适用范围进一步萎缩到仅限极简服务器或嵌入式实验。
3. LFS 13.0 的技术路线转折
其实linux从教学式科教系统转向黑盒化生产系统一直是行业的大趋势，只有从多样性转向深度。LINUX运营商、系统开发者才能更关注系统本身，而不是内核的技术细节，这样分工化的发展是系统越发庞杂的必然选择。linux0.9只有2M，现在的系统动辄4-8G。 放弃 SysV 后，LFS 团队可以将精力集中在 systemd 的深度整合上，比如更好地支持 Cgroup v2、内存安全增强以及与新版内核（ 6.19/7.0）的特性匹配。
适应时代的教学意义的转变。以前 LFS 是学习 Linux 如何从传统的 Unix 风格演进的重要参考，现在的 LFS 将更多地变成学习“现代 Linux 工业标准”是如何构建的，教学系统的搭建思路已经发生了变化。
这种大一统虽然牺牲了选择的多样性，但确实有助于推广一些现代特性。systemd 对 Sandbox 和 Resource Control 的原生支持，其实比 SysV 脚本更容易实现安全的系统环境。
如果你依然迷恋极简的初始化系统，可以关注 Gentoo 或 Devuan 社区，它们目前依然是 SysV 和 OpenRC 的坚实堡垒。
