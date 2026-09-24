# Build Your Own Database From Scratch

发现一本不错的书籍，名叫《Build Your Own Database From Scratch》，也就是从零实现一个你自己的SQL数据库，书中有完整的代码演示，用Go语言实现。
https://build-your-own.org/database/
《Build Your Own Database From Scratch》（也叫 BYO-DB）是 2024~2025 年全球最火的“动手写数据库”实战书，作者是日本独立开发者 d2（GitHub 同名），全书只有 200 多页，却能让你从零写出一个 能跑真实 SQL 的类 SQLite 数据库内核。

### 一、核心卖点（为什么这么多人推）

| 项目                | 这本书做到的事（几乎无人能敌）                                 |
|---------------------|-------------------------------------------------------------|
| 语言                | 纯 Go（2024 版） / 纯 Rust（2025 新版）二选一                 |
| 行数                | 完整内核 < 3000 行（Go 版） / < 2500 行（Rust 版）            |
| 功能完整度          | B+树存储引擎 + REPL + 类 SQLite SQL 子集 + 事务 + 崩溃恢复     |
| 难度曲线            | 第1页就能跑，第100页就支持 SELECT/JOIN，第200页支持 ACID     |
| 价格                | 免费 PDF + Gumroad 付费（约 30~50 美元）                       |
| 影响力              | 2025 年 HN / Reddit / 微博 / B站 刷屏，国内数据库培训机构直接拿来当教材 |

### 二、分章节实际能写出来的东西（2025 最新版目录）

| 章节 | 你写完这章后拥有什么能力 |
|------|--------------------------|
| 1    | 一个键值存储（类似 Bitcask） |
| 2    | 持久化的 B+树（支持范围查询） |
| 3    | 简易 REPL + 命令行交互 |
| 4    | 真正的 SQL Parser（手写递归下降） |
| 5    | 单表 SELECT/INSERT/UPDATE/DELETE |
| 6    | 多表 JOIN + 索引 |
| 7    | 事务 + WAL（Write-Ahead Log） |
| 8    | 锁与并发控制 |
| 9    | 崩溃恢复（Redo/Undo） |
| 10   | 真空（Vacuum）与页面碎片整理 |

写完第10章，你的项目能通过 SQLite 的 `test/select1.test` 大部分用例。

### 三、和同类书的对比（2025 年最新）

| 书名                        | 语言     | 行数   | 完整度       | 推荐人群                     |
|-----------------------------|----------|--------|--------------|------------------------------|
| Build Your Own Database     | Go/Rust  | ~3000  | ★★★★★       | 想最快跑通完整数据库的最佳选择 |
| Build Your Own Redis        | C        | ~4000  | ★★★★        | 只想学 KV                    |
| CMU 15-445/645 项目         | C++      | >2万   | ★★★★★       | 想进大厂数据库组             |
| Let's Build a Simple DB     | Rust     | ~5000  | ★★★★        | 偏学术，代码较散             |
| Writing a SQLite Clone      | C        | ~8000  | ★★★★★       | 想彻底理解 SQLite            |

一句话结论：想 1~2 周内写出一个能跑 SQL 的玩具数据库，BYO-DB 是 2025 年性价比最高、口碑最好的选择。

### 四、获取方式（2025 年最新）

- 免费版（PDF）：https://build-your-own.org/database
- 付费版（带完整代码 + 持续更新）：Gumroad 搜索 “build your own database”
- Rust 版（2025 新版）

国内很多人做完这本书后，直接拿去秋招/春招当“个人项目”，面试官一看“自己写过数据库内核”，基本当场 offer。

强烈建议：先用 Go 版 7 天写完，再用 Rust 版重写一遍，这才是 2025 年最硬的数据库入门路径。
## 跨年摘录（2020–2026 日常笔记聚合，2026-09-23 整理）

### 2025-08
> 《The Fine Art of Small Talk》《Simply Said》《How to Say lt》和《Business Vocabulary inUse》，以及更多惊喜哦！

