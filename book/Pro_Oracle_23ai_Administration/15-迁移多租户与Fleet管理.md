# 15 · 迁移到多租户与 Fleet 管理（原书 Ch.17, pp.533-555）

> 章题 ✅ Crossref 实抓（DOI 10.1007/979-8-8688-1038-1_17, "Migration to Multitenant and Fleet Management"）。章内小节自拟 ⚠️。Oracle 行为一律 ⚠️ 转述；取证：Administration ✅ https://docs.oracle.com/en/database/oracle/oracle-database/23/admin/index.html 、Concepts 多租户节 ✅ …/23/cncpt/index.html（Multitenant 专册/Fleet 工具深链口径见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §2.4）。

## 15.1 问题陈述：遗产非 CDB 时代的收尾工程

23ai 语境里本章是"还旧账"的章：存量非 CDB 库（11g/12c 时代建成）要进容器化+云化轨道，同时几百套库的日常管理要"批量化"。两条主线：**迁移动词**（怎么进 CDB/怎么升版本）与**舰队名词**（进了之后怎么按组管）。许可提醒：多租户选项的授权边界（每 CDB 免费 PDB 额度、超出需许可 ⚠️ 以 Oracle 授权指南为准）是迁移方案的第一页。

## 15.2 非 CDB → PDB 的四条路（⚠️ 方法谱系）

| 路线 | 机制 | 停机窗 | 适用/禁忌 |
|---|---|---|---|
| 就地插拔（no-pdb 时代遗产） | 12.1 曾支持非 CDB 直接 `plug`，**后续版本取消此路径** ⚠️ | — | 仅作历史知识；旧文档出现即警惕版本错配 |
| 完全可传输导出导入 | full transportable export（源 12c+）：元数据+数据文件跨平台搬迁，目标以 PDB 形态落位 | 小时级（表空间拷贝）| 大库首选；平台/字符集检查先行 |
| Data Pump 常规 | expdp/impdp 过网或过文件 | 视体量；可分阶段+增量 | 通用兜底；对象重定义量大时索引重建账（07 章）|
| 复制软件（GoldenGate 类） | 逻辑复制持续追平后秒切 | 分钟级 | 零窗需求+双向回退保险；许可与运维成本高 ⚠️ |

通用前置：AutoUpgrade/预检查工具（16 章件）先跑"能不能进、进去缺什么"（版本对齐、字符集、公共用户前缀冲突 05 章、临时表空间/UNDO 形态 11 章本地 UNDO 决策）⚠️。

## 15.3 迁移动作的标准剧本（⚠️ 以完全可传输为例）

1. 源：官方预检查走 AutoUpgrade analyze 模式+目标平台字节序核对（`dbms_transportable_platform`/`db_transportable_platform` 视图线，函数与视图名以文档为准 ⚠️）；
2. 源全量传输导出（`expdp full transportable ...`）+ 表空间文件跨网拷贝；
3. 目标 CDB：`create pluggable database ... using '<datapump 集>' copy`（或 no copy 直接挂）；
4. 插后：字典对齐（datapatch →16）、统计回传（09 章 transport 保画像）、临时/UNDO 表空间复核、作业与服务注册（11 章 save state/服务）；
5. 回退位：源库保持只读挂账至验收（切换窗口=回退窗口，写进变更单）。

## 15.4 舰队抽象：Fleet / Group / 目标值（⚠️ 工具名以官方为准）

- **管理对象升维**：从"库"到"组"——EM 的 Fleet（数据库/主机/GI 集群/中间件的分组与成员）、`dbcli`（GI 栈的 Fleet/数据库生命周期 CLI：`dbcli create database/import database/...` ⚠️ Exadata/GI 语境）、`oci` CLI（云侧 ATP 群）三工具共同回答"这一批"的问题；
- **目标值对账（configuration drift）**：为组定义参数/补丁/策略基线，逐成员 diff 出漂移——03 章 spfile 台账的规模化形态 ⚠️；
- **批量动作**：一次补丁打全组（滚动 RU 编排，16 章）、一次基线克隆 N 套 PDB（`create pluggable database from clone` 的工厂化，11 章）、一次策略下发（锁定 profile 到全部租户 PDB，05 章）；
- **软件库/黄金镜像（software library/Golden Image）**：二进制作为版本化工件分发（黄金镜像=装好的 HOME+补丁清单），新库=PDB 从 SEED+镜像挂载——把 01 章"装"彻底消灭在生产流程外 ⚠️。

## 15.5 迁移后的运维收敛指标（⚠️ 管理章的验收面）

1. 整合比：N 非 CDB → M CDB 的 M/N 与资源余量（03 章内存配额的对照实验）；
2. 补丁时窗：单机全时停 → 组内滚动停（16 章联动）；
3. 开通时延：建"新租户"从周级（装+建+加固）→ 小时级（PDB 克隆+安全模板 05 章）；
4. 漂移告警数：目标值对账的红灯趋势——Fleet 上线三个月内应单调下降。

## 15.6 AutoUpgrade 配置件速记（⚠️ 声明式升级的代表样例）

```ini
# autoupgrade_my.ini —— 一文件描述一批库(15.4 目标值思想的升级侧应用)
global.preupgrade_timezones=ALL
upg1.source_home=/u01/app/oracle/product/19c
upg1.target_home=/u01/app/oracle/product/23ai
upg1.sid_list=oldcdb1,oldcdb2          # 同 HOME 多实例批入
upg1.upgrade_operation=auto            # analyze 后自动续 deploy
upg1.database_name=cdb_tgt
upg1.target_cdb=cdb_tgt                # 非 CDB → 指定 CDB 的 PDB 化去向(路线表 §15.2 的机器形)
upg1.checking_only_issues_excluded=... # 例外清单一行一议题, 全部留痕评审人
upg2.username=upg_admin  upg2.password=***   # 凭据件走 wallet, 不入文(05 章)
```

用法节奏：`-mode analyze`（只读体检报告）→ 修报告 → `-mode fixups`（安全自动修）→ `-mode deploy`（真升级+字典+时区文件升级流水线）→ 日志目录逐库验收 ⚠️。**每个 stage 都可重放、每步产物落盘**——它同时是本章"迁移工程化"的最佳教具。

## 15.7 迁移风险登记册（⚠️ 模板形）

| 风险 | 触发面 | 前置闸 | 回退位 |
|---|---|---|---|
| 字符集不可映射 | 全库搬家后乱码/问号 | 源库 csscan（字符集扫描器）预演 | 源重导+映射表修正 |
| 版本-补丁错配 | plug 成功但组件 INVALID | AutoUpgrade analyze 先行 | 卸载 PDB/重插 |
| 统计画像断层 | 新库计划集体劣化 | 09 章统计传输+升级后自动收集窗口观察 | 基线回滚 SPM/统计重导 |
| 服务/凭据断链 | 应用连接串/钱包未随迁 | 15.4 组清单核对 | 双写迁移期 DNS/别名并行 |
| 许可超卖 | PDB 数量越线 | §15.1 第一页审计 | 冻结新 PDB 开通 |
| 归档链断裂 | 迁移件不在保留政策内 | 12 章链语境复位检查 | 独立全备补基线 |

登记册纪律：**每行都写"谁签字"**——迁移是组织工程，技术路线表（§15.2）只是其中一列 ⚠️ 本目录立场。

## 15.8 迁移后的"新债清零"清单（⚠️ 收口件）

1. 源库退役三拍：只读挂账期→对象冻结→下线归档（Data Pump 留一份"墓碑导出"作法律件）；
2. 监控/备份/审计三方对账：新 PDB 是否已在 14 章告警族、12 章保留政策、05 章审计策略覆盖内；
3. 旧脚本排雷：硬编码非 CDB 路径/服务名的巡检件全部重写为容器感知（cdb_* 视野，09 章）；
4. 知识回写：迁移手册更新一轮——手册版本落后=给下一批迁移埋雷。

## 15.9 迁移决策三问（收束本章的问句形）

- **去哪**：自家 CDB（多租户整合）/ 云上托管（ATP/RDS）/ 换引擎（去 Oracle 化）——三个目的地的技术重合度高、组织成本完全不同，先定目的地再选路线表 ⚠️ 本目录立场；
- **带什么**：数据（§15.2）之外，统计画像（09）、计划基线（SPM）、审计策略（05）、凭据与密钥（05/13）都是"随迁资产"——漏一件，新环境就带病运行；
- **何时停**：回退窗（PIT）与业务低峰的交集决定迁移方式（§15.2 停机谱）——"零停机"多数时候的正确翻译是"零计划外停机"。

- **Fleet 的开源化平行宇宙**：批量 DB 管理在 MySQL/PG 生态由 ansible collection/GitOps 承担（⚠️ 通说）——本章的 EM/dbcli 语义与"仓库里的一份 desired-state YAML"是同一治理思想两种载体，跨引擎 DBA 转岗时此映射最快建立 ⚠️ 本目录立场。
- **组织学脚注**：迁移项目的真实瓶颈排序（复盘通说 ⚠️）：连接串/凭据治理 > 停机窗谈判 > 技术路线选择——§15.2 表格好背、§15.7 登记册难落地，Pro 读者的增值在后者。

- **数据供给（data provisioning）** — 以 PDB 克隆/快照秒开新环境的开发侧流水线（11/16 章交汇）。
- **墓碑导出** — 退役库留档的"法律件"导出：对象定义+关键审计表，比全量备份更常被回看 ⚠️ 本目录语。

## 自测（能默写=过关）

- 四条迁移路线的停机谱与选择问句；12.1 遗产路径为何要划掉。
- AutoUpgrade 四模式各产出什么工件、失败重放位在哪。
- 拔插对（unplug→keep→plug）中 XML 描述件承载了哪些"库的身份证"。
- 完全可传输五步剧本的回退位设在哪。
- Fleet 三概念（组/目标值/黄金镜像）各自消灭了哪类手工。
- 风险登记册里"统计画像断层"的前置闸与回退位分别引哪两章。

**串读题**：给一批 11g 非 CDB + 一个目标 23ai CDB + 应用连接串写死 SID 三条件，产出 15 行以内的迁移方案骨架（路线表选行+前置件+验收件各一）——能写出来，本章即毕业。

## 核心概念速览（中英对照）

- **非 CDB → PDB 迁移** — migration to multitenant：遗产库进入容器轨道的总称。
- **完全可传输** — full transportable：Data Pump+跨平台表空间拷贝的整库搬家术。
- **跨平台传输** — cross-platform transportable：字节序一致/转换前提下的文件级搬迁。
- **AutoUpgrade** — 自动升级器：analyze/fix/deploy 模式序列的版本迁移指挥台。
- **Fleet** — 舰队：EM 对库/主机/中间件成员的组抽象与批量面。
- **目标值/漂移** — desired values/configuration drift：基线与现实的 diff 治理。
- **黄金镜像** — golden image/software library：版本化二进制工件的批量分发。
- **dbcli** — 基础设施 CLI：GI/Exadata 栈的数据库生命周期命令行。
- **滚动补丁** — rolling patch：组内逐成员停-打-起的时窗压缩法（→16）。
- **整合比** — consolidation ratio：迁移项目的密度验收指标。
- **PIT 回退窗** — rollback window：源库只读挂账期内的反悔通道。
- **锁定下发** — lockdown rollout：安全基线按 Fleet 组批量施加（05 章联动）。

## 最新演进与工业实践

- **ZDM（Zero Downtime Migration）工具化（⚠️ 转述）**：厂商把 §15.2 路线表产品化为迁移编排器（源库→目标平台/云的全流程+回退），2024+ 与 23ai/26ai 升级周期绑定推广 ✅（Oracle 官方迁移文档族存在，本册 /26/ 重排后深链不稳，口径 00 §2.4）；"迁移即项目"正变"迁移即流水线" ⚠️。
- **许可经济学**：多租户选项与 PDB 计数的授权策略直接影响 §15.1 第一页——整合叙事必须与许可审计同表计算 ⚠️（以官方授权指南为准，非技术文档域）。
- **上云即换轨**：大量"迁多租户"项目被"直接迁 ATP/EC2 托管"截胡——本章技能的落点从"把库搬进自家 CDB"变成"搬进云上容器"（Fleet/镜像思想被 IaC/Terraform 状态机替代 ⚠️ 通说）；盘上云仓对位见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §四互链表（Snowflake_TDG），本波兄弟 BigQuery/Redshift/Advanced Snowflake 仅演进节提及（登记见其 00 §八）。
- **数据不动应用动**：duality 视图/ORDS（08 章）给"迁移窗口内新旧并行"提供了文档 API 层的绞杀者（strangler）缝口 ⚠️ 本目录延伸观点。
