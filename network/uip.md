# uip

uip这个库一千多行，有资料可参考有代码可借鉴的情况下确实不难。

UIP由瑞典计算机科学学院(网络嵌入式系统小组)的Adam Dunkels开发.
.良好的文档和源代码注释 - 几乎每一行代码都有注释.
.代码非常少.
.占用非常少的内存, 在编译时候可以设置.
.支持ARP, SLIP, IP, UDP, ICMP(ping)和TCP协议.
.提供一套实例程序: web服务器, web客户端, 电子邮件发送程序(SMTP客户端), Telnet服务器, DNS主机名解析程序.
.同时活动的TCP链接数没有限制, 在编译时候可以设置.
.可免费用于商业和非商业用途.
.TCP和IP协议遵循RFC标准, 包括流控制, 片断分割和重传超时估算.

UIP计算机网络库的源代码托管地址是：https://github.com/adamdunkels/uip

http://www.sics.se/~adam/uip/

uIP is a very small implementation of the TCP/IP stack that is written
by Adam Dunkels <adam@sics.se>. More information can be obtained 
at the uIP homepage at http://www.sics.se/~adam/uip/.

This is version $Name: uip-1-0 $.

The directory structure look as follows:

apps/  - Example applications
doc/   - Documentation
lib/   - Library code used by some applications
uip/   - uIP TCP/IP stack code
unix/  - uIP as a user space process under FreeBSD or Linux


## 编译
git clone https://github.com/adamdunkels/uip
cd uip/unix
make
sudo make install

## 竞品
lwip
LIP（Lightweight Interlayer Protocol）

先把结论说清楚：

- **uIP、lwIP：都是「轻量级 TCP/IP 协议栈」，解决的是同一类问题（嵌入式跑 IP/TCP/UDP）**
- **LIP（Lightweight Interlayer Protocol）：不是 TCP/IP 协议栈，而是一个「中间层安全协议」**，放在 L2～L3 之间做认证防护，和 uIP/lwIP 不在同一赛道

下面分块讲清楚联系、区别、选型。

---

## 一、uIP vs lwIP：同源、同用途、不同量级

### 1. 共同点（联系）
- 同一作者：**Adam Dunkels**（瑞典计算机科学院）
- 都是**开源、轻量级 TCP/IP 协议栈**，面向**无操作系统 / RTOS 的嵌入式设备**
- 都实现：IP、ICMP、UDP、TCP（基础版）
- 都用 C 写，可移植到 8/16/32 位 MCU

### 2. 核心区别（一张表）

| 对比项 | uIP（micro IP） | lwIP（Lightweight IP） |
|---|---|---|
| **定位** | **极致精简**：面向 8/16 位、KB 级 RAM | **轻量全功能**：面向 32 位、几十 KB RAM |
| **代码体积** | ~**10–20 KB** | ~**60–100 KB** |
| **RAM 占用** | **几百字节～几 KB** | **40–60 KB** |
| **TCP 连接** | **单连接**（同一时间只能 1 个 TCP） | **多连接**（默认 16–32 个） |
| **协议完整度** | 极简：无滑动窗口、无拥塞控制、无多连接 | 较完整：滑动窗口、拥塞控制、IPv6、多线程 API |
| **API 风格** | 事件驱动、回调式（raw API） | raw / netconn / socket 三种接口 |
| **典型场景** | 8051、STM32F103 小 RAM、传感器、简单 Web Server | STM32F4/F7、RTOS（FreeRTOS）、复杂物联网设备 |

简单记：
- **uIP = 能用就行，极致省资源**
- **lwIP = 够用且好用，功能更全、更稳定**

---

## 二、LIP（Lightweight Interlayer Protocol）是什么？

### 1. 基本定义
- 全称：**Lightweight Interlayer Protocol**（轻量级中间层协议）
- 发表：2007 年，移动自组网（MANET）安全领域
- **定位：不是 TCP/IP 协议栈，而是一个「L2～L3 之间的安全中间件」**

### 2. 作用
- 解决：**移动自组网中的「数据包注入攻击」**（恶意节点伪造包耗尽资源）
- 核心：**逐跳认证（hop-by-hop authentication）**，节点只认证直连邻居的包
- 位置：在 **MAC（L2）与 IP（L3）之间**，透明于上层路由协议，可随时开关

### 3. 和 uIP/lwIP 的关系
- **无直接竞争关系**：
  - uIP/lwIP：做「**TCP/IP 通信功能**」（能不能联网）
  - LIP：做「**网络安全防护**」（联网后防不防攻击）
- **可以叠加使用**：  
  嵌入式设备用 **lwIP/uIP + LIP**，既实现 TCP/IP，又防注入攻击。

---

## 三、一句话总结三者关系
- **uIP、lwIP：亲兄弟，都是 TCP/IP 协议栈，uIP 极简，lwIP 更强**。
- **LIP：远房亲戚，不是协议栈，是给网络加安全锁的中间层**。

---

## 四、选型建议（你实际开发时怎么选）
1. **8 位 MCU / RAM < 10 KB / 单连接** → 选 **uIP**
2. **32 位 MCU / RAM > 20 KB / 多连接 / RTOS** → 选 **lwIP**（工业界主流）
3. **移动自组网、无线传感器网络、需要防注入攻击** → 叠加 **LIP**

---

如果你是要做「嵌入式 TCP/IP 协议栈选型」，我可以帮你整理一份**uIP/lwIP 移植要点 + 常见坑清单**，直接照着就能用。需要吗？