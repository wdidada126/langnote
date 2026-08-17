# Perennial：验证并发、崩溃安全 Go 系统的框架

## 它是什么

Perennial 是 MIT PDOS 维护的系统验证框架，用于证明同时存在并发和崩溃恢复需求的系统正确性。它构建在 Iris 之上，并通过 Goose 将受支持子集的 Go 程序转成可在 Coq/Rocq 中推理的 `goose_lang` 表示。Perennial 的关注点包括并发安全、持久化状态、崩溃后的恢复过程和模块化 refinement；Grove 是同一生态中面向分布式系统的扩展。

它的核心价值是让系统程序证明不只停留在伪代码：证明可以连接到实际 Go 源码的受支持部分、其内存并发语义和显式建模的外部系统调用。它不是把 Go 程序“编译为绝对正确的二进制”，而是要求开发者同时提供实现、规格、环境模型和 Coq 证明。

```text
Go 源码（受 Goose 支持的子集）
    -> Goose 翻译
goose_lang：带内存、并发和外部 FFI 语义的目标语言
    -> Perennial program logic（基于 Iris）
并发、崩溃、恢复、幂等与 refinement 规格
    -> Coq/Rocq 内核检查的证明
```

## Perennial 提供的能力

| 能力 | 解决的问题 | 典型用途 |
| --- | --- | --- |
| 并发程序逻辑 | 多线程访问、锁、原子操作、共享内存不变式 | 并发 map、日志、缓存、事务管理器。 |
| crash weakest precondition | 程序任意崩溃点后仍应满足什么恢复前提 | 写前日志、copy-on-write、检查点、幂等恢复。 |
| crash invariants | 将持久化状态与恢复代码需要保持的约束关联 | 文件系统元数据、数据库页/日志、持久队列。 |
| idempotence / recovery helping | 多次重放恢复过程或由其他线程完成某步骤时仍正确 | 崩溃恢复、后台清理、协作式并发任务。 |
| refinement | 证明复杂实现细化一个更简单的抽象状态机/接口 | 将日志、缓存、并发协议隐藏在事务或文件系统 API 后。 |
| Goose | 连接 Go 源码与证明语言 | 验证实际实现，而不是仅验证重新手写的伪代码。 |

Perennial 的 `goose_lang` 是有内存、并发和可通过 FFI 建模外部世界的 lambda calculus；它不是完整 Go 语言规范。因此使用前必须确认目标代码、标准库调用、反射、unsafe、cgo、网络/磁盘接口是否有对应翻译和模型。

## 与 vMVCC 的关系

vMVCC 是 Perennial 生态中的一个被验证案例，不是 Perennial 本身。它实现高性能事务性键值库：为事务分配严格递增时间戳，保留旧版本供读者读取，通过 `tslast` 与锁检测冲突，并在安全时间点回收旧版本。

vMVCC 的 Go 实现由 Goose 引入证明环境，再借助 Perennial/Iris 证明其事务规格。论文将 `db.Run` 的规格解释为严格可串行化事务语义的程序逻辑形式化；证明覆盖该并发事务库的算法与优化，例如 RDTSC 驱动的严格递增时间戳、版本 GC 和逻辑原子性。

必须区分“框架可表达什么”与“这个案例已证明什么”：Perennial 支持崩溃安全推理，但 vMVCC 论文的主要贡献是并发 MVCC 事务库验证。不能据此断言 vMVCC 已经验证 WAL、磁盘落盘、SQL、复制、分片、网络故障恢复或完整数据库 ACID 实现。

## 阅读源码时的目录地图

Perennial 主仓库的结构会持续演进，阅读时以目标 commit 的 README 为准。当前目录职责大致为：

| 路径 | 作用 |
| --- | --- |
| `src/program_logic/` | 崩溃安全推理库，包括 crash WP、crash invariant、幂等和 crash refinement。 |
| `src/goose_lang/` | Goose 的目标语言及其与 Iris/Perennial 接口。 |
| `src/program_proof/` | 已验证系统的证明；vMVCC 对应 `program_proof/mvcc`。 |
| `src/Helpers/` | 整数、状态关系、列表等复用辅助库。 |
| `src/algebra/`、`iris_lib/`、`base_logic/` | 对 Iris 的扩展与基础逻辑组件。 |
| `external/Goose/` | 若干真实 Go 代码经 Goose 生成并提交的结果。 |

仓库正在迁移到与旧版不兼容的 “new Goose”。因此教程、论文 artifact、旧 tag 和当前 `main` 不能假设 API/目录完全一致；复现实验时应使用论文指定的 tag 或 lockfile，而不是盲目追最新版本。

## 最小实践流程

1. 先在独立 opam switch 或 Nix development shell 中准备依赖，避免污染本机其他 Rocq 项目。
2. 固定 Perennial commit，按仓库 README 安装依赖并运行 `make`，先确认既有证明可以通过。
3. 选择很小的 Go 模块，明确抽象状态、操作规格、崩溃模型和信任的 FFI；先翻译并检查 Goose 输出。
4. 在 Perennial/Iris 中写资源谓词、模块不变式和 WP 规格，逐函数证明，再组合为端到端定理。
5. 将证明作为 CI 的一部分，同时保留普通单元/集成/故障注入测试。形式化证明补强模型内正确性，测试覆盖真实环境、性能和未建模集成。

## 常见误区

- **“Go 测试全绿，所以 Goose 证明容易。”** 测试只能采样执行；证明必须解释所有可能调度、失败路径与资源所有权，工作量差异很大。
- **“Perennial = Coq。”** Coq/Rocq 是证明器，Iris 是并发逻辑，Perennial 是更上层的 Go/崩溃安全框架，Goose 是翻译桥梁。
- **“验证了程序就没有硬件/运维风险。”** 时钟、持久化原子性、文件系统/网络 FFI、编译器、部署配置和资源耗尽都必须纳入模型或单独控制。
- **“每个服务都应该引入 Perennial。”** 它更适合小而关键、错误代价极高、并发和恢复逻辑复杂且语义可明确的底层组件；证明维护成本需要长期预算。

## 学习顺序

1. Coq/Rocq 基础与普通分离逻辑。
2. Iris Tutorial：所有权、invariant、ghost state、logical atomicity。
3. 阅读 Perennial README、SOSP 2019 论文和一个小型已验证案例。
4. 阅读 vMVCC 算法，再对照 `program_proof/mvcc`；先理解规格与不变式，再进入 tactics。
5. 尝试为一个不涉及外部 I/O 的小 Go 并发容器建立规格。只有在模型明确后再加入 crash/FFI 和恢复逻辑。

## 参考资料

- Perennial 源码、构建说明与目录结构：<https://github.com/mit-pdos/perennial>
- Perennial 项目介绍与 SOSP 2019 论文入口：<https://www.chajed.io/perennial/>
- vMVCC 项目、论文、代码与证明：<https://pdos.csail.mit.edu/projects/vmvcc.html>
- vMVCC OSDI 2023 论文：<https://iris-project.org/pdfs/2023-osdi-vmvcc.pdf>
- Iris 项目：<https://iris-project.org/>
