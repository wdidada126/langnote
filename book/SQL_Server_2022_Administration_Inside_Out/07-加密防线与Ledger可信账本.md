# 07 加密防线与 Ledger 可信账本（目录版 · 精读重构）

> ⚠️ 主题重构章（取证降级见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 第三节）。SQL Server 不可本机实测：全章"转述 + ⚠️"，✅ Learn 验真 URL 为准绳；SQLite 加密生态（可选扩展）仅作反衬注记，类比义务见 03/04/05/08 章 🔧。

## 本章地图

1. 加密分层总图：数据在盘/在途/在用/在账
2. TDE：透明数据加密的证书链与运维坑
3. Always Encrypted：客户端加密与密钥托管谱系
4. Backup Encryption 与列级加密的补位
5. SQL Server 2022 Ledger：防篡改账本的工程学
6. 密钥灾难演练：加密体系的"备份的备份"

## 一、加密分层：别把四层压成一层

- 四层心智 ⚠️：**静态加密**（盘/文件级，TDE）、**传输加密**（TLS 通道）、**细粒度数据加密**（列级：AE/细胞级 CMK）、**证明加密**（完整性方向：Ledger/哈希链）——四层的责任主体、密钥位置、故障模式完全不同。
- Inside Out 式追问："密钥在哪？谁轮换？丢了谁负责？"每层三问，本章按三问展开 ⚠️ 体例注。
- 与权限层关系：加密**不替代**访问控制（06 章）——TDE 防"搬走磁盘文件"，不防合法登录者 SELECT ⚠️。

## 二、TDE：数据库文件的"黑匣子"

- 官方机制 ✅ https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/transparent-data-encryption：数据库级 DEK（Database Encryption Key）加密数据文件页；DEK 由服务器级证书保护；证书私钥的密码保护与备份是体系命门。
- 运维三坑 ⚠️ 转述：① 证书/私钥备份丢失=库变砖（灾难恢复时目标实例必须先恢复证书）；② 备份文件随库加密——把加密库的备份拷到无证书环境不可还原（合规友好，误操作也友好）；③ TDE 开启有扫描成本，大库安排在维护窗口并盯日志进度 ⚠️。
- 与 AG 的交互：副本端要有同一证书（或相应密钥迁移流程）⚠️——衔接 [05-高可用与灾难恢复AlwaysOn.md](05-高可用与灾难恢复AlwaysOn.md)：加密让切换脚本多一步密钥检查。
- Always On/备份压缩/TDE 三者组合的性能账 ⚠️：加密吃 CPU 换磁盘面安全，现代 CPU AES-NI 摊薄成本 ⚠️ 转述。

## 三、Always Encrypted：应用侧的"零知识"尝试

- 官方机制 ✅ https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/always-encrypted-database-engine：列密钥（CEK）在**客户端**加解密，引擎只见密文；列密钥本身由主密钥（CMK）保护——CMK 放证书或 Azure Key Vault。
- 两种加密型：确定性（可等值查询/索引）vs 随机性（更强但查询面受限）⚠️——选型=查询需求与泄露面的拉锯。
- Enclave（安全区）扩展：Always Encrypted with secure enclaves 让部分运算进可信区，缓解"密文上没法查"⚠️ 转述（VBS/SGX 路线文档演进中）。
- AKV 集成缓存（Integrated Caching）把云 HSM 密钥访问的往返降下来 ✅ 概念页 ⚠️（专页 URL 当前 404，弃引；以 AE 主页为准绳）。
- 责任重分配是 AE 的管理学本质：DBA 丢"看见明文"的权力，密钥归应用/安全团队——组织流程要跟得上 ⚠️。

## 四、Backup Encryption 与列级补充

- `BACKUP ... WITH ENCRYPTION`（算法+服务器证书/非对称密钥）✅ 概念在备份文档域，专页不可达 ⚠️（backup-devices 主页 ✅ 可作入口 https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/backup-devices-sql-server）。
- 与 TDE 的互补：备份加密管"离开实例的文件"，TDE 管"在实例里的库"——全链闭合需要两把锁 ⚠️。
- 哈希与完整性原语：SHA-2 族在对象定义/签名中的应用（`HASHBYTES`）⚠️——Ledger 之前夜的土法防篡改。

## 五、Ledger：2022 的"防篡改录像机"

- 官方定位 ✅ https://learn.microsoft.com/en-us/sql/relational-databases/security/ledger/ledger-overview：内置**篡改可证（tamper-evident）**机制——账本表维护双序列（当前态+历史态），每行配密码学摘要与 Merkle 树式累积根，配合事务日志保证"链上历史不可抵赖"。
- 两类账本表 ⚠️ 转述：SEQ Ledger（可 INSERT/UPDATE/DELETE，历史自动追加）与 APPEND_ONLY（禁改禁删）——分别对应"业务会改但留痕"与"日志式只追加"。
- 取证动作：`LEDGER_VIEW()` 摊开历史+哈希链；外部公证（blockchain proof/notary 路线）把根摘要锚到链上/第三方，实现"连 SQL Server 自己都不能悄悄改"⚠️。
- 管理面成本 ⚠️：账本表有额外写入放大与存储（历史副本），索引与容量规划接 [03-数据库存储与文件组管理.md](03-数据库存储与文件组管理.md)；备份/AG/审计链路与普通表同形但恢复后要做链验证 ⚠️ 转述。
- 适用画像：财务台账、法务证据、供应链记录、医疗变更史——"审计要的是可证明未改，不是不可改"⚠️ 观念句。

## 六、密钥灾难演练清单（本章的"备份的备份"）

1. TDE 证书+私钥备份的**异地还原演练**（在新实例上恢复证书→挂载加密库）⚠️。
2. AE 的 CMK 访问权轮换演练：证书过期/人员变动后应用能否继续解密 ⚠️。
3. 备份加密证书的"双人保管"流程（密钥与备份分道）⚠️。
4. Ledger 链验证脚本纳入季度 DR 演练（还原后 `LEDGER_VIEW` 抽查+根比对）⚠️。
5. 所有密钥物料纳入密码清单台账，与 10 章作业日历绑定 ⚠️。

## 七、与其他章/其他笔记的联系

- 权限与身份前提 → [06-安全主体与权限体系.md](06-安全主体与权限体系.md)；备份链上的加密件 → [04-备份还原与恢复模型.md](04-备份还原与恢复模型.md)。
- 审计观测面（Security 类 XEvents 会话）→ [08-监控排障DMV扩展事件与查询存储.md](08-监控排障DMV扩展事件与查询存储.md)。
- 反衬教材：SQLite 默认无库内加密（盘上明文，加密靠可选扩展/整盘方案）——"引擎不管密钥"的极简形态恰能看清 TDE/AE 各层在解决什么问题 → [../The_Definitive_Guide_to_SQLite_2e/00-总览与阅读地图.md](../The_Definitive_Guide_to_SQLite_2e/00-总览与阅读地图.md)（注：非本书引擎行为，仅结构对照）。
- 同波安全册（#51 Database Hacker's Handbook）落盘后与本章互链，波尾主代理处理。

## 八、常见坑清单（⚠️ 转述整理，非原书条文）

1. **TDE 开了就删证书**：DEK 保护链断裂，库直接不可用——证书生命周期与库同寿 ⚠️。
2. **私钥备份不设密码/密码也同箱**：加密只是把"明文泄露"升级成"整箱丢失" ⚠️。
3. **AG 副本没同步证书**：故障转移瞬间库变砖（TDE 库尤其）——切换脚本缺密钥检查步骤 ⚠️。
4. **确定性加密列被建索引后当"随机"**：等值可查=频率可推断，泄露面在选型时已注定 ⚠️。
5. **AE 换驱动忘了列密钥提供程序配置**：应用突然全量解密失败，密钥没变、通道变了 ⚠️。
6. **Ledger 表当审计日志无限追加**：历史副本写入放大×2 起，容量与备份窗口没预算（03/04 章联动）⚠️。
7. **把"可证未改"当"不可改"**：Ledger 是篡改**可证**不是篡改**免疫**——DBA 仍可物理还原旧备份分叉账本，须靠链锚/公证收口 ⚠️（官方语义以 ✅ ledger-overview 页为准）。

## 九、四层防线速查卡（⚠️ 示意）

| 层 | 武器 | 密钥在谁手 | 防的是 |
| --- | --- | --- | --- |
| 盘 | TDE | 实例证书链 | 文件被搬走 |
| 途 | TLS | 服务器证书 | 链路窃听 |
| 用 | AE/CMK | 应用/HSM | DBA 肉眼可见 |
| 账 | Ledger | 链锚/公证 | 事后悄悄改 |

- 讲给业务方的一句话 ⚠️：四层各管一段事故剧本，缺层的代价在取证那天显形。

## 十、本章回看自测

- DEK 与证书的保护关系？证书丢了会发生什么？（二/八·1）
- 确定性 vs 随机加密的选择轴？（三）
- 为什么 AE 本质是"责任重分配"？（三末条）
- SEQ 与 APPEND_ONLY 各配什么业务？（五）
- "备份的备份"演练清单里 TDE 演练的最小闭环？（六·1）

## 十一、复现与延伸（可选自修）

- 🔧 反衬小实验（SQLite，非本书引擎行为）：`sqlite3 file.db ".read dump.sql"` 前后直接 `strings file.db | grep -i secret`——明文裸奔的直观恐吓，反推 TDE（盘）与 AE（列）分别堵哪个洞；再对同库做 `VACUUM INTO`（04 章 E5）想"加密库的备份文件是否自带密文形态"。
- 延伸阅读：TDE/AE/Ledger 三官方页（见第二/三/五节 ✅ URL）；Ledger 的"可证未改"与哈希链理论可回看 [../../db/db.md](../../db/db.md) 密码学条目方向（指路级 ⚠️，DOI 未逐条核验）。
- 自修题三则：① 画出 DEK→证书→私钥备份→异地保管的责任链，标出单点（→二节）；② 确定性加密列在 BI 导出时的泄露面推演（→三节/06 章五节）；③ 为什么链锚必须离开本实例才谈"不可抵赖"（→五节/八·7）。

## 核心概念速览（中英对照）

- **TDE** — Transparent Data Encryption：库文件级静态加密，DEK+服务器证书双环。
- **DEK** — Database Encryption Key：逐库加密密钥，被证书保护。
- **Always Encrypted** — 客户端列级加密：引擎零知识，CEK/CMK 双层密钥。
- **确定性/随机加密** — Deterministic vs Randomized：可查性与泄露面的取舍档。
- **Secure Enclaves** — 安全区：密文上受限运算的可信执行延伸。
- **Azure Key Vault** — 云 HSM 密钥托管：CMK 外置与轮换的现代归处。
- **备份加密** — Backup Encryption：离开实例的文件的独立锁。
- **Ledger 表** — SQL Server 2022 Ledger：双序列+密码学链的防篡改账本。
- **SEQ / APPEND_ONLY** — 账本表两型：可改留痕 vs 只追加。
- **LEDGER_VIEW** — 账本视图函数：摊开历史行与哈希链的取证入口。
- **Merkle 根** — 摘要树根：批量行完整性的单点锚。
- **公证/链锚** — Notary/Blockchain Proof：把根摘要交给第三方或链上作证。
- **密钥轮换** — Key Rotation：证书/CMK 到期治理的运维节拍。

## 最新演进与工业实践

- Ledger 文档线 2024–2026 持续维护 ✅（ledger-overview 页 200 验真）；工业采用集中在强监管行业试点，通用 OLTP 渗透仍低 ⚠️ 转述。
- "BYOK/ HYOK"成主流密钥策略：密钥所有权向客户 HSM/KMS 收拢，AE+AKV 是落地模板 ⚠️ 转述；Azure SQL/托管实例的同类机制反向影响本地版本路线 ✅ What's new 页 https://learn.microsoft.com/en-us/sql/sql-server/what-s-new-in-sql-server-2022。
- 合规驱动组合拳：TDE+备份加密+RLS/脱敏+Audit 会话，映射到等保/SOX/PCI 条款的对照表成为交付物常态 ⚠️。
- 开源对照：PG 的 pgcrypto/TDE 路线图（长期争议）、MySQL 的 tablespace keyring 体系 → [../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md](../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md)、[../MySQL_8_Administrators_Guide/00-总览与阅读地图.md](../MySQL_8_Administrators_Guide/00-总览与阅读地图.md)；SQLite 加密扩展生态对照 → [../Using_SQLite/00-总览与阅读地图.md](../Using_SQLite/00-总览与阅读地图.md)。
- 密码学边界声明 ⚠️：本章只登记机制与运维责任，不评算法强度；论文线可回看 [../../db/db.md](../../db/db.md) 的相关条目与区块链锚定文献（书名级指路，DOI 未逐条核验）。
