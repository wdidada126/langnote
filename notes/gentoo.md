# gentoo



https://www.gentoo.org/

https://www.gentoo.org/get-involved/mailing-lists/

## code
https://github.com/gentoo/gentoo


支持 GURU（Gentoo 用户仓库）的 层叠 (Overlay) 仓库的概念，允许用户添加 Gentoo 尚未提供的软件包


layman已经无了

## Gentoo官方WIKI

https://wiki.gentoo.org/wiki/Main_Page


https://wiki.gentoo.org/wiki/Handbook:AMD64/Full/Installation/zh-cn


在Gentoo系统中，"Stage"包是指创建Gentoo系统的各个不同阶段。这些阶段包括Stage 1、Stage 2、Stage 3和Stage 4。以下是每个阶段的详解：

Stage 1：这是第一个阶段，通常是从源代码构建的系统包。每种系统配置文件在这个阶段都是独特的。Stage 1包含了构建系统所需的基本文件和工具，但不包括编译好的二进制文件。因此，使用Stage 1安装Gentoo需要用户自行编译大量的软件，包括系统内核和工具链。
Stage 2：Stage 2在Stage 1的基础上进行了编译，并包含了Stage 1的所有文件以及编译出来的二进制文件。这意味着Stage 2是一个自包含的包，它可以自己编译自己。使用Stage 2安装Gentoo可以节省一些编译时间，因为一些基本的工具链和库已经预先编译好了。
Stage 3：Stage 3包含了系统必备工具的集合，即要安装的系统基础组件（不包括内核和引导器）。它提供了运行基本系统所需的大部分软件，包括命令行工具、文件系统和网络配置工具等。使用Stage 3安装Gentoo可以进一步节省时间，因为大部分系统组件都已经预先编译和配置好了。
Stage 4：Stage 4在Stage 3的基础上增加了内核和系统引导器，因此它是一个可运行的包。Stage 4通常用于虚拟机或需要快速部署Gentoo系统的场景。使用Stage 4安装Gentoo可以最快地得到一个完整的、可运行的系统。
需要注意的是，选择使用哪个Stage包取决于用户的需求和偏好。对于希望从头开始构建系统并自定义每个组件的用户，可以选择使用Stage 1或Stage 2。而对于希望快速安装和配置Gentoo系统的用户，可以选择使用Stage 3或Stage 4。无论选择哪个阶段，都需要一定的技术知识和经验来进行安装和配置。


官网上只有Stage 3

## docker镜像
