# MyRocks
https://github.com/facebook/mysql-5.6/blob/fb-mysql-8.0.32/

### MyRocks 介绍与源代码访问地址

MyRocks是由Facebook（现Meta）开发的开源存储引擎，基于RocksDB（一个高性能的LSM-Tree键值存储库）集成到MySQL中。它旨在解决传统InnoDB引擎在存储效率和写放大方面的痛点，特别适合读多写少的OLTP场景（如Facebook的社交数据存储）。MyRocks于2016年左右开源，主要基于MySQL 5.6 分支，后续被MariaDB等项目集成。相比InnoDB，它能将存储空间压缩2-3.5倍，写放大降低10倍左右，但读性能略有牺牲（适用于Flash/SSD优化）。

#### 关键特性
| 特性           | 描述                                                                 | 优势 |
|----------------|----------------------------------------------------------------------|------|
| 存储引擎   | RocksDB 后端，支持列族（Column Family）和压缩（如 ZSTD/LZ4）         | 空间节省 70%+，写放大 <2x |
| 兼容性     | MySQL 5.6 兼容，支持二级索引、事务（但非全 ACID）                     | 易迁移现有 MySQL 应用 |
| 优化场景   | 读密集型工作负载，低延迟点查/范围扫描                                 | Facebook 生产环境验证，TPS 高达百万级 |
| 局限性     | 不支持全文索引/空间索引；MVCC 版本链较长可能导致膨胀                  | 适合 OLTP，不宜 OLAP |

#### 源代码访问地址
MyRocks 的源代码托管在 GitHub 上，由 Facebook 维护。官方仓库包含 MySQL 5.6 分支的完整实现，包括构建指南和 Wiki 文档。

- GitHub 仓库：https://github.com/facebook/mysql-5.6
  - 分支/路径：MyRocks 集成在主仓库中，核心代码位于 `storage/rocksdb` 目录。
  - 克隆命令：`git clone https://github.com/facebook/mysql-5.6.git`
  - 文档：仓库 Wiki（https://github.com/facebook/mysql-5.6/wiki）提供构建步骤、配置（如 my.cnf 中的 `rocksdb` 插件启用）和基准测试。

如果需要集成到 MariaDB（10.3+ 版本原生支持 MyRocks），可参考 MariaDB 官方仓库：https://github.com/MariaDB/server/tree/10.3/storage/rocksdb。

#### 2025 年现状
MyRocks仍活跃于生产环境（如Meta、Twitter衍生项目），但随着TiDB/YugabyteDB等分布式引擎兴起，其单机优化正逐步转向云原生变体。最新更新包括RocksDB8.x兼容和ARM支持。如果你需要构建指南或基准数据，推荐直接查看仓库的README和Wiki。
