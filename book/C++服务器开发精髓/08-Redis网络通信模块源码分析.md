# 第8章 Redis网络通信模块源码分析 — 用 Redis 验收第 7 章

> 对应原书第 8 章（§8.1–8.4，原书第 587–680 页）。目录经豆瓣条目 35491437 核实 ✅。
> 全书的"现场考"：第 7 章画的经典结构图，拿 Redis（源码约 6.x/7.x 时代，书以当时主干为准 ⚠️）
> 的 ae 事件循环 + anet 封装 + 客户端状态机逐件对号。作者用 gdb（02 章技能）动态验证静态阅读结论，
> 是本目录"可复算"精神在书内的对应物。
> ⚠️ 实测边界声明：Redis 生产语义依赖 epoll/fork，**Windows 上无原生 Redis**（Memurai/WSL 为移植/子系统，
> 语义非上游验证目标），本章不做本机实测，机制按 redis/redis 公开源码（anet.c/ae.c/server.c/networking.c）转述，
> 版本细节未逐行核对者标 ⚠️。

## 核心概念速览（中英对照）

- **ae 事件循环** — aeEventLoop：Redis 自研 mini-reactor（ae.c/ae_epoll.c/ae_select.c 多后端可插拔）
- **文件事件/时间事件** — file event / time event：读写就绪回调 vs 定时回调（`beforeSleep` 是二者汇合点）
- **anet 封装** — anet.c：跨平台 socket 工具层（blocking/tunnel/非阻塞转换、错误字符串统一）
- **客户端即连接** — client = connection：`redisClient` 结构聚合 fd、输入/输出缓冲、状态机标志
- **客户端输出缓冲** — client output buffer：服务端积压的"每连接额度"（`client-output-buffer-limit`），即 7.7.3 高水位的配置化
- **多命令流水线** — pipelining：客户端狂发、服务端按序处理——把 4.6 的写聚合抬到协议层
- **RESP 协议** — REdis Serialization Protocol：`*N\r\n$len\r\n...` 的递归 bulk 数组，一个自定义协议的活标本（06 章对照）
- **内联命令** — inline command：`PING\r\n` 式裸文本——telnet 调试通道（5.3 技能的服务端镜像）
- **钩子函数** — `beforeSleep`/`afterSleep` hooks（8.2.12）：事件循环每轮空闲前后的挂点，flush 缓冲与定时器在此收口
- **Redis 6 多线程 I/O** — io-threads：主线程保持全部**命令执行**单线程，把 read/parse/write 的 syscall 摊给 IO 线程（8.2.7）
- **客户端管理** — `clients` 链表 + `paused_clients`/暂停-恢复语义（8.2.8）：fork/RDB 期间的流量治理
- **断开流程** — `freeClient` 延迟释放（`clients_to_close`）：事件迭代中不可直接 free 的经典问题

## 动机：为什么拿 Redis 而不是 Nginx 当网络教具

Redis 的响应式骨架足够小（ae.c 数百行讲完一个 reactor），却五脏俱全：LT epoll、双缓冲、
定时器、协议状态机、客户端生命周期、背压限额、多线程 IO 演化——**每一段都能在第 7 章找到对应的抽象格子**。
Nginx 反而太大（模块/阶段/共享内存把信号淹没）。作者在第 2 章用 gdb 调 Redis、第 7 章画结构、
第 8 章闭环，三章互为教具。

## 机制：从 listen 到回复的完整路径（8.2 主线复述+注解）

1. **初始化**（8.2.1）：`listen()` 前 anet 设非阻塞 + `SO_REUSEADDR`（7.12.1 的具象）；
   监听 fd 以**可读**事件挂上 epollfd（8.2.4 的 AE_READABLE 注册）。
2. **接受连接**（8.2.2）：`acceptClient` → `anetTcpAccept`（backlog 打满时 EAGAIN 退出循环不挂死）→
   新客户端 `createClient`（非阻塞+自己的 input/output 缓冲）→ 注册可读。
3. **epollfd 与事件注册**（8.2.3–8.2.4）：`aeApiCreate` 建 epoll 实例；`aeCreateFileEvent` 用
   `EPOLLIN/EPOLLOUT` 的**增改**（ADD/MOD）映射到 AE_READABLE/AE_WRITABLE——
   **LT 模式**（书明确 Redis 不用 ET），因此"读不干净"安全（与 4.14.3 的 ET 炸弹论对照：Redis 用 LT 换鲁棒）。
4. **收数据**（8.2.5 `readQueryFromClient`）：每次 `read` 进 `client->querybuf`（sds），
   循环 `processInputBuffer` 按 RESP 状态机切命令；**单次事件读多个命令**（pipeline 支持）；
   缓冲超 `PROTO_MAX_QUERYBUF_LEN` 即断连（用户态缓冲的输入侧背压）。
5. **可写事件处理**（8.2.6）：平时**不注册** AE_WRITABLE（LT 下可写恒真=忙循环）；
   仅当 `addReply` 发现输出缓冲写不完才注册，flush 完立刻摘除——7.6/7.7 "攒够再写、可写才写"的源码版。
6. **多线程 IO**（8.2.7，6.0）：主循环把"读事件批次"派给 io 线程（各自 read+parse），
   主线程串行执行命令（**单线程语义不变**），再派写回；join 点在主线程 `afterSleep` 前。
   设计动机：命令 O(1) 而 syscall/拷贝成为瓶颈时，水平扩 read/write 而不是扩数据语义。
7. **客户端管理与断开**（8.2.8–8.2.9）：`freeClientAsync` 挂到 `clients_to_close`，
   等本轮事件循环结束再真正释放（**迭代器安全**——在 ae 遍历 fd 事件表期间 free 会 use-after-free）；
   暂停客户端用 `pauseAllClients`（写缓冲转丢弃）而非挂起事件——比"停 epoll"细腻。
8. **定时器**（8.2.11）：时间事件 `aeCreateTimeEvent` 用**无序链表**插 O(1)，
   `processTimeEvents` 每轮全表扫到期（N 很小：serverCron 等少数几个）；**毫秒级业务超时**
   （客户端 idle、阻塞超时）反而不在 ae timer 里做，而在 serverCron 扫 `clients` 链表时批量判
   ——7.9 三流派之外的"第四答案"：定时器数量少时，扫描就是最优。
9. **redis-cli 侧**（8.3）：同一 anet/ae 库的微型复用 + **stdin 也当 fd 挂进循环**（标准输入可读写事件）——
   事件循环通用的漂亮注脚；8.4 RESP：请求 `*N/$len` 数组化一切（06.4 TLV 的极简版），
   `+/-/:/$/*` 五类型；RESP3（书后演进，见下）加 map/set/stream 型。

**钩子**（8.2.12）：`beforesleep` 集中做 reply 缓冲 flush、AOF fsync 策略、定时器任务——
"把一切延后到空闲边界"的循环设计模式（与 09 章日志异步落盘同一哲学：**热路径只记账，冷路径结账**）。

## 权衡与边界（本章四个"为什么这样选"）

- **LT vs ET（8.2.3 的立场）**：Redis 单线程 + 读干净循环，ET 省的唤醒对它价值低（QPS 瓶颈在内核命令执行
  而非 epoll 唤醒数），而 ET 漏读风险伤及 pipeline 正确性——LT 是理性的"保守"。
- **为什么不用 libevent**：ae 只有 ~1000 行且零依赖，Redis 的内存/信号安全需求（fork 期禁 realloc 风暴之类）
  自研更可控；书 8.2 的源码走读本身证明"读 reactor 源码"比"读库文档"更便宜。
- **单线程命令执行 vs IO 多线程**：数据无锁的确定性（10 万 QPS 时代够用）优先；
  当网卡中断与 syscall 成为新瓶颈才拆 IO 线程——6.0 的演进顺序（书 8.2.7 覆盖）即最好的"别过早优化"教材。
- **每客户端缓冲限额**：全局内存上限救不了单连接垄断（大 key 堆积）——`output-buffer-limit` 三级
  （hard/soft+秒）是 7.7.3 四种背压策略里"超限断连"的配置化实现。

## 相邻概念对比

| 概念（第 7 章抽象） | Redis 实体 | 备注 |
| --- | --- | --- |
| acceptor loop | 主线程 aeApi + 监听 fd | Redis 主线程兼 acceptor+executor |
| IO loop 池 | io-threads（6.0+） | 只摊 IO，不摊执行 |
| Connection 状态机 | `client->mstate` RESP 多行状态机 | 6.3 的源码版 |
| 发送缓冲 | `client->reply` 链表 + `buf` 内联头 | 小回复零分配（7.11 侵入式思想） |
| 定时器 | aeTimeEvent 链表 + serverCron 扫描 | "第四流派" |
| 高水位回调 | output-buffer-limit | 策略=断连 |
| beforeSleep 钩子 | hooks | 7.5.4 handle_other_things 同位 |

## 读后自问自答（本章验收，5 问）

1. **为什么 `accept` 要 while 循环 + EAGAIN 退出，而不是 accept 一次？**
   一轮 epoll 里监听 fd 的"可读"可能对应 backlog 中多个已完成握手；LT 虽会再报，
   但一次事件多接可少一轮 loop 延迟——配合 listenfd 非阻塞（7.12.1 闭环）。
2. **AE_WRITABLE 为什么不能常挂？** LT 语义下 socket 发送缓冲有空即"可写"恒真，
   epoll_wait 每轮都醒→空转满核。只有"有货发不完"时临时挂、flush 完立刻摘（8.2.6）。
3. **客户端 idle 超时为什么不用 `aeCreateTimeEvent` 逐个登记？**
   连接数万级时每连接一个时间事件=扫描/插入税全付给 ae；
   serverCron 秒级批量扫 clients 链表（精度损失换 O(N)/秒 的摊销）——7.9 权衡表的第三行。
4. **io-threads 为什么不能"顺手"并行执行命令？**
   单线程执行是 Redis 全部数据结构无锁的前提；命令一旦并发，`dict`/过期/事务语义全线崩塌——
   6.0 只敢把"与 keyspace 无关"的 syscall 摊出去（8.2.7 的边界感）。
5. **RESP 为什么 `*N\r\n$len\r\n` 而不是 TLV Type 字段？**
   Redis 是"单一命令命名空间"协议：Type 由数组首元素的 bulk 字符串充当（命令名），
   长度前缀已保证边界——06 章"定长头+变长体"在文本协议下的最简实现，够用即美德。

## 最新演进与工业实践

- **RESP3（Redis 6.2/7.x 推进）**：推模型（`push` 型）、map/double/boolean——客户端协议从"请求-应答"迈向
  "可订阅流"；驱动是 RESP 客户端生态（py 客户端的 push handler 即示例）。一手规范：
  [RESP 官方文档](https://redis.io/docs/latest/develop/reference/protocol-spec/)（redis.io 可达；版本细节未逐条核对 ⚠️）。
- **io_uring 与 Redis**：社区长期有"ae 后端接 io_uring"提案/实验分支 ⚠️ 未成为主干默认；
  **Valkey**（Linux 基金会 fork，2024）与 **Dragonfly** 等现代实现已用 io_uring/协程路线，
  多 IO 线程方向比 Redis 更激进（"命令执行也并发化"——破坏单线程心智模型换扩展性）。
- **事件库谱系对读**：ae.c ≈ 教科书版 muduo EventLoop 的 C 化；读本章时平行打开
  [../Linux多线程服务端编程.md](../Linux多线程服务端编程.md) 第 6–8 章（EventLoop/TimerQueue 同款）收益翻倍。
- 交叉互链：[../Redis设计与实现.md](../Redis设计与实现.md)（数据结构/持久化全景，与本章的"网络侧"互补）、
  [../深入理解Redis.md](../深入理解Redis.md)、[../Redis5设计与源码分析.md](../Redis5设计与源码分析.md)、
  [../Redis实战.md](../Redis实战.md)、[../master-redis.md](../master-redis.md)、
  [02-工具链与gdb调试.md](02-工具链与gdb调试.md)（本章的调试方法来自那里）、
  [07-单个服务的基本结构.md](07-单个服务的基本结构.md)（格子与实体对表）、
  [04-网络编程重难点.md](04-网络编程重难点.md)（LT/ET、EINTR、SIGPIPE 源码现场）。

## 本章小结

第 8 章的正确读法是**拿着第 7 章的图找格子**：ae 事件循环=loop、readQueryFromClient=收数据正确姿势、
output-buffer-limit=高水位、serverCron=定时器第四流派、beforeSleep=把结账挪到空闲边界。
读完应当获得的元能力：**任何服务的网络层，两周内都能这样拆完**——这正是作者"掌握原理就能造轮子"总思想的验收单。

上一站：[07-单个服务的基本结构.md](07-单个服务的基本结构.md) ｜ 下一站：[09-服务器常用模块设计.md](09-服务器常用模块设计.md)
