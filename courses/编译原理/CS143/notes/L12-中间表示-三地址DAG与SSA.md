# L12 中间表示：树、三地址码、DAG 与 SSA

> 讲次：CS143 L12 ｜ 阅读：龙书 ch8.1-8.2 ｜ 配套：projects/04_ir（三地址码）；SSA 深入见 L17

## 核心概念

### IR 设计光谱
- 树形（AST 直译）：贴近源码，语义分析后仍保留高层信息（Clang AST → LLVM 前的 "Instruction Building" 阶段）。
- 线性（三地址码/四元式）：`x = y op z` 加跳转/标签，每条至多一个运算——数据流分析友好。
- 图（DAG）：显式共享子表达式，GVN 的原始形态。
- SSA（每个变量单次赋值，φ 函数汇合）：现代编译器通用货币（LLVM IR、JVM HotSpot C2、rustc MIR）。
- 粒度谱：HIR（高层）→ MIR → LIR，一个编译器多副 IR 面孔已是常态。

### 三地址码记账法
```
addr(x) = 名字(x) 或 临时名 t1,t2,...
x = -y        →  t = 0 - y        （单目归一）
x = y         →  MOVE             （或保留 COPY，供复制传播消费）
if x goto L   →  IFZ / IFNZ + 显式比较
数组 A[i]：t1 = i * 4; t2 = &A + t1; x = load t2   ← 间接寻址显式化
```
- COOL/PA4 使用"抽象汇编树"（每个 COOL 节点带寄存器/栈约束标签）——介于树与三地址之间的课程定制 IR，理解本讲后能看懂它为何两不像却又够用。

### DAG：公共子表达式的"出生证明"
```
a = b + c; d = a + e; a = e + b; d = a - d;
DAG 折叠后: b+c 与 e+b 同一节点 ⇒ a 的新值即旧 a（节点复用），
d 被重定义 ⇒ 旧 d 节点可能变死。
DAG 表示 = "值编号 (value numbering)" 的图形化，直接导出 GVN（L17）。
```

### SSA 最小样例 + φ 插入（Cytron 算法预告，细节 L17）
```
x = 1; if c { x = 2 } else { x = 3 }
SSA:  x1 = 1; if c { x2 = 2 } else { x3 = 3 }  x4 = φ(x2,x3); print x4
规则：每个 store 定义一个新版本号；使用点引用"支配该点的最内层定义"；
汇合点（多条入边且版本不同）插 φ。
```

### 选择 IR 的工程准则
- 优化目标决定 IR：要跑数据流框架 → 线性+CFG；要结构重写（循环变换/多面体）→ 树/区域嵌套（MLIR 的 affine 方言、Polly 的 SCoP）。
- 类型信息放哪：LLVM IR 弱类型（类型标签极简），Rust MIR 保留类型擦除前信息——本讲无标准答案，只有权衡。

## 与前后讲的联系
- 上游：L10 类型标注、L11 帧布局是 IR 生成的输入；L13 交付 IR 的生产流水线。
- 下游：L14 数据流、L15 指令选择、L16 活跃性都在 IR 上定义——IR 换掉，下游全部重写（这就是 L1 的 m+n 论据）。
- SSA 与本讲 DAG 的深层关系：SSA 是"把依赖显式进图"的 DAG 推广——φ 节点即多入边的值节点。

## 跨课程联系
- **CS61A**：字节码/AST 求值 = 两种最朴素 IR；"环境模型"对应 SSA 的支配树（见 L17）。
- **MLC/10-414**：TVM Relay（函数式 IR）→ TIR（循环 IR）→ LLVM 的三段 lowering 是"多 IR 光谱"的当代最佳案例；PyTorch 的 TorchScript/excutorch IR 亦然。
- **15-445/CS186**：查询计划树/火山模型 iterator ≈ 数据库界的"IR + 解释执行"组合——同一套阶段划分换个域名重现。
- **6.006/CS170**：CFG 是图算法的舞台；SSA 构造依赖支配树（Lengauer-Tarjan，见 L17 延伸阅读）。

## 开源项目中的应用
- **LLVM**：SSA 型三地址 + 强类型标签的最小可行语言，官方 LangRef 值得通读——当代 IR 设计的教科书。
- **MLIR**：把"IR 方言"本身做成基础设施（多方言共存、渐进 lowering）——对 L12 问题的结构性回答。
- **rustc MIR**：为借用检查设计的"半高级 IR"：保留 move/copy/drop 语义细节——IR 可以为首发消费者（borrowck）定制。
- **CPython bytecode / WASM**：两种栈式 IR；栈式 IR 短小易发射，寄存器式 IR 利于优化——L15 再对照。
- **tree-sitter** 不做 IR；但 "TS→AST→LSP" 场景提醒：并非所有工具都要三地址，IR 选择跟着用途走。

## 延伸阅读
- 龙书 ch8.1-8.2；LLVM LangRef（导论部分）。
- Cytron et al. 1991（SSA 原文，L17 精读）；Cooper & Torczon "Engineering a Compiler" IR 章（比龙书更现代）。
- MLIR 论文（Lattner et al., PLDI 2021）。
