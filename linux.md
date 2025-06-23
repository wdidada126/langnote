 # Linux

## linux 系统api

列表的
https://man7.org/linux/man-pages/dir_all_alphabetic.html



搜索的
https://man.archlinux.org/man/epoll.7.zh_CN

man.archlinux.org	https://man.archlinux.org/
man7.org (Linux man pages)	https://man7.org/linux/man-pages/
cppreference.com（C/C++标准库）	https://en.cppreference.com/
kernel.org 文档	https://www.kernel.org/doc/html/latest/

https://docs.kernel.org/core-api/kernel-api.html

Linux 内核版本 **6.0**（发布于 2022 年 9 月）引入了许多新特性，包括对系统编程 API 的更新和增强。这些新增或改进的 C/C++ 系统调用、库函数以及内核接口，主要集中在性能优化、安全性、资源管理、异步 I/O 和硬件支持等方面。

---

## 📌 Linux 6.0 新增/改进的主要系统编程 API（C/C++）

下面列出的是 **Linux 6.0 版本中与系统编程相关的重大变更和新增 API**，适用于 C/C++ 开发者，尤其是从事高性能网络、存储、虚拟化、安全等底层开发的人员。

---

###  1. `io_uring` 改进（更强大的异步 I/O 接口）

#### 🔧 背景：
`io_uring` 是近年来 Linux 最重要的异步 I/O 框架之一，用于替代传统的 `aio` 接口。

####  Linux 6.0 中的新功能：

- **IORING_REGISTER_FILES_UPDATE**: 动态更新已注册的文件描述符。
- **IORING_SETUP_SQPOLL_NONFIXED**: 允许在 SQPOLL 线程中使用非固定队列。
- **IORING_FEAT_FAST_POLL**: 支持更快的 poll 操作，减少唤醒延迟。
- **IORING_OP_MSG_RING**: 支持跨 io_uring 实例的消息传递。

#### 💡 使用场景：
- 高性能 Web 服务器
- 数据库引擎（如 MySQL、PostgreSQL）
- 存储系统（如 Redis、RocksDB）

#### 示例代码片段：

```c
#include <liburing.h>

struct io_uring ring;
io_uring_queue_init(32, &ring, 0);
```

---

###  2. `landlock` 安全机制（轻量级沙箱）

#### 🔧 背景：
Landlock 是一个基于 eBPF 的轻量级安全模块，允许应用程序限制自身对文件系统的访问权限。

####  Linux 6.0 中的新功能：

- 支持对进程自身的文件访问进行细粒度控制。
- 提供新的系统调用：`landlock_create_ruleset()`, `landlock_add_rule()`。

#### 💡 使用场景：
- 沙箱环境
- 安全容器
- 浏览器插件运行时保护

#### 示例代码片段：

```c
int ruleset_fd = landlock_create_ruleset(NULL, 0, LANDLOCK_CREATE_RULESET_VERSION);
if (ruleset_fd < 0) {
    perror("landlock_create_ruleset");
    return -1;
}
```

---

###  3. `pidfd` 增强（无竞争获取进程状态）

#### 🔧 背景：
传统上使用 `wait()` 或 `waitpid()` 获取子进程状态容易引发竞态条件，`pidfd` 提供了更现代的方式。

####  Linux 6.0 中的新功能：

- **`pidfd_getfd()`**: 允许父进程从子进程中“偷取”打开的文件描述符。
- 支持通过 `pidfd_open()` 创建的 fd 来监控子进程状态，避免信号处理复杂性。

#### 💡 使用场景：
- 安全容器运行时（如 LXC/LXD）
- 进程监控工具
- 服务守护程序

#### 示例代码片段：

```c
pid_t child = fork();
if (child == 0) {
    // 子进程
    execl("/bin/ls", "ls", NULL);
}

int pidfd = pidfd_open(child, 0);
if (pidfd < 0) {
    perror("pidfd_open");
    return -1;
}
```

---

###  4. `mount_setattr()`（安全挂载配置）

#### 🔧 背景：
传统的 `mount()` 接口存在灵活性和安全方面的不足。

####  Linux 6.0 中的新功能：

- 引入 `mount_setattr()` 系统调用，用于修改已有挂载点的属性。
- 可以设置只读、不可写、不可执行等属性。

#### 💡 使用场景：
- 容器运行时
- 文件系统安全加固
- 安全策略实施

#### 示例代码片段：

```c
struct mount_attr attr = {
    .attr_set = MOUNT_ATTR_RDONLY,
};
int ret = sys_mount_setattr(AT_FDCWD, "/mnt/myfs", 0, &attr, sizeof(attr));
```

> 注：需要使用 `syscall(SYS_mount_setattr, ...)` 或 glibc 未来支持。

---

###  5. `openat2()` 增强（安全路径解析）

#### 🔧 背景：
`openat2()` 是 `open()` 的扩展，提供更强的安全性和路径限制能力。

####  Linux 6.0 中的新功能：

- 支持 `RESOLVE_IN_ROOT` 标志，限制路径解析范围。
- 支持 `RESOLVE_NO_XDEV`，防止跨越挂载点。

#### 💡 使用场景：
- 安全沙箱
- 容器文件访问控制
- 路径隔离工具

#### 示例代码片段：

```c
struct open_how how = {
    .flags = O_RDONLY | O_CLOEXEC,
    .resolve = RESOLVE_IN_ROOT | RESOLVE_NO_MAGICLINKS,
};
int fd = syscall(SYS_openat2, AT_FDCWD, "/safe/path", &how, sizeof(how));
```

---

###  6. `bpf()` 系统调用增强（eBPF）

#### 🔧 背景：
eBPF（extended Berkeley Packet Filter）是 Linux 最具革命性的技术之一，广泛用于网络、安全、性能分析等领域。

####  Linux 6.0 中的新功能：

- 支持 BPF_MAP_TYPE_HASH_TABLE（更高效的哈希表结构）
- 增强 CO-RE（Compile Once – Run Everywhere）支持
- 新的 BPF helper 函数和 map 类型

#### 💡 使用场景：
- 网络包过滤
- 性能分析（perf）
- 安全审计（LSM）
- 内核旁路（XDP）

#### 示例代码片段（伪代码）：

```c
union bpf_attr attr = {0};
attr.map_type = BPF_MAP_TYPE_HASH;
attr.key_size = sizeof(int);
attr.value_size = sizeof(int);
attr.max_entries = 1024;

int fd = bpf(BPF_MAP_CREATE, &attr, sizeof(attr));
```

---

## 📘 Linux 6.0 系统编程相关头文件

| 头文件 | 描述 |
|--------|------|
| `<sys/syscall.h>` | 所有系统调用的定义 |
| `<linux/bpf.h>` | eBPF 相关定义 |
| `<linux/io_uring.h>` | io_uring 结构体定义 |
| `<sys/mount.h>` | mount_setattr 相关 |
| `<sys/landlock.h>` | Landlock 安全模块 |
| `<sys/fcntl.h>` | openat2 / pidfd 相关 |

---

## 🚀 推荐学习资源

| 名称 | 地址 |
|------|------|
| [Linux Kernel Newbies](https://kernelnewbies.org/Linux_6.0) | https://kernelnewbies.org/Linux_6.0 |
| [The io_uring Documentation](https://unixism.net/loti/) | https://unixism.net/loti/ |
| [Landlock Documentation](https://docs.kernel.org/security/landlock/index.html) | https://docs.kernel.org/security/landlock/index.html |
| [eBPF.io](https://ebpf.io/) | https://ebpf.io/ |
| [man7.org Linux man pages](https://man7.org/linux/man-pages/) | https://man7.org/linux/man-pages/ |

---

##  总结一句话

> Linux 6.0 在系统编程方面带来了多项重要更新，包括 `io_uring` 增强、`landlock` 安全机制、`mount_setattr`、`pidfd` 增强、`openat2` 改进以及 `eBPF` 功能扩展，非常适合用于构建高性能、安全、低延迟的 C/C++ 应用。

---

如果你希望我帮你：

-  构建完整的 `io_uring` 高性能服务器模板
-  编写基于 `landlock` 的沙箱程序
-  实现基于 `mount_setattr` 的容器安全策略
-  提供 CMake + Linux 内核兼容性检测脚本

## linux是如何支持新的硬件

## linux是如何支持新的磁盘文件系统

## 大带宽网卡，linux如何优化

`/etc/profile` 和 `/etc/bashrc` 是两个用于配置用户环境变量的脚本文件。它们在用户登录时被执行，以便设置一些全局的环境变量和函数。
1. `/etc/profile`：这个文件主要用于设置系统级别的环境变量，例如系统路径、环境变量等。当用户登录时，这个文件会被执行。
2. `/etc/bashrc`：这个文件主要用于设置 Bash shell 的个性化配置，例如别名、函数等。当用户登录时，这个文件会被执行。
这两个文件通常位于 `/etc` 目录下，可以通过文本编辑器（如 vi、nano 等）进行编辑。在编辑完成后，需要保存并退出编辑器，然后重新登录或运行 `source /etc/profile` 或 `source /etc/bashrc` 使更改生效。

## ubuntu

bionic ubuntu 18

[Unable to locate package while trying to install packages with APT](https://askubuntu.com/questions/378558/unable-to-locate-package-while-trying-to-install-packages-with-apt)

ubuntu 16查看libmysqlclient-dev包含的文件
https://packages.ubuntu.com/xenial/amd64/libmysqlclient-dev/filelist 

[Linux内核态与用户态区别](https://www.cnblogs.com/a-lai/articles/7293828.html)

##### Systemd 入门教程：命令篇
https://juejin.im/post/5a5119886fb9a01ca2675013 

apt get 原理

https://www.cnblogs.com/kex1n/p/5845782.html

### yum

yum install

List

### debian

get

### term android
