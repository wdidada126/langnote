# keepalived
Keepalived是一款用于实现高可用性（HA）和负载均衡的开源工具，核心功能包括健康检查、故障切换和VRRP协议支持。
虚拟ip
新建局域网
一旦局域网一台挂掉，可以动态添加

keepalive配置mysql自动故障转移
https://blog.csdn.net/u010391029/article/details/48470295

Keepalive+mysql主主同步
https://blog.csdn.net/hizamaru/article/details/88206068

利用keepalive+mysql replication 实现数据库的高可用

利用mysql自带的replication和keepalive提供的虚拟IP和故障检查来实现数据库的高可用
replication 就是主备
https://www.cnblogs.com/lengfo/p/4212910.html

本文主要记录了基于Linux环境下的Mysql Replication配置步骤。
https://dev.mysql.com/doc/refman/5.7/en/replication-solutions.html

## 官网
https://www.keepalived.org/

## 编程语言
c
## 协议

## 版本
v2.3.4 2025  Jun 11
2024-11-03 | Release 2.3.2
This release brings improvements and fix some issues reported. Refer to Release Notes for more infos.

2024-05-24 | Release 2.3.1
Minutes release to fix minor regression. Refer to Release Notes for more infos.

2024-05-21 | Release 2.3.0
This release brings improvements and fix some minor issues reported. Refer to Release Notes for more infos.

2023-05-31 | Release 2.2.8
This release brings improvements and fix some minor issues reported. It add some new VRRP and BFD features as well. Refer to Release Notes for more infos.

2022-01-16 | Release 2.2.7
This release brings lots of improvements and fix some minor issues reported. It add some new VRRP features as well. Stability has been even more extended. Refer to Release Notes for more infos.

2021-08-21 | Release 2.2.4
This release fix some minor build issues brought by last release. All coverity open issues are fixed. Refer to Release Notes for more infos.

2021-08-14 | Release 2.2.3
This release add some new features and fix some minor bugs. genhash utility is now part of the mainline daemon. Refer to Release Notes for more infos.

2021-03-05 | Release 2.2.2
This release fix some minor systemd integration issues. Its drops old kernel related support. Refer to Release Notes for more infos.

2021-01-17 | Release 2.2.1
This release fix some minor regressions brought by last release. Refer to Release Notes for more infos.

2021-01-09 | Release 2.2.0
This release bring a bunch of new features and extensions. This release targetted corner cases and resilient handling. This release is a major milestone for us ! please consider upgrading, this is the fruit of hard stabilization and non-regression effort. Refer to Release Notes for more infos.

2020-07-13 | Release 2.1.5
This is a minute fix release, fixing regression on include directive. Refer to Release Notes for more infos.

2020-07-10 | Release 2.1.4
This release extend some documentation elements. Some fix for the building process. DNS_CHECK fix and extensions. Properly handle ipvs_sync_daemon. Refer to Release Notes for more infos.

2020-06-23 | Release 2.1.3
This release fix 2 uninitialized list which can lead to a SEGV when using track_process or track_bfd. There are some minor fixes, IPVS configurations improvements and some cosmetics. Refer to Release Notes for more infos.

2020-06-14 | Release 2.1.2
This is a minute fix release. Refer to Release Notes for more infos.

2020-06-13 | Release 2.1.0
Lot of efforts have been put all together to make this new release even more robust. Refer to Release Notes for more infos.

2020-01-22 | Release 2.0.20
Fix track process and track script features. Some BFD extensions and cleanup. Reworked debug configuration. Snap updates. Docker updates. Add support to set pref lft for static and virtual IPv6 addresses. Refer to ChangeLog for more infos.

## 源代码编译
https://github.com/acassen/keepalived

这是一个典型的 头文件包含冲突 问题。错误的原因是系统同时包含了两个定义相同内容的头文件：

• /usr/include/netinet/in.h (GLIBC 的标准头文件)

• /usr/include/linux/in.h (Linux 内核头文件)

在编译 keepalived 时，这两个头文件都被包含了，导致重复定义错误。

解决方案

方案一：修改编译配置（推荐）

在 configure 步骤添加参数，避免包含冲突的头文件：
#!/bin/bash
set -e

echo "修复 keepalived 编译头文件冲突问题..."

cd /tmp/keepalived

# 清理之前的编译
make distclean 2>/dev/null || true

# 重新配置，添加避免冲突的参数
./configure \
    --prefix=/usr \
    --sysconfdir=/etc \
    --localstatedir=/var \
    --enable-snmp \
    --enable-sha1 \
    --with-systemdsystemunitdir=/lib/systemd/system \
    CPPFLAGS="-D_GNU_SOURCE -D__USE_GNU"

# 尝试编译
make -j$(nproc)
sudo make install

echo "编译完成！"


方案二：手动修复头文件包含顺序

创建一个补丁文件来修复包含问题：
#!/bin/bash

# 创建修复补丁
cat > /tmp/keepalived_fix.patch << 'EOF'
--- a/keepalived/include/ip_vs.h
+++ b/keepalived/include/ip_vs.h
@@ -15,7 +15,9 @@
 #ifndef _IP_VS_H
 #define _IP_VS_H
 
+#define _GNU_SOURCE
 #include <stdio.h>
+#include <netinet/in.h>
 #include <linux/netfilter.h>	/* for NF_IP_* and NF_INET_* */
 #include <linux/ip_vs.h>
 
EOF

# 应用补丁
cd /tmp/keepalived
patch -p1 < /tmp/keepalived_fix.patch


方案三：使用更完整的修复脚本

#!/bin/bash
set -e

echo "=========================================="
echo "修复 Keepalived 编译头文件冲突"
echo "=========================================="

# 检查当前目录
if [ ! -f "configure.ac" ]; then
    echo "错误：请在 keepalived 源码根目录运行此脚本"
    exit 1
fi

# 备份可能被修改的文件
BACKUP_DIR="./backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# 方法1: 修改核心头文件包含
echo "方法1: 修改头文件包含顺序..."

# 修复 ip_vs.h 包含问题
if [ -f "keepalived/include/ip_vs.h" ]; then
    cp "keepalived/include/ip_vs.h" "$BACKUP_DIR/ip_vs.h.bak"
    
    # 创建修复版本
    cat > /tmp/ip_vs_fixed.h << 'EOF'
#ifndef _IP_VS_H
#define _IP_VS_H

#define _GNU_SOURCE
#include <stdio.h>
#include <netinet/in.h>

/* 防止重复定义 */
#ifndef IPPROTO_UDPLITE
#include <linux/netfilter.h>
#include <linux/ip_vs.h>
#endif

/* 原有的其他内容保持不变 */
#ifdef _WITH_LVS_
#ifdef _WITH_SNMP_
extern int (*agentx_check_value)(char *buffer, int buffer_len);
extern int (*agentx_check_notify)(int version, const char *proto, 
                                 const char *vs, const char *rs, int weight);
#endif
#endif

#endif /* _IP_VS_H */
EOF
    
    cp /tmp/ip_vs_fixed.h "keepalived/include/ip_vs.h"
fi

# 方法2: 修改编译标志
echo "方法2: 设置编译环境变量..."

export CPPFLAGS="-D_GNU_SOURCE -D__USE_GNU -D_DEFAULT_SOURCE"
export CFLAGS="-O2 -g -Wno-error=redundant-decls"

# 方法3: 如果上述方法仍不行，尝试使用系统自带的keepalived头文件
echo "方法3: 检查系统IPVS头文件..."

# 安装系统IPVS头文件
sudo apt update
sudo apt install -y libipvs-dev

# 重新配置
echo "重新配置编译环境..."
make distclean 2>/dev/null || true

./configure \
    --prefix=/usr \
    --sysconfdir=/etc \
    --localstatedir=/var \
    --enable-snmp \
    --enable-sha1 \
    --with-systemdsystemunitdir=/lib/systemd/system \
    --disable-hardening

# 尝试编译
echo "开始编译..."
if make -j$(nproc); then
    echo "✓ 编译成功！"
    sudo make install
    echo "✓ 安装完成！"
else
    echo "编译失败，尝试替代方案..."
    
    # 方案4: 使用apt安装预编译版本
    echo "方案4: 使用系统包管理器安装..."
    sudo apt install -y keepalived
    
    if which keepalived > /dev/null; then
        echo "✓ 通过apt安装成功！"
        keepalived --version
    else
        echo "✗ 所有方案都失败了"
        exit 1
    fi
fi


方案四：最简单的解决方案 - 使用系统包安装

如果编译问题难以解决，Ubuntu 24.04 的仓库中已经有预编译的 keepalived：
#!/bin/bash
echo "使用系统包安装 keepalived..."
sudo apt update
sudo apt install -y keepalived

# 验证安装
if which keepalived > /dev/null; then
    echo "✓ keepalived 安装成功！"
    keepalived --version
else
    echo "✗ 安装失败"
fi


根本原因分析

这个问题的根本原因是：
1. 头文件包含顺序问题：linux/in.h 应该在 netinet/in.h 之后包含
2. 特性测试宏问题：需要正确定义 _GNU_SOURCE 等宏
3. 内核头文件与用户空间头文件冲突

推荐解决步骤

1. 首先尝试方案四（使用系统包安装），这是最简单的方法
2. 如果必须从源码编译，按顺序尝试方案一、二、三
3. 如果所有方案都失败，考虑使用 Ubuntu 22.04 或更早版本进行编译，然后移植到24.04

通常来说，对于生产环境，推荐使用系统包管理器安装，这样可以避免编译依赖和兼容性问题。
