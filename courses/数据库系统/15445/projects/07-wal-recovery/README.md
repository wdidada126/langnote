# 07 — WAL Log & Redo/Undo Recovery（日志与撤销/重做）

- **对应讲次**：L19 Database Logging、L20 Database Recovery
- **机制**：顺序追加的 **WAL**（每条 Update 带 before/after image，LSN 单调）；
  内存页写即生效（**STEAL**）、提交只写 commit 记录不强制刷盘（**NO-FORCE**）；
  `Crash()` 让内存回退到最后落盘状态；`Recover()` 做 mini-ARIES：
  - **REDO**（正向、幂等）：重放所有已提交事务的 Update；
  - **UNDO**（反向、用 before-image）：回滚所有既未提交也未回滚的 loser 事务。
- **文件**：`main.cpp`。
- **测试覆盖**：A 提交+已刷盘/loser 未提交；B 提交但未刷盘靠 redo 复原；C 同键被 loser 覆盖需回退到提交值；D 显式 abort 立即回滚。

## 构建
- Windows：`build.bat`　Linux/macOS：`bash build.sh`

## 与讲义的接缝
- before="~" 表示键原本不存在——对应 ARIES 的 insert/delete 补偿。
- Checkpoint() 简化为"冻结刷盘"（非 fuzzy）；真实 ARIES 用 fuzzy checkpoint + dirty page table（见 L20 与 papers）。
- redo 幂等性靠页 LSN 判断，这里用"只重放提交事务"近似；扩展到 DPT/page-LSN 是不错的练习。
