- Octotree

Code tree for GitHub

```shell

ABRT 已检测到 '1' 个问题。预了解详细信息请执行：abrt-cli list --since 1556155459
[root@localhost ~]# abrt-cli list --since 1556155459
id 90f62afa3de73624bc6a53f8ea9842c6addecdf0
reason:         WARNING: CPU: 1 PID: 0 at net/sched/sch_generic.c:356 dev_watchdog+0x248/0x260
time:           2019年04月25日 星期四 09时42分38秒
cmdline:        BOOT_IMAGE=/vmlinuz-3.10.0-957.5.1.el7.x86_64 root=/dev/mapper/centos-root ro crashkernel=auto rd.lvm.lv=centos/root rd.lvm.lv=centos/swap rhgb quiet LANG=zh_CN.UTF-8
package:        kernel
uid:            0 (root)
count:          1
Directory:      /var/spool/abrt/oops-2019-04-25-09:42:38-4927-0
已报告：    无法报告


已禁用自动报告功能。请考虑启用该功能，方法是
作为有 root 特权的用户使用命令 'abrt-auto-reporting enabled'

```







DAEMONToolsLite