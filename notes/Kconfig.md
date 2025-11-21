# Kconfig

https://blog.csdn.net/u011425939/article/details/80472324

当执行#make menuconfig时会出现内核的配置界面，所有配置工具都是通过读取"arch/$(ARCH)Kconfig"文件来生成配置界面，这个文件就是所有配置的总入口，它会包含其他目录的Kconfig

java标准项目，配置文件多处

autoconfig配置
