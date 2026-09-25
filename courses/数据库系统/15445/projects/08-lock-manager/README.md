# 08 — Lock Manager（2PL 锁管理器：冲突矩阵 + 死锁等待图）

- **对应讲次**：L16 Concurrency Control Based on Two-Phase Locking
- **机制**：`LockManager` 维护 `oid -> {持有者 map, 等待队列}`；S/X **冲突矩阵**（仅 S/S 兼容）；
  锁被冲突持有者占用时，为申请者建立 **wait-for 边（waiter -> 每个持有者）**，
  随即在等待图上做 **DFS 找环检测死锁**，有环则报 `Deadlock` 并给出牺牲者；
  `Unlock` 释放后尝试唤醒/授予排队的等待者；事务在 growing 期一直持锁（2PL）。
- **文件**：`main.cpp`。
- **测试覆盖**：S/S 兼容、X 阻塞读写、经典双事务循环等待被检测为 Deadlock、S→X 升级被另一读者阻塞、持锁到释放。

## 构建
- Windows：`build.bat`　Linux/macOS：`bash build.sh`

## 与讲义的接缝
- 死锁用**检测+回滚**（InnoDB 路线），未实现 **Wait-Die/Wound-Wait 预防**（L16）——可作为扩展。
- 简化处：waiter 记名不记模式（唤醒时按 S 授予）；真实实现须记住请求模式再精确授予。
- gap/next-key 锁、锁升级、意向锁属工业增量（L16 §1.5），本项目聚焦冲突矩阵与等待图核心。
