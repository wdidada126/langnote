# asop note

源码学习 android os source code 
打印日志，集中看某一个模块


高通 soc厂商提供Android源码

图形 opengl
vulkan
skia

多媒体

android kernel被从Linux Kernel中移除了，现在又恢复了

bionic

静态链接

termus

apt下载适用于Android平台的库

 Vulkan是一个跨平台的2D和3D绘图应用程序接口（API），最早由科纳斯(Khronos)组织在2015年游戏开发者大会（GDC）上发表。旨在替代OpenGL，提高图形性能。 

https://www.khronos.org/registry/vulkan/specs/1.0/refguide/Vulkan-1.0-web.pdf

Android 图像渲染有两种方式一是 CPU 渲染, 另一种是 GPU 渲染

## 一) CPU 渲染

**CPU 渲染称之为软件绘制**, Android CPU 渲染引擎框架为 **[Skia](https://skia.org/)**, 它是一款在底端设备上呈现高质量的 2D 跨平台图形框架, Google 的 Chrome、Flutter 内部都有使用这个图形渲染框架

## 二) GPU 渲染

**GPU 渲染称之为硬件绘制(即开启硬件加速)**

### 1. OpenGL

市面上最常用于图形渲染的引擎莫过于 [OpenGL](https://developer.android.com/guide/topics/graphics/opengl) 了, Android 系统架构中的外部链接库中有 OpenGL ES 的依赖, 并且提供了应用层的 API, 用于做高性能的 2D/3D 图形渲染

- Skia: 2D 图像绘制, 关闭硬件加速时使用该引擎
- OpenGL: 2D/3D 图像绘制, 开启硬件加速时使用该引擎

   Skia has a Vulkan implementation of its GPU backend. The Vulkan backend can be built alongside the OpenGL backend. The client can select between the OpenGL and Vulkan implementation at runtime. The Vulkan backend has reached feature parity with the OpenGL backend. At this time we find that many Vulkan drivers have bugs that Skia triggers for which we have no workaround. We are reporting bugs to vendors as we find them. 