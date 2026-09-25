# 03 — Record / Slotted Page Storage

- **对应讲次**：L04 Database Storage II（页结构）、L05 Storage Models
- **机制**：手写一个字节级 **slotted page**——固定头（num_slots、free_end）+ 从页头向后长的槽表 + 从页尾向前长的记录区；`(slot)` 作为稳定 TID，删除仅置 `size=0xFFFF` 墓碑（不即时回收，留 compaction）。再在其上包一层单页 **HeapTable**（行 = int id + string name 的序列化）。
- **文件**：`main.cpp`。
- **测试覆盖**：插入/点读/删除后其余 TID 稳定、scan 只返回活行、页满时拒收新记录。

## 构建
- Windows：`build.bat`（Developer Command Prompt）
- Linux/macOS：`bash build.sh`

## 与讲义的接缝
- free_end 与槽表相对生长 = L04"页内两个方向生长、中间是自由空间"。
- 删除留洞、scan 跳过墓碑 = Postgres 死元组 / InnoDB delete-mark 的最小缩影；真正回收靠 vacuum/purge（L18）。
- 记录 `Serialize/Deserialize` 的定长头 + 变长尾 = L04 记录格式（offset/length）的玩具版。
