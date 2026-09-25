# L04 Bigtable：可扩展分布式存储

> 阅读：Chang et al., *Bigtable: A Distributed Storage System for Structured Data*, OSDI 2006
> 承 L02/L03：MapReduce/GFS 之上，Google 需要"随机读写的半结构化数据"这一层。

## 1. 核心问题

- 需求来源：URL 索引（数十亿条目）、个人化搜索、地理数据……既要
  **关系型的灵活性（稀疏列族）+ NoSQL 的水平扩展 + 毫秒级随机读写**，
  又只需**行内原子性**而非跨行事务。
- 规模目标：PB 级数据、数千台机器、每秒数十万操作——单库关系型不可能。
- 核心权衡：**放弃强一致的全表事务，换取可扩展与高可用**。

## 2. 设计与取舍

### 2.1 数据模型
稀疏、多维、有序、持久映射：`(row, column, timestamp) -> value`。
行按字典序存储，行前缀可被高效扫描（→ 用"行键反转/加盐"设计热点规避）。
column family 是 I/O 与存储格式的单位（同一 family 的列物理相邻 → 列式存储）。

### 2.2 LSM-Tree：本课最重要的一块基石
- 写入：MemTable（有序内存缓冲）满 → flush 成 SSTable（磁盘、只读、块内二分）→
  后台 compaction 逐层归并。写放大换读性能 + 顺序磁盘写。
- 读取：MemTable + 若干层 SSTable 合并；用 Bloom filter 跳过不含 key 的文件。
- 恢复：commit log（GFS 上）+ SSTable 重放。**这是 15-445 bufferpool/WAL 之外的
  另一大存储引擎范式**：RocksDB/TiKV/Cassandra/HBase 全部是 LSM 家族。

### 2.3 架构三件套
- **Client Library**：本地缓存元数据、直接读写 tablet server。
- **Tablet Server**：管理 ~100–200MB 的 tablet（行的连续切片），类似"分区 DB 节点"。
- **Master**：tablet 分配/负载均衡/failover，但**不在数据路径上**（client 直接找 tablet server）。
- **GFS + BigLock (Chubby)**：SSTable/MemTable flush/commit log 落 GFS；
  分布式锁服务 Chubby 负责选主、成员、tablet 唯一性——
  "用外部共识做协调"是 L05 Raft/L12 ZooKeeper 的对照方案（自建共识 vs 外包共识）。

### 2.4 容错细节
tablet 分配用 Chubby lease 保证"至多一个 server 服务一个 tablet"；
老 server 复活发现自己 lease 过期即自我了断（fencing，同 GFS/L05 term）。
compact 与分裂期间可能多 server 同服务一个 tablet 的只读副本——读操作幂等所以安全。

## 3. 论文间脉络

- L03→L04：Bigtable 把 GFS 当"磁盘"，把 Chubby 当"锁"，是分层设计的教科书。
- L04→L15：Spanner = Bigtable + 真全局事务（Paxos + TrueTime），
  回答"Bigtable 放弃的东西如何花大代价买回来"。
- L04→L21：TAO/Memcached 是"Bigtable 式后端 + 缓存前门"的图数据特化版。

## 4. 跨课程联系

- **15-445/15-721**：LSM vs 原生 B+Tree（索引页 vs SSTable）是两大存储引擎路线；
  MVCC 的多版本（timestamp 列）与 Bigtable 的时间戳模型同构；
  事务缺失恰是 15-445 后半程（OCC/2PL）想补的东西。
- **CS149**：tablet 分区 = 数据并行；行键设计 = 负载静态划分防倾斜。
- **6.S081**：MemTable→SSTable 的批量落盘与内核 page writeback / journaling 类比。
- **CSAPP**：Bloom filter、块缓存、二分查找 SSTable 是"数据结构换性能"的综合演练。

## 5. 开源项目中的应用

- **HBase**：Bigtable 论文的直接开源复刻（HDFS + ZooKeeper 对应 GFS + Chubby）。
- **Cassandra/DynamoDB**：借用"稀疏列族 + 有序键 + LSM"，但去中心化（见 L11/L23）。
- **LevelDB/RocksDB/TiKV**：单机 LSM 引擎到分布式 KV，"Bigtable 装进一个库"；
  RocksDB 是 TiKV、CockroachDB（存储层）、MyRocks 的心脏。
- **ClickHouse**：列族思想在 OLAP 的放大（MergeTree 引擎名字就致敬 LSM）。

## 6. 延伸阅读

- Ousterhout《Why Are There So Many Storage Formats for Data Analysis?》(hotstorage'21)——LSM/BTree/列式谱系梳理。
- Chubby 论文（2006）与 ZooKeeper 论文（2010）对照："外包共识"两大流派。
- Bigtable 实战：Google Cloud Bigtable 服务文档中的 row key 反热点设计指南。
