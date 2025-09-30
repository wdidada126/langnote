# zstd

## 源代码
https://github.com/facebook/zstd

## 编译安装
vcpkg install zstd

Zstandard (zstd) 是 Facebook 开发的高性能无损压缩算法

## 数据库
OceanBase支持多种压缩算法包括lz4、zstd和snappy

<dependency>
    <groupId>com.github.luben</groupId>
    <artifactId>zstd-jni</artifactId>
    <version>1.5.5-2</version>
</dependency>

http://archive.ubuntu.com/ubuntu/pool/main/libz/libzstd/libzstd-dev_1.5.5%2bdfsg2-2build1.1_amd64.deb

OceanBase 中的 zstd 实现
1. 存储引擎集成架构
OceanBase 采用 LSM-Tree 存储架构，zstd 作为其通用压缩算法之一，与自研编码技术协同工作：

•
分层存储：数据分为宏块(2MB)和微块(变长)两级

•
压缩时机：在 compaction 过程中批量压缩落盘

•
异步解压：通过后台I/O线程解压，避免阻塞查询

2. 压缩配置示例
在 OceanBase 中可通过 DDL 指定表的压缩算法：

CREATE TABLE account_info (
    id BIGINT PRIMARY KEY,
    name VARCHAR(100),
    balance DECIMAL(15,2)
) COMPRESSION = 'zstd' 
  REPLICA_NUM = 3 
  BLOCK_SIZE = 16384;
参数说明：

•
COMPRESSION: 指定压缩算法(zstd/zlib/lz4/snappy)

•
REPLICA_NUM: 数据副本数

•
BLOCK_SIZE: 微块大小(影响压缩粒度)

3. 性能对比
OceanBase 中不同压缩算法的表现：

算法

压缩速度

解压速度

压缩比

适用场景

zstd

中

快

高

通用场景

lz4

最快

最快

低

高性能需求

zlib

慢

中

高

高压缩比需求

snappy

快

快

中

平衡型需求

实际案例：某客户历史库迁移至 OceanBase 后，使用 zstd 压缩使存储成本降低80%

三、高级功能实现
1. 自适应编码+zstd 二级压缩
OceanBase 的创新压缩流程：

1.
数据编码：先使用bit-packing/字典编码/差值编码等去除结构化冗余

2.
通用压缩：再用 zstd 进行二次压缩

3.
自适应选择：根据数据特征动态选择最佳编码组合

2. 列间压缩技术
针对多列关联数据的特殊优化：

-- 列间等值编码示例（自动识别）
CREATE TABLE order_items (
    order_id VARCHAR(20),
    item_id VARCHAR(24) -- 自动识别为order_id的后缀
) COMPRESSION = 'zstd';
原理：当 item_id 是 order_id 的子串时，只存储差异部分

3. 冷热数据分层压缩
OceanBase 针对不同温度数据采用差异化策略：

数据类型

压缩策略

zstd级别

存储位置

热数据

快速压缩(lz4/zstd低级别)

1-3

高性能SSD

温数据

平衡压缩(zstd中等级别)

5-10

普通SSD

冷数据

高压缩(zstd高级别)

15-22

高容量HDD

四、最佳实践建议
1.
参数调优：
• 交易型表：使用 zstd level 1-3
• 分析型表：使用 zstd level 10-15
• 归档数据：使用 zstd level 19-22

2.
监控指标：

-- 查看压缩效果
SELECT table_name, 
       compression_ratio, 
       compression_algorithm 
FROM oceanbase.__all_virtual_table_stat;
3.
异常处理：

• 解压失败时 OceanBase 会自动从其他副本恢复数据
• 可通过 ALTER TABLE ... SET COMPRESSION='zstd'在线变更算法

4.
限制注意：

• 压缩后的单行数据不宜超过256KB
• 高压缩级别会增加CPU使用率
• 频繁更新的表建议使用lz4而非zstd

Zstandard 在 OceanBase 中的深度集成，使其在保证高性能的同时实现了显著的成本节约，特别适合海量数据存储场景。通过自适应编码与zstd的结合，OceanBase在TPC-H测试中展现了比传统数据库更优的存储效率
