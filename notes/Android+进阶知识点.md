# Android 进阶知识点

## 资深Android UI工程师（自定义控件方向，源码方向）

### 适合人群

#### 对于原生UI自定义控件想更深入了解

#### 对Google开发的Android系统架构想深入学习的

#### 企业追求原生性能上的体验的

### 企业级屏幕适配

### UI绘制流程及其原理

#### View的源码分析

#### View的布局

####  Android xml布局到屏幕绘制流程原理

### 事件传递机制深入源码层解析

####  事件传递机制从屏幕驱动到View层全解析（站在Google工程师角度-手写事件分发机制）

### 绘图及其高级特效

#### Paint画笔高级技能

##### Paint的方法使用技巧

##### 高级渲染

###### BitmapShader位图渲染

###### LinearGradient线性渲染

###### RadialGradient环形渲染

###### SweepGradient扫描渐变渲染

###### ComposeShader组合渲染

##### Xfermode

##### 滤镜效果

###### BlurMaskFilter滤镜

###### EmbossMaskFilter滤镜

##### 颜色通道过滤

###### ColorMatrixColorFilter 颜色矩阵过滤

###### LightingColorFilter曝光颜色过滤

###### PorterDuffColorFilter图层混合颜色过滤

##### Canvas画板高级技能

###### Canvas基础使用技巧

###### Canvas区域切割技巧

##### Canvas图层与状态方法使用技巧

###### 通过save和restore解决图层绘制技术

###### 离屏缓冲技术

###### PorterDuffColorFilter图层混合颜色过滤

##### 超强辅助英雄-Path工具类的使用

### 项目实战之自定义控件开发

#### Scroller详解及源码浅析

#### ViewDragHelper详解及源码浅析

#### 自定义View触摸工具类解析

##### ViewConfiguration基础参数工具类

##### VelocityTracker手势速率工具类

##### GestureDetector手势工具类

#### 大量自定义控件实践

##### 滑动选择价格区间标签控件

##### 热门标签--流式布局

##### 腾讯内部技术-QQ空间之打造个性化可拉伸头部控件

##### 个性化滑动指示器

##### Material Design---RecyclerView实现时光轴效果

### 高级动画特效

#### 属性动画源码完全解析

#### MaterialDesign动画

#### Reveal effect（揭露效果）

#### Activity转换效果

#### Curved motion（曲线运动）

#### Animate Vector Drawables（矢量动画）

#### GIF动画引擎框架

### Material Design设计思想与原理分析

#### NavigationView+DrawerLayout主流侧滑实现

#### Material Design控件详解及源码分析

##### Toolbar

##### CoordinatorLayout

#### 手写Material Design最核心控件CoordinatorLayout，了解Google为什么这样设计Material Design

### 手写RecyclerView(手写竖向回收池，支持千万级Item)

## Android底层开发工程师（音视频方向，图像识别方向，智能家居方向）

### 适合人群

#### 想往底层方向发展，突破native层瓶颈的

#### 想与同行拉开差距，保持核心技优势

#### 没有任何C基础编程语言

### 基础知识

#### 函数

#### linux内存布局原理

##### 指针（N级指针概念、指针数组、数组指针）

#### 结构体和共用体

#### so动态库设计与编译

### C++基础晋升

#### 命名空间、引用、C/C++混合编程、引用、函数扩展

#### 对象管理、类的构造和析构、友元函数与友元类、操作符重载

#### c++编译器对象管理模型分析、类的继承、多态、抽象类、函数模板、类模板，模板的继承

#### C++类型转换、C++ IO、异常处理

#### 序列式容器、堆栈容器、双向链表容器、关联式容器、对组、算法详解

### Linux系统编程

#### Linux系统管理、VIM使用、GCC GDB使用

#### Linux环境讲解（Android和Tomacat环境搭建，安全组策略）

#### 常用命令（ls,grep,find,vim,gcc,,time,netstat，ssh）

#### 用户和，户组管理，文件读写权限分配

#### 阿里云服务器配置详解，ssh远程连接登录

### MakeFile语法详解

#### 静态库与动态库原理与编译流程详解

#### MakeFile文件走读

#### 编译，链接，处理程序

#### Makefile语法规则

#### 预定义变量，预定义宏函数

#### Android.mk文件与so打包流程详解

### Shell语法详解

#### 变量的定义到使用

#### 语法（数组，管道，遍历，流程控制，条件判断，云算法）

#### 方法参数传递机制详解

#### shell脚本编写与执行编译ffmpeg库

### 详解及其AndroidStudio编译So原理

#### AndroidStudio2.3之后为什么集成Cmake语法来编译So过程详解

#### cmake与makefile区别详解

#### Cmake语法详解

##### 指令（meassage，ADD_DEFINITIONS，FILE，INCLUDE，OPTIONAL，FIND_FILE ，FIND_PATH，FIND_LIBRARY）

##### 常用Cmake变量与环境变量（CMAKE_BINARY_DIR PROJECT_BINARY_DIR _BINARY_DIR）

#### CmakeList.txt(语法配置，引入第三方静/动态库，引入额外的CMakeList.txt文件，编译模块划分)

#### CmakeLists.txt文件详解（add_library，find_library，target_link_libraries方法执行流程）

### 爱奇艺音视频实战

#### 手写shell脚本编译FFmpeg（gcc命令详解）

#### AndroidStudio搭建音视频开发环境（集成FFmpeg环境）

#### 音频解码、视频解码、音视频同步处理

#### 音视频编码原理详解

##### 视频编码

###### 为什么视频能够压缩

####### 空间冗余，编码冗余，视觉冗余，知识码冗余

#######  人类视觉系统HVS（视觉敏感详解）

####### YUV编码为什么能完胜RGB编码

###### H261,MEPG1,MPEG2,H263,MPEG4,H264主流编码格式详解

###### 关键帧，前后帧，非关键帧详解

###### 帧内预测，帧间预测与算法

###### H264视频格式文件走读（sps,pps）

###### NALU技术在视频编码中的应用

##### 音频

###### 音频编码格式详解（AAC,AC-3,MP3）

###### 通道数详解

###### 采样率与人生声原关系

##### X264开源解码库编译

##### Faac库的编译与继承

#### OpenSl ES对象生命周期详解及音频播放

#### 用ffmpeg手写电视台直播app（直播cctv，凤凰卫视）

### 一线互联网企业核心技术

#### 手写阿里云andfix热修复与Sophix原理分析（class字节码在虚拟机加载流程，探索起源之java方法调用底层分析）

#### java方法在Dalvik和Art虚拟机运行原理

#### 今日头条双进程实现原理（linux层socket实现进程拉起）

#### 利用系统源码打造gif图的播放

#### Bsdiff实现实时更新（服务端linux生成patch）

### Opencv详解与应用

#### opencv原理详解，结构体 颜色通道使用

#### AndroidStudio cmake配置OpenCV开发环境

#### OpenCV打造人脸识别

#### Opencv打造实时换脸，美女与野兽的新定义

#### 利用opencv和OCR打造身份证识别，让你的手机变成公安局

#### OpenCV人工智能应用揭秘——车牌号码检测与识别

#### 人工智能神经网络在分类器中的运用——android 与人工智能

### 手写斗鱼视频直播

#### 斗鱼直播解决方案（nginx流媒体服务器部署）

#### 音视频采集与编码（faac编译到音频推流）

#### 视频编码与根据pts和系统计时实现音频同步（X264混合编译和h264编码原理）

#### 生产者与消费者实在推流中应用

### 仿写抖音小视频实战课程

#### opencv人脸跟踪与定位

#### 人脸磨皮算法与美白

#### 用ARToolkit打造立体甩狗脸趣味功能（增强现实技术）

#### 识别嘴型以及变换与放大（图形变化与持续跟踪）

#### 视频与音频合成原理分析以及手写实现

### 美白篇之美颜相机

#### 人脸动态贴纸 (opengl FBO与PBO、着色器GLSL语言、OpenCv人脸定位)

#### 大眼瘦脸(图像局部缩放、平移，人脸关键点检测)

#### 优酷核心技术opengl 打造高性能播放器

### qq音视频通话核心技术

#### 腾讯QQ视频通话核心技术-WebRTC

#### webrtc实现点对点通信原理

#### 实现内网之间直接通信的穿透原理与机制

#### 手写QQ视频通话-打造无延时高质量的p2p通话以及多人视频会议

#### QQ语音变声-让你秒变成萌妹大汉大叔叔

### 服务器搭建与开发实战

#### Tomacat服务器搭建与Servlet接口编写

#### 阿里云之Nignx直播服务器搭建

#### Webrtc之房间服务器搭建与原理

#### Webrtc之信令服务器

#### Webrtc之ICE服务器部署配置

### 智能家居实战讲解

#### 串口概念与波特率

#### 定制平板与底层通信控制

#### 协议制定与分发

#### 利用http版本协议打造高可靠的底层通信协议（有效帧，无效帧，主动丢帧，关键帧还原）

## Android资深架构师（一线互联网核心架构设计方向，framework方向）

### 架构师成长第一站-UML建模

#### 正向工程与逆向工程在UML图中的应用

#### 图的详解（用例图，类图,序列图,状态图,活动图,组件图,流程图）

#### 关系（依赖、泛化 、关联 、实现 ）画法与注意事项

#### 代码的结构实现图形化展示（架构初探）

#### AOP面向切面架构设计

#### OOC,AOP设计思想由来，Aspect、Joint point、Pointcut、Advice、用户行为统计场景、性能监控场景及其应用，Aspect源码分析

#### 面向切面思想之用户权限的架构设计

### 适合人群

#### 成为Android架构师

#### 想努力提高就业薪资

#### 有java基础

### 架构师成长第二站-无死角分析Android系统源码

#### Android Handler源码分析及其手写Handler架构

#### Message链表原理与重用机制

#### Binder核心原理与架构设计

#### PackageManagerService源码解析及其apk安装原理

#### ActivityManagerService架构设计和揭秘Activity夸进程跳转

#### App启动流程源码全解析及Android App应用本质揭秘

### Android事件总线框架设计（手写可跨进程的EventBus架构）

#### EventBus3.0源码详解与架构分析

#### 手写实现EventBus3.0事件总线框架（跨线程调用）

#### 手写饿了么进程通信框架Hermes（单例跨进程调用）

#### fastjson打造对象在多进程共享桥梁（一个aidl文件解决所有进程通讯需求）

#### 进阶之路--手写Hermes与EventBus完美结合框架(适合插件，多app通信)

### 网易云换肤核心技术

#### QQ,美团，网易云 动态式换肤架构分析

#### 手写网易云可动态替换的换肤框架(字体，状态栏换肤，自定义控件，fragment换肤)

#### 项目实战之高可扩展性换肤应用(多种动态皮肤之加载与切换)

#### 高德地图，今日头条 编译式换肤详解

### 组件化框架设计

#### 组件化之集中式路由--手写阿里巴巴ARouter原理（无Intent式）

#### Android项目组件化配置

#### 手写ARouter 组件化路（应用AbstractProcessor编译时技术实现,Path与Activity编译时映射）

#### 终结篇--项目实战手写组件化式路由（重定向，跳转前预处理--登录，统一跳转入口，支持多类型参数传递，多Moudle跳转）

### 插件化框架设计（插桩式）

#### 大众点评核心技术揭秘-AndroidDynamicLoader架构分析

#### 支付宝是如何集成共享单车功能于一身的占坑式插件解决方案

#### Activity,Service ,四大组件无缝插桩。生命周期标准制定与接入

#### 宿主和插件之间组件的通信，以及宿主和插件的调用

#### 插件内页面之间Activity自由跳转（无注册式）

### 插件化框架设计（Hook式）

#### 手写360 DroidPlugin式插件化架构

##### Activity启动流程原理详解 及hook点寻找

##### 插件架构如何设计才能实现类似于Android系统稳定性

#####   Activity四大启动模式预注册规则

##### 手写PMS服务实现插件包管理

##### hook AMS服务实现大型登陆架构

##### 广播插件的两种实现模式和apk安装原理

#####    Android系统在启动时加载App中so流程分析

#####  手写微型android系统 打造宿主管理插件系统架构（手写AMS，PMS服务）

##### 手写360式插件架构--支持在不安装商业应用内直接跳转

### 插件化升级之路

#### APK运行机制原理详解（伪造虚拟AMS，PMS，欺骗系统加载分身）

#### 手写微信多开项目（通过aidl打造系统运行沙箱环境）

### 数据库框架设计

#### 开源技术之ORMLite核心架构分析

#### 华为核心技术-面向对象式手写数据库架构设计（增删改查，自动建表设计）

#### 大型项目之实现数据库分库（多用户，多角色，多权限数据库架构设计）

#### xml脚本打造数据库版本全量升级架构（xml脚本结构定义，支持数据库单独升级）

### 手写OKHttp网络访问框架设计

#### 网络层七层模型及其原理（TCP IP握手）

#### OkHttp源码分析与架构解密

#### Http格式分析

#### 手写OkHttp任务队列架构设计

#### Socket连接池复用机制详解

#### 拦截器责任链模式实现重连，补全Http头，链接与Http协议解析等

#### 使用泛型完成手写高扩展的OKHttp网络访问框架设计(支持高并发，请求队列)

### 手写Glide加载框架设计

#### Glide架构思维分析与源码详解

#### 手写Glide图片加载框架

#### 手写Glide注入内部生命周期(打造不一样的缓存方式)

#### 建造者模式打造手写Glide架构的高扩展性

#### 请求队列、请求转发、加载器、加载策略、缓存策略详解

#### LruCache和DiskLruCache解析

#### 完结篇--手写Glide图片加载框架设计

### RXJava2响应式编程框架设计

#### Rxjava2架构分析与源码详解

#### 高阶泛型详解 和泛型变换应用

#### 手写RxJava响应式架构(链式调度，事件变换，线程切换)

#### 深入递归式实现Rxjava订阅链（观察者模式变种）

### IOC框架设计

#### 运行时

##### XUtils3.0源码详解

##### 手写Xutils核心模块IOC注入式框架设计

##### 注解的注解解决事件三要素（扩展Android20种事件注入）

##### 静态代理和动态代理模式详解与应用

##### 完结篇--手写Xutil动态注入架构（注入布局、视图、事件）

#### 编译时

##### ButterKnife详解与原理分析

##### Java文件结构化文本详解（TypeElement,VariableElement,ExecuteableElement,ExecuteableElement）

##### 手写ButterKnife架构实现无性能损耗的编译时框架

#### Dagger2核心原理分析

##### APT实现手写Dagger注入式框架

##### 注解实现依赖注入（让你的类依赖 变得更简单）

##### 手写Component 完成被依赖对象到依赖者的绑定

### 架构师必备技能

#### 面向对象思想构建万能interface

#### 阿里巴巴FastJSON原理分析与手写实现

#### 手写Android全版本编译时权限申请框架（含8.0 动态申请）

#### 动态代理打造高可替换的网络库隔离

### 设计模式

#### MVC架构设计与经典的三层模型详解

#### MVP思想精髓与解耦View与Mode的巧妙设计详解

#### 架构提升之路 MVP思想实现项目基础框架搭建

#### 更节省的设计模式之MVVM实现数据双向绑定

#### DataBinding原理和编译时绑定布局与对象

### 架构篇之项目实战

#### 项目基础框架搭建

#### 基类与业务逻辑详解

#### 主流架构集成与解耦

#### 项目实战之注入式模块集成

#### 项目实战之网络请求，图片加载，内存集中式管理，路由跳转

#### 打造以MVP,Rxjava,OkHttp,EventBus,Dragger2,greenDao项目

## 原生性能优化与混合式优化实战

### 内存泄露分析

#### 发生OOM的条件分析

#### 避免内存泄漏

#### 如何使用更高效的ArrayMap容器

#### 如何避免不经意的“自动装箱”

#### 优化工具的使用

##### Lint

##### StictMode

##### MAT

##### LeakCanary

##### Memory Monitor

##### TraceView

##### hierarchyviewer布局检测工具

#### 内存管理机制

##### 共享内存

##### 分配与回收内存

##### 限制应用的内存

##### OOM（查看内存使用情况）

##### onLowMemory与onTrimMemory的回调

#### 安装包性能优化

##### 打包流程分析

##### aapt资源文件打包原理

##### resources_arsc二进制机构分析

##### 资源文件压缩

##### 资源动态加载

##### Lint工具优化

##### 极限压缩、

##### Proguard混淆

##### Dex加密与反编译（app加固）

##### Gradle插件自动化减少apk文件大小

#### 数据传输的效率优化

#####  ProtolBuffer提升数据传输效率

#### 隐形内存杀手Service的调优

#### 如何优化后台服务的内存消耗

##### 如何保障服务的常驻内存

##### 双进程守护

#### 多线程并发的性能问题

##### AsyncTask源码级分析及注意

##### HandlerThread的处理

##### IntentService使用场景分析和实践

##### 线程间通讯

#### 混合式优化

##### 帧率详解及其卡段分析 UI线程掉帧与内存避免（reactnative）

#### 避免render方法过渡重绘

#### ScrollView内存优化实战（可见与不可见终极解决方案）

#### 分析程序启动流程、优化启动流程和提速

## 混合式开发工程师

### Weex篇

#### ES6语法详解

#### Promise是抽象异步处理对象以及对其进行各种操作

#### vue与Weex的前生今世

#### weex环境搭建与开发部署（window，mac）

##### 常用组件

###### Text

###### image

###### video

###### 列表web

#### Weex常用命令与热更新实战

#### Weex与android交互原理

#### 模块详解

##### storage存储模块

##### navigator引导模块

##### webview页面模块

#### 使用 Vuex 和 vue-router实现页面管理

##### 跳转

##### 回退

##### 历史记录

### 适合人群

#### 想成为全栈工程师

#### 往混合式方向发展（企业正在用到混合式编程）

#### 希望成为全栈工程师

#### 没有任何前端基础，和js基础

### ReactNaitve篇

#### JSX语法详解

#### 环境搭建

##### Window

##### Mac

#### 调试与打包发布（Android,IOS）

#### 常用组件

##### View

##### Text

##### TextInput

##### Image

##### Picker

#### 组件通信在浏览器中原理揭秘

#### Android原生控件与React组件区别，与转换原理

#### flexbox布局模型深入与探究

#### React 数据流和State的传递

#### ReactNative 中的MVVM模型与Android思想的应用于区别

#### ReactJs组件生命周期详解

##### 热更新原理及其热部署（Android）

#### ReactJs的组件与原生通信原理

### 美团电商实战，用ReactNative打造美团app

#### 打造美团首页头部Banner

#### ListView实现多布局展示页面

#### Item样式和类型的扩展

#### 美团购物中心结构搭建

#### 美团订单详情页面
