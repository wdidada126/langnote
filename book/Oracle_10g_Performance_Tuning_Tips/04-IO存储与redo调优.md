# 04 IO存储与redo调优 — Oracle Database 10g Performance Tuning Tips & Techniques（精读重构）

> ⚠️ 主题重组口径（章号非原书章号，降级声明见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §3）。本章=块在 IO 栈的旅行图：布局、多块读、checkpoint 节拍与 redo 双等待对。
> Oracle 行为一律 ⚠️ 转述；官方锚点 ✅：10.2 PTG B14211 Ch8《I/O Configuration and Design》/Ch9《OS Resources》（目录实抓在册）。

## 1. 一个块的旅程（⚠️ 通说模型）

服务器进程 → 在缓冲缓存找（命中即终点的 `logical read`）→ 未命中：单块（索引路径 `db file sequential read`）或多块（全扫 `db file scattered read`）→ `pfile put/get wait event` 进 IO 栈 → 操作系统/卷/阵列/盘 → 完成回填并继续。
- 调优推论：每一段旅程都有对价——缩短路径（索引）加次数，摊长路径（全扫）加单跳体重；**IO 调优=设计旅程形状，不是消灭物理读** ⚠️。
- OS 层证据 ⚠️：`iostat`（tps/MBps/svctm/await）与 Oracle 事件名并排看；10g 的 `V$FILESTAT`/`V$TEMPFILE`/`V$IOSTAT_FUNCTION`（异步 IO 口径）给文件级延迟账。

## 2. mbrc：10g 最被争论的一个参数（⚠️）

- `db_file_multiblock_read_count`（mbrc）决定全扫一次旅程搬几块；9i/10g 手工时代"越大吞吐越高"，但 CBO 成本模型同步把"全扫变便宜"→ 索引可能被弃 ⚠️——经典连锁贴士：**改 mbrc=改计划**。
- 10g 系统统计（`CPU_IO_STATS`，B14211 Ch14 域 ✅）登场后的官方口径 ⚠️：让 NOWORKLOAD/WORKLOAD 统计接管 IO 成本，mbrc 的"手感调参"退居二线——本册恰处两者交接期。
- DSS 夜批场景的实操残值 ⚠️：会话级放大（`alter session set db_file_multiblock_read_count=...`）+ 并行全扫，仍是当年报表窗口标准配方。

## 3. 布局学：从条带分到 ASM（10g 新生 ✅ B14211 Ch8 收录 ASM 线）

- 经典分盘律 ⚠️：redo 与数据分离；索引与表分离（热点不同）；TEMP 独立卷；热文件分散（`V$FILESTAT` 的 read+write 加权排序找热点）。
- **ASM（10.1 引入）** ✅ 概念在册：条带+镜像交给卷管理层，`asm_power_limit` 再平衡节拍、AU（allocation unit）尺寸影响条带粒度 ⚠️；本册时代=ASM 第一代使用证词，RAC 场景几乎强制项。
- RAW 设备/文件系统 DIRECT I/O 之争（10g 时代现实 ⚠️）：绕 OS 缓存避免双重缓存与 fpb（fallocate 风格预分配）话题——2026 已由 ASM/云卷吸收（速判表 00 §12.6"裸设备=化石"）。
- 与盘上教材对读：体系与命名底座 ✅ [../Oracle_Essentials_5e/02-物理存储结构与表空间.md](../Oracle_Essentials_5e/02-物理存储结构与表空间.md)。

## 4. checkpoint 节拍：DBWn 的心电图

- 目标函数 ⚠️：实例恢复时间 ≈ 需要重应用的 redo 量 → `fast_start_mttr_target`（10g 起 MTTR 自适应 checkpoint）替你调"检查点激进度"；`log_checkpoints_to_alert` 取证 ⚠️。
- 观测账本 ⚠️：`V$INSTANCE_RECOVERY`（目标 MTTR/缓存恢复时间/检查点老化分布）、`V$BG_EVENT_STATS`（DBWn 批大小）；AWR `Checkpoints` 节看 `DBWR checkpoints` 频率。
- 病理两则 ⚠️：checkpoint 风暴（全扫冲刷脏块 → 时间性 IO 尖峰）与"检查点饥饿"（日志切换才触发 → 切换风暴时 DBWn 追赶写）。
- 10g 的增量检查点早已成熟（8i 起），贴士价值转向 **脏块老化线（checkpoint queue 长度）与缓冲缓存的博弈** ⚠️。

## 5. redo 双等待对：`log file sync` vs `log file parallel write`

- 机理 ⚠️：用户进程 commit → 通知 LGWR（`log file sync` 等 ACK）；LGWR 写组（`log file parallel write` 等盘）。**前高后低=LGWR 忙/被排队；后高前低=盘慢**——本册时代的分诊口诀。
- 处方谱 ⚠️：日志独立低延迟卷（禁与热数据共 spindle）；日志组数/尺寸防"切换等待"（`log switch`/`checkpoint not complete`）；应用侧减少碎提交（→ `09` 章事务边界）；`log_checkpoint_interval` 族在新代际已让位自动策略。
- 异步/网卡场景的 `log file sync: X` 细分（11g 后事件拆分）本册未及 ⚠️，演进节记。
- 跨引擎对照（盘上实证 ✅）：SQL Server 写日志等待 `WRITELOG`（[../SQL_Server_Advanced_Troubleshooting/03-存储与I_O故障排除.md](../SQL_Server_Advanced_Troubleshooting/03-存储与I_O故障排除.md)）、MySQL redo fsync 线（[../高性能mysql.md](../高性能mysql.md)）——"提交等待=日志盘税"三引擎同构。

## 6. 临时表空间与排序溢出 IO（⚠️ 与 `03` 章 PGA 账衔接）

- 排序/哈希/建索引溢出入 TEMP：`V$SORT_SEGMENT`/`V$TEMPSTAT` 类账本 ⚠️；夜批失败模式=TEMP 与数据同卷 → 溢出高峰撞白天 OLTP。
- 贴士谱 ⚠️：TEMP 多文件同尺寸（利用轮询分配）、大排序作业独占表空间、`sort_area_size` 手工放大替代溢出（承接 `03` 章 MANUAL 策略）。
- 盘上案例实证：同域疑难案例在 [../Oracle_Database_Problem_Solving/08-临时文件IO与闩锁争用.md](../Oracle_Database_Problem_Solving/08-临时文件IO与闩锁争用.md) ✅——2000 年代 IO 病理学与现代案例的连续标本。

## 7. 存储时代特征表（本册 vs 2026，⚠️ 判定+✅ 概念锚）

| 10g 贴士对象 | 2026 状态 |
|---|---|
| mbrc 手调改变成本 | ⚠️ 化石（系统统计+异步 IO 主导，参数已废/隐藏线） |
| 条带分盘布局学 | ⚠️ 半化石（ASM/云卷吸收，"热点分散"思想现役） |
| `fast_start_mttr_target` | ✅ 现役（19c/23ai 文档在册 ⚠️ 未逐页实抓） |
| redo 双等待分诊 | ✅ 现役（事件细分更密，口诀不变） |
| RAW/DIRECT IO 之争 | 化石 |
| ASM 初代条带参数 | ✅ 现役且为云基座（版本线 10g→23ai） |

## 8. 本章证据接口小结

- "旅程形状"决定等待事件名 → 回 `02` 速诊表分诊；
- 多块读与全扫成本 → `05` 统计章成本口径；
- TEMP 溢出 → `03` PGA + `09` 批处理章联动；
- IO 子系统内幕（异步/SLRU）→ [../Oracle_Internals_An_Introduction/01-内部服务导论.md](../Oracle_Internals_An_Introduction/01-内部服务导论.md) 纵深（✅ 在盘）。

## 9. redo 组尺寸与切换节拍算术（⚠️ 通说配方）

- 观测口径 ⚠️：`V$LOG`（组/成员/序列）+`V$LOG_HISTORY`（每小时切换次数）+`ALERT log` 的 checkpoint 行；10g 起日志切换频率已是 AWR `DB Instance Activity` 的常规行。
- 目标函数 ⚠️：**别让 DBWn 因"写满"被迫追写**（切换等待=`checkpoint not complete`），也别让它闲到实例恢复预算爆表（MTTR 反方向）。
- 经验配方（⚠️ 仅 10g 语境）：切换间隔 15–30 分钟为宜 → 组尺寸 ≈ 每小时 redo 量 ÷ (60/间隔分) ；`fast_start_mttr_target` 给足缓冲让自适应检查点自己呼吸。
- 反例账 ⚠️：`log_checkpoint_interval` 拍脑袋设小 → 检查点风暴 → 白天 IO 尖峰；设 `LOG_CHECKPOINTS_TO_ALERT` 取证两周再动第二轮——贴士册的"先看再改"样板。
- 跨引擎对照（✅ 在盘）：SQL Server 的 VLF/checkpoint 节拍（[../SQL_Server_Advanced_Troubleshooting/03-存储与I_O故障排除.md](../SQL_Server_Advanced_Troubleshooting/03-存储与I_O故障排除.md)）、MySQL redo 尺寸与 fsync 策略（[../高性能mysql.md](../高性能mysql.md)）——"日志=恢复预算的载体"三引擎同文。

## 10. IO 校准与异步 IO 一瞥（⚠️ 本册边缘话题，✅ 概念锚）

- 校准动机 ⚠️：系统统计（`05` 章）要吃"真实 IO 时延"，存储换型（HDD→SSD/阵列改条带）后若不重测，CBO 继续按旧时延选计划=计划与硬件吵架。
- 本册时代手工艺：`dbfs_direct` 测试器、自研脚本跑 mbrc 谱曲线 ⚠️；**官方校准器（11g SMT adapter/`DBMS_RESOURCE_MANAGER.CALIBRATE_IO`）在本册成书后登场**（✅ 概念锚 19c 文档 I/O 校准节在册 ⚠️ 未逐页实抓）——史料上这是"手感 mbrc"退场的发令枪。
- 异步 IO 词表 ⚠️：`V$IOSTAT_*`（10g 起按组件/文件给 iops/MB/s/延迟三列）、`FILEIO_ASYNC` 参数族、滑环队列深度与阵列 write-back cache 开关（OS/存储层，`iostat` 的 `svctm<<await`=排队为主的判据 ⚠️）。
- 判定纪律：校准数据喂的是**成本模型**，等待事件量的是**现场**——两者互相校验，不可互替 ⚠️。
- 2026 对应：云卷性能规格（IOPS/吞吐/突发额度）就是当代"校准表"；读本章贴士时把"盘型号"脑内替换为"SLA 等级"即可保留全部推理结构。

### 附记：IO 栈词表速查（⚠️ 本册时代→OS/阵列对照）

| 层 | 本册语境词表 | 观测通道 |
|---|---|---|
| Oracle 会话 | `db file sequential/scattered read`、直接读写 | `V$SESSION`/`V$FILESTAT` |
| Oracle 后台 | DBWn/LGWR/ARCH/PMON 族的文件 IO | AWR `Background waits` 节 |
| 卷/文件系统 | buffered vs direct、`O_DIRECT`、预留空间 | `iostat -x`、`svctm/await` |
| 阵列 | RAID 级、条带深度、写缓存 BBU、队列深度 | 阵列控制台/厂商统计 |
| 盘 | seek/rotational、IOPS 上限、吞吐上限 | `iostat`+SMART 线 |
- 判读法 ⚠️：自上而下对表（Oracle 等待→OS 延迟→阵列排队→盘规格），任何两层矛盾处即漏报处（例：await 高而 svctm 低=排队不是介质）。
- 10g 的 `V$IOSTAT_FUNCTION` 把"谁在吃 IO"按功能类分账 ✅ 概念在册（B14211 Ch8 域）——现代 AWR 的 IO 表是其直系后代。
- 阵列写缓存的"断电保护"话题（BBU）属存储采购条款而非调参条款——本册时代贴士常混入，读时剥离 ⚠️。
- 2026 对应：表内"盘/阵列"两行整体换成"云卷规格+突发额度"，其余三层推理原样可用。

### 附记二：redo 组体检五步（⚠️ 通说配方收口）

1. `V$LOG`：组数（≥3 组成员数双镜像起步）与尺寸列同屏记录 ⚠️。
2. `V$LOG_HISTORY`：每小时切换序列均值/峰值——峰值小时对应业务峰 ⚠️。
3. `ALERT`：`checkpoint not complete`/`thread ... switched to log seq` 行频 ⚠️。
4. AWR：redo size/s 与切换次数的比值复核第 9 节算术 ⚠️。
5. 处置阶梯：先尺寸（撑到 15–30 分钟）→ 再盘（独立卷）→ 最后才怀疑应用节拍（`09` 章联动）⚠️。
- 口诀：**组少不镜像=单点、组小切得勤、盘混必排队**——本册 redo 贴士的三行总结 ⚠️。
- 本附记全部为 ⚠️ 转述；19c/23ai 的日志事件细分与并行服务器语境先对新版 Reference 再动手。
## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
|---|---|---|
| 多块读计数 | `db_file_multiblock_read_count` (mbrc) | 全扫单次搬运块数，兼改成本模型 |
| 分散读 | `db file scattered read` | 全扫多块进非连续块槽 |
| 顺序读 | `db file sequential read` | 索引路径单块读 |
| 自动存储管理 | ASM (Automatic Storage Management) | 10g 条带+镜像卷层 |
| 分配单元 | AU (allocation unit) | ASM 条带粒度 |
| 快速启动检查点目标 | `fast_start_mttr_target` | 以恢复时间反推检查点激进度 |
| 实例恢复视图 | `V$INSTANCE_RECOVERY` | 检查点老化与恢复预算账 |
| 日志同步等待 | `log file sync` | 提交等 LGWR 确认 |
| 日志并行写等待 | `log file parallel write` | LGWR 等盘落 |
| 临时溢出 | Temporary segmentation/spill | 排序哈希落 TEMP 的 IO 税 |

## 最新演进与工业实践

- **文档延续 ✅**：19c/23ai《Performance Tuning Guide》的 I/O Configuration 章线在册（✅ 门户实抓，见 00 §12.7）；mbrc 已从新版调优面淡出（`db_file_multiblock_read_count` 在自动优化下不推荐手设 ⚠️，以 19c 文档口径为准）。
- **redo 观测换代 ⚠️**：`log file sync` 在 12c/19c 拆出 `log file sync figure wait time` 类细分子事件与 IMEI/并行服务器优化；19c 起异步/直接 redo 提交路径（`.lgwr` 交互）显著改写 10g 口诀的适用边界——分诊仍先分"人等 vs 盘等"。
- **存储终局**：Exadata/OCI 智能扫描、通用云 EBS/NVMe 分层把"布局学"升维成"带宽+延迟 SLA 选型学"；ASM 成为 Oracle 系存储事实标准（✅ 概念锚 docs.oracle.com ASM 线，本会话未逐页实抓 ⚠️）。
- **SSD 时代的遗产翻案 ⚠️**：10g 时代"随机单块读贵"的成本直觉在 SSD/NVMe 上重估——盘上现代案例集已给 SSD 瓶颈新解（✅ [../Oracle_Database_Problem_Solving/09-SSD瓶颈与索引设计.md](../Oracle_Database_Problem_Solving/09-SSD瓶颈与索引设计.md)），本册布局贴士要按此打折读。
- **可迁移内核**：块旅程模型+等待对分诊是跨引擎性能素养（对读盘上 [../Efficient_MySQL_Performance/00-总览与阅读地图.md](../Efficient_MySQL_Performance/00-总览与阅读地图.md) 的 disk/flush 章线）；参数本体已入博物馆，记账法仍在流水线。
