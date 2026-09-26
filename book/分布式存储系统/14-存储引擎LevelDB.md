# 第 14 章　存储引擎 LevelDB

> 原书第 14 章拆解一个真实、经典的嵌入式存储引擎——LevelDB（Google，LSM-Tree），
> 并延伸到 Go 移植 `goleveldb`。这是把前面所有单机知识（I/O、缓存、校验、文件系统）
> 汇成「一个能跑的引擎」的章。本章小节为重建（仅取得章名，未取得出版逐节原文），不宣称是出版原文。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 14.1 LSM-Tree 思想 | 把随机写变顺序写，后台合并偿还 | 写优化的核心哲学 |
| 14.2 MemTable 与 SSTable | 内存有序表 + 落盘不可变有序文件 | 读写路径的两条主干 |
| 14.3 WAL | 写前日志保崩溃安全 | 「内存改之前日志先落盘」的引擎版 |
| 14.4 Compaction | minor/major 合并、回收旧版本 | 偿还写放大，也是延迟毛刺来源 |
| 14.5 布隆过滤器 | 判「肯定没有」避免无谓磁盘读 | 压住 LSM 的读放大 |
| 14.6 Go 移植 goleveldb | `syndtr/goleveldb` 的实现与差异 | 在 Go 里用/读 LevelDB 思路 |

## 核心精讲

（以下为教学性梳理，代码均**教学示意，不参与构建**。）

### 14.1–14.3 写路径：顺序写 + 内存表 + WAL

LevelDB 写流程：先**追加写 WAL**（保崩溃可恢复）→ 写入内存的 **MemTable**（跳表，有序）；
MemTable 满则冻结为不可变 MemTable，后台**转储成 SSTable（L0）**。随机写被「WAL 顺序写 +
内存写」消化，避免原地更新的随机 I/O——这正是 [04-04]/[05] 章顺序 I/O 思想的兑现。

```text
# 教学示意，不参与构建：LevelDB 写读路径
write(k,v):  WAL.append(record(k,v))   # 顺序写，先落盘保命
             MemTable.put(k,v)          # 内存有序插入，极快
read(k):     MemTable -> Immutable -> L0 -> L1 -> ... -> Ln
             # 每层配 Bloom filter 挡掉"肯定没有"的查询
```

### 14.4 Compaction：偿还与代价

- **minor compaction**：MemTable → SSTable；
- **major compaction**：多层 SSTable 归并，丢弃被覆盖版本与墓碑（删除标记）。
compaction 消除读放大/空间放大，但**大 compaction 与前台共享 I/O/缓存，是延迟毛刺高发点**
（也是 [12-数据策略.md](12-数据策略.md) 12.5 限速思想的来源）。

### 14.5 布隆过滤器：压读放大

每层 SSTable 配布隆过滤器，点查时先问「这个 key 肯定不在该文件吗？」，若肯定不在就跳过磁盘读，
把 LSM 的读放大显著压低。布隆过滤器是 LSM 工程的标配（见 [02] / 经典论文段）。

### 14.6 Go 移植：goleveldb

`syndtr/goleveldb`（6322★，2026-09 实测）是 LevelDB 的纯 Go 移植，API 近似、无 CGO 依赖，
适合嵌入 Go 存储服务。它与 `google/leveldb`（39448★）、`facebook/rocksdb`（32137★）同源不同系：
RocksDB 是 Facebook 在 LevelDB 上的增强（列族、更高写吞吐），生产多用 RocksDB 系。

## 版本演进

- LSM/MemTable/SSTable/WAL/compaction/布隆过滤器的原理长期稳定，2024 年书出版时与当前一致。
- 🔧 **2026 视角补入**：**LSM 的现代优化**（键值分离 WiscKey、最优布隆 Monkey、自适应合并 Dostoevsky）
  已成共识，书若只讲 leveled/tiered 基础，应补这些把「三种放大」变连续可调的工作
  （详见 [../大规模分布式存储系统/02-单机存储系统.md](../大规模分布式存储系统/02-单机存储系统.md) 经典论文段）。
- 🔧 **2026 视角补入**：**ZNS SSD 利好 LSM**（顺序写约束与 LSM 天然契合），是介质侧新变量。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| O'Neil et al.《The Log-Structured Merge-Tree》 | Acta Informatica 1996 | LSM 奠基，对应 14.1 |
| Bloom《Space/Time Trade-offs in Hash Coding》 | CACM 1970 | 布隆过滤器，对应 14.5 |
| Chang et al.《Bigtable》 | OSDI 2006 | SSTable 的工业源头（LevelDB 受其启发） |
| Lu et al.《WiscKey》 | FAST 2016 | 键值分离，🔧 2026 必补 |
| Dayan et al.《Monkey》 / 《Dostoevsky》 | SIGMOD 2017/2018 | 布隆最优分配 / 自适应合并，🔧 2026 必补 |

## 近年研究与工业界开源实践（2015–2026）

- **LSM 引擎三系**：`google/leveldb`（39448★）、`facebook/rocksdb`（32137★）、
  `syndtr/goleveldb`（6322★，Go 移植，对应 14.6），2026-09 实测。
  RocksDB 被 TiKV/CockroachDB/Flink state 广泛嵌入，是 LSM 工业事实标准。
- **Go 存储项目用 LSM 思路**：`minio/minio`、`seaweedfs/seaweedfs` 的元数据/索引层常借鉴 LSM。
- **compaction 限速**实践见 `facebook/rocksdb` 的 rate limiter，对应 14.4 与 [12-数据策略.md](12-数据策略.md)。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「LSM 写快读慢，绝对」 | 是三种放大的配比；范围扫描 LSM 很快，差异在延迟方差 |
| 2 | 「compaction 是后台活不影响前台」 | 大 compaction 共享 I/O，是生产毛刺高发点 |
| 3 | 「goleveldb 就是 leveldb」 | 是 Go 移植，与 C++ leveldb/rocksdb 同源不同系，性能/特性有差 |
| 4 | 🔧 只讲基础 LSM | 2026 年补 WiscKey/Monkey/Dostoevsky 与现代放大权衡 |

## 与其他章 / 其他书的联系

- **本书内**：14.3 WAL → [04-Linux存储基础.md](04-Linux存储基础.md)/[05-存储I-O实践.md]（落盘）；
  14.4 compaction 限速 → [12-数据策略.md](12-数据策略.md) 12.5；14.5 布隆 → [08-缓存模式.md](08-缓存模式.md)（减无效读）。
- [../设计数据密集型应用/03-存储与检索.md](../设计数据密集型应用/03-存储与检索.md)
  ——DDIA 第 3 章是 LSM/SSTable 最系统对读材料。
- [../大规模分布式存储系统/02-单机存储系统.md](../大规模分布式存储系统/02-单机存储系统.md)
  ——同主题但带 2026 补丁（WiscKey 等），互补。
