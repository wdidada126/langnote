# 第 2 章精读重构——安装和升级 MySQL 8

> 原书章题：Installing and Upgrading MySQL 8（⚠️ 英题回译；中题 ✅ 社区译本，取证见 [00-总览与阅读地图.md](00-总览与阅读地图.md)）。
> ✅ 官方仓库存在 `Chapter02/Ch2-commands.txt` 代码包（GitHub tree 实抓），本章是全书记录"动手起点"的实证。
> 本文件为**精读重构**；具体包名/参数以手册主题域转述（⚠️），镜像页 ✅ 200 核验：
> https://mysql.net.cn/doc/refman/8.0/en/programs.html 及 option-files/mysqld 等页。

## 2.1 本章定位

DBA 的第一块地盘：在 Linux/Windows/源码三种世界里把 mysqld 立起来，并把 5.6/5.7 存量库安全推到 8.0。
本书体裁决定它是"清单式"的——每条路径给命令、给坑位，不给原理（原理在 [../mysql/08-MySQL的数据目录.md](../mysql/08-MySQL的数据目录.md)）。

## 2.2 安装形态地图（⚠️ 手册转述 + 任务清单重构）

| 形态 | 载体 | 管理员要点 |
| --- | --- | --- |
| 发行版包 | apt / yum（MySQL APT/YUM 仓库） | 先装 mysql-community-release 再装 server；企业内网须镜像仓库 |
| 通用二进制 | mysql-8.0.x-linux-glibc2.12-x86_64.tar.xz | 手工建 mysql 用户、basedir/datadir，systemd unit 自写 |
| Windows | MSI Installer / ZIP | MSI 走向导（配置类型 DevTools/Server/Workstation）；服务账户权限是重灾区 |
| 源码 | cmake 构建 | 书时代仍可，2026 工业界几乎只用于定制补丁 |

- 初始化两种口径（⚠️）：`mysqld --initialize`（生成临时 root 密码进错误日志）与 `--initialize-insecure`（空密码，
  仅测试环境；本书示例多用后者）。8.0 数据目录不再需要手写 .mylogin 前的建目录动作，InnoDB 系统表空间随初始化生成。
- 配置体系：option 文件加载顺序（`/etc/my.cnf` → `/etc/mysql/my.cnf` → `~/.my.cnf` → datadir my.cnf，⚠️ 以
  ✅ 页 https://mysql.net.cn/doc/refman/8.0/en/option-files.html 为准），`mysqld --verbose --help` 与
  `PERFORMANCE_SCHEMA` 之外的 SET_PERSIST 差分见 [12-优化MySQL8.md](12-优化MySQL8.md)。
- 服务化：systemd 下 `Restart=on-failure`、`User=mysql`、`LimitNOFILE` 三件套（⚠️ 通行实践转述，非原书条文）。

## 2.2a Linux 通用二进制安装实操清单（⚠️ 依手册任务流重构，可当巡检底稿）

```text
1  groupadd mysql && useradd -r -g mysql -s /bin/false mysql
2  tar -xJf mysql-8.0.x-linux-glibc2.x-x86_64.tar.xz -C /usr/local/
3  mkdir -p /data/mysql/{data,log,tmp} && chown -R mysql:mysql /data/mysql
4  写 /etc/my.cnf：basedir/datadir/socket/log_error_tmpdir/inode 预算项
5  mysqld --defaults-file=/etc/my.cnf --initialize-insecure
6  systemd unit 注册 → systemctl start mysqld
7  mysql -S <socket> → ALTER USER 'root'@'localhost' IDENTIFIED BY '强口令'
8  mysql_secure_installuration 等价手工五问（匿名用户/远程 root/test 库/权限表重载）
```

- 步骤 5 的报错九成是 datadir 非空或权限位；步骤 7 后必须补 `mysql.mysqluser` 的认证插件口径（→ [11-安全.md](11-安全.md)）。
- Windows MSI 与 tar 包装的本质差异只在服务注册与 ACL，清单 1-8 语义不变（⚠️）。

## 2.3 升级路径与工具（⚠️ 转述）

1. **路线约束**：5.5 不能直升 8.0（须 5.5→5.6→5.7→8.0 逐级，官方升级手册主题，✅ 镜像页
   https://mysql.net.cn/doc/refman/8.0/en/upgrading.html）；8.0 内小版本就地升级。
2. **升级前检查**：mysql upgrade 检查工具（Shell/Docker 版，社区工具链）扫保留字、utf8mb3、查询缓存依赖、
   分区表 FK 遗留（⚠️ 清单依 8.0 手册"Notices of Obsolete Items"主题域重构）。
3. **mysql_upgrade 的命运**：8.0.16 起 InnoDB 字典就地自动升级，mysql_upgrade 转废弃、8.4 移除（⚠️+演进节 2026 修正）。
4. **降级**：官方不支持跨大版本 downgrade，8.0.16+ 数据字典前滚不可逆（⚠️）——升级窗口=单向门，回滚靠备份重放。
5. 书中场景的 2026 翻译：以上"8.0 升级"现在都应读作"8.0→8.4 迁移"：先清 mysql_native_password 账户、
   再逐项对照 8.4 移除项（⚠️ 转述，规范链接 dev.mysql.com 8.4 升级手册，本环境 403）。

## 2.4 复制环境的滚动升级剧本（⚠️ 主题域重构）

1. 顺序：**从库先升、主库后升**——复制向下兼容（新从收旧主事件流），反向不保证；GTID 环境更须守住该序。
2. 每一步的"半路上"风险窗口：主从版本混跑期间，从库上的 8.0 新类型（如新的 JSON 二进制形态）事件是否可解析——
   手册升级章要求先完成全部从库再动主库（⚠️）。
3. 回滚锚点：升级前全量备份 + binlog 位点记录（PITR 剧本见 [05-数据库管理.md](05-数据库管理.md)），
   "降级=重建从库+重放"而非换二进制（2.3 第 4 条）。
4. 灰度顺序模板：备份从 → 只读从 → 业务从 → 准主 → 主（每级观察窗口指标见 [12-优化MySQL8.md](12-优化MySQL8.md)）。

## 2.5 常见安装期事故登记（⚠️ 通行排错经验，对读第 15 章）

- 字符集默认变了但应用连接串写死 latin1 → 中文注释变问号；
- Windows 服务启动失败 99% 是 datadir 权限/被旧版占用；
- tar 包 glibc 不匹配（CentOS 6 时代经典，2026 语境=OS 基线与二进制矩阵）；
- `--initialize` 后忘记从错误日志捞临时密码，反复重装导致数据目录半初始化——8.0 会拒绝在**非空 datadir** 上初始化（⚠️）。

## 2.6 与 repo 的分工与互链

- 数据目录物理布局的中文深潜：[../mysql/08-MySQL的数据目录.md](../mysql/08-MySQL的数据目录.md)、
  [../mysql/09-表级别的操作.md](../mysql/09-表级别的操作.md)——本章只给"怎么装"，彼册给"装出来的每个文件是什么"。
- 配置变量体系源码向：[../Understanding_MySQL_Internals/05-配置变量.md](../Understanding_MySQL_Internals/05-配置变量.md)（2003 语境对照 8.0 的 my.cnf 三态：编译默认→文件→SET PERSIST）。
- 同题中文实操笔记：[../MySQLDBA工作笔记.md](../MySQLDBA工作笔记.md)（安装/升级章节与本章逐条可对读）；
  运维纵深：[../MySQL运维内参.md](../MySQL运维内参.md)。
- 升级后的"值不值"性能论证：[../Efficient_MySQL_Performance/00-总览与阅读地图.md](../Efficient_MySQL_Performance/00-总览与阅读地图.md)。
- 论文/系统语境（安装介质之外的世界观）：[../../db/db.md](../../db/db.md)。

## 2.7 本章任务清单（自测）

1. 在无外网 Linux 上离线安装 8.0 通用二进制并注册 systemd 服务；
2. 用 `--initialize-insecure` 完成初始化并改 root 密码为强口令（联动 [11-安全.md](11-安全.md) 的 validate_password）；
3. 为一个 5.7 存量库列出升级检查单（保留字/字符集/认证插件/查询缓存四必查）；
4. 说明为什么"升级失败回滚=重装+重放备份"而不是 `mysqld --version=5.7`；
5. 排出一份 1 主 2 从的滚动升级时刻表，标注每级的回滚锚点。

## 2.8 本章缺口声明

- 原书本章的确切小节编号、命令逐字清单未获（packtpub TOC 403）；`Ch2-commands.txt` 代码包存在（✅）但内容未逐行核。
- Windows/源码安装细节仅主题域重构（⚠️），OS 发行版矩阵以 2026 年现实为准（书内 OS 清单已过时：CentOS 6/7 时代）。

## 核心概念速览（中英对照）

- **datadir** — 数据目录：所有库表物理文件与元数据之家，非空即拒绝 --initialize（⚠️）。
- **basedir** — 安装根目录：二进制与共享库所在，tar 包安装三要素之一。
- **option file** — 选项文件：my.cnf 家族，加载顺序决定"谁覆盖谁"，排错第一现场。
- **--initialize** — 初始化模式：生成系统表空间与数据字典，产出临时 root 密码（insecure 变体=空密码）。
- **in-place upgrade** — 就地升级：同数据目录上大版本直推；8.0 内小版本的标准姿势。
- **logical upgrade** — 逻辑升级：mysqldump 导出→新版本导入，5.5 时代遗留库的保底路线（⚠️）。
- **mysql_upgrade** — 升级收尾程序：比对系统表并修补，8.0.16 起渐被自动字典升级取代，8.4 移除（⚠️）。
- **MSI Installer** — Windows 安装器：向导式配置角色（Server/Workstation/DevTools）并注册服务。
- **systemd unit** — 服务单元：Linux 下 mysqld 托管方式，Restart/LimitNOFILE 是可靠性关键。
- **保留字冲突** — reserved word collision：升级检查头号项，8.0 新增 GROUPING/RANK 等 SQL 标准词。
- **前滚不可逆** — forward-only dictionary：数据字典升级后无法被旧二进制读取 → 降级不受支持（⚠️）。

## 最新演进与工业实践

- **版本口径 2026**（✅ https://endoflife.date/mysql 2026-09-27 实抓）：本书的 8.0 安装指引现应平移至 **8.4 LTS**
  （发布 2024-04-30，支持至 2029-04-30）；8.0 常规支持已于 2025-04-30 结束、EOL 2026-04-30 ——
  "新装 8.0"在 2026 年等于给下一轮升级埋雷。
- **安装形态变迁**（⚠️ 转述）：官方 Docker 镜像、Oracle 的 MySQL Shell Database Administration（`dba.install()`/
  `dba.configureInstance()` 系列）与 OCI/各大云 RDS 已分流掉"裸装"场景；本书手工安装清单的价值转为
  容器/云排错时的底层理解（云 RDS 8.4 上线动态：阿里云 RDS MySQL 8.4 正式发布报道，✅ 检索命中 developer.aliyun.com/article/1734449，2026-05）。
- **mysql_upgrade 终局**（⚠️）：8.4 已无 mysql_upgrade，升级检查改由 MySQL Shell `util.checkForServerUpgrade()` 独任——
  本书 2.3 的"工具双轨"叙述只剩一轨。
- **认证与 TLS 前置**：8.4 默认停用 mysql_native_password（书成时尚为"可选增强"），安装即生成证书（`--auto-generate-certificates`
  成为默认路径）→ 安装章与 [11-安全.md](11-安全.md) 在 2026 语境下强耦合。
- **本册 🔧 缺席说明**：安装/升级动作无法在 SQLite/DuckDB 上类比（无服务器进程模型），按纪律**如实 ⚠️**，
  类比实测义务在 04/05/07/08/09/11/15 各章兑现（≥4 组，见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 第六节）。
