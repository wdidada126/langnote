# asop note

当然有区别，拿国内手机厂商的开发来说：
别看大家都是在Google的AOSP上面改，差别还是非常大的
手机厂商一般不会直接使用Google的AOSP 代码，他们拿到的一般是高通或者联发科给过来的底包，这里面是包含高通或者联发科的代码的，通常高通和联发科会在Linux和Framework 做一些功能开发和优化
然后手机厂商拿到这些代码之后，一般会在下面几个点进行开发
硬件相关的开发。比如说某个手机引入了新的硬件，那么从底层驱动到 Framework 到上层 App都有可能涉及到修改，不管是交互逻辑还是代码逻辑，最显著的就是屏下指纹
Linux 相关技术的开发。Android 底层用的是 Linux ，什么文件系统，内存管理，调度器，哪一个都是需要投入人力做研发的，有很多基于移动设备的优化工作可以做
Framework 相关技术的开发。这一部分涉及到系统上层，起到承上启下的作用，上面与 Android App 打交道，下面与 Linux 和硬件打交道，本身的逻辑也十分复杂，所以可以开发和优化的地方也很多，就看公司的开发实力。另外也会对高通和联发科的一些功能做二次开发，以适应自己公司的策略、跨平台性、功能等；另外快省稳的一部分也在这里
APP 层开发。这里包含了系统应用和独立应用，包括系统界面、锁屏、通知中心、桌面、设置、商店这些，这些系统应用和独立应用构成了一个系统的界面美学，可以说是一个系统的功能和颜值担当
说到不同，上面四层里面，各家由于硬件、软件、功能、设计的不同，代码实现肯定说不一样的，比如说应用后台管理，各家的实现方案、管控颗粒度、管控力度、智能程度不尽相同，比较考验各家的技术实力
这样来看的话，整个 Android 系统的开发是非常庞大的一个工程，这就非常考验一个公司的研发实力，资源多的话，可以多点开花，资源少的话就集中到一个点，有的小公司一个人负责好几个模块，有的大公司十几个人负责一个模块，这就是实力（Money）的差距；再说了，资源不够，加班来凑，你看看排名前几的手机公司，那个不是已加班著称的……只能说压力大没办法，现在是红海，你死我亡

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