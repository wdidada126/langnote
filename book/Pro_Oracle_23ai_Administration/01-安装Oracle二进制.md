# 01 · 安装 Oracle 二进制（原书 Ch.1, pp.1-27）

> 章题 ✅ Crossref 实抓（DOI 10.1007/979-8-8688-1038-1_1, "Installing the Oracle Binaries"）。章内小节为本目录自拟重构 ⚠️，不代表原书划分。Oracle 不可本机实测：以下全部引擎行为为 ⚠️ 转述，取证 URL 见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 第二节白名单。

## 1.1 本章在全书的位阶

安装章在 Pro 管理册里不是"装软件教程"，而是**后续 17 章的地基声明**：二进制（ORACLE_HOME）、环境变量、权限模型、日志位置这四样东西决定了全书所有命令的执行上下文。原书把安装放第 1 章，读者应把本章当作"术语与目录结构的词典"反复回查。

## 1.2 版本与介质形态（23ai 时代口径 ⚠️）

- Oracle Database 23ai 是 23c 预览线更名后的 LTS（长期支持）版本，2024 年 GA。补丁模型从"PSU 大包"转为**季度 Release Update（RU）**，安装介质本身即包含到发布日的 RU ⚠️。
- 介质分层（本书语境）：
  - **Enterprise/Standard Edition**：官方下载需账号协议，Linux x86-64 为主战场；
  - **Oracle Database Free**：免费可再分发版，功能配额受限（CPU/内存/每 PDB 数据量），是个人练手与本系列 🔧 类比之外的"最接近真实"的载体 ⚠️；安装文档见 ✅ https://docs.oracle.com/en/database/oracle/oracle-database/23/ladbi/index.html（2026 年起 301 至 /26/ 同名路径）。
- 容器/云端形态：安装章不谈，但演进节必须谈——OCI/AWS RDS for Oracle/自治事务库（ATP ⚠️，文档 ✅ https://docs.oracle.com/en/cloud/paas/autonomous-database/serverless/adbsb/ ）已把"装二进制"这件事整体消灭，见 §1.7。

## 1.3 预检：OS 侧准备（⚠️ 转述官方口径）

典型清单（Administration Guide 安装章，✅ https://docs.oracle.com/en/database/oracle/oracle-database/23/admin/index.html ）：

| 项 | 要求示意 | 失败症状 |
|---|---|---|
| 操作系统版本 | 认证矩阵内的 Linux 发行版（OL/RHEL/SLES/Ubuntu LTS） | 预检器直接拦停 |
| 内核参数 | shmmax/sem 组、文件描述符上限 | 链接或启动期 ORA-271xx |
| 软件包 | glibc/libaio/compat 库组 | relink 失败 |
| 用户组 | oracle 属 oinstall；dba 组决定是否 OS 认证 | sysdba 登录异常 |
| 磁盘布局 | ORACLE_HOME 与数据/诊断盘分离 | 日志撑爆根盘 |

纪律提示：**认证矩阵（certify.oracle.com / 支持文档）优先于博客经验** ⚠️——Pro 级读者的第一习惯。

## 1.4 图形与静默安装

- 图形安装器（runInstaller/OUI）走向导：创建种子数据库 or 仅装软件、设置 ORACLE_BASE/ORACLE_HOME 层级（OFBase 结构）。
- **静默安装**是自动化世界的正门：`runInstaller -silent -responseFile db_install.rsp`，响应文件把全部向导答案参数化 ⚠️。原书倾向给出可脚本化路径，与第 14 章（自动化）呼应。
- 23ai 的 Linux 安装进一步收敛到统一包管理与简化的 rpm 路径 ⚠️（社区通说，未逐条实证，标待核验）。

## 1.5 目录结构与文件位标（全书回查表）

| 路径 | 内容 | 后章引用 |
|---|---|---|
| $ORACLE_HOME | 二进制+字典脚本+PL/SQL 包 | 09/16 |
| $ORACLE_BASE/diag | **ADR** 自动诊断库（trace/alert/log） | 14 |
| oradata | 数据文件默认落地 | 04 |
| fast_recovery_area | 闪回区/归档区 | 04/12 |
| network/admin | listener.ora / tnsnames.ora | 02/14 |
| dbs orapw*/spfile* | 口令文件与服务器参数 | 02/05 |

## 1.6 环境变量与客户端连通

`ORACLE_SID / ORACLE_HOME / PATH / TNS_ADMIN` 四件套决定 `sqlplus / as sysdba` 到底连到谁；多 HOME 共存时先查 `env | grep ORACLE` 再动手 ⚠️——这是"装完连不上"类工单的第一排查位。监听侧：`lsnrctl status`，动态注册 vs 静态注册差异在 02 建库后生效。

装完必做的五连验（⚠️ 社区共识清单，逐条可在书后各章复用）：

1. `sqlplus / as sysdba` 能进 NOMOUNT 实例或已建库 → 二进制与 OS 认证 OK；
2. `select banner_full from v$version;`（23ai 起视图口径有变，⚠️ 以 09 章字典口径为准）→ 字典脚本完整；
3. `lsnrctl status` + 从远端 `tnsping <别名>` → 网络栈 OK；
4. `opatch lspatches` / ` Datapatch 状态`（详见 16 章）→ RU 与字典对齐；
5. `adscli` 或直查 `$ORACLE_BASE/diag/rdbms/.../trace/alert_*.log` 无启动报错 → 诊断面干净。

**🔧 类比（非本书引擎行为）**：本机没有 Oracle 的可对照物只有轻量引擎——以 SQLite 为例，"二进制 vs 数据库"的边界在 Oracle 是 HOME/实例/数据库三层，SQLite 只有文件本身：

```
$ python -c "import sqlite3;c=sqlite3.connect('demo.db');print(c.execute('pragma user_version').fetchone())"
(0,)
```

`user_version` 这个 4 字节头字段充当 SQLite 世界的"版本号+迁移位"，类比 Oracle 里 `v$version`/registry$ 的角色——一个进程外可查的最小元状态。演示于 Python 3.13.2 / sqlite 3.45.3，仅为概念锚点，**非本书引擎行为**。

第二组类比（DuckDB 1.5.5 🔧，非本书引擎行为）：Oracle 的"客户端/驱动连库串"（tns 别名）在 DuckDB 里对应连接串极简——进程内直连：

```
$ python -c "import duckdb;print(duckdb.connect().sql('select version()').fetchall())"
[('1.5.5',)]
```

对比意义：Oracle 把"连到哪个实例"做成显式网络配置（listener/tnsnames），嵌入式引擎把这个问题整体取消——理解这个差异，才能明白 1.3-1.6 全部预检工作为何在 SQLite/DuckDB 世界里不存在，也才能明白为何云托管（§1.7）正把 Oracle 拉回"连接串即一切"的形态。

## 1.7 本章的 23ai 陷阱清单（⚠️ 社区经验转述）

1. 用 Free 版介质练 23ai，却按企业版文档找选项 → 参数缺省差异。
2. glibc 版本与介质不匹配：下载"latest RU 合并介质"前先看支持矩阵。
3. 防火墙/SELinux 未预检，监听器起、连接超时，误判为"数据库坏了"。
4. 同机多版本共存未设 TNS_ADMIN，客户端串库。
5. 跳过 `root.sh/rootca.sh` 后脚本，口令文件与 OS 认证行为异常。

## 1.8 装机工单案例重构（⚠️ 社区复盘通说，非原书逐字案例）

**案一：装完 sqlplus 秒连秒断。** 现场：新主机、Free 介质、向导安装。根因链：安装用户与运行用户不同 → orapw 文件属主错 → 口令文件认证回退 OS 组认证 → dba 组未含运行用户。处置：重跑 `mkstore`/重建口令文件+组整改。教训位：§1.5 表里 dbs 一行不是"文件清单"是"信任链清单"。

**案二：同机双版本互踩。** 现场：19c 生产旁装 23ai 演练库。症状：`sqlplus` 进错版本、补丁号对不上。根因：PATH 与 ORACLE_HOME 环境变量在不同 shell profile 层互相覆盖（/etc/profile.d 与用户级 ~/.bashrc 打架）。处置：统一走 `oraenv`+`/etc/oratab` 登记，禁手工 export。教训位：§1.6 四件套要进主机初始化模板，不进个人记忆。

**案三：安装器预检全绿仍 ORA-27125。** 现场：静默安装成功、建库 NOMOUNT 失败。根因：`/dev/shm` 尺寸远小于 SGA_TARGET（容器化主机常见默认 64M）。处置：OS 层扩 shm 或改 ASMM+锁页。教训位：预检查的是"许可装"，不是"能跑"——内存三章（03）的账在 01 就要还。

三案的公共结论：安装章的产出物不是"装上了"，而是**一份可交接的《主机-环境-认证基线单》**：介质版本+RU 号、目录布局、组与口令文件策略、环境变量模板、预检与五连验输出存档。下一站（02 建库）以此为输入。

## 自测（能默写=过关）

- 说出 ORACLE_BASE 分层的目的与四个关键环境变量。
- 静默安装响应文件解决的是什么运维问题？与 14 章自动化如何衔接？
- ADR 目录树里 alert log / trace / incident 三者关系（详 14）。

## 核心概念速览（中英对照）

- **二进制安装** — binary installation：只装软件不建库，产出 ORACLE_HOME。
- **OFBase 结构** — Optimal Flexible Architecture base：ORACLE_BASE/ORACLE_HOME 标准目录分层。
- **静默安装** — silent install：响应文件驱动的无界面安装，自动化基线。
- **响应文件** — response file：把向导答案参数化的 .rsp 文本。
- **Release Update** — RU：季度补丁包，23ai 时代替代 PSU 的单元。
- **Oracle Database Free** — Free：免费配额版，练手与轻量部署载体。
- **ADR** — Automatic Diagnostic Repository：diag 目录树下的统一诊断库。
- **口令文件** — password file：orapw 文件，远端 sysdba 认证依据。
- **spfile** — server parameter file：服务端持久化参数，先于 pfile 时代。
- **监听器** — listener：network/admin 配置下的连接入口进程。
- **认证矩阵** — certification matrix：OS/版本/补丁的官方兼容表。
- **环境变量四件套** — ORACLE_SID/ORACLE_HOME/PATH/TNS_ADMIN：命令行连库的上下文。

## 最新演进与工业实践

- **23ai→26ai 更名与路径重定向**（✅ 2026-09 curl 实证）：docs.oracle.com /23/ 全线 301 至 /26/，本书"23ai 基线"在 2026 年中后进入版本夹缝期；升级决策参考 Oracle LTS 政策页 ⚠️（未直抓）。
- **装二进制正在消失**：工业侧新增部署大量走 OCI Autonomous（✅ adbsb 文档线）、AWS RDS for Oracle、Azure 托管——DBA 的"安装"从 runInstaller 变成 Terraform/ora_db_system 模块 ⚠️ 通说；本册安装章的知识转化为"理解托管库底下是什么"的元能力。
- **Free 版的战略位阶**：Oracle 以 Free 替代 XE 作获客与教育入口（✅ https://www.oracle.com/database/free/ 可达），本书读者用 Free 复现大部分章节实验（容器版例外），这是 2024 后学 Oracle 管理最实际的降本路径 ⚠️。
- **容器与镜像**：官方容器镜像仓库（container-registry.oracle.com ⚠️ 转述）把"预检+安装"固化为镜像层，K8s 上的有状态数据库部署由运营商承担——Pro 册的 OS 预检清单在云原生岗位的面目缩减，但排障时仍需全量知识。
- **跨引擎对照**：本波云仓三册（BigQuery/Redshift/Snowflake，见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 第八节登记）把"安装"归零为"开账号"，运维价值从装机转向成本与数据治理——读本章时保持这个对照组，才能理解传统 DBA 技能的迁移方向。
