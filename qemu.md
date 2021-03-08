# qemu



模拟器

不是虚拟机


AIX系统只支持IBM的power cpu，一般的的虚拟机软件（如VMware，VirtualBox）只技术X86架构，无法完成安装。因为QEMU的全仿真的特点，可以模拟出power cpu，以实现系统安装。

安装AIX 系统
创建一个空的4GB qcow2磁盘映像文件，把aix系统iso也存放在同一目录下面

 qemu-img create -f qcow2 hdisk0.qcow2 20G

此命令将创建具有指定设置的AIX VM，并从光驱动启动它

qemu-system-ppc64 -cpu POWER8 -machine pseries -m 4096 -serial stdio -drive file=hdisk0.qcow2,if=none,id=drive-virtio-disk0 -device virtio-scsi-pci,id=scsi -device scsi-hd,drive=drive-virtio-disk0 -cdrom AIX_7.2.4.0.iso -prom-env "boot-command=boot cdrom:"


https://www.cnblogs.com/xueyixue/p/13750847.html

