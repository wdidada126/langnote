# cpulimit

cpulimit -- limits the CPU usage of a process

你遇到的情况非常典型，说明 `cpulimit` 没有安装在你的 Linux 系统中。

我们来一步步解释：
###  为什么 `man cpulimit` 和 `cpulimit` 都找不到？

因为：

>  `cpulimit` 不是 Linux 系统默认自带的命令，它是一个第三方工具，需要手动安装。

所以：
- `man cpulimit`：没有安装，自然没有手册。
- `cpulimit: command not found`：命令不存在。

###  如何确认 `cpulimit` 是否存在？

```bash
which cpulimit
# 或
whereis cpulimit
```

如果输出为空，说明未安装。

###  如何安装 `cpulimit`？

#### 方法 1：使用包管理器安装（推荐）

##### Ubuntu / Debian
```bash
sudo apt update
sudo apt install cpulimit
```

##### CentOS / RHEL / Fedora
```bash
# CentOS 7/8 需要先启用 EPEL 仓库
sudo yum install epel-release
sudo yum install cpulimit

# 或 Fedora
sudo dnf install cpulimit
```

安装完成后，就可以用了：

```bash
cpulimit --help
man cpulimit  # 现在应该可以查看手册了
```

#### 方法 2：从源码编译安装（适用于无法联网的机器）

```bash
# 下载源码
wget https://github.com/opsengine/cpulimit/archive/master.zip
unzip master.zip
cd cpulimit-master

# 编译
make

# 安装到系统路径
sudo cp src/cpulimit /usr/local/bin/
```

> ⚠️ 注意：需要 `make` 和 `gcc` 环境。

###  `cpulimit` 基本用法

```bash
# 限制某个命令的 CPU 使用率不超过 50%
cpulimit -l 50 -- make -j8

# 限制一个正在运行的进程（PID=1234）不超过 30%
cpulimit -l 30 -p 1234

# 后台运行（不阻塞终端）
cpulimit -l 50 -- make -j8 &
```

###  替代方案（如果无法安装 `cpulimit`）

如果你不能安装 `cpulimit`，也可以用以下方式间接控制 CPU 占用：

#### 1. 使用 `nice` + 减少并行数
```bash
nice -n 10 make -j4  # 只用 4 个核心，而不是全部
```

#### 2. 使用 `taskset` 绑定到部分 CPU
```bash
# 只允许 make 使用 CPU 0 和 1
taskset -c 0,1 make -j2
```

#### 3. 使用 `systemd-run` 控制资源（高级）
```bash
systemd-run --scope -p CPUQuota=50% make -j$(nproc)
```
> 这会限制整个任务的 CPU 使用率不超过 50%。

###  总结
| 问题 | 原因 | 解决方案 |
|------|------|-----------|
| `man cpulimit` 找不到 | 未安装 | 安装 `cpulimit` 包 |
| `cpulimit: command not found` | 未安装 | `apt/yum install cpulimit` |
| 想限制编译 CPU 占用 | 编译太耗资源 | 用 `cpulimit` 或 `nice` + `-jN` |

###  面试加分点

如果你在面试中说：

> “我知道 `cpulimit` 不是系统自带的，需要通过 `apt install cpulimit` 安装。如果环境不允许安装，我可以用 `nice -n 10 make -j4` 来降低优先级和并行度，达到类似效果。”

这表明你不仅知道工具，还具备实际运维能力和备选方案思维，是非常加分的！

需要我写一个脚本自动判断是否安装 `cpulimit` 并降级使用 `nice`，也可以继续扩展。
