# 09 · Development SQL（Ch9 · 静态/动态双轨与程序化 SQL）

> 章名 ✅ InformIT 出版社页实抓；正文 ⚠️ 转述重构。预编译/绑定语义按 IBM 公开文档口径。

## 一、章定位

本章把"SQL 怎么写进程序"讲成 DBA 必修课：DB2 独有的**静态 SQL 预编译+绑定成包**路线与应用侧动态 SQL 路线并存；SQLCA/SQLDA 的宿主接口、SQL PL 的过程化扩展、EXPLAIN 工具链。它同时是 14 章"包缓存/段调优"与 15 章"驱动选型"的前置。

## 二、静态 vs 动态 SQL（⚠️ 转述）

1. 动态：应用提交语句文本，引擎现解析现优化；灵活但每次付编译成本（受 SQL cache 缓解），权限运行时查。
2. 静态：预编译期固化语句，绑定成**包（package）**存于库目录；权限在建包时定格（"以包定义者权运行"语义）；升级需重绑（REBIND）。
3. 混合现实：C 嵌入 SQL（`.sqc`）+ COBOL/ Fortran 静态传统仍在金融存量；Java/JDBC 几乎全动态；SQL PL 存储过程体内部语句属"服务端预编译"（⚠️ 措辞保守）。
4. 认证眼：`BIND` 参数 `RELEASE(BIND|CLOSE|DEALLOCATE)` 决定包在断连后存留——连接池时代默认 CLOSE 习惯。

## 三、预编译与绑定流水线（⚠️ 转述）

```text
prep prog.sqc  # 预编译+生成绑定文件（旧式合一）
# 或
db2预编译 prog.sqc → prog.bnd（绑定文件）
db2 bind prog.bnd BLOCKALL ALL YES GRANT PUBLIC
db2 "select pkgname, pkgcreatetime from syscat.packages"
# 重绑：db2 "rebind <collid>.<pkgname>"
```

- 集合标识符（collection ID）≈包命名空间；`SYSCAT.PACKAGES/SYSCAT.SECTIONS` 为治理视图。
- `BLOCKALL ALL`（一次会话级块）vs `NO` 是游标跨语句行为开关（⚠️ 细节以现行核）。
- 变更表/临时表等语法在预编译期同样校验——静态路线的早期纠错红利。

## 四、宿主接口件（⚠️ 转述）

- SQLCA：SQLCODE + SQLERRM/SQLERRP 的诊断金三角；SQLCODE 0/100/>0/<0 三段判读是 731 必考点。
- SQLDA：描述区，列元数据与宿主变量绑定的数据结构；动态 SQL 用 `DESCRIBE` 填充。
- 主机变量声明区 `BEGIN DECLARE SECTION`；指示器变量处理 NULL。
- 错误面：SQL0204N（对象不存在）、SQL0911N（锁/死锁被回滚，→10 章）、SQL16067 系 XML（→08 章）——原书按码讲解，读时做成个人码表。

## 五、SQL PL 与服务端例程（⚠️ 转述）

1. 对象：函数/过程/方法，`CREATE PROCEDURE ... LANGUAGE SQL`；外部例程 `LANGUAGE C/JAVA` 挂 ODRIVER?（⚠️ 保守）。
2. 语言面：变量/控制流/游标/条件处理器 `DECLARE ... HANDLER FOR SQLEXCEPTION`。
3. Java 存储过程经 JDK 在实例内嵌 JVM（`DB2_JDK_PATH` 系 ⚠️ 运维细节）。
4. 模块（9.5，05 章呼应）：例程的命名容器与重载定位。
5. 触发器：BEFORE/AFTER/INSTEAD OF（视图），FOR EACH ROW 与过渡变量；触发器内禁动态类限制逐版漂移（⚠️）。

## 六、EXPLAIN 工具链（与 14 章接口）

- 建立 `EXPLAIN` 实例表：`db2exinst`?（⚠️ 脚本名保守：原书以 `EXPLAIN` 语句+样例表讲述）。
- 用法：`db2 "explain plan for <sql>"` 后格式化 `db2exfmt -d demo -1 0 -o plan.txt`。
- 读计划四问：访问方式/连接方式/物化(temp)操作/基数与成本来源（统计新鲜度 →12 章）。
- `db2expln` 即时图形/文本面适合交互式；`section` 级成本进包后可用于段调优（14 章）。

## 七、易错雷点（例题库精华）

1. 预编译用了新语法但绑定环境是旧 FP——"包版本漂移"故障。
2. `RELEASE(BIND)` 与连接池混用导致包句柄泄漏/目录膨胀。
3. SQLCODE=100（NOT FOUND）误当错误分支——游标语义经典题。
4. 静态包权限在迁移后失效：GRANT 随包重建（SECADM，→04 章）。
5. SQL PL 异常处理器吞 SQLCODE 不回传应用——诊断链断裂。
6. 动态 SQL 拼串未走参数标记：性能（缓存命中）+安全双输（注入面参见波内 #51 登记名）。

## 八、自查问题

- 静态 SQL 的权限定格语义与动态的运行时检查各举一个运维后果。
- BLOCKALL/RELEASE 两参数分别管什么生命周期？
- 说出 SQLCA 三字段与 SQLCODE 三段判读。
- 动态 SQL 何时必须 DESCRIBE？（无固定结构场景）
- SQL PL 处理器与 CLI 错误分支的责任边界设计？
- REBIND 的触发场景列举三个（版本升级/统计变更/依赖对象重建 ⚠️ 口径）。
- EXPLAIN 四问中"基数来源"依赖哪两个统计对象？（→12 章）

## 十、SQLCODE 速读表（本章例题库核心，⚠️ 码值以现行手册核）

| SQLCODE | 含义 | 归属层 | 首查动作 |
|---|---|---|---|
| 0 | 成功 | — | — |
| 100 | 无行（NOT FOUND） | 游标语义 | 判循环终点，非错误 |
| -204 | 对象不存在 | 目录/编目 | 03 章编目面+schema 折叠 |
| -206 | 列名非法 | SQL | DESCRIBE 列名核对 |
| -407/-408 | NOT NULL/约束违例 | 完整性 | 05 章约束与装载裁决 |
| -530/-531 | 外键父/子违例 | 完整性 | LOAD FKCONSTR（06 章） |
| -668 | 表态挂起 | 工具态 | SET INTEGRITY/LOAD 续 |
| -911 | 锁/死锁回滚 | 并发 | 10 章观测三板斧 |
| -1006/-1007 | 内存/堆类 | 资源 | 14 章 sortheap/锁内存 |
| -803 | 唯一索引重复 | 完整性 | 异常表 DUPKEY（06 章） |

- 读法：正数=警告族、0=成功、-1xx 以下按"目录/完整性/并发/资源"四族归档——731 与面试都按族考。

## 十一、快速回看卡（本文件内导航）

- 双轨分野一句话：静态=编译期固化+权限定格；动态=运行期提交+缓存缓解（第二节）。
- 流水线四命令：PRECOMPILE→绑定文件→db2 bind→REBIND（第三节块）。
- RELEASE/BLOCKALL 两参数的生命周期管辖（第三节第 4 条 + 雷点 2）。
- SQLCA/SQLDA 分工：诊断回传 vs 元数据描述（第四节）。
- SQL PL 处理器边界：库内异常吞与吐的设计题（第五节 2 条 + 雷点 5）。
- EXPLAIN 四问：第六节——本章与 14 章共用同一把读计划钥匙。
- 注入防线衔接：动态拼串纪律在第六节雷点 6，安全双线另见 #51 登记名。

## 核心概念速览（中英对照）

- **static SQL** — 静态 SQL：预编译期固化的语句
- **dynamic SQL** — 动态 SQL：运行时提交的语句文本
- **PRECOMPILE/BIND** — 预编译/绑定：生成包的两段流水线
- **package** — 包：静态语句+权限+计划的目录载体
- **collection ID** — 集合标识符：包命名空间
- **REBIND** — 重绑：不改语句刷新包对象
- **SQLCA** — SQL 通信区：SQLCODE/错误文本回传结构
- **SQLDA** — SQL 描述区：列元数据接口
- **host variable** — 宿主变量：程序与 SQL 的绑定点
- **indicator variable** — 指示器变量：NULL 的宿主表示
- **SQL PL** — SQL 过程语言：DB2 服务端过程化扩展
- **handler** — 条件处理器：异常/警告的声明式分支
- **db2exfmt** — EXPLAIN 格式化器：计划可读化

## 最新演进与工业实践

- 2024–2026：嵌入预编译路线在 Db2 仍受支持但新项目几乎清零；服务端 SQL PL 持续增强（PL/SQL 兼容包、Db2 11.5 的 SQL 函数丰富），Java 存储过程让位于应用层+函数计算（⚠️ 转述；入口 ✅ https://www.ibm.com/docs/en/db2 ）。
- 动态 SQL 缓存与语句监视现代化：`SYSPROC.MON_GET_SECTION` 系+Statement Cache 治理成"新 SQL 调优面"（14 章演进呼应）。
- PL/SQL 生态位之争：Db2 对 Oracle PL/SQL 兼容模式（11.x 迁移包）承接去 O 工程——本章的 SQL PL 语法是兼容层的地基（⚠️ 趋势转述）。
- 跨引擎镜像：PG 的 PL/pgSQL、SQL Server 的 T-SQL 批与包文化对照——见 [../SQL_Server_2012_Internals/00-总览与阅读地图.md](../SQL_Server_2012_Internals/00-总览与阅读地图.md) 计划缓存章。
- 备考：731 静态绑定域已退役；Db2 11.1 认证仍以动态 SQL/存储过程为主（`IBM_Db2_11_1_Certification_Guide` 登记名，见 00 文件）。
