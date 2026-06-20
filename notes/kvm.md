# kvm



 4、KVM：

​             kvm.ko（内核模块），只用于管理虚拟 CPU 和内存。IO 的虚拟化，就交给 Linux 内核和qemu来实现。


　　       **Libvirt：是 KVM 的管理工具**。Libvirt 除了能管理 KVM 这种 Hypervisor，还能管理 Xen，VirtualBox 等。**OpenStack 底层也使用 Libvirt**。


　　       Libvirt 包含 3 个东西：**后台 daemon 程序 libvirtd、API 库和命令行工具 virsh**


（1）libvirtd是服务程序，接收和处理 API 请求；


（2）API 库使得其他人可以开发基于 Libvirt 的高级工具，比如 virt-manager，这是个图形化的 KVM 管理工具，后面我们也会介绍；


（3）virsh 是我们经常要用的 KVM 命令行工具，后面会有使用的示例。作为 KVM 和 OpenStack 的实施人员，virsh 和 virt-manager 是一定要会用的。

 

## 三、虚拟化VT开启确认

KVM 本身也有一些弱点，那就是相比裸金属虚拟化架构的 Xen 、 VMware ESX 和 HyperV ， **KVM 是运行在 Linux 内核之上的寄居式虚拟化架构，会消耗比较多的计算资源**；不过针对这一点， Intel 、 AMD 已经在处理器设计上有专门的**VT-x 和 AMD-V 扩展**，这种特性在每次硬件更新的时候也会更新，往往每次更新后都对虚拟化性能和速度上有明显的提升，所以长远来看，也不是什么大问题。

KVM 的虚拟化需要硬件支持（需要处理器支持虚拟化：如 Intel 厂商的 Intel-VT （ **vmx** ）技术&&AMD 厂商的 AMD-V （ **svm** ）技术。**是基于硬件的完全虚拟化**。而 Xen 早期则是基于软件模拟的**半虚拟化（ Para-Virtualization** ），新版本则是基于硬件支持的完全虚拟化。但 **Xen 本身有自己的进程调度器，存储管理模块**等，所以代码较为庞大。



你当前的 CPU 是否支持 VT 技术？当不确定你当前 CPU 是否支持 VT 技术时

1. 可以在 windows 下使用 cpu-z 软件来进行测试
2. 可以在 Linux 下查看 CPU 的相信信息来确定



https://baijiahao.baidu.com/s?id=1612142653122584145&wfr=spider&for=pc