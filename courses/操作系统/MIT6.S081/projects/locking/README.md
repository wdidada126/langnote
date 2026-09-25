# locking — 自旋锁 / 互斥锁 / epoch-RCU 演示（pthread / Win32）

对应讲次：**L02（锁与并发）**、**L15（RCU 与无锁读）**；lab-lock / lab-thread 的用户态微缩版。

## 机制说明

| 部件 | 对应内核代码 | 说明 |
| --- | --- | --- |
| `pth.h` 自旋锁 | xv6 `spinlock.c: acquire/release` | test-and-set（`InterlockedExchange`/`__sync_lock_test_and_set`）+ 指数退避 + acquire/release 栅栏；"关中断"在用户态不需要，其余语义一致 |
| `pth.h` 兼容层 | — | POSIX 走 pthread；Windows 走 CreateThread/CRITICAL_SECTION。原子操作只用编译器 builtin/Win32 API，无第三方依赖 |
| epoch-RCU | lab-thread / Linux `kernel/rcu` | 读者登记自己的 epoch（`tstate[tid]`），退出即静默；写者推进 epoch、把删除的节点挂退役表，**全员越过旧 epoch（grace period）后才 free** |
| 负载 | — | 有序链表：4 读者 × 60k 次查找 + 2 写者 × 2k 次插删；三种保护模式跑同一负载，输出吞吐/命中率/回收统计 + 链表完整性校验 |

实验看点：
1. **RCU 读端最快**：没有锁、没有共享计数器写——读吞吐显著高于 mutex/spin（读者不互相干扰）；
2. **回收才是难点**：终端输出会打印 `reclaimed/pending`——pending>0 即"还有旧读者在看，节点不能死"；
3. main.c 末尾的"危险改造"：把 `retire(x)` 改成 `free(x)` 重跑，会大概率段错误——
   亲手撞一次 use-after-free，比读十页论文更懂 RCU。

## 构建与运行

Linux/macOS（MinGW 同理）：
```sh
./build.sh        # cc -pthread → lock_demo
```
Windows（Developer Command Prompt）：
```bat
build.bat         # cl → lock_demo.exe（自动链接 kernel32，无需 pthread 库）
```

## 已知简化
- 内存序用"够用"的 `__sync`/`MemoryBarrier` 近似，不是 C11 atomics 的正式 acquire/release（MSVC 的 C11 `<stdatomic.h>` 支持史是坑，故走保守路线）；
- 写者内部仍有自旋锁（"多写者 RCU"如 boost::concurrent 需要 CAS 环——留作练习）；
- grace 判定是"扫描所有线程槽"的教学版 O(n)；Linux Tree RCU 用分层收敛把扫描摊薄。
