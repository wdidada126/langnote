# 01 — Buffer Pool（Clock 置换 + 页固定计数）

- **对应讲次**：L06 Memory Management（缓冲池调度与分配）
- **机制**：固定帧数组 + pid→frame 页表；每帧 `pin_count`（>0 不可淘汰）、`is_dirty`（换出前须回写）、`ref` 引用位；**Clock / second-chance** 环形指针扫描近似 LRU，遇 `pin>0` 或刚给过第二机会的页跳过；池满且全被 pin 时 `FetchPage` 返回 nullptr（模拟资源耗尽）。
- **文件**：`main.cpp`（DiskManager 模拟盘 + BufferPoolManager + 自测）。
- **测试覆盖**：命中/未命中、脏页回写、跨帧淘汰后盘上值一致、全 pin 阻塞淘汰。

## 构建与运行
- Windows（MSVC，在 Developer Command Prompt）：`build.bat`
- Linux/macOS：`bash build.sh` 或 `chmod +x build.sh && ./build.sh`
- 手工：`g++ -std=c++17 -Wall main.cpp -o bufferpool && ./bufferpool`

## 与讲义的接缝
- `UnpinPage` 忘记调用 = BusTub P1 经典泄漏 bug（帧永远进不了淘汰候选）。
- `FlushPage` 对应后台 flusher；真正的"何时安全淘汰脏页"依赖 L19 的 WAL——脏页即使不回写也能从日志恢复。
- 参考 Postgres clock-sweep、InnoDB young/old LRU 双链。
