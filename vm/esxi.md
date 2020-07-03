# esxi



HW-->VMware ESXi-->OS1-------------------------------------------------------------->APP 

HW-------------------->OS1->VMware Workstation-->**OS2 Kernel + OS2 Bin/Lib**--->APP

HW-------------------->OS1->KVM-------------------->**OS2 Kernel + OS2 Bin/Lib**--->APP

HW-------------------->OS1->Docker------------------>**OS1 Kernel+ Image Bin/Lib-**>APP

VMware其实是有两种虚拟化产品，楼下好多人提到的都是VMware workstation，这个一般装在桌面系统，生产环境中可不是这个，而是VMware ESXi。

VMware ESXi，可是直接安装在硬件上的，其他虚拟化技术，VMware Workstation、KVM、Docker可不行，必须跑在操作系统上，不能跑在裸金属上。

后面三种虚拟化技术，从工作层面来讲，是一样的，都得先有OS，它们才能工作。不同的是，它们提供的服务。

Workstation和KVM提供的都是完整的操作系统，然后系统上跑APP。Docker提供的服务是调用系统的Kernel，然后Bin/Lib由运维人员定制，其上再跑APP。

