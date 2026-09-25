# L21 TAO 与 Memcached at Facebook：社交图谱与缓存一致性

> 阅读：Bronson et al., *TAO: Facebook's Distributed Data Store for Social Graphs*, ATC 2013；
> 辅读：Niu et al., *Scaling Memcache at Facebook*, NSDI 2013
> 主线：读多写少的全球规模——"Bigtable 后端 + 专用前端 + 缓存层"的一致性工程。

## 1. 核心问题

- 社交图谱：数十亿对象（用户/照片/评论）+ 数千亿条边；
  负载特征：**读 : 写 ≈ 500:1**，绝大多数读是"取某对象的邻接表"
  （一次好友列表、一面时间线）——**单跳/双跳局部读，几乎从不全局扫描**。
- 通用图数据库/关系 JOIN 撑不住；Spanner 的强一致对多数页面无必要且贵。
- 答案：**为"对象+边"定制的专用存储 API（TAO）**，
  前端（graph API）→ TAO 缓存/合并层 → MySQL 分片集群持久层。

## 2. TAO 设计

### 2.1 API 即架构
仅四类操作：`get(sg, key)`、`getmultik`、`getsparse`（稀疏边过滤）、`assoc`（建边）。
**没有跨对象事务**（Facebook 选择把一致性责任推给业务层）——
与 Spanner（L15）相反端点：**够用就好的 API 最小化**。

### 2.2 分层与复制
- **MySQL 分片（source-of-truth）**：对象与边按 **slice**（关联对象的集合）分片；
  每分片主从树 + 地理复制（异步 → 有延迟，一致性窗口所在）。
- **TAO 集群**：每区域一组无状态 TAO 服务器 + 共享 memcached 池（region cache），
  后端接本区域 MySQL；跨区先打本区，miss 再回源（origin）。
- **写路径**：写 MySQL → **删除/更新缓存（invalidation）** → 异步复制到其他区域。
- 缓存策略"读时填充（fill-on-read）" + 边与对象**合并成单个 key**
  （一次读把对象 + 稀疏边打包 → 减少往返，L01 RPC 批量思想）。

### 2.3 一致性问题与工程对策
- 读写分离 + 异步复制 → **最终一致**。产品层的补丁：
  **session 保证（sticky session 回同区域写库读己之写）**、
  关键对象（余额/关系状态）走 MySQL 强读路径。
- **删除风暴（cache invalidation stampede）**：热点对象更新会引发
  "全缓存失效 + 集体回源"→ 用 **surrogate keys**（版本号集合）
  把"删 N 个派生缓存"变成"改 1 个版本号"；批量删除队列化。
- 缓存命中率优先：TAO 服务器"永不拒绝服务"——过载时**降级为非缓存直通**而非报错，
  **缓存层挂掉时数据库就是最坏情况 → 设计目标"缓存几乎不失效"**（L09 面向故障的实例）。
- 多写（geo-replication 写冲突）→ 单区域为主写（"origin 单主"），
  避免 Dynamo 式 vector clock（L11）：简单性优先，接受区域级故障切换延迟。

## 3. Memcached at Facebook（NSDI 2013）——缓存作为基础设施

- 数千实例、数十 TB 聚合内存；**对象池化/租约复用、批量删除、
  一致性哈希 + 会话（客户端分片）、mini-object 合并小包**。
- "热 key"处理：**mirror 集群**（热 key 复制到其他区域服务）——
  读扩展的极致工程（L19 CRAQ 读扩展、L23 一致性哈希同一问题域）。
- 哲学：**缓存不是性能补丁，而是被当作一级分布式系统来设计**——
  故障演练、容量规划、可观测一个不缺（L09 呼应）。

## 4. 论文间脉络

- L04 Bigtable：TAO 的"稀疏结构化 + 合并读 + 分片"直接继承 Bigtable 世界观；
  但用"API 最小化 + 外包事务给应用"换吞吐。
- L11 Dynamo：同为"牺牲强一致"，Dynamo 去中心多主，TAO 中心单主 + 缓存——
  两条 AP 路线对照。
- L13/L15：S3/Spanner 用工程/硬件买回强一致；TAO 决定不买（多数场景不值）。
- 主线位置：**"一致性按需付费"（consistency as you need it）**的最佳工业样本。

## 5. 跨课程联系

- **15-445/15-721**：读缓存 ↔ bufferpool 的脏页/失效（TAO 是"把 bufferpool 做成网络服务"）；
  slice 分片 ↔ 数据库 partitioning；无事务 ↔ 隔离级别降到"无"。
- **自顶向下网络**：回源风暴 = 应用层"广播风暴/缓存惊群"，TTL/jitter 缓解同 DNS。
- **CS149**：mirror 热 key = 数据复制以扩展读者侧带宽，与并行程序复制共享只读数据同理。
- **6.S081**：surrogate key 的"间接层换批量失效" ↔ 内核页表/间接块（一切计算机科学问题都可以再加一层间接）。

## 6. 开源项目中的应用

- **Twitter 的 Tigon/图存储、LinkedIn 的 Espresso→Graph、抖音/快手关系链**：
  社交存储同题作文。
- **Redis/Memcached/KeyDB + 两级缓存（本地 Caffeine + 远端 Redis）**：
  直接复用失效/合并/热 key 三件套。
- **MySQL 生态（Vitess/ProxySQL）读写分离 + 缓存 + 单主多从**：TAO 模式的开源化身。
- **CDN 缓存一致性（surrogate key → Fastly 的 Surrogate-Key HTTP 头！同名同源）**：
  Web CDN 的按标签批量失效思想一致。
- **GraphQL 数据源（DataLoader 批量 + 缓存）**：小尺度上复刻"合并取对象+关联"。

## 7. 延伸阅读

- *Facebook 的 TAO 与 MySQL 分片治理*（Facebook Eng Blog 若干篇）——容量增长史。
- *MinaRego/CAHA* 或 *PolarFS*（SIGMOD 2018）：云原生数据库的另一折中（存算分离）。
- 对照论文：Spanner（L15）读一份"强一致怎么买回来"，两份合读构成完整光谱。
- 习题：为一个"关注/取关"热点事件设计缓存失效方案，推导 surrogate key vs 逐个删除的放大。
