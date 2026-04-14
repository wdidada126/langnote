# df

df -h --output=source,fstype,size,avail
Filesystem     Type      Size Avail
/dev/sda2      ext4       11G  5.5G
udev           devtmpfs   10M   10M
tmpfs          tmpfs     112M  100M
tmpfs          tmpfs     280M  280M
tmpfs          tmpfs     5.0M  5.0M
tmpfs          tmpfs     280M  280M
/dev/sda1      ext3      359M  311M

df      # 原始单位（块）
df -h   # 人类可读格式（G/M），最常用
df -i   # 查看 inode 使用情况
df -T   # 显示文件系统类型

# df 与 du 的区别和联系
## 核心区别
- df：disk free
  查看文件系统（分区）的空间使用情况，统计的是整个分区的已用、剩余、总容量。
- du：disk usage
  统计目录 / 文件实际占用的空间大小，是对文件逐个累加计算的。

## 详细对比
1. 统计对象不同
   - df：面向分区、磁盘
   - du：面向目录、单个文件

2. 数据来源不同
   - df：直接读取文件系统超级块信息，速度极快
   - du：遍历目录树，逐个文件统计，速度较慢

3. 数值可能不一致
   常见现象：du 统计总和 < df 显示的已用空间
   原因：
   - 已删除但进程仍占用的文件，du 看不见，df 仍算占用
   - 文件系统日志、保留块、硬链接重复计数等

4. 使用场景
   - df：想知道硬盘还剩多少空间、哪个分区满了
   - du：想知道哪个文件夹 / 文件最大、占了多少空间

## 联系
- 都是查看磁盘空间相关的系统命令
- 配合使用：
  1. df 发现分区满了
  2. du 逐层查找大文件
  3. 删除后再用 df 确认空间释放
  