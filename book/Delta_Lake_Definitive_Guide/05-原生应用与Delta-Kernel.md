# 第 6 章 用 Delta Kernel 与 delta-rs 构建原生应用

> 原书第 6 章「Building Native Applications with Delta Lake」。主题只有一个：
> **不把 Spark 拖进来，如何读写 Delta 表**。本文件按「协议 → Kernel（Java/C）→ delta-rs（Rust）→
> 自研引擎接入清单」展开。所有代码为**自拟教学示意，非书中原文**；API 形态以 delta.io Kernel 文档为准。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 6.1 为什么要有 Kernel | 每个引擎重复实现日志解析是生态税 | 把协议实现做成库，引擎只做「怎么执行」 |
| 6.2 Delta Kernel 架构 | Snapshot / Transaction / Expression / Read API | 「你提供 IO 与执行，我提供正确性」 |
| 6.3 Kernel 的读写路径 | 事务构建、提交、DV 感知的过滤 | 写仍是完整 OCC 提交 |
| 6.4 C/FFI 绑定 | kernel-ffi → 其他语言桥 | Java 核心的可移植层 |
| 6.5 delta-rs | Rust 独立实现 + Python 绑定 | 非 JVM 世界的事实第二实现 |
| 6.6 自研接入检查表 | 协议版本、特性协商、冲突处理 | 接入前先读 PROTOCOL.md |

## 核心精讲

### 6.1 问题设定：表格式税

第 3 章说过：读一张 Delta 表 = 重放 `_delta_log`、合并 add/remove、解析 stats、应用 DV。
Trino、Flink、DuckDB、每个自研服务若都重写一遍，就会出现「同一份表，各引擎理解不一致」的裂脑。
**Delta Kernel = 官方提供的「协议正确性」库**：

```text
┌ 你的引擎 ─────────────────┐
│ 查询计划 / 执行 / IO 调度  │  ← 引擎自己负责（性能在这层）
├ Delta Kernel ─────────────┤
│ 日志解析、快照、schema、    │  ← 协议正确性（事务/特性协商）
│ 事务构建、表达式/分区过滤    │
└───────────────────────────┘
```

### 6.2 Kernel 的四大入口（Java API 形态，教学示意）

```java
// 自拟示例，非书中原文；签名以 delta-io/delta kernel 仓库为准
Engine engine = DefaultEngine.create(new EngineProperties() { ... }); // 你注入 JSON解析/行格式/执行器

Snapshot snapshot = Snapshot.Builder.forTable(dataPath, tableId)
        .withEngine(engine).build();                 // 打开一个版本快照
List<DataFileStatus> files = snapshot.getAllFiles(engine, null); // 已按分区/表达式过滤的文件清单

Transaction tx = snapshot.newTransaction();          // 读快照 → 起事务
// ... 由引擎自己写出 parquet 文件 ...
tx.commit(engine, List.of(new AddFile(...), new RemoveFile(...))); // 走完整 OCC 提交
```

要点：

- **Engine 接口反转**：Kernel 不要你的数据，要你的「能力」——JSON 解析、行对象模型、表达式求值器、
  元数据 IO。正确性归 Kernel，性能归引擎。
- **Read API 的边界**：早中期 Kernel 故意**不管文件内行级扫描**（parquet 解码留给引擎），
  之后补齐「读计划 + 表达式引擎」；做新引擎接入时先查目标 Kernel 版本支持的 surface。
- **协议协商**：`Snapshot` 暴露 reader/writer features（DV、type widening…），
  引擎按自己支持的特性子集决定能否打开表——这就是第 3 章「抬高 minReaderVersion 会拒读旧引擎」的另一面。

### 6.3 用 Kernel 写事务

- 流程与 Spark 完全同构：读版本 → 写文件 → 组 commit → 冲突则重读重算。
- Kernel 负责生成合法的 commit JSON（commitInfo/protocol/metaData 齐全）、
  校验 schema/约束（逐步增强中），引擎负责并行与 IO。
- 适用：**自定义 ingest 服务、非 Spark 流引擎、嵌入式分析**；
  不建议拿它替代「Spark 用户」——你已经有全功能 delta-spark 了。

### 6.4 kernel-ffi（C 绑定）

- `delta-kernel-rs`/kernel-ffi 把 Java Kernel 的核心逻辑桥成 C ABI，供 C/C++/Go/Rust 引擎调。
- 典型用户：给现有 C++ 查询引擎加「能正确读 Delta」的模块，而不移植整个 JVM。

### 6.5 delta-rs（Rust 实现）

```python
# 教学示意（deltalake PyPI 包）
from deltalake import DeltaTable
dt = DeltaTable("/mnt/warehouse/events")
print(dt.version(), dt.schema())
df = dt.to_pyarrow_table(version=42)   # 时间旅行 → Arrow
```

- 独立于 Kernel 的第二条原生路线：Rust 全栈实现日志解析/写事务（写能力持续演进），
  Python 绑定走 Arrow FFI——**DuckDB、Polars、Pandas、DataFusion 场景几乎都经它接 Delta**。
- `deltalake-rs` 也被若干 catalog/查询服务用作元数据后端；
  与 Kernel 的关系：**同源不同栈**（一个 Java 核心 + FFI，一个纯 Rust）。

### 6.6 自研引擎接入 Delta 检查表

| 项 | 必做 |
| --- | --- |
| 读 PROTOCOL.md | 弄清 add/remove 语义、checkpoint 重放规则 |
| 特性协商 | 对 DV/column mapping/type widening 明确「支持/拒绝」，别静默错读 |
| stats 解析 | 不做 min/max 过滤没关系，做错 NULL 语义会算错结果 |
| 提交路径 | 只经 Kernel/合法协议提交；**永远不要手改 `_delta_log`** |
| VACUUM 交互 | 读快照要容忍文件缺失，或直接拒绝低于 vacuum 水位的版本 |

## 版本演进

| 时间 | 事件 |
| --- | --- |
| 2022–2023 | Delta Kernel 立项并发布（Java），目标「引擎只需一个 JAR 即可兼容协议」 |
| 2023 | delta-rs 成熟、Python 绑定进入 Polars/DuckDB 生态视野 |
| 🔧 2024–2025 | Kernel 0.x 快速迭代（表达式引擎、C 绑定、事务面扩大）；API 仍在 0.x = 未冻结 |

## 文献与文档

- delta.io / GitHub `delta-io/delta` 的 `kernel/`（API 文档与示例）；PROTOCOL.md。
- `delta-io/delta-kernel-rs`（C 绑定）；`delta-io/delta-rs`（Rust）。
- Arrow FFI / DataFusion 文档：delta-rs 与 Arrow 生态的对接方式。

## 常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「Kernel 会替我执行查询」 | 它管协议正确性，扫文件/算子仍是引擎的活 |
| 2 | 「有 API 0.x 文档就不用追版本」 | Kernel 迭代快（0.x 阶段接口会变），锁版本 + 跑协议一致性测试 |
| 3 | 「手写日志解析器更轻」 | 每个方言偏差都是数据损坏风险；这正是 Kernel 要消灭的 |
| 4 | 🔧 「delta-rs 与 Kernel 二选一」 | 两条实现并存互补，按语言栈与特性支持表选型 |

## 与其他章 / 其他书的联系

- ← `02`：没有第 3 章的日志/OCC 模型，本章的 API 无法理解。
- ← `03`：4.1 的「连接器能力 = 协议子集」由本章的协商机制解决。
- → `12`：跨组织共享时，第三方工具也走同一套原生实现读 share 数据。
- → [../bigdata/10-计算引擎的演进.md](../bigdata/10-计算引擎的演进.md)：引擎与存储解耦的终局形态。
