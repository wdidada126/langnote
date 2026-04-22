# oracle
# Oracle 临时表、分区表 超清晰概念解析
用开发易懂、面试能背、工作能用的方式讲，不绕官方废话。

---

## 一、Oracle 临时表（Temporary Table）
### 1. 什么是临时表？
临时表 = 只在当前会话/事务生效，数据临时存放，断开连接自动清空、不占永久表空间的表。

Oracle 临时表表结构是永久的，只有数据是临时的。
不像 MySQL 临时表，断开连接连表结构都没了。

### 2. 两种类型（最重要）
#### ① 会话级临时表（ON COMMIT PRESERVE ROWS）
```sql
CREATE GLOBAL TEMPORARY TABLE temp_user(id number)
ON COMMIT PRESERVE ROWS;
```
- 提交事务（commit）数据不删除
- 直到断开会话/关闭连接才自动清空
- 多个会话互不干扰，各自数据独立

#### ② 事务级临时表（默认）
```sql
CREATE GLOBAL TEMPORARY TABLE temp_user(id number);
```
- 一执行 `commit` / `rollback`，数据立刻清空
- 用完即丢，最常用

### 3. 临时表特点
1. 数据存在临时表空间 undo/temp，不占业务永久表空间
2. 不同会话插入的数据互相隔离、看不见对方
3. 断开连接自动清空，不用手动 delete
4. 可以建索引、主键、约束、视图
5. 不产生 redo 日志，插入速度极快
6. 不能做外键关联主表

### 4. 适用场景
- 复杂 SQL 中间结果暂存
- 存储过程/函数内部临时计算数据
- 大批量数据临时处理、分页、统计
- 避免创建永久中间表污染业务库

### 5. 常见误区
- ❌ 临时表不是速度快，是不写日志、不持久化
- ❌ 不是全局共享表，是会话隔离
- ❌ truncate/drop 临时表结构没用，断开数据就没了

## 二、Oracle 分区表（Partition Table）
### 1. 什么是分区表？
一张超大业务表，按规则切成很多个小物理分区，
对外看起来还是一张完整的表，SQL 完全不用改。

逻辑上：一张表
物理上：N 个独立分区文件

### 2. 为什么要用分区表？（解决什么问题）
单表数据量过大（千万/亿级）：
1. 查询变慢（全表扫描）
2. DML 更新慢
3. 备份、归档、删除极慢
4. 索引失效、维护困难

分区表优势：
- 查询只扫对应分区，不用全表扫描
- 删除历史数据直接删分区，秒完成（不用 delete）
- 分区独立维护、独立索引、独立表空间
- SQL 写法和普通表完全一致，业务零改造

### 3. Oracle 4 种常用分区类型（面试必考）
#### ① 范围分区 Range Partition（最常用！按时间）
按日期、数字范围切分
例：按月、按年分区订单表
```sql
PARTITION BY RANGE (create_time)(
    PARTITION p202501 VALUES LESS THAN (TO_DATE('2025-02-01','yyyy-mm-dd')),
    PARTITION p202502 VALUES LESS THAN (TO_DATE('2025-03-01','yyyy-mm-dd'))
);
```
适用：订单、日志、流水表（时间维度）

#### ② 列表分区 List Partition（按枚举值）
按字段固定值分区
例：按地区、状态、渠道分区
```sql
PARTITION BY LIST (status)(
    PARTITION p_wait VALUES ('0'),
    PARTITION p_success VALUES ('1'),
    PARTITION p_fail VALUES ('2')
);
```

#### ③ 哈希分区 Hash Partition（均匀分散）
字段 hash 取模，均匀分到 N 个分区
适合没有时间、没有规律，只想打散数据

#### ④ 复合分区（组合）
范围+列表、范围+哈希
例：先按年范围，再按渠道列表分区

### 4. 分区表核心特点
1. 透明：业务 SQL 完全不用改
2. 分区独立：一个分区坏了不影响其他
3. 清理历史：`ALTER TABLE DROP PARTITION` 秒删
4. 支持本地索引、全局索引
5. 分区可以单独放到不同表空间

### 5. 适用场景
单表 千万级以上数据
订单流水、交易记录、日志、账单、历史数据

# 三、临时表 VS 分区表 一句话对比（面试背诵版）
1. 临时表：结构永久、数据临时、会话隔离、不持久化、用于中间临时计算
2. 分区表：数据永久存储、大表拆分优化性能、用于正式海量业务数据

完全不是一类东西，没有替代关系。

# 四、极简面试答题版（直接背）
## 临时表
Oracle 全局临时表表结构永久保存，数据临时，事务/会话结束自动清空；数据存在临时表空间，不产生重做日志，会话隔离，用于存储过程中间结果、临时计算数据。

## 分区表
将大表按范围/列表/哈希切分为多个物理分区，逻辑上仍是一张表；提升大表查询性能、快速清理历史数据，SQL 无感知改造，适用于亿级流水、订单等时序业务表。

需要我给你各写一段可直接运行的建表 SQL 示例吗？

Oracle Data Guard 是Oracle数据库的核心高可用和灾难恢复解决方案，通过创建和维护一个或多个备用数据库（Standby Database）来保护主数据库（Primary Database），确保业务连续性。

一、核心架构与工作原理

1. 基本架构

Data Guard采用主备架构，由以下组件构成：
• 主数据库（Primary Database）：处理生产事务

• 备用数据库（Standby Database）：实时接收并应用重做日志

• 重做传输服务（Redo Transport Services）：将重做数据从主库传输到备库

• 日志应用服务（Log Apply Services）：在备库应用重做数据

• 角色转换服务（Role Transitions）：实现主备切换

2. 数据同步机制

Data Guard通过重做日志（Redo Log） 实现数据同步：
• 主库产生重做日志

• 重做传输服务将日志传输到备库

• 备库应用服务将重做应用到数据文件

• 保证主备数据一致性

二、两地三中心部署模式

1. 部署架构

两地三中心通常采用主备+异地灾备模式：
• 生产中心：主数据库 + 同城备库（Active Data Guard）

• 同城灾备中心：同步备库（最大保护模式）

• 异地灾备中心：异步备库（最大性能模式）

2. 典型配置

-- 主库配置
ALTER SYSTEM SET LOG_ARCHIVE_DEST_2='SERVICE=standby_sync LGWR SYNC AFFIRM VALID_FOR=(ONLINE_LOGFILES,PRIMARY_ROLE) DB_UNIQUE_NAME=standby_sync';
ALTER SYSTEM SET LOG_ARCHIVE_DEST_3='SERVICE=standby_async LGWR ASYNC VALID_FOR=(ONLINE_LOGFILES,PRIMARY_ROLE) DB_UNIQUE_NAME=standby_async';

-- 保护模式设置
ALTER DATABASE SET STANDBY DATABASE TO MAXIMIZE PROTECTION;


3. 网络拓扑

• 同城中心：高速光纤网络（<10ms延迟），同步传输

• 异地中心：广域网（WAN），异步传输

• 多路径传输，避免单点故障

三、保护模式

1. 最大保护模式（Maximum Protection）

• 特点：零数据丢失，同步传输

• 工作方式：主库事务提交前，必须等待备库确认

• 适用场景：同城灾备，金融交易系统

• 风险：网络故障可能导致主库挂起

2. 最大可用模式（Maximum Availability）

• 特点：零数据丢失（正常情况），自动降级

• 工作方式：同步传输，备库故障时自动切换为异步

• 适用场景：高可用要求，允许短暂异步

3. 最大性能模式（Maximum Performance）

• 特点：异步传输，性能最优

• 工作方式：主库不等待备库确认

• 适用场景：异地灾备，对性能要求高

• 数据保护：可能存在数据丢失窗口

四、备库类型

1. 物理备库（Physical Standby）

• 特点：块级复制，与主库物理结构一致

• 应用方式：重做日志直接应用到数据文件

• 优势：切换速度快，数据一致性高

• 用途：容灾切换、报表查询、数据保护

2. 逻辑备库（Logical Standby）

• 特点：SQL级复制，逻辑结构可不同

• 应用方式：重做日志转换为SQL语句执行

• 优势：可读可写，支持不同表结构

• 用途：报表查询、数据整合、滚动升级

3. 快照备库（Snapshot Standby）

• 特点：临时可读写，可回滚到只读状态

• 应用方式：暂停重做应用，可读写操作

• 用途：测试、开发、数据验证

五、角色转换

1. 切换（Switchover）

• 特点：计划内切换，零数据丢失

• 场景：系统维护、负载均衡

• 步骤：

  1. 主库转换为备库角色
  2. 备库转换为主库角色
  3. 客户端连接切换到新主库

2. 故障转移（Failover）

• 特点：计划外切换，最小化数据丢失

• 场景：主库故障，灾难恢复

• 步骤：

  1. 检测主库故障
  2. 激活备库为主库
  3. 客户端重连到新主库

3. 快速启动故障转移（Fast-Start Failover）

• 特点：自动故障检测和切换

• 配置：通过Data Guard Broker配置

• 条件：需要Observer进程监控主备状态

六、两地三中心优势

1. 高可用性

• RTO（恢复时间目标）：分钟级切换

• RPO（恢复点目标）：零数据丢失（同步模式）

• 多级保护：同城同步+异地异步

2. 数据保护

• 零数据丢失：最大保护模式

• 数据一致性：物理备库保证块级一致

• 多副本：多地多副本，防数据丢失

3. 业务连续性

• 快速切换：自动或手动切换

• 透明切换：客户端自动重连

• 滚动升级：通过切换实现不停机升级

4. 成本效益

• 硬件利用：备库可用于报表查询

• 资源复用：快照备库用于测试开发

• 分级保护：按业务重要性配置不同保护级别

七、典型应用场景

1. 金融行业

• 核心交易系统：同城同步+异地异步

• 监管要求：两地三中心，RTO<30分钟

• 数据保护：零数据丢失，审计合规

2. 政府机构

• 电子政务：7×24小时服务

• 数据安全：多地备份，防数据丢失

• 灾难恢复：快速恢复业务

3. 互联网企业

• 电商平台：大促期间高可用

• 用户数据：多地容灾，防单点故障

• 全球化部署：多地数据中心

八、配置最佳实践

1. 网络配置

-- 配置重做传输服务
ALTER SYSTEM SET LOG_ARCHIVE_DEST_STATE_n=ENABLE;
ALTER SYSTEM SET LOG_ARCHIVE_DEST_n='SERVICE=standby LGWR SYNC AFFIRM';

-- 配置网络超时
ALTER SYSTEM SET LOG_ARCHIVE_DEST_n='SERVICE=standby LGWR SYNC NET_TIMEOUT=30';


2. 性能优化

-- 启用并行应用
ALTER DATABASE RECOVER MANAGED STANDBY DATABASE USING CURRENT LOGFILE DISCONNECT FROM SESSION PARALLEL 8;

-- 压缩重做传输
ALTER SYSTEM SET LOG_ARCHIVE_DEST_n='SERVICE=standby LGWR SYNC COMPRESSION=ENABLE';

-- 批量传输
ALTER SYSTEM SET LOG_ARCHIVE_DEST_n='SERVICE=standby LGWR SYNC BATCH=YES';


3. 监控与管理

-- 查看备库状态
SELECT NAME, DATABASE_ROLE, PROTECTION_MODE, OPEN_MODE FROM V$DATABASE;

-- 查看重做传输
SELECT DEST_ID, STATUS, ERROR FROM V$ARCHIVE_DEST;

-- 查看应用延迟
SELECT APPLIED_SEQ#, APPLIED_TIME FROM V$ARCHIVED_LOG;


九、常见问题与解决方案

1. 网络延迟

• 问题：同步模式导致主库性能下降
• 解决方案：
  • 使用异步模式或最大可用模式
  • 优化网络带宽和延迟
  • 启用重做压缩

2. 备库延迟

• 问题：备库应用速度跟不上主库
• 解决方案：
  • 启用并行应用
  • 优化备库I/O性能
  • 调整重做传输参数

3. 切换失败

• 问题：角色转换失败
• 解决方案：
  • 检查网络连通性
  • 验证备库状态
  • 使用Data Guard Broker简化管理

十、总结

Oracle Data Guard的两地三中心部署为企业提供了多层次、高可用、强一致的数据保护方案。通过合理的保护模式配置、网络优化和监控管理，可以实现：
• 业务连续性：分钟级故障切换
• 数据安全：零数据丢失保护
• 成本优化：资源复用和分级保护
• 合规要求：满足监管和审计要求

Data Guard是Oracle数据库高可用架构的核心组件，结合Oracle RAC、GoldenGate等技术，可以构建更完善的容灾体系。



-- 查看当前密码策略 SELECT * FROM dba_profiles WHERE profile = 'DEFAULT' AND resource_name = 'PASSWORD_LIFE_TIME'; 
-- 修改密码永不过期 ALTER PROFILE DEFAULT LIMIT PASSWORD_LIFE_TIME UNLIMITED;
在Oracle数据库中，DBA_PROFILES 是一个重要的数据字典视图，它记录了数据库中所有的资源限制配置文件（Resource Limit Profiles）的定义信息。以下是它的核心作用与详细说明：

1. 核心作用

DBA_PROFILES 主要用于管理Oracle的资源限制配置，包括：
• 密码策略（如密码复杂度、有效期）
• 资源限制（如CPU时间、会话数）
• 账户锁定规则（如登录失败次数限制）

这些配置通过Profile（配置文件）实现，Profile可以被分配给用户，控制其资源使用和密码安全策略。

2. 关键字段说明
字段名 数据类型 说明

PROFILE VARCHAR2(128) 配置文件的名称（如 DEFAULT）

RESOURCE_NAME VARCHAR2(32) 资源/密码参数名（如 FAILED_LOGIN_ATTEMPTS）

RESOURCE_TYPE VARCHAR2(8) 参数类型：PASSWORD（密码）或 KERNEL（资源）

LIMIT VARCHAR2(128) 参数的限制值（如 10、UNLIMITED）

COMMON VARCHAR2(3) 是否为CDB（多租户）中的公共配置：YES/NO

3. 典型应用场景

(1) 查询所有Profile的配置

SELECT * FROM DBA_PROFILES 
ORDER BY PROFILE, RESOURCE_TYPE, RESOURCE_NAME;


(2) 查看默认Profile的密码策略

SELECT RESOURCE_NAME, LIMIT 
FROM DBA_PROFILES 
WHERE PROFILE = 'DEFAULT' AND RESOURCE_TYPE = 'PASSWORD';

输出示例：

RESOURCE_NAME          LIMIT
---------------------- --------------
FAILED_LOGIN_ATTEMPTS  10
PASSWORD_LIFE_TIME     180
PASSWORD_REUSE_TIME    UNLIMITED


(3) 修改Profile配置

ALTER PROFILE developer LIMIT 
  FAILED_LOGIN_ATTEMPTS 5
  PASSWORD_LOCK_TIME 1;


(4) 创建自定义Profile

CREATE PROFILE audit_user LIMIT
  SESSIONS_PER_USER         2
  CPU_PER_SESSION           UNLIMITED
  PASSWORD_REUSE_MAX        5;


4. 重要参数详解

密码策略参数（RESOURCE_TYPE = 'PASSWORD'）

参数名 说明 示例值

FAILED_LOGIN_ATTEMPTS 允许的连续失败登录次数 5

PASSWORD_LIFE_TIME 密码有效期（天） 90

PASSWORD_REUSE_TIME 密码可重复使用的时间（天） 365

PASSWORD_LOCK_TIME 账户锁定时间（天） 1
资源限制参数（RESOURCE_TYPE = 'KERNEL'）
参数名 说明 示例值

SESSIONS_PER_USER 每个用户的最大会话数 3

CPU_PER_SESSION 每个会话的CPU时间（百分之一秒） 100000

CONNECT_TIME 会话最大连接时间（分钟） 60

5. 实际应用示例

场景：为财务用户创建严格的Profile  
-- 1. 创建Profile
CREATE PROFILE finance_profile LIMIT
  FAILED_LOGIN_ATTEMPTS  3
  PASSWORD_LIFE_TIME     60
  PASSWORD_REUSE_TIME    180
  SESSIONS_PER_USER      2;

-- 2. 分配给用户
ALTER USER acc_001 PROFILE finance_profile;
ALTER USER acc_002 PROFILE finance_profile;


6. 注意事项

1. 默认Profile：Oracle会自动创建名为 DEFAULT 的Profile，所有未明确分配Profile的用户使用此配置。
2. 权限要求：查询 DBA_PROFILES 需要 SELECT_CATALOG_ROLE 或 DBA 角色权限。
3. 多租户环境：在CDB中，COMMON 字段标识是否为所有PDB共享的配置。
4. 参数继承：如果某个参数在Profile中设为 DEFAULT，则继承 DEFAULT Profile中的值。

7. 相关数据字典视图

• USER_PROFILES：当前用户可访问的Profile

• RESOURCE_COST：资源成本权重设置

• DBA_USERS：查看用户分配的Profile

通过 DBA_PROFILES，DBA可以精细控制数据库的安全性和资源使用，是Oracle数据库安全管理的重要工具。

https://sqlfiddle.com/


ifnull()类似的函数，有吗？
豆瓣

case
  when xxx isnull or xxx = '' then
    0
  else
    1
end as yyy

https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/Data-Types.html#GUID-1BABC478-FB47-4962-9B0C-8B8BD059E733

“两地三中心”是中国人民银行在2002年提出、2004年开始逐步实施的有关央行系统数据中心布局的战略部署，也被称为“一主两备”或“一个同城加两个异地”。它是指在北京建立两个数据中心，同时在天津和上海各建立一个数据中心。
在这个方案中，北京的两个数据中心采用双活模式，天津和上海的数据中心则采用异步方式（近同步）复制北京的数据，但不对用户开放。这样做的目的是保证当任何一个地方发生灾难时，其他的地方还可以对外提供服务。
这个方案的实施得到了花旗银行的支持。花旗银行的现金管理平台采用了Oracle真正应用集群（RAC）来整合位于纽约和伦敦的两个数据中心，并使用Oracle Data Guard作为第三点故障切换。这种多点集群技术可以提供更高的可用性，使系统在遇到故障时能够自动进行切换，从而最大限度地减少了系统的停机时间。


Oracle sql merge 语法

Oracle SQL中的MERGE语句用于将一个表的数据合并到另一个表中。它的基本语法如下：

```sql
MERGE INTO 目标表 AS T1
USING 源表 AS T2
ON (T1.匹配条件 = T2.匹配条件)
WHEN MATCHED THEN
    UPDATE SET T1.列名1 = T2.列名1, T1.列名2 = T2.列名2, ...
WHEN NOT MATCHED THEN
    INSERT (列名1, 列名2, ...)
    VALUES (T2.列名1, T2.列名2, ...);
```

其中，`目标表`是要更新或插入数据的表，`源表`是包含要合并数据的另一个表。`匹配条件`是两个表中用于匹配的列。`WHEN MATCHED`部分表示当匹配成功时，需要更新的目标表中的列值；`WHEN NOT MATCHED`部分表示当匹配失败时，需要插入到目标表中的新列值。


Oracle中的Service_name和SID都是用于标识数据库实例的参数，但它们之间存在一些区别。首先，Service_name是在Oracle 8i版本中引入的。在8i之前，使用SID来表示一个数据库实例。但在Oracle的并行环境中，一个数据库可以有多个实例，这意味着需要为每个实例设置一个网络服务名，导致设置变得繁琐。为了简化并行环境中的设置，引入了Service_name。具体来说，ServiceName方式是Oracle推荐的。对于集群来说，每个节点的SID可能不一致，但ServiceName是一致的，包含所有节点。而SID方式是我们在实际部署时经常使用的连接方式，其格式为：jdbc:oracle:thin:@<地址：端口号：SID。
简而言之，SID是数据库的一个实例，一个数据库可以有多个SID；而Service_name对应数据库，一个数据库也可以对应多个Service_name。在选择使用哪一种方式时，需要根据实际的应用场景和需求来决定。

还是很有希望的，Oracle现在已经是屎山了。我记得邓侃从国外回来的时候他们那边就已经新代码铺旧代码，谁都不敢轻易改了。不过oracle的特性还是很强，估计当前开源的这批关系型数据库连oralce 10G的特性都没有完全实现。不过那时候我最喜欢看的还是oralce有个专栏叫做ask tom，他们的VP讲oracle的一些功能细节实现真的很棒。

Oracle公司的"Ask Tom"专栏是一个非常受欢迎的技术问答栏目，由Oracle公司的副总裁Tom Kyte主持。Tom Kyte是Oracle公司的一位资深技术专家，拥有多年的数据库开发经验，对Oracle数据库的内部实现和最佳实践有着深入的了解。
在"Ask Tom"专栏中，Tom Kyte会回答用户提出的各种关于Oracle数据库的问题，内容包括性能优化、SQL调优、数据结构设计等方面。他的回答通常非常详细，不仅会解释问题的原因，还会给出具体的解决方案和代码示例。
Tom Kyte的回答经常被开发者们视为权威性的解答，因为他对Oracle数据库的了解非常深入，并且在实际应用中也有着丰富的经验。他的回答往往能够帮助开发者们更好地理解和使用Oracle数据库，提高应用程序的性能和稳定性。
总的来说，"Ask Tom"专栏是Oracle公司的一个非常有价值的资源，为开发者们提供了一个与专家交流的平台，帮助他们解决在实际开发中遇到的问题。

Tom Kyte是Oracle公司的一位副总裁，也是一位资深的技术专家和作家。他在数据库和软件开发领域有着丰富的经验，尤其擅长Oracle数据库的开发和优化。
Tom Kyte在Oracle公司担任多个职务，包括Oracle数据库开发团队的成员、Oracle支持团队的负责人、以及Oracle大学的教师。他对Oracle数据库的内部实现和最佳实践有着深入的了解，经常在全球范围内的技术会议上发表演讲。
除了"Ask Tom"专栏外，Tom Kyte还撰写了多本关于Oracle数据库和SQL的书籍，其中包括《Expert Oracle Database Architecture》、《Effective Oracle by Design》等。这些书籍被广大开发者视为权威性的参考资料，帮助他们更好地理解和使用Oracle数据库。
总的来说，Tom Kyte是一位备受尊重的技术专家，他的知识和经验对Oracle数据库的开发和优化领域产生了深远的影响。

oracle 需要手动提交事务

testoraclemybatis
资深dba 专家型dba推荐的学习Oracle的资料
https://dbaplus.cn/news-10-1475-1.html
https://dbaplus.cn/news-10-1475-1.html
https://dbaplus.cn/news-10-1475-1.html

Oracle 返回id
https://blog.csdn.net/mlsama/article/details/106690730

### oracle 11g docker安装

Oracle Database 11g Enterprise Edition Release 11.2.0.1.0 - 64bit Production

registry.aliyuncs.com/helowin/oracle_11g

【Docker】拉取Oracle 11g镜像配置 - OLIVER_QIN - 博客园.mhtml
https://www.cnblogs.com/OliverQin/p/9765808.html

dell刀片服务器

docker镜像

navicat连接oracle，服务名：helowinXDB
登录服务器
oracle

root


设置环境变量

sqlplus登录

sys system默认密码无

新建账户ETS，密码ETS，字母大写


wdidada账户 lock解除
alter user wdidada account unlock;
alter user wdidada identified by wdidada;
alter user sys identified by sys;
alter user system identified by system;
https://www.jb51.net/article/118365.htm

### Oracle新建表

先选择数据库
数据库操作可以用Database Configuration Assistant

选择或者新建表空间

默认表空间
TEMP
USER

```sql
CREATE TABLE "tb_user" (
  "ID" NUMBER(24,0) VISIBLE NOT NULL,
  "user_name" VARCHAR2(255 BYTE) VISIBLE,
  "password" VARCHAR2(255 BYTE) VISIBLE,
  "name" VARCHAR2(255 BYTE) VISIBLE,
  "age" NUMBER(3,0) VISIBLE,
  "sex" NUMBER(3,0) VISIBLE,
  "birthday" DATE VISIBLE,
  "created" DATE VISIBLE,
  "updated" DATE VISIBLE
)
LOGGING
NOCOMPRESS
PCTFREE 10
INITRANS 1
STORAGE (
  INITIAL 65536 
  NEXT 1048576 
  MINEXTENTS 1
  MAXEXTENTS 2147483645
  BUFFER_POOL DEFAULT
)
PARALLEL 1
NOCACHE
DISABLE ROW MOVEMENT
;
```

执行之后表不存在？
存在，但是查看的慢

https://blog.csdn.net/weixin_39559750/article/details/111490430

### Oracle Java代码仓库

https://gitee.com/edidada/testoracle


### Oracle Win 10电脑关闭和启动
https://blog.csdn.net/weixin_44291381/article/details/125160942

listener.ora tnsnames.ora
这两个文件ip修改

OracleOraDB12Home2TNSListener
OracleServiceDD
OracleServiceORCL
这个服务

备注：TNSListener 这个服务没启动，连接不上

Oracle ASM神书《拨云见日 解密Oracle ASM内核》
ui工具 oracle developer 自带的

idea datasource

自增 存储过程
int 没有 只有number
datetime -> date

oracle 12c 2013年6月发布

Oracle Database 19c 

问题：Oracle数据库创建数据库

方式之一：Database Configuration Assistant创建数据库

Oracle 12C 创建用户以c##开头
https://blog.csdn.net/songpeiying/article/details/82894922

Oracle 12C引入了CDB（Container Database数据库容器）与PDB（Pluggable Database插拔数据库）的新特性

Common User是指在每个容器中都存在的用户

```sql
create table C##TEST01.Users(id  number(3) primary key,name varchar2(20),email varchar2(20),country varchar2(20),password varchar2(20));
INSERT INTO C##TEST01.Users (id, name, email, country, password) VALUES (1, 'Pankaj', 'pankaj@apple.com', 'India', 'pankaj123');
INSERT INTO C##TEST01.Users (id, name, email, country, password) VALUES (4, 'David', 'david@gmail.com', 'USA', 'david123');
INSERT INTO C##TEST01.Users (id, name, email, country, password) VALUES (5, 'Raman', 'raman@google.com', 'UK', 'raman123');
commit;
```

![c## or C## ](oracle_users.jpeg)

### book

- Oracle Database 12c完全参考手册  第7版.pdf
- Oracle 12c数据库应用与开发 https://www.zhihu.com/pub/reader/119582341/chapter/1183441714831908864

表navicate上
所有者
表空间

https://github.com/edidada/testoracle

lsnrctl status
tnsping orcl

D:\Oracle\DataBase\app\edidada\product\12.1.0\dbhome_1\NETWORK\ADMIN
路径下三个文件sqlnet.ora listener.ora tnsnames.ora

oracle数据库tns配置方法详解
https://www.jb51.net/article/44668.htm
TNS是Oracle Net的一部分，专门用来管理和配置Oracle数据库和客户端连接的一个工具，在大多数情况下客户端和数据库要通讯，必须配置TNS，当然在少数情况下，不用配置TNS也可以连接Oracle数据库，比如通过JDBC。如果通过TNS连接Oracle，那么客户端必须安装Oracle client程序。

使用tcp.validnode_checking允许、限制机器访问数据库
https://www.cnblogs.com/lcword/p/8232066.html

https://blog.csdn.net/demonson/article/details/39506215

tnsping 192.168.0.104
TNS Ping Utility for 64-bit Windows: Version 12.1.0.2.0 - Production on 02-4月 -2021 21:37:09
Copyright (c) 1997, 2014, Oracle.  All rights reserved.
已使用的参数文件:
D:\Oracle\DataBase\app\edidada\product\12.1.0\dbhome_1\network\admin\sqlnet.ora
已使用 EZCONNECT 适配器来解析别名
尝试连接 (DESCRIPTION=(CONNECT_DATA=(SERVICE_NAME=))(ADDRESS=(PROTOCOL=TCP)(HOST=192.168.0.104)(PORT=1521)))
TNS-12541: TNS: 无监听程序

windows 防火墙开放端口访问
https://blog.csdn.net/weixin_43465312/article/details/102510619

刚装的Oracle 12c 访问 https://localhost:5500/em/login 使用 system 登录 报错 （权限/口令错误）

右键计算机 ->管理 -> 服务 ，右击名称 输入O 弹出以O开头的服务名称 ,找到 OracleJobSchedulerORCL
启动它。 再登录就OK了。

https://localhost:5500/em

在环境变量中把ORACLE_HOME 设置成D:\Oracle\DataBase\app\edidada\product\12.1.0\dbhome_1

netstat -an

windows服务
OracleOraDB12Home2TNSListener

如何实现Oracle的监听（listener）多个IP地址
https://blog.csdn.net/funnyfu0101/article/details/51029674

oracle工具
oracle net namager


https://blog.csdn.net/weixin_29888579/article/details/114017404

Oracle Database Express Edition (XE) Release 18.4.0.0.0 (18c)
https://www.oracle.com/database/technologies/xe-downloads.html

Linux on System z (64-bit)
HP-UX ia64
IBM AIX power
Oracle Solaris (SPARC systems, 64-bit)
Linux x86-64
Microsoft Windows x64 (64-bit)

20191212 搞Oracle 12

jdbc:oracle:thin:@192.168.3.98:1521:orcl
jdbc:表示采用jdbc方式连接数据库
oracle:表示连接的是oracle数据库
thin:表示连接时采用thin模式(oracle中有两种模式)

jdbc:oralce:thin:是一个jni方式的命名

@表示地址
1521和orcl表示端口和数据库名

@192.168.3.98:1521:orcl整个是一块
也就是说是这样[jdbc]:[oracle]:[thin]:[@192.168.3.98:1521:orcl]

二、
oracle的jdbc连接方式:oci和thin

oci和thin是Oracle提供的两套Java访问Oracle数据库方式。
thin是一种瘦客户端的连接方式，即采用这种连接方式不需要安装oracle客户端,只要求classpath中包含jdbc驱动的jar包就行。thin就是纯粹用Java写的ORACLE数据库访问接口。
oci是一种胖客户端的连接方式，即采用这种连接方式需要安装oracle客户端。oci是Oracle Call Interface的首字母缩写，是ORACLE公司提供了访问接口，就是使用Java来调用本机的Oracle客户端，然后再访问数据库，优点是速度 快，但是需要安装和配置数据库。
https://www.cnblogs.com/qingxinblog/p/4043173.html

Oracle 服务名/实例名，Service_name 和Sid的区别
Service Name

Service_name 和Sid的区别
Service_name：该参数是由oracle8i引进的。
在8i以前，使用SID来表示标识数据库的一个实例，但是在Oracle的并行环境中，一个数据库对应多个实例，这样就需要多个网络服务名，设置繁琐。为了方便并行环境中的设置，引进了Service_name参数，该参数对应一个数据库，而不是一个实例，而且该参数有许多其它的好处。

oracle 查看用户、权限、角色命令
https://blog.csdn.net/nature_fly088/article/details/8504823


https://blog.csdn.net/make_zhf/article/details/70154160


/oradata/TEST30/APPADMIN_TEMP_01.dbf

TEST_01.dbf
D:\Oracle\DataBase\app\edidada\oradata\orcl\


在Maven仓库中添加Oracle JDBC驱动
https://www.cnblogs.com/leiOOlei/p/3380568.html


cd/d D:\Oracle\DataBase\app\edidada\product\12.1.0\dbhome_1\jdbc\lib\
mvn install:install-file -DgroupId=com.oracle -DartifactId=ojdbc7 -Dversion=12.1.0.2.0 -Dpackaging=jar -DgeneratePom=true -Dfile=ojdbc7.jar
上述命令报错，在powershell中报错，在cmd中先运行cmd之后运行成功
https://stackoverflow.com/questions/6704813/maven-generating-pom-file/11199865#11199865

https://www.e-learn.cn/content/qita/2671944


https://www.oracle.com/database/technologies/jdbc-drivers-12c-downloads.html

Maven引入oracle ojdbc驱动

https://www.jianshu.com/p/70b68ce0dab2

oracle rac集群

https://blog.csdn.net/stevensxiao/article/details/90605443 sample是linux的，不是windows的

https://www.cndba.cn/dave/article/1985

navicate
用户角色
defalut
sysdba
sysoper

https://www.cnblogs.com/sunnyliu357/articles/2301738.html
orcl or（a cl（e 去掉 a e
Oracle RAC
https://docs.oracle.com/database/121/index.htm
https://www.oracletutorial.com/getting-started/oracle-sample-database/
https://www.cnblogs.com/lcword/p/8231860.html
navicate 连接oracle，是自动提交的
OCP/OCA认证考试指南全册:Oracle Database 11g
待正式从业后，再择机通过OCM认证提高自己。
OCA,OCP
现在基本上都是OCP，网上听课，然后线下就近考点考试即可，考试通过可以拿个证书，但是对于有工作经验的人来说好像价值已经不大了，现在ocm都漫天飞了。


在cmd中
C:\Documents and Settings\Administrator>sqlplus/nolog
SQL*Plus: Release 9.2.0.1.0 - Production on 星期四 11月 1 15:14:12 2007
Copyright (c) 1982, 2002, Oracle Corporation. All rightsreserved.
SQL> connect/as sysdba
已连接。

新版本都是云的    19

18
IBM Aix

HP Unix

oracle 12 c，其中c表示cloud

Oracle Database 19*c*

12c
https://www.oracle.com/database/technologies/database12c-win64-downloads.html

关于oracle sql语句查询时表名和字段名要加双引号的问题
https://blog.csdn.net/u011754180/article/details/85097434

1、oracle表和字段是有大小写的区别。oracle默认是大写，如果我们用双引号括起来的就区分大小写，如果没有，系统会自动转成大写。

2、我们在使用navicat使用可视化创建数据库时候，navicat自动给我们加上了“”。

https://docs.oracle.com/database/121/TDDDG/tdddg_dml.htm#TDDDG99941

```SQL
INSERT INTO EMPLOYEES (
  EMPLOYEE_ID,
  FIRST_NAME,
  LAST_NAME,
  EMAIL,
  PHONE_NUMBER,
  HIRE_DATE,
  JOB_ID,
  SALARY,
  COMMISSION_PCT,
  MANAGER_ID,
  DEPARTMENT_ID
)
VALUES (
  10,              -- EMPLOYEE_ID
  'George',        -- FIRST_NAME
  'Gordon',        -- LAST_NAME
  'GGORDON',       -- EMAIL
  '650.506.2222',  -- PHONE_NUMBER
  '01-JAN-07',     -- HIRE_DATE
  'SA_REP',        -- JOB_ID
  9000,            -- SALARY
  .1,              -- COMMISSION_PCT
  148,             -- MANAGER_ID
  80               -- DEPARTMENT_ID
);

```


select username,created from dba_users where created>sysdate-1;

sqlplus system/5Edidada@127.0.0.1:1521/ORCL

sqlplus system/5Edidada@127.0.0.1:1521/ORCL @mksample.sql 5Edidada 5Edidada 5Edidada 5Edidada 5Edidada 5Edidada 5Edidada 5Edidada users temp C:\Users\edidada\Desktop\db-sample-schemas-12.1.0.2\log\ 127.0.0.1:1521/ORCL
sqlplus system/5Edidada@127.0.0.1:1521/ORCL@drop_hr.sql


https://docs.oracle.com/en/database/oracle/oracle-database/12.2/comsc/installing-sample-schemas.html#GUID-1E645D09-F91F-4BA6-A286-57C5EC66321D

https://github.com/oracle/db-sample-schemas/releases/tag/v12.1.0.2

https://www.linuxidc.com/Linux/2017-08/146337.htm

http://www.uwenku.com/question/p-ymnovpyv-ts.html

https://docs.oracle.com/database/121/TDDDG/tdddg_connecting.htm#TDDDG99998

https://docs.oracle.com/database/121/TDDDG/tdddg_dml.htm#TDDDG99941

https://docs.oracle.com/database/121/CNCPT/tablecls.htm#CNCPT010
https://docs.oracle.com/database/121/index.htm#

登录https://localhost:5500/em/shell#/dbhome/show_regions
输入用户名system，密码5Edidada，可以登录


?\demo\db-sample-schemas-12.1.0.2\log\hr_main.log
127.0.0.1:1521/ORCL
D:/Oracle/DataBase/app/edidada/product/12.1.0/dbhome_1/demo/db-sample-schemas-12.1.0.2/human_resources

https://www.jianshu.com/p/7530246fc34b


```
conn as sysdba;
sys 5Edidada
alter session set container=PDBORCL;
DROP USER hr cascade;
CREATE USER hr IDENTIFIED BY "5Edidada";
ALTER USER hr DEFAULT TABLESPACE users;
ALTER USER hr TEMPORARY TABLESPACE temp;
GRANT CREATE SESSION, CREATE VIEW, ALTER SESSION, CREATE SEQUENCE TO hr;
GRANT CREATE SYNONYM, CREATE DATABASE LINK, RESOURCE , UNLIMITED TABLESPACE TO hr;
GRANT execute ON sys.dbms_stats TO hr;

show con_name;
select con_id,dbid,NAME,OPEN_MODE from v$pdbs;



CREATE TABLE employees( employee_id NUMBER(6),first_name VARCHAR2(20),last_name VARCHAR2(25) CONSTRAINT emp_last_name_nn NOT NULL,email VARCHAR2(25),phone_number VARCHAR2(20),hire_date DATE CONSTRAINT emp_hire_date_nn NOT NULL,job_id VARCHAR2(10)	CONSTRAINT     emp_job_nn  NOT NULL    , salary         NUMBER(8,2)    , commission_pct NUMBER(2,2),manager_id NUMBER(6),department_id NUMBER(4),CONSTRAINT emp_salary_min CHECK(salary > 0),CONSTRAINT emp_email_uk UNIQUE(email));

CREATE UNIQUE INDEX emp_emp_id_pk ON employees (employee_id);

ALTER TABLE employeesADD(CONSTRAINTemp_emp_id_pk PRIMARY KEY(employee_id),CONSTRAINT emp_dept_fk FOREIGN KEY(department_id) REFERENCES departments,CONSTRAINT emp_job_fk FOREIGN KEY(job_id) REFERENCES jobs (job_id),CONSTRAINT emp_manager_fk FOREIGN KEY(manager_id) REFERENCES employees);

ALTER TABLE departments ADD ( CONSTRAINT dept_mgr_fk FOREIGN KEY (manager_id)REFERENCES employees (employee_id));

```

登录sqlplus之后，执行sql脚本
@?/demo/hr_create.sql



https://www.jb51.net/article/92720.htm



cmd输入

```
查看oracle的sid叫什么，比如创建数据库的时候，实例名叫“orcl”，那么先手工设置一下oralce的sid，cmd命令窗口中，set ORACLE_SID=orcl（还是大写？？
不然报错：ORA-01034: ORACLE not available ORA-27101

用sqlplus / as sysdba登陆oracle系统，这种登录方式来使用的是操作系统的验证方式，因此，无源需输入用户名和密码即可直接登录进去。

sqlplus sys/orcl as sysdba       //orcl是数据库

select USERNAME, USER_ID  from dba_users;//查看数据库用户 前提是你度是有dba权限的帐号，如sys,system；
```

SYSTEM

SYS

HR       hr用户是个示例用户，是在创建数据库时选中“示例数据库”后产生的，实际上就是模拟一个人力资源部的数据库。

OE

PM

IX

SH

BI

Oracle数据库中sys，system，scott，hr用户的区别
https://blog.csdn.net/zhang18330699274/article/details/55517836

###### sys和system的区别？

存储的数据的重要性不同。所有oracle的数据字典的基表和视图都存放在sys用户中，这些基表和视图对于oracle的运行是至关重要的，由数据库自己维护，任何用户都不能手动更改。sys用户拥有dba,sysdba,sysoper等角色或权限，是oracle权限最高的用户。

　　system用户用于存放次一级的内部数据，如oracle的一些特性或工具的管理信息。system用户拥有普通dba角色权限。

cdb pdb

Oracle 12C引入了CDB与PDB的新特性

cdb容器数据库 pdb可插播数据库 

https://blog.csdn.net/qq877507054/article/details/81209967

新建数据库 C##开头

oracle12c 启用容器数据库之后，创建用户名只能c#[#开头，那怎么才能不适用c#](http://tieba.baidu.com/hottopic/browse/hottopic?topic_id=0&topic_name=开头，那怎么才能不适用c)#开头的用户呢。
如果你去搜索的话，90%的答案会告诉你重新创建数据库实例，然后把创“建为容器数据库”勾选掉。

其实并不用那么麻烦，只需要几部就可以创建不带C##的用户。
1.使用sqlplus 以 DBA 身份链接。 命令：sqlplus / as sysdba
2.在链接成功后，通过命令查看存在的PDB服务。语句：show pdbs;
3.切换到pdb服务上。语句：
alter session set container=pdb服务名;
alter pluggable database pdb服务名 open;
4.尝试创建不带C##的用户吧。

###### Oracle 12C 创建用户以c##开头

https://blog.csdn.net/songpeiying/article/details/82894922

角色

https://zhuanlan.zhihu.com/p/59402726

创建非cdb数据库

打开Database Configuration Assistant

点击“下一步”出现如下界面，在创建数据库的时候将“创建为容器数据库”项取消勾选。

数据库名要大写

TEST202005
5Edidada

ORA-03113:通信通道的文件结尾 解决办法
https://blog.csdn.net/zwk626542417/article/details/39667999

重点
https://blog.csdn.net/wangsimiao118/article/details/78818836

orcl表示数据库名

[oracle连接两种方式thin与oci区别](https://blog.csdn.net/kevin_pso/article/details/54949476)
thin:表示知连接时采用thin模式道(oracle中有两中模式)
Java连接Oracle两种方式thin与oci区别
1 从使用上来说，oci必须在客户机上安装oracle客户端或才能连接，而thin就不需要，因此从使用上来讲thin还是更加方便，这也是thin比较常见的原因。 
2 原理上来看，thin是纯java实现tcp/ip的c/s通讯；而oci方式,客户端通过native java method调用c library访问服务端，而这个c library就是oci(oracle called interface)，因此这个oci总是需要随着oracle客户端安装（从oracle10.1.0开始，单独提供OCI Instant Client，不用再完整的安装client） 
3 它们分别是不同的驱动类别，oci是二类驱动， thin是四类驱动，但它们在功能上并无差异。 
4 虽然很多人说oci的速度快于thin，但找了半天没有找到相关的测试报告。

oracle 命令行创建标（也可以用工具创建

https://jingyan.baidu.com/article/948f5924de98add80ef5f952.html

service name 和sid区别

https://www.cnblogs.com/matd/p/11051884.html

service name 该参数的缺省值为Db_name. Db_domain，即等于Global_name。一个数据库可以对应多个Service_name，以便实现更灵活的配置。该参数与SID没有直接关系，即不必Service name 必须与SID一样。Sid是数据库实例的名字，每个实例各不相同。

```
sqlplus查看服务名
查看服务名：

show parameter service
查看实例名：
select * from v$instance;

 查看数据库名：
select name from v$database;
查看数据库用到几个表空间：
select distinct TABLESPACE_NAME from tabs；

```

Oracle 12c 用户密码过期设置的一些问题

https://blog.csdn.net/seagal890/article/details/82716798

https://blog.csdn.net/weixin_39921821/article/details/82720851
oracle11g ORA-01078与LRM-00109 解决方法（详细）
https://blog.csdn.net/qq_15904277/article/details/86521808

新建数据库 ORA-03113: 通信通道的文件结尾

D:\Oracle\DataBase\app\edidada\admin

数据库文件

```
CREATE USER "AAA" IDENTIFIED BY "5Edidada" DEFAULT TABLESPACE "USERS" TEMPORARY TABLESPACE "TEMP";
GRANT "DBA" TO "AAA" WITH ADMIN OPTION;
ALTER USER "AAA" DEFAULT ROLE "DBA";
ALTER USER "AAA" QUOTA UNLIMITED ON "USERS";
GRANT UNLIMITED TABLESPACE TO "AAA" WITH ADMIN OPTION
```

oracle跟mysql区别在哪儿？
https://www.cnblogs.com/ios9/p/8227574.html#_label0

https://blog.csdn.net/qq_41303486/article/details/104452529

ORA-01034: ORACLE not available
https://blog.csdn.net/qq_22498277/article/details/51621863

web管理台
https://localhost:5500/em/shell#/dbhome/show_regions
https://www.cnblogs.com/sunsiyuan/p/8485418.html

Oracle 12c视频教程
[【千锋涛哥】最适合小白入门的Oracle 12c 教程](https://www.bilibili.com/video/BV1d54y197n3?p=10)

Oracle实例
Oracle数据库管理软件运行时占用内存，生成的进程

管理工具

sqlplus     有自己的指令
isqlplus是网页版

navicate
pl/sql
oem 数据库的企业管理功能

oracle账户
本地管理员
在sqlplus上输入用户名system as sysdba         （只输入system不行
密码输入5Edidada
system/5Edidada as sysdba
本地管理员可以不输入密码

disconn 断开
conn     连接
网络用户登录
username/pwd

连接时没有指定数据库，默认连接orcl

连接指定是数据库

### fucntion
sysdate

oracle表空间

https://www.cnblogs.com/fnng/archive/2012/08/12/2634485.html





navicate 15 查看表空间

undo表空间

temperary表空间    Temporary  Tablespaces





oracle 12c自带表空间有哪些？





​     在Oracle 12C之前，实例与数据库是一对一或一对多的关系（RAC）：即一个实例只能与一个数据库相关联，数据库可以被多个实例所加载。而实例与数据库不可能是一对多的关系。

​     当进入Oracle 12C后，实例与数据库可以是一对多的关系。





ORA-12514: TNS:listener does not currently know of service requested in connect descriptor

[oracle 新建数据库dd连接不上](https://stackoverflow.com/questions/10786782/ora-12514-tnslistener-does-not-currently-know-of-service-requested-in-connect-d)



需要切换service name

默认service name是orcl





```sql
select value from v$parameter where name='dd'
```
