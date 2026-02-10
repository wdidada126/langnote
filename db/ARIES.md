# ARIES (1992) 论文信息  

全称：ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging  
作者：C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh, Peter Schwarz  
发表：ACM Transactions on Database Systems (TODS)，Vol. 17, No. 1, March 1992, Pages 94–162  
这是数据库恢复领域的奠基性论文，几乎所有现代 DBMS（PostgreSQL、MySQL InnoDB、Oracle、SQL Server 等）的事务日志恢复机制都直接或间接受其影响。

### 论文全文下载地址（免费公开版本）
以下是可靠的公开 PDF 链接（基于学术机构/教育资源，2026年仍可访问，无需付费或登录）：

1. Stanford University 课程镜像（最稳定、完整版，推荐首选）：  
   https://web.stanford.edu/class/cs345d-01/rl/aries.pdf  
   （直接下载，约 70 页，包含所有图表和伪代码）

2. GitHub 学术论文存档（tpn/pdfs 仓库）：  
   https://github.com/tpn/pdfs/blob/master/ARIES%20-%20A%20Transaction%Recovery%20Method%20Supporting%20Fine-Granularity%20Locking%20and%20Partial%20Rollbacks%20Using%20Write-Ahead%20Logging%20(1992).pdf  
   （Raw 下载链接：https://raw.githubusercontent.com/tpn/pdfs/master/ARIES%20-%20A%20Transaction%20Recovery%20Method%20Supporting%20Fine-Granularity%20Locking%20and%20Partial%20Rollbacks%20Using%20Write-Ahead%20Logging%20(1992).pdf）

3. 其他镜像（备用）：  
   - UBC 课程 slides + 部分引用：https://www.cs.ubc.ca/~rap/teaching/504/2018W2/slides/aries.pdf（简版总结，非全文）  
   - ACM Digital Library（需机构访问或付费）：https://dl.acm.org/doi/10.1145/128765.128770

如果以上链接失效，可搜索关键词“ARIES Mohan 1992 pdf Stanford”或在 Google Scholar 上找引用链接，大多指向 Stanford 的教育镜像。

### 论文大纲（结构概述）
论文很长（约 70 页），但逻辑清晰，分为引言、核心算法、扩展讨论和总结。以下是主要章节结构（基于原文目录和常见总结）：

1. Introduction（引言，1–5 页）  
   - 动机：为什么需要新的恢复方法（支持细粒度锁、部分回滚、崩溃恢复）。  
   - 对比早期方法（Shadowing、Undo-only、Redo-only 等）的不足。  
   - ARIES 的三大原则：Write-Ahead Logging (WAL)、Repeating History、Logging Changes During Undo。

2. Preliminaries（预备知识，5–10 页）  
   - 基本概念：事务、锁、缓冲区管理、页面 LSN（Log Sequence Number）。  
   - WAL 协议规则（Redo、Undo、Undo-NextLSN）。  
   - 脏页表（Dirty Pages Table）、事务表（Transaction Table）的作用。

3. ARIES Normal Processing（正常操作阶段，10–20 页）  
   - 日志记录格式（Update、Compensation、Begin/End 等）。  
   - Checkpointing（模糊检查点）：如何记录 Dirty Pages Table 和 Transaction Table。  
   - 正常事务执行中的日志写入和锁管理。

4. ARIES Recovery（恢复算法，核心部分，20–40 页）  
   - 三阶段恢复（经典 ARIES 流程）：  
     - Analysis Phase（分析阶段）：从最后一个 checkpoint 开始前向扫描日志，重建 Dirty Pages Table 和 Transaction Table，确定 Winner（已 commit）和 Loser（需回滚）事务。  
     - Redo Phase（重做阶段）：从最早的 Dirty Page LSN 开始前向重做所有日志记录（即使已写盘的页面也要 Redo，确保 idempotence）。  
     - Undo Phase（撤销阶段）：逆向 Undo Loser 事务的更新，使用 Compensation Log Records (CLR) 记录 Undo 操作（CLR 本身不可 Undo）。  
   - 崩溃恢复中的细节：嵌套事务支持、部分回滚（Savepoint）、细粒度锁下的恢复。

5. Extensions and Variations（扩展与变体，40–50 页）  
   - ARIES 的变种：ARIES/NT（嵌套事务）、ARIES/CS（影子页面）、ARIES/RDS（远程数据访问）。  
   - 索引管理（ARIES/IM）、B-tree 等结构下的恢复。  
   - 与其他方法的对比（Shadow paging、System R 等）。

6. Performance Implications and Conclusions（性能影响与总结）  
   - 实验评估（模拟结果）。  
   - ARIES 的优势：简单、高效、支持细粒度锁、无需 fuzzy checkpoint 时的复杂性。  
   - 未来方向。

复现建议（简单 WAL + Recovery 目标）：
- 先读 Section 3–4（核心算法），重点看伪代码（Fig. 2–Fig. 10 左右的算法框）。
- 复现时可参考 xv6 或 bustub 的简单 WAL 模块起步，实现：日志追加、LSN、Redo/Undo、简单 checkpoint、Analysis-Redо-Undo 三阶段。
- 社区常复现简化版：只支持单表、页级恢复，不需细粒度锁。

需要我帮你总结某个具体阶段（如三阶段恢复的伪代码细节）或推荐基于 ARIES 的教学项目代码仓库吗？