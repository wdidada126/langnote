# L20 Fabric：面向终端用户的高性能虚拟化

> 阅读：Anil, Gosewe-Pereira, Lockerman, Morris, *Operating Kernel Virtualization with Fabric: High-Bandwidth I/O for End-User Virtualization*, ATC 2019
> 主线：PDOS 自家系统论文——虚拟化的最后 20%：把"用户态设备直通"做成可用产品。

## 1. 核心问题

- 桌面用户跑 VM（安卓仿真、Windows 游戏/专业软件、Chrome 沙箱）时，
  **GPU/USB/磁盘等高速外设的 I/O 是最大短板**：
  全虚拟化（hypervisor 模拟设备）带宽损失一个数量级；
  设备直通（VT-d passthrough）要求独占设备，多 VM 共享不了。
- 分布式视角：Fabric 是"把设备驱动从客户机/宿主机内核里拽出来，
  放进独立用户态进程"的**解耦 + IPC 性能**问题——本课罕见的单机系统论文，
  但方法论（分层、消息、代理）与 RPC/L12 完全同构。

## 2. 设计

- **Fabric server**（用户态进程）持有真实设备（GPU 经 DRM/OpenGL 接口），
  暴露一个**虚拟 GPU**给客户机；VM 内核（guest Linux + miniGPU 驱动）
  与 server 之间走**共享内存环（doorbell + 环形缓冲）**传命令与数据。
- 三类通信各取所需：
  1. 小包控制命令 → VM-exit 陷入 + 共享内存（低延迟）；
  2. 大批量数据（纹理/顶点缓冲）→ 共享内存零拷贝搬运；
  3. 显示输出 → server 直接 scanout 到宿主帧缓冲。
- **客户机可见语义是"真 GPU"**：guest 驱动做命令批处理/验证，
  server 侧再做安全隔离（guest 不可信）——**验证成本换可用性**的经典分布。
- 性能：视频播放/3D 基准达裸机 80–90%+（对比 QEMU 全虚拟化个位数）；
  多 VM 共享一个 GPU（时间片 + 优先级）。

## 3. 取舍与洞察

- 为什么放用户态而非内核（virtio-vhost 路线）：
  **驱动 bug 不弄挂宿主内核、可独立重启、开发迭代快**——
  可用性/可维护性优先，用共享内存 + doorbell 把 IPC 开销压回内核态水平。
- 半虚拟化（paravirt）的又一次胜利：guest 配合装驱动（非"任意 OS 透明"）
  换来高性能——对照 Xen/KVM virtio 的通用结论：**透明性、性能、隔离三角**。
- 与容器对比：Fabric 面向"要跑异架构/商业驱动"的强隔离场景；
  gVisor/Firecracker 面向云多租户轻隔离——虚拟化的两条市场线（延伸阅读）。

## 4. 论文间脉络

- 看似离主线，实则回收全课母题：
  RPC/IPC（L01）的"跨保护域调用"、复制/缓存（读缓存换带宽）、
  分层抽象（L02/L17 的"抽象换工程效率"）在单机虚拟化里重现。
- 与 6.S081 直接接力：xv6/Labs 之后，6.1810 后半程正是虚拟化（KVM/xv6-labs 的 hypervisor lab）——同一位老师（Morris）的两门课在此握手。

## 5. 跨课程联系

- **6.S081**：系统调用/陷入/共享内存映射——Fabric 的性能预算全部花在与内核同样的
  trap 与页表操作上；读它等于读"用户态内核"的进阶版。
- **体系结构（CS61C/DDCA）**：DMA、IOMMU（VT-d）、doorbell/中断机制是论文的地基词汇。
- **CS149**：命令环 = 生产者-消费者队列；GPU 时间片 = 任务调度。
- **自顶向下网络**：vhost-net/DPDK 的"用户态驱动 + 共享内存环"与 Fabric 完全同构
  （网络设备的 Fabric 化）。

## 6. 开源项目中的应用

- **virtio / vhost-user / SPDK / DPDK**：内核-用户态半虚拟化 I/O 主干
  （Fabric 的"通用化亲戚"，SPDK 的 NVMe 用户态驱动几乎是同款哲学）。
- **Crosvm（ChromeOS 虚拟机监视器，PDOS 邻居项目）、Rust VMM（Firecracker/Cloud Hypervisor）**：
  用户态设备模型的现代主流。
- **QEMU + GPU 直通 / Intel GVT-g / NVIDIA vGPU**：Fabric 瞄准的市场现状；
  Looking Glass/virgl 项目为开源社区版近似解。
- **gVisor**：另一条"用户态内核"路线（拦截 syscall 而非虚拟化设备）。

## 7. 延伸阅读

- 6.S081/6.1810 hypervisor lab 与 xv6 的 vm 实验（动手前置）。
- *vServer / Disco / Xen 半虚拟化*（Baron 2006 前后经典）——paravirt 概念史。
- SPDK 白皮书（用户态 NVMe 驱动的性能论证）。
- Fabric 项目主页 pdos.lcs.mit.edu/fabric 与源码（C，可跑安卓 VM 实战）。
