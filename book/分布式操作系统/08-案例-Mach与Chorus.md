# 第 8、9 章 实例研究 2、3：Mach 与 Chorus（08-案例-Mach与Chorus）

> **覆盖原书第 8 章**（实例研究 2：Mach）与**第 9 章**（实例研究 3：Chorus），并在结尾附带原书第 10 章（DCE）的定位说明。

## 本章地图

| 部分 | 内容 | 一句话结论 |
| --- | --- | --- |
| Mach 1 背景与设计目标 | CMU，1985 起；兼容 Unix 的微内核研究 | 「在 Mach 之上重建 Unix」，兼容优先 |
| Mach 2 核心抽象 | 任务（task）、线程（thread）、端口（port）、消息（message）、内存对象 | 四个抽象至今活在 macOS 内核里 |
| Mach 3 通信 | 端口队列 + 消息发送/接收；out-of-line 大数据 | 拷贝语义 → 虚拟内存技巧优化 |
| Mach 4 存储 | 外部存储管理器（external pager）：内存对象与分页解耦 | 分页策略交给用户态，影响深远 |
| Mach 5 线程模型 | Cthreads/C-Threads 包；迁移线程（migrating threads）设想 | 迁移线程是 RPC 优化的极端形态 |
| Chorus | 法国 INRIA → Chorus Systèmes；Nucleus（监督者）+ 系统进程 | 可嵌入、可裁剪，最终卖给了 Sun |
| DCE（附带） | OSF/DCE：RPC + 线程 + 目录 + 分布式文件服务 | 中间件路线对 OS 路线的胜利标志 |

## 核心精讲

### 1 Mach 的四个抽象（原书第 8 章主线）
- **任务**：资源容器（地址空间、端口权限）——相当于传统「进程」的静态一半。
- **线程**：执行单元，任务内可有多个——动态一半。任务 + 线程 = 进程。
- **端口**：**受内核保护的通信通道**，消息队列；对端口的持有权即发送/接收权限——
  「权能」思想（[04-命名.md](04-命名.md)、[07-案例-Amoeba.md](07-案例-Amoeba.md)）在 Mach 的形态。
- **消息**：带类型的字节块，可内含端口权能与内存对象的 OOL（out-of-line）数据。

四个抽象的组合规则值得单独记录（理解 XNU/各种「Mach 概念」文章的钥匙）：

- 端口是**单接收者、多发送者**的队列：接收权（receive right）同一时刻只有一个持有者，
  发送权（send right）可以任意分发——「谁能收」是稀缺资源，天然构成安全边界。
- 任务不执行、线程不持有资源：所有 IPC 都经端口，线程只是「跑在任务地址空间里的执行流」。
- 内核自己的服务（比如通知、异常处理）也走端口——**异常就是消息**（发到异常端口），
  调试器 attach 进程的本质是拿到该端口的接收权。这一设计在 macOS 上活到今天。

### 2 Mach 的消息与虚拟内存魔法
小消息走端口队列拷贝；大块数据用 **copy-on-write 映射**传递：发送方把页面映射进
接收方地址空间，谁先写谁付拷贝成本——把「通信」变成「内存管理」问题是 Mach 最聪明的一笔。
单机对照见 `book/Linux内核完全剖析/13-内存管理.md`（0.11 的写保护异常处理）。

### 3 外部存储管理器（external pager）
传统内核把「分页」焊死在内核里；Mach 把内存对象（memory object）的后备存储交给
**用户态 pager**：缺页时内核向 pager 发消息要数据。收益是策略可插拔（网络内存、数据库
自己管页）；代价是每次缺页一次 IPC——性能争论直接催生了 L4 一代微内核。

### 4 迁移线程（migrating threads）
原书介绍了 Mach 实验中的线程迁移设想：RPC 期间**调用者的线程直接跑到被调端执行**，
省去消息队列往返。它是「让 IPC 快到不像 IPC」的极端方案；L4 的 recursive RPC 与
后来「将函数执行搬到数据端」的 Serverless 思想（[09-从分布式OS到现代云OS.md](09-从分布式OS到现代云OS.md)）
都能看到它的影子。

### 5 Chorus：为嵌入式而生的微内核
- **Nucleus（监督者）**：极小内核，含调度、IPC、内存管理底层。
- **系统进程（supervisor actors / system processes）**：驱动、文件系统、网络栈都是
  不同特权级的 actor；实模式（安全）与用户模式（灵活）的 actor 混合部署。
- **卖点**：可裁剪可嵌入、UNIX System V 兼容层（Chorus/MiX）。
  商业上并入 Sun（后随 Sun 消逝），技术遗产流向嵌入式与电信实时系统。

Chorus 的 **actor 模型**（不是 Erlang 的 actor，但神似）有三个属性值得对照记忆：

| 属性 | 说明 | 对照 |
| --- | --- | --- |
| 地址空间隔离 | 每.actor 独立地址空间 | Mach 的任务 |
| 消息通信 | 无共享内存，全走 Nucleus IPC | Mach 端口消息 |
| 特权级可选 | 同一 actor 可在管态或用户态构建 | Chorus 独有：性能与安全按需切换 |

第三个属性是 Chorus 对「微内核太慢」的早期回应——把关键服务推进内核态，
本质上放弃了纯微内核的纯度。这个折中在 2026 年的辩论（unikernel、
libOS、unikraft 一类「把服务库进应用」路线）里以新名字继续。

```c
/* 教学示意，不参与构建：Mach 风格的消息发送（概念版，API 细节以 Mach 手册为准）。 */

typedef struct {
    mach_msg_header_t head;      /* 消息头：目标端口、大小、位 */
    int               payload;   /* in-line 数据 */
} msg_t;

mach_msg(&m.head,                       /* 消息 */
         MACH_SEND_MSG | MACH_RCV_MSG,  /* 一次调用同时发送并接收 */
         sizeof(m), sizeof(m), recv_port,
         MACH_MSG_TIMEOUT_NONE, MACH_PORT_NULL);
/* mach_msg 是 Mach IPC 的原点：端口即队列，发送/接收是同一原语的两个方向。 */
```

### 6 DCE 为什么放在这章末尾（原书第 10 章定位）
DCE（OSF）把线程、RPC、目录服务、DFS 做成**跑在现有 OS 之上的中间件包**——
它不接管内核，却提供了分布式 OS 的全部服务。原书把 Amoeba/Mach/Chorus/DCE 并列，
本身就是结尾伏笔：DCE 的路线（内核之上做分布式）赢了，微内核 OS 原型退守
（[09](09-从分布式OS到现代云OS.md)）。

DCE 的组件清单本身就是一张 1995 年的「分布式 OS 服务面」截图：

| DCE 组件 | 提供什么 | 2026 年对应 |
| --- | --- | --- |
| DCE Threads | POSIX 风格线程库 | 语言 runtime 线程/协程 |
| DCE RPC | IDL + NDR 编码 + 目录绑定 | gRPC |
| CDS（单元目录） | 名字→绑定信息 | CoreDNS/Consul |
| 安全服务（Kerberos 系） | 认证与授权 | mTLS + SPIFFE/RBAC |
| DFS（分布式文件服务） | 跨机文件 | 云存储/分布式 FS |

## 版本演进

| 时期 | Mach / Chorus 的命运 | 关键事件 |
| --- | --- | --- |
| 1985–1991 | CMU Mach 1.0–2.5；Chorus V3 | 微内核研究黄金期 |
| 1991–1994 | Mach 3.0 纯微内核化；GNU Hurd 选定 Mach | 性能问题暴露（「微内核比单体内核慢一截」） |
| 1995–2000 | **Apple 取 Mach + BSD 合成 XNU**（macOS 内核）；Liedtke 提出 L4 | 微内核从研究转向商业（桌面）与再研究（L4 验证） |
| 2000–2015 | Hurd 难产；Chorus 归档 | Linux 宏内核全面胜出 |
| 2015–2026 | seL4（形式化验证，`seL4/seL4` 5766★）、QNX（车载）、Fuchsia（`star 未核验`） | 微内核在安全关键与可验证场景成为刚需 |

**一条最值得记住的支线：Mach 是怎么「赢」成 macOS 内核的。**

| 阶段 | 事件 | 对本章的意义 |
| --- | --- | --- |
| 1989 | NeXTSTEP 选 Mach（Mach 2.5 + BSD 4.3 单内核化运行） | 微内核以「混合内核」形态首次商品化 |
| 1997 | Apple 收 NeXT，macOS 内核定为 XNU（Mach + BSD + IOKit） | 原书第 8 章的抽象直接进入消费级设备 |
| 2007–今 | iPhone 与 Mac 全线运行 XNU | Mach 端口/IPC 成为数十亿设备的日常机制 |

读法提示：XNU 里的 Mach 层早已不是纯微内核（BSD 与 Mach 在同一地址空间）——
「微内核的胜利」与「微内核的妥协」同时发生在这一行代码里。

## 经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Accetta, Baron, Bolosky, Golub, Rashid, Tevanian, Young《Mach: A New Kernel Foundation for UNIX Development》 | USENIX Summer 1986 | Mach 奠基论文：任务/线程/端口/外部 pager |
| Draves, Bershad, Rashid, Dean《Using Continuations to Implement Thread Management and Communication in Operating Systems》 | SOSP 1991 | Mach 线程与 IPC 的续体实现优化 |
| Rozier et al.《CHORUS Distributed Operating Systems》 | Computing Systems 1(4), 1988 | Chorus 的权威综述（Nucleus/actor/消息模型） |
| Liedtke《On µ-Kernel Construction》 | SOSP 1995 | 微内核性能论战的关键转折：最小化 IPC 路径 |

> Mach 相关更细的 API 文献（CMU《Mach Kernel Interface Manual》等）属技术报告系列，
> 具体版本信息本次未逐字核对，按约定不列具体出处，标注「出处待核」。

**三篇论文的关系**（帮助建立阅读地图）：Accetta 1986 给出抽象（是什么），
Draves 1991 给出实现（怎么做快），Liedtke 1995 给出裁决（能做到多快、哪些东西
不该留在微内核里）。按 1 → 3 → 2 的顺序读，论证链条最顺。

## 近年研究与工业界开源实践（2015–2026）

- **Mach 的商业后裔无处不在**：macOS/iOS 的 XNU 内核 = Mach 微内核基座 + BSD 单内核层；
  Mach 端口至今是苹果系统 IPC（XPC 的底层）的原语——这是三大分布式 OS 原型中
  唯一「活在数十亿设备里」的代码血统。
- **微内核的安全关键化**：seL4（`seL4/seL4`，5766★）提供端到端形式化证明（seL4 Proofs），
  已用于国防/车载/无人机；QNX（闭源，车载份额最高）是 Chorus「嵌入式微内核」路线的最大赢家；
  Fuchsia 的 Zircon 内核重拾 Mach 式对象+IPC 模型（GitHub 无主仓，**star 未核验**）。
- **外部 pager 思想的回声**：用户态文件系统（FUSE）、SPDK、DAX、以及数据库自管缓冲池
  （绕开 OS page cache）都是「存储策略离开内核」的延续；io_uring 则反过来证明
  「系统调用路径越短越好」——Liedtke 论点在 Linux 的胜利。
- **沙箱 IPC 的对照**：`google/gvisor`（19420★，2026-09-26 实测）用用户态内核拦截系统调用，
  其通信面与 Mach 端口解决的是同一问题（不可信代码与内核之间的窄接口）。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「Mach 是分布式操作系统」 | Mach 本体是单机微内核；其分布式能力来自上面叠的 NetOS/透明共享内存等研究层，原书选它正是为了讲「如何把单机内核扩到分布式」 |
| 2 | 「端口就是消息队列容器，无安全含义」 | 端口权受内核保护，**持有权即权限**——安全模型藏在通信原语里 |
| 3 | 「微内核天然更慢，所以都失败了」 | 1990s 慢在 IPC 路径；L4 之后 IPC 可达百纳秒级；失败更多是生态与应用兼容问题 |
| 4 | 🔧 **「Mach 是未来」的语气需校正** | 2026 年事实：XNU 活着但已高度单内核化；研究主流转向 seL4/Zircon；「微内核复兴」发生在安全关键领域而非通用计算 |
| 5 | 🔧 **Chorus 的商业史需要补** | 原书成书时 Chorus Systèmes 尚存；1997 年并 Sun、Sun 2010 年被 Oracle 收购，技术遗产散入实时/嵌入式 |
| 6 | 🔧 **迁移线程结论要更新** | 该设想未成主流；RPC 优化走过了 L4 的「直通调度」、RDMA 的「内核旁路」与 gRPC 的「流复用」三条路 |
| 7 | 「Chorus 是 Amoeba 的法国翻版」 | 目标完全不同：Amoeba 追求处理器池的学术理想，Chorus 从一开始瞄准可嵌入的商业实时市场——后者反而活得久 |

## 与其他章 / 其他书的联系

- **纵向**：端口权能与 Amoeba 权能（[07-案例-Amoeba.md](07-案例-Amoeba.md)）、命名章的权能一节
  （[04-命名.md](04-命名.md)）构成「名字即权限」三部曲；外部 pager 与
  [06-一致性复制与容错.md](06-一致性复制与容错.md) 的 DSM 章共享「内存/存储边界可插拔」思想；
  微内核命运在 [09-从分布式OS到现代云OS.md](09-从分布式OS到现代云OS.md) 收尾。
- **横向**：任务/线程抽象与 [03-进程与线程.md](03-进程与线程.md) 4.1 节互为印证——
  Mach 证明了「线程可以不必是内核进程」。
- **横向（外部 pager 深挖）**：外部 pager 与数据库内核的「自管缓冲池」是同一选择的两个极端：
  数据库干脆把所有页都拿到用户态——原书第 8 章读完，去看任一现代数据库的
  buffer pool 文档，会发现它们都在回答「内核 pager 为什么不够用」。
- **跨书**：`book/操作系统设计与实现.md`（MINIX）是同为微内核的「教材型」对照；
  `book/Linux内核完全剖析/` 提供宏内核反方；`book/现代操作系统.md` 的对应章
  给出 Tanenbaum 本人对 Mach 的单机化表述。
- **延伸**：DCE 的 RPC 与线程包是 [02-分布式系统中的通信.md](02-分布式系统中的通信.md)
  2.4 节 DCE RPC 的实例研究来源；若后续建 `book/分布式系统/` 目录，DCE 与现代中间件的对照可另立文件。
- **延伸练习（本目录自拟）**：在 macOS 上用 `launchctl`/`proc_pidinfo` 一类工具观察端口
  与 Mach 消息的存在（只观察、不改系统），把「Mach 活在你口袋里」变成可操作的检查。
