# 第 3–5 章：全局缓存缓冲区忙等待 · 自适应游标共享 · 用 SPM 稳定响应时间

> ⚠️ 文档转述（章题取自中译本逐字目录 ✅，章内小节自拟 ⚠️；Oracle 行为描述均为 11gR2–12cR1 口径转述，无 Oracle 实测）。本文件 🔧 为 SQLite 锁争用类比，**非 Oracle 行为**。

## 本文件定位

三章共同回答一类高频问题：**"昨天还好好的，今天突然慢/抖"**。第 3 章是集群层的突发（gc 类等待），第 4、5 章是优化器层的突发（计划漂移与钉住）。合起来正好构成"并发-计划"双通道的抖动排查树。

## 第 3 章 处理全局缓存缓冲区忙等待事件

### 3.1 症状与语义（⚠️ 转述）

- `gc buffer busy acquire`（本实例会话等待）/ `gc buffer busy release`（其他实例正转发 CR 块，本会话等待）两个事件在 AWR Top Events 中占大头；单实例版对应 `buffer busy waits`。
- 语义：块在别的节点缓存里，需经互联以 Cache Fusion 协议取副本；"忙"= 该块的并发拷贝/转换在排队。
- 高发对象画像：序列的 `SEQ$UNIQUE`、索引最右叶（单调键插入）、段头块（空间管理未自动化）、热行 UPDATE、SecureFiles 段头/LOB chunk 链（回看第 1 章）。

### 3.2 诊断路径（⚠️ 转述）

1. `v$session` 等该事件的会话 → p1/p2/p3 = 资源类/文件号/块号，`dba_extents` 反查对象。
2. 分类处置对象：`v$gc_block_master` 类视角看当前持有节点与角色，判断是"跨节点乒乓"还是"热点集中"。
3. 看互联面：集群网络延迟（私有网 ping/OS stat）与 `cluster wait time` 是否同涨——同涨则网络问题伪装成数据库问题。

### 3.3 处置（⚠️ 转述）

- 序列：加大 CACHE 值或改 12c 序列新语法 `SESSION SEQUENCE`/`EXTEND`；避免多节点同抢一个缓存项。
- 索引热叶：反向键索引/哈希分区表打散；应用改批量提交节奏。
- 段头：ASSM + 自动段空间管理重建对象；多 freelist 老办法仅用于老对象。
- 热行：拆分行/改排队逻辑/用应用缓存吸收读放大。
- 结构性：把同一业务对象的数据亲和到同一节点（服务/分区路由），减少跨节点取块次数。

## 第 4 章 自适应游标共享

### 4.1 背景与症状（⚠️ 转述）

- 11g 引入 Adaptive Cursor Sharing（ACS）：绑定变量列上有直方图且不同值组基数差异大时，优化器可同一 SQL 产生多个绑态游标（bind-aware），按谓词选择度浮动选计划。
- 症状面两类：其一，**没有 ACS 保护**的计划漂移——一个"运气好"的绑值把共享游标定型成坏计划，其他值全部陪葬（`v$sql` 看 IS_BIND_SENSITIVE/IS_BIND_AWARE 均为 NO）；其二，**ACS 生效中的振荡**——游标库中堆多个绑态子游标，硬解析与版本计数上升。

### 4.2 诊断与处置（⚠️ 转述）

- 检查绑敏感前提：列上直方图是否存在、统计是否过期（与 CBOF 直方图章同一因果链）；谓词里隐式类型转换会让 ACS 完全失效。
- 快速止血：`dbms_shared_pool.purge` 逐出坏游标让重解析；或 SQL Profile/SQL Patch 强制计划（衔接第 12 章顾问）。
- 结构处置：让 ACS 有工作条件（加直方图、修统计任务）；或对确认单形态的选择度问题改用字面量/绑定掩蔽（`CURSOR_SHIPPING` 谨慎）。
- 长期：12c 起计划侧还有自适应计划（统计反馈改连接方法），与 ACS（选择度侧）分层，别混为一谈。

## 第 5 章 使用SPM稳定查询响应时间

### 5.1 语义（⚠️ 转述）

- SQL Plan Management：基线（baseline）= 一组"被接受"的计划；优化器在硬解析时优先取基线内计划，新计划先走"演化-验证-接受"流程。
- 典型场景：版本升级/统计刷新/绑定漂移导致响应时间抖动——把"历史上表现好的计划"钉住，先止血再查根因。

### 5.2 操作阶梯（⚠️ 转述）

1. 打开自动捕获（`optimizer_capture_sql_plan_baselines`），保证"好计划有档案"。
2. 从 AWR/游标库加载基线（`dbms_spm.load_plans_from_cursor_cache`，支持 sql_id→plan_hash_value 定点）。
3. 演化任务把关新计划（`SPM_EVOLVE_TASK`，12c 起自动运行；11g 手动）。
4. 与相邻机制的取舍：SQL Profile（对单语句注入提示）更轻、SPM（对语句集合制度化）更稳；升级窗口用 SPM staging+批量迁移计划。
5. 坑（⚠️ 社区口径）：基线计划依赖的统计/索引被删，计划"钉而无效"；要定期用 `dbms_spm.describe_sql_plan_baselines` 审计可行性。

## 🔧 实验 G1 · 争用与"等待还是报错"二象限（非 Oracle；SQLite 3.45.3）

Oracle 的 gc buffer busy/enqueue 本质都是"资源被占，等待或失败"。SQLite 用文件锁给出最小可实测同型：

```text
### G1 lock contention (latch/enqueue vs SQLITE_BUSY)
timeout=0.0 -> 'database is locked' errcode=5 name=SQLITE_BUSY waited=0ms
busy_timeout=1500 -> SQLITE_BUSY after waiting 1706ms
after holder commit -> success in 2ms, final v=after-commit
```

- 方法：连接 A `BEGIN IMMEDIATE` 持写锁不放；连接 B（`timeout=0.0`）立即拿到错误码 5/SQLITE_BUSY；连接 C（`PRAGMA busy_timeout=1500`）先等 1.7s 再报同一错误；A 提交后 C 重试 2ms 成功。
- 对照 Oracle：busy_timeout=0 ↔ 应用不设超时直接见 `ORA-00054 resource busy`；busy_timeout=1500 ↔ `enqueue timeout (ORA-30002)` 前的等待段；"持锁方提交即通" ↔ gc 等待随块角色转换完成而结束。**等待不消灭争用，只把它从报错变成延迟**——与第 3 章"热点打散才是根治"同一结论。

## 症状 → 动作速查表

| 症状 | 第一动作 | 章节 |
|---|---|---|
| Top Events 见 gc buffer busy | p1/p2 反查对象，分类热点（序列/索引叶/段头/热行） | Ch.3 |
| cluster wait 与 gc 同涨 | 先查私有网互联，后查库内热点 | Ch.3 |
| 同 SQL 时快时慢且绑值敏感 | 查 IS_BIND_SENSITIVE/直方图/隐式转换 | Ch.4 |
| 坏计划已共享 | purge 游标 + SQL Profile 止血 | Ch.4/12 |
| 升级/统计后计划批量翻转 | 加载 SPM 基线钉住旧好计划 | Ch.5 |
| 基线越攒越多变慢 | 演化任务清理 + 审计计划可行性 | Ch.5 |

## 关联阅读

- 选择度与直方图机理：[../Cost_Based_Oracle_Fundamentals/07-直方图.md](../Cost_Based_Oracle_Fundamentals/07-直方图.md)、[../Cost_Based_Oracle_Fundamentals/03-单表选择度.md](../Cost_Based_Oracle_Fundamentals/03-单表选择度.md)
- 解析与共享游标机理：[../Troubleshooting_Oracle_Performance_2e/12-解析.md](../Troubleshooting_Oracle_Performance_2e/12-解析.md)；SQL 优化技术全景：[../Troubleshooting_Oracle_Performance_2e/11-SQL优化技术.md](../Troubleshooting_Oracle_Performance_2e/11-SQL优化技术.md)
- 计划抖动的事后取证：[../Troubleshooting_Oracle_Performance_2e/05-不可复现问题的事后分析.md](../Troubleshooting_Oracle_Performance_2e/05-不可复现问题的事后分析.md)
- 同目录：[06-RAC故障诊断与SQL顾问.md](06-RAC故障诊断与SQL顾问.md)、[05-AWR分析优化.md](05-AWR分析优化.md)

## 自测题

1. gc buffer busy acquire 与 release 的等待方分别是"谁在动"？
2. 为什么单调键索引的最右叶是 RAC 热点？给出两种打散手段。
3. ACS 生效需要哪两个统计/形态前提？缺其一的后果各是什么？
4. 隐式类型转换为什么会让绑敏感检测失效？
5. SQL Profile 与 SPM 在"作用范围与制度化程度"上怎么取舍？
6. 🔧G1 里为什么加了 busy_timeout 之后错误并没有消失，只是延后？对应 Oracle 的哪两种报错？

## 核心概念速览（中英对照）

- **全局缓存忙等待** — GC Buffer Busy Waits：Cache Fusion 取块时该块正被并发处理而排队 ⚠️
- **缓存融合** — Cache Fusion：RAC 节点间块/克隆传递协议 ⚠️
- **互联延迟** — Interconnect Latency：私有网往返时间，gc 等待的物理底座 ⚠️
- **反向键索引** — Reverse Key Index：打散单调插入热点的索引形态 ⚠️
- **绑定变量嗅探** — Bind Peeking：硬解析时用首个绑值定计划 ⚠️
- **自适应游标共享** — Adaptive Cursor Sharing (ACS)：按绑值组维护多绑态游标 ⚠️
- **绑敏感/绑态游标** — Bind-Sensitive / Bind-Aware：ACS 的检测态与生效态标记 ⚠️
- **SQL 计划基线** — SQL Plan Baseline：SPM 中被接受计划的集合 ⚠️
- **计划演化** — Plan Evolution：新计划与基线比较后决定接受的流程 ⚠️
- **游标逐出** — Cursor Purge：dbms_shared_pool.purge 强制重解析的止血术 ⚠️
- **资源繁忙** — ORA-00054 / ORA-30002：不等待立即失败 / 等待超时失败 ⚠️
- **文件锁忙** — SQLITE_BUSY (errcode 5)：🔧 SQLite 单文件写锁争用信号（非 Oracle）

## 最新演进与工业实践

- **19c/23ai 口径**：SPM 成为默认打开（`optimizer_use_sql_plan_baselines=TRUE` 出厂化），自动演化任务成为夜间作业常态；23ai 增加 SQL Plan Directives 与自动索引联动，"钉计划"进一步无人化 ⚠️ 转述（docs.oracle.com 23/19 参考指南，域名 ✅ 可达）。
- **ACS 的退居**：自动优化器增强（扩展 SQL 统计/行数反馈）在多数场景替代了手工直方图+ACS 的组合；社区共识是"绑态问题先看统计自动化再谈嗅探" ⚠️。
- **RAC 热点工具箱**：12c 序列 EXTEND 缓存、19c 硬分区亲和与 DG 内全局临时表新语义，把第 3 章老办法部分自动化 ⚠️。
- **跨引擎镜像**：SQLite busy_timeout/SQLITE_BUSY 与 PG `lock_timeout`/`deadlock_timeout`、MySQL `innodb_lock_wait_timeout` 同构——"等待窗口换失败率下降"的权衡是各引擎通用语言；🔧G1 即为该母题的最小实测样本。
