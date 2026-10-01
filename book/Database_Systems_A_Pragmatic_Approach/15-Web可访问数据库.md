# 15 Web 可访问数据库（原书第 25 章）

> 书目：《Database Systems: A Pragmatic Approach》，Elvis C. Foster & Shripad V. GodBole，Apress 2014，章 DOI `10.1007/978-1-4842-0877-9_25`（pp.403–412）。
> 证据级：章题/页码/DOI/首段 ✅ 一手；展开 ⚠️ 重构（Web 技术栈年代细节不回推原书）；🔧 类比仅 SQLite/DuckDB，**非本书行为**。

## 1 本章定位与摘要逐字锚

Division 五收束章，全书"数据库作为资源"叙事在互联网侧的兑现。首段（✅）：

> "Another new area of database systems that has become widespread since the 1990s is Web-accessible databases. The proliferation of these databases is strongly correlated to the growth of the World Wide Web (WWW or W3); both phenomena have become part and parcel of…"（截断）

10 页体裁=名词巡礼。⚠️ 重构的"标准目录"（同年代教材通行）：

- **形态谱**：静态页→CGI→服务器脚本（PHP/ASP/JSP）→应用框架 MVC→三层 Web 架构（呈现/业务/数据，回收 ch20/22）。
- **连接之道**：DB 驱动层（ODBC/JDBC/原生 API）与**连接池**——高并发下"每请求一连"的死刑与池化救赎。
- **动态内容**：查询串→SQL 参数化（⚠️ 本册是否点 SQL 注入名未取证——2014 教材普遍有，按惯例登记待考）。
- **平台搭子**：LAMP（回收 ch19 MySQL 的生态位）、托管/虚拟主机时代的部署。
- **会话与状态**：cookie/session 上的"数据库外扩"，状态入库的权衡。

## 2 技术考古注记（⚠️ 时代对照，非原书断言）

- 2014 年教材的"Web 数据库"栈在 2026 已全部化石或转世：CGI→函数计算；单体 PHP 框架→前后端分离+API 网关；JSP/ASP→React/Vue；会话文件→Redis/JWT（盘上 Learning_Redis 域 ⚠️ 不展开）。
- **不变量**是本章真正的教学资产：三层分离、连接复用、参数化查询、"无状态 HTTP 与有状态数据的接缝设计"——每一条都活到今天。

## 3 🔧 类比观察（非本书行为）

- **Web×嵌入式的 2026 新形态**（E8/E6 复用）：SQLite 作"进程内网站数据库"、DuckDB 在服务端做分析微 API——ATTACH 双库联邦（E8b 跨库 JOIN 出 `[('left','right')]`）演示"多租户=多文件"的极简 Web 后端模型；目录可查性（E6 `sqlite_master`/`duckdb_columns()`）则支撑"schema 驱动前端表单"——本章"Web 访问数据库"主题的最小当代标本。
- ⚠️ HTTP 服务本身不在本工作区实测范围（零新装红线，不启服务）；登记为概念类比。

## 4 与本书其他章的接线

- ←ch19（MySQL 的 LAMP 语境）、←ch20/ch22（前端与三层）、←ch13（Web 场景里视图=权限切片更刚需）、←ch21（DBA 支持"网站团队"的新职能面）。本章是全书"环境论"的最大外延：**访问者从组织内用户变成匿名全网流量**。

## 5 对位阅读（实链，已验名）

- [../Databases_Illuminated_4e/14-NoSQL与大数据.md](../Databases_Illuminated_4e/14-NoSQL与大数据.md)：同代教材把本章后半直接换代成 NoSQL 叙事——两册并读即"2014 Web 栈的分岔"。
- [../Database_Modeling_and_Design_5e/09-XML与Web数据库.md](../Database_Modeling_and_Design_5e/09-XML与Web数据库.md)：同年代教材的"Web 数据库"兄弟章（XML 路线对照，波2 #11）。
- [../设计数据密集型应用/02-数据模型与查询语言.md](../设计数据密集型应用/02-数据模型与查询语言.md)：Web 规模下读写模型的正典讨论。
- [../Seven_Databases_in_Seven_Weeks_2e/00-总览与阅读地图.md](../Seven_Databases_in_Seven_Weeks_2e/00-总览与阅读地图.md)：Web 时代数据库多元生态的巡礼本（盘上波3 域册，00 统一约定名终检复验）。

## 6 教学与实操要点

1. 用"五化石一 invariant"法读本段：CGI/会话文件/单体模板/DB 直连托管/FTP 部署五个化石+四层不变量（表示-逻辑-访问-存储）。
2. 安全补课清单（本书级缺口）：注入、最小权限账号、连接串保密、备份脱敏——2026 版 Web 数据库第一章永远是 OWASP Top10。
3. 给同学讲连接池：一条 `SELECT count(*) FROM pg_stat_activity`/`processlist` 观感>千言（⚠️ 不可实测，文档口径）。

## 7 深挖与自测

### 概念辨析十问
1. "强相关于 WWW 增长"（✅ 摘要）的因果链？——浏览器=通用瘦客户端→数据服务化→DB 上移服务端。
2. CGI 与服务器脚本的分界？——每请求新进程 vs 进程常驻——连接池叙事的起点。
3. 连接池池的是什么成本？——TCP+认证+会话初始化+引擎侧内存——高频短请求的放大器。
4. 参数化查询为何是"语义级"防御？——把值与代码在协议层分离（预编译计划不掺值）。
5. 三层 Web 架构与 ch22 三层是同一物吗？——同一分层的两种行业口径（呈现/业务/数据）。
6. 会话存哪三选项？——DB/内存/客户端令牌——状态与可伸缩的三角权衡。
7. LAMP 为何与 ch19 MySQL 同章出现？——开发生态捆绑：教材的"产品×场景"配对 ⚠️ 推断。
8. 本册未讲的 Web DB 大件？——ORM、读写分离、缓存层、多租户 schema 策略——2026 必读 DDIA。
9. "匿名全网流量"改变了 DB 的什么假设？——峰值突发+不可信输入+慢查询攻击面——可用性/安全权重暴涨。
10. Serverless 后本章词汇还剩多少？——连接池换了宿主（Proxy 层/按计费收敛），其余全部存活。

### 常见误区六条
- 字符串拼 SQL 的肌肉记忆——参数化是底线不是优化。
- 每请求新建连接"简单可靠"——池化+限流才是简单；裸连是雪崩燃料。
- 把 ORM 当银弹——N+1 与批量写入需 SQL 层自觉（回收 ch12 集合式思维）。
- 缓存层独立于建模——热点查询形状决定缓存键——库与缓存是一家。
- Web 安全=注入一项——越权（回收 ch13 视图切片）/信息泄露/备份暴露同样致命。
- 用 2014 技术名词背题——PHP 模板/CGI 之外全换代；背"不变量"才保值。

### 🔧 加餐：嵌入式 Web 后端标本（非本书行为）
- E8b：多文件 ATTACH=多租户/分库路由的最小演示。
- E6：sqlite_master 可查性=schema 驱动表单/接口的元数据底座。
- 登记：本工作区不启 HTTP 服务（零新装红线）——以上为概念类比。

### 一分钟版
- 10 页=一段互联网考古+四条不过时不变量（分层/复用/参数化/状态分离）。
- 本章 2026 书名应叫"API 后面的数据库"。

## 8 术语快卡与跨书对位

| 术语 | EN | 一句话定位 |
|---|---|---|
| CGI | Common Gateway Interface | Web 触库的最老一层皮 |
| PHP/ASP | 服务端脚本 | 本书时代的网页绑库主流 |
| JDBC/ODBC | Java/通用驱动 | 统一 API 下藏方言 |
| 连接池 | Connection Pool | 复用昂贵连接 |
| SQL 注入 | SQL Injection | 动态拼串的原罪 |

**跨书对位（盘上已验证目录）**：
- 参 [设计数据密集型应用](../设计数据密集型应用.md)：Web 规模下的数据系统权衡。
**速测**：合上书，给"参数化查询根治注入"配一个 2026 技术栈。

**速测**：合上书，用一句话向同事讲清本册最难的概念；讲不清就回到 §7 误区清单重读。

**快验证问答（补）**

- Q：CGI 的致命伤？A：每请求一进程，开销大。
- Q：连接池怎么权衡？A：上限、排队等待、超时回收三者折中。
- Q：为何双保险转义仍不建议？A：注入面太多，参数化是唯一标准答案。
- Q：2026 替代 PHP+MySQL 两件套的？A：仍大量存在，新增主线是 API 服务+云托管库+ORM。
- Q：REST 与 SQL 的关系？A：资源层掩盖查询细节，安全交给认证。
- Q：本书"第三波前置端"的现代对应？A：Serverless+托管数据库。
- Q：读多写少先做什么？A：先缓存，再谈直连。
- Q：Web 规模的库侧答案？A：读写分离、分片与托管列存。

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
|---|---|---|
| Web 可访问数据库 | web-accessible database | ✅ 摘要题词：DB 经浏览器暴露 |
| CGI/服务器脚本 | CGI / server-side scripting | 动态页两代技术 |
| 三层 Web 架构 | three-tier web architecture | 呈现/业务/数据 |
| 连接池 | connection pool | 昂贵句柄的复用器 |
| 参数化查询 | parameterized query | 注入的第一解药 |
| LAMP | Linux-Apache-MySQL-PHP/Python/Perl | 2000s 默认全栈 |
| 无状态/有状态 | stateless HTTP vs stateful data | 会话难题之源 |

## 最新演进与工业实践

- **API-first 与 Serverless**：REST/GraphQL/gRPC+函数计算取代脚本直连；托管数据库（Supabase/Firebase/Aurora Serverless）把"Web 数据库"合成一个 SDK——本册名词整体转世。
- **边缘与嵌入式回归**：SQLite 在浏览器/边缘运行时（WASM/移动 App 后端）二次创业——✅ https://www.sqlite.org/json1.html（200，JSON 即 Web 数据交换的存储层化）。
- **注入防御工程化**：ORM/prepared statement 成默认、WAF/参数审计成运维项；本工作区盘上波7 #51 Database Hacker's Handbook 恰是本章暗线的深度对应（目录在册，挂点供波尾回链）。
- ⚠️ 托管平台的容量/成本叙事超出本册视野——盘上 [../Amazon_DynamoDB_TDG](../Amazon_DynamoDB_TDG/00-总览与阅读地图.md) 域与云仓文档为续读方向（00 文件名统一约定，终检复验）。
