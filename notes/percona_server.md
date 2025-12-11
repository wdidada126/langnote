# percona server

https://www.oschina.net/p/percona+server

https://github.com/percona/percona-server

http://www.percona.com/downloads/Percona-Server-5.6/

Percona
Percona Server for MySQL
不支持windows

https://www.percona.com/downloads/Percona-Server-LATEST/#

Percona-Server-8.0.22-13-r6f7822f-el7-x86_64-bundle.tar	1.05 GB
Download Packages Separately
percona-mysql-router-8.0.22-13.1.el7.x86_64.rpm	4.4 MB
percona-server-client-8.0.22-13.1.el7.x86_64.rpm	12.0 MB
percona-server-debuginfo-8.0.22-13.1.el7.x86_64.rpm	551.3 MB
percona-server-devel-8.0.22-13.1.el7.x86_64.rpm	1.8 MB
percona-server-rocksdb-8.0.22-13.1.el7.x86_64.rpm	11.6 MB
percona-server-server-8.0.22-13.1.el7.x86_64.rpm	57.8 MB
percona-server-shared-8.0.22-13.1.el7.x86_64.rpm	1.4 MB
percona-server-shared-compat-8.0.22-13.1.el7.x86_64.rpm	1.2 MB
percona-server-test-8.0.22-13.1.el7.x86_64.rpm	429.2 MB
percona-server-tokudb-8.0.22-13.1.el7.x86_64.rpm	1.9 MB

doc
https://www.percona.com/doc/percona-server/LATEST/index.html

### Percona Server for MySQL 版本代码开源情况

是的，Percona Server for MySQL（简称 PS for MySQL） 的源代码是完全开源的。它是 Percona 公司基于 MySQL Community Edition 开发的增强版数据库服务器，采用 GPLv2 许可协议，免费提供给任何人使用、生产或修改，无任何企业版限制或锁-in。Percona 强调“保持开源开源”，其代码仓库公开托管在 GitHub 上，包含所有核心功能、增强特性（如更好的性能优化、审计插件）和构建指南。

#### 关键开源事实（2025年现状）
| 方面             | 详情                                                                 |
|------------------|----------------------------------------------------------------------|
| 许可协议     | GPLv2（与 MySQL Community 相同），允许自由分发、修改和商业使用。     |
| 开源程度     | 100% 开源，包括服务器核心、存储引擎（如 XtraDB）和工具链。           |
| 下载/访问    | 通过 GitHub 仓库克隆；官方二进制包也免费下载。                       |
| 企业支持     | 开源免费，但 Percona 提供付费支持服务（如 24/7 专家协助）。         |
| 兼容性       | 完全兼容 MySQL 协议，可作为 MySQL 的 drop-in 替换。                  |

#### 源代码访问地址
- 官方 GitHub 仓库：https://github.com/percona/percona-server  
  - 克隆命令：`git clone https://github.com/percona/percona-server.git`  
  - 文档与 Wiki：仓库内有 README、CONTRIBUTING.md 和安装指南；支持 MySQL 5.7、8.0+ 版本分支。  
  - 最新更新：截至 2025 年 12 月，仓库活跃维护，支持 MySQL 8.4 兼容和 ARM 架构优化。

#### 为什么选择 Percona Server？
- 优势：相比原生 MySQL，添加了企业级功能（如线程池、数据字典改进），性能提升 20-50%（读写并发场景），存储效率更高。  
- 适用场景：高负载 OLTP（如电商、金融），或需要免费审计/备份工具的团队。  
- 社区活跃：数千企业使用（如 Netflix、Twitter 衍生项目），Jira 问题跟踪器公开。

如果你需要构建指南、特定版本源码或迁移建议，推荐直接访问仓库或 Percona 官网（https://www.percona.com/mysql/software/percona-server-for-mysql）。
