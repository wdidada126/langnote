# innodb_read_view
一致性读视图，即 consistent read view

MVCC模型在MySQL中的具体实现则是由 三个隐式字段，undo日志 ，Read View 等去完成的

这里说的 read view 是InnoDB 在实现 MVCC 时用到的一致性读视图，即 consistent read view，用于支持 RC(Read Committed，读提交)和 RR(Repeatable Read,可重复读)隔离级别的实现。 
read view 并没有物理结构,作用是事务执行期间用来定义"我能看到什么数据"。

MySQL_read_view在RR和RC隔离级别下的异同-一只阿木木-博客园.mhtml


InnoDB里面每个事务有一个唯一的事务ID,叫做transaction id。它是在事务开始的时候向InnoDB的事务系统申请的，是按申请顺序严格递增的。 
在innodb存储引擎下，聚簇索引记录中都包含两个必要的隐藏列: 
trx_id：每次对某条记录进行改动时,对会把对应的事务id赋值给trx_id隐藏列; 
roll_pointer：每次对某条记录进行改动时,这个隐藏列会存一个指针,可以通过这个指针找到该记录修改前的信息,也就是undo回滚段中的内容。

一文搞懂Undo_Log版本链与ReadView机制如何让事务读取到该读的数据.mhtml
注意看roll_pointer

ReadView  可见性规则

a
c
i 
d redo log

MySQL事务的特性也是基于某些底层的功能来实现的，这些特性的实现如下：

【原子性】通过undo log（回滚日志）来保证的
【一致性】则是通过持久性+原子性+隔离性来保证
【隔离性】通过MVCC（多版本并发控制+读写锁）来保证的
【持久性】通过redo log （重做日志）来保证的


MySQL InnoDB ReadView 详解及与PostgreSQL对比
一、MySQL InnoDB ReadView 深度解析
1. ReadView 是什么？
ReadView是MySQL InnoDB实现MVCC（多版本并发控制）的核心数据结构，它定义了事务在某个时间点能够看到的数据版本。简单说，ReadView就是一个"快照"，记录了当前事务启动时系统的状态。
2. ReadView 的数据结构

// InnoDB源码中的ReadView（简化版）
class ReadView {
private:
    // 高水位：大于等于此值的事务ID不可见
    trx_id_t m_low_limit_id;
    
    // 低水位：小于此值的事务ID可见（除非在活跃列表中）
    trx_id_t m_up_limit_id;
    
    // 创建ReadView时活跃的事务ID列表（有序数组）
    ids_t m_ids;
    
    // 创建此ReadView的事务ID
    trx_id_t m_creator_trx_id;
    
    // 是否已关闭
    bool m_closed;
};

关键字段说明：
• m_low_limit_id：高水位线，下一个要分配的事务ID
• m_up_limit_id：低水位线，最早活跃的事务ID
• m_ids：活跃事务ID列表（已开始但未提交的事务）
• m_creator_trx_id：创建此ReadView的事务ID

3. ReadView 的创建时机
ReadView的创建时机取决于隔离级别：
隔离级别 ReadView创建时机 备注
READ COMMITTED 每个SQL语句开始时 语句级一致性
REPEATABLE READ 事务开始时（第一个读操作） 事务级一致性
SERIALIZABLE 不使用ReadView，使用锁机制 通过加锁实现串行化

-- 示例：不同隔离级别的行为差异
-- 会话1
SET SESSION transaction_isolation = 'READ-COMMITTED';
BEGIN;
-- 此时不创建ReadView
SELECT * FROM t; -- 创建ReadView1
-- 执行其他操作...
SELECT * FROM t; -- 创建ReadView2（新快照）
-- 两次SELECT可能看到不同的数据
-- 会话2
SET SESSION transaction_isolation = 'REPEATABLE-READ';
BEGIN;
-- 此时不创建ReadView
SELECT * FROM t; -- 创建ReadView（事务级快照）
-- 执行其他操作...
SELECT * FROM t; -- 复用同一个ReadView
-- 两次SELECT看到相同的数据

4. ReadView 的作用原理
可见性判断算法
bool changes_visible(trx_id_t id, const ReadView* view) {
    // 1. 自己修改的数据总是可见
    if (id == view->m_creator_trx_id) {
        return true;
    }
    
    // 2. 事务ID小于低水位线，且不在活跃列表中
    //    说明事务在快照前已提交
    if (id < view->m_up_limit_id) {
        return true;
    }
    
    // 3. 事务ID大于等于高水位线
    //    说明事务在快照开始后启动，不可见
    if (id >= view->m_low_limit_id) {
        return false;
    }
    
    // 4. 事务ID在低水位和高水位之间
    //    检查是否在活跃事务列表中
    return !binary_search(view->m_ids, id);
}


实际查找可见版本的流程


当前行（最新版本）
    ↓
检查创建事务ID（DB_TRX_ID）对当前ReadView是否可见
    ↓ 可见？
    ├── 是 → 返回该版本
    └── 否 → 通过DB_ROLL_PTR找到上一个版本
                ↓
            重复上述检查
                ↓
           直到找到可见版本或Undo Log末尾

5. 完整示例分析
-- 初始化数据
CREATE TABLE account (
    id INT PRIMARY KEY,
    balance DECIMAL(10, 2)
) ENGINE=InnoDB;

INSERT INTO account VALUES (1, 1000.00);

-- 时间线执行
-- T1: BEGIN; -- trx_id = 100
-- T2: BEGIN; -- trx_id = 101 (活跃事务列表: [100, 101])
-- T1: UPDATE account SET balance = 900 WHERE id = 1; -- 未提交
-- T2: SELECT * FROM account WHERE id = 1; -- 创建ReadView

-- T2的ReadView内容：
-- m_up_limit_id = 100 (最早活跃事务)
-- m_low_limit_id = 102 (下一个事务ID)
-- m_ids = [100, 101] (活跃事务列表)
-- m_creator_trx_id = 101 (T2自己的事务ID)

-- 当T2执行SELECT时：
-- 当前行版本：balance=900, DB_TRX_ID=100
-- 检查可见性：id=100，在活跃列表中 → 不可见
-- 通过Undo Log找到上一个版本：balance=1000, DB_TRX_ID=90
-- 检查可见性：id=90 < m_up_limit_id(100) → 可见
-- 返回：balance=1000（看不到T1未提交的修改）

6. ReadView 的生命周期管理

// ReadView的创建和销毁
class ReadViewManager {
public:
    // 创建新的ReadView
    ReadView* create_view(trx_id_t creator_trx_id) {
        ReadView* view = new ReadView();
        view->m_creator_trx_id = creator_trx_id;
        
        // 获取当前系统状态
        view->m_low_limit_id = get_next_trx_id();  // 下一个事务ID
        view->m_up_limit_id = get_oldest_active_trx_id();  // 最老活跃事务ID
        
        // 复制活跃事务列表
        copy_active_trx_ids(view->m_ids);
        
        return view;
    }
    
    // 关闭ReadView（事务结束时）
    void close_view(ReadView* view) {
        view->m_closed = true;
        // 放入复用池或删除
    }
    
    // 判断事务是否活跃（供Purge线程使用）
    bool is_active(trx_id_t trx_id, ReadView* view) {
        if (trx_id < view->m_up_limit_id) {
            return false;
        }
        if (trx_id >= view->m_low_limit_id) {
            return true;  // 在快照之后开始的，视为"活跃"（对Purge而言）
        }
        return binary_search(view->m_ids, trx_id);
    }
};


二、与PostgreSQL MVCC方案对比
架构对比概览
方面 MySQL InnoDB PostgreSQL
版本存储 Undo Log集中存储 Heap内联存储（表文件中）
版本标识 事务ID + Undo指针 xmin/xmax系统列
可见性判断 ReadView数据结构 Snapshot + xmin/xmax比较
清理机制 Purge线程异步清理 Vacuum进程（自动/手动）
空间管理 全局Undo表空间 每个表独立管理
更新操作 原地更新+Undo记录 写新版本+标记旧版本

1. 版本存储方式对比
MySQL InnoDB：集中式Undo Log

表空间结构：
表数据文件（.ibd）
    ├── 聚簇索引（B+树）
    │   ├── 行记录（当前版本）
    │   └── 隐藏列：DB_TRX_ID, DB_ROLL_PTR
    └── Undo Log段（通过指针链接）

版本链：当前行 → Undo记录1 → Undo记录2 → ...

优势：
• 二级索引不包含版本信息，空间占用小
• Undo Log集中管理，便于崩溃恢复
• 历史版本与当前数据物理分离

劣势：
• 查找历史版本需要遍历Undo Log链，可能较慢
• 长事务导致Undo Log膨胀

PostgreSQL：堆内联存储

表文件结构：
Heap文件（堆组织）
    ├── 页面1
    │   ├── 元组头（xmin, xmax, ctid）
    │   ├── 元组数据
    │   ├── 元组头（旧版本）
    │   └── 元组数据（旧版本）
    └── 页面2...

版本链：通过ctid指针链接


优势：
• 版本查找直接，通过ctid快速定位
• 每个版本完整独立，恢复简单
• Hot Update（仅更新变长字段）可避免索引更新

劣势：
• 表膨胀问题严重（多版本堆积）
• 每个索引都指向最新版本，需要VACUUM清理

2. 可见性判断机制对比
MySQL：ReadView算法

# MySQL可见性判断伪代码
def is_visible_mysql(trx_id, read_view):
    # 规则1：自己创建的数据
    if trx_id == read_view.creator_trx_id:
        return True
    
    # 规则2：事务在快照前已提交
    if trx_id < read_view.up_limit_id:
        return True
    
    # 规则3：事务在快照后开始
    if trx_id >= read_view.low_limit_id:
        return False
    
    # 规则4：检查是否活跃
    return trx_id not in read_view.active_ids


PostgreSQL：Snapshot + xmin/xmax

# PostgreSQL可见性判断伪代码
def is_visible_pg(xmin, xmax, snapshot, current_txid):
    # 规则1：插入事务未提交
    if not TransactionIdDidCommit(xmin):
        return False
    
    # 规则2：插入事务在快照之后
    if TransactionIdFollowsOrEquals(xmin, snapshot.xmax):
        return False
    
    # 规则3：插入事务在活跃列表中
    if TransactionIdIsInProgress(xmin, snapshot):
        return False
    
    # 规则4：检查删除
    if xmax != InvalidTransactionId:
        if not TransactionIdDidCommit(xmax):
            # 删除未提交，可见
            return True
        if TransactionIdPrecedes(xmax, snapshot.xmin):
            # 删除在快照前已提交，不可见
            return False
        if TransactionIdIsInProgress(xmax, snapshot):
            # 删除事务活跃，可见
            return True
    
    return True


3. 事务快照对比

MySQL快照（ReadView）

-- MySQL通过事务ID范围判断
活跃事务列表：需要精确记录每个活跃事务ID
实现方式：复制当前活跃事务列表到ReadView

-- 查看活跃事务
SELECT * FROM information_schema.innodb_trx;


PostgreSQL快照

-- PostgreSQL使用XID范围判断
快照格式：xmin:xmax:xip_list
示例：100:104:100,102
含义：所有<100的已提交，>=104的未开始，100,102是活跃事务

-- 查看快照
SELECT txid_current_snapshot();
-- 查看事务年龄
SELECT age(xmin), age(xmax) FROM pg_stat_activity;


关键差异：
• MySQL：需要维护精确的活跃事务列表
• PostgreSQL：使用XID范围+活跃列表，查询更高效

4. 清理机制对比

MySQL：Purge机制

-- InnoDB的Purge线程异步清理
-- 清理条件：
-- 1. 行版本对所有活跃ReadView都不可见
-- 2. 对应的事务已提交

-- 相关配置
SHOW VARIABLES LIKE 'innodb_purge%';
-- innodb_purge_threads = 4
-- innodb_purge_batch_size = 300


PostgreSQL：VACUUM机制

-- PostgreSQL需要显式或自动VACUUM
-- 清理条件：
-- 1. 元组对所有活跃快照都不可见
-- 2. 没有被任何索引引用（或通过HOT链）

-- 自动VACUUM配置
SELECT name, setting FROM pg_settings 
WHERE name LIKE 'autovacuum%';

-- 手动执行
VACUUM (VERBOSE, ANALYZE) table_name;


5. 性能特点对比

操作类型 MySQL InnoDB PostgreSQL 说明

点查询 优秀 优秀 两者都很快

范围查询 良好 良好 需要版本可见性检查

更新操作 优秀 中等 PostgreSQL需要复制整行

删除操作 优秀 中等 PostgreSQL标记删除，需要VACUUM

长事务影响 Undo Log膨胀 表膨胀 都会导致问题，但表现不同

二级索引维护 优秀 中等 PostgreSQL更新可能需更新所有索引

6. 实际使用对比示例

场景：长时间运行的报表查询

-- MySQL（使用REPEATABLE READ）
START TRANSACTION;
-- 创建ReadView（快照）
SELECT COUNT(*) FROM large_table; -- 长时间查询

-- 在此期间其他事务的UPDATE/DELETE
-- 不会影响此查询的结果一致性
-- Undo Log会保留旧版本直到查询结束

-- PostgreSQL
START TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- 获取快照
SELECT COUNT(*) FROM large_table;

-- 在此期间其他事务的UPDATE会产生新版本
-- 旧版本保留在表中，可能导致表膨胀
-- 长时间运行会阻止VACUUM清理

场景：高并发更新

-- MySQL热点行更新
UPDATE counters SET value = value + 1 WHERE id = 1;
-- InnoDB：行锁+Undo记录，性能较好
-- 但可能产生锁等待

-- PostgreSQL热点行更新  
UPDATE counters SET value = value + 1 WHERE id = 1;
-- 产生新版本，旧版本保留
-- 大量更新导致表膨胀，需要频繁VACUUM
-- HOT更新可减少索引维护


7. 配置优化建议

MySQL InnoDB优化

# my.cnf配置
[mysqld]
# Undo Log配置
innodb_undo_tablespaces = 2
innodb_undo_log_truncate = ON
innodb_undo_logs = 128

# Purge配置
innodb_purge_threads = 4
innodb_purge_batch_size = 300

# 长事务监控
innodb_rollback_segments = 128


PostgreSQL优化

-- postgresql.conf配置
# 自动VACUUM
autovacuum = on
autovacuum_max_workers = 3
autovacuum_vacuum_scale_factor = 0.1
autovacuum_analyze_scale_factor = 0.05

# 事务ID管理
vacuum_freeze_min_age = 50000000
vacuum_freeze_table_age = 150000000

-- 表级配置
ALTER TABLE large_table SET (
    autovacuum_vacuum_scale_factor = 0.05,
    toast.autovacuum_vacuum_scale_factor = 0.05
);


三、总结对比

设计哲学差异

方面 MySQL InnoDB PostgreSQL

设计目标 OLTP性能优化，空间效率 功能完整性，数据一致性

版本管理 集中式Undo Log，分离当前和历史 堆内联存储，版本与数据共存

清理策略 后台Purge，按需清理 VACUUM进程，定期或触发式

索引维护 二级索引指向主键，更新影响小 索引指向物理位置，更新可能需维护所有索引

选择建议

选择MySQL InnoDB当：
1. 需要更好的空间利用率，避免表膨胀
2. 更新密集型负载，特别是热点行更新
3. 希望自动化的Undo管理，减少运维
4. 使用二级索引较多的场景

选择PostgreSQL当：
1. 需要复杂查询和数据分析
2. 读多写少的场景
3. 使用JSON、GIS等高级数据类型
4. 需要更灵活的事务管理（如DDL事务）

性能关键指标

-- MySQL监控
SHOW ENGINE INNODB STATUS\G
-- 关注：
-- History list length（历史链表长度）
-- Undo log entries（Undo记录数）
-- Purge状态

-- PostgreSQL监控
SELECT 
    schemaname, relname,
    n_dead_tup, -- 死元组数量
    n_live_tup, -- 活元组数量
    last_vacuum, last_autovacuum
FROM pg_stat_user_tables;


发展趋势

1. MySQL 8.0改进：
   • 瞬时DDL（类似PostgreSQL）

   • 更好的Undo Log管理

   • 性能模式增强

2. PostgreSQL改进：
   • 并行VACUUM

   • 增量排序等查询优化

   • 逻辑复制增强

核心结论：
• MySQL的ReadView更注重性能和空间效率，适合高并发OLTP
• PostgreSQL的MVCC更注重功能完整性和数据一致性，适合复杂场景
• 两者都在不断改进，取长补短，选择应根据具体业务需求和技术栈决定