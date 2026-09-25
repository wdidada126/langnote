# L17 高级优化：支配树、SSA 构造与经典优化族

> 讲次：CS143 L17 ｜ 阅读：龙书 ch10.1-10.6 ｜ 对应 HW5 压轴；projects/06_optimizer 实现其中三件套

## 核心概念

### 支配树（Dominator Tree）
```
d 支配 n（d dom n）：所有 entry→n 路径都经过 d；严格支配排除自身。
立即支配 idom(n)：除 n 外支配 n 的所有节点中"被其他每个支配者支配"的那个 ⇒ 唯一，构成树。
迭代算法（Cooper-Harvey-Kennedy 2001，RPO 序下几轮收敛）:
  idom(entry)=entry
  for n in RPO(≠entry):
    idom(n) = 首个已处理前驱 p
    for 其余前驱 q: idom(n) = Intersect(q, idom(n))   // 沿支配树同时上爬
Intersect(a,b): while a≠b: a=idom(a); b=idom(b)（按树深度取较大者先上爬）
支配边界（DF）：n 的 DF = { y | n 支配 y 的每个前驱但不严格支配 y }；
  while 循环体入口 ∈ DF(条件块)——φ 插入位置的集合论刻画。
```

### SSA 构造（Cytron et al. 1991 精髓）
1. 对每个变量 V 求"定义块集合 def(V)"。
2. φ 放置：从 def(V) 沿支配树"先 DF 后向上"扩散（迭代 worklist：块入队 → 其 DF 块放 φ 或标 V 待放置），只访问一次每块——φ 恰放在"多条入边版本不同"处，不冗余。
3. 重命名：支配树上 DFS 维护版本栈（name-stack），进入块压入新 def，退出回滚；使用点读栈顶；φ 参数取各前驱栈顶。
```
x=1; if c { x=2 } else { x=3 } print x
块: B0(x=1) → B1(x=2) / B2(x=3) → B3(print x)；DF(B0)={B3}
SSA: B0: x1=1; B1: x2=2; B2: x3=3; B3: x4=φ(x2,x3); print x4
性质：每个使用恰好一个到达定义（def-use 链即时可查）→ 常量传播/DCE 退化为图可达。
```

### 优化族谱与最小实现（projects/06 的三件套）
- **常量折叠**：`a=2; b=a*3` → 生成期或 pass 内直接把表达式归约成常数（L9 的 S 属性视角：编译期可求值 = 折叠）。
- **常量传播**（SCCP 带分支消除）：格映射迭代；`if 0 goto L` → 删除不可达块——可达性随常数演化。
- **复制传播**：`b=a` 后用 b 处替换为 a，再 DCE 掉无用的 `b=a`；SSA 上即 φ 消除（select/平行赋值实现）。
- **死代码消除（DCE）**：从"有副作用指令"（store/调用/print/分支）沿 use-def 链反向标记存活，未标记即删——SSA 上一步可达性遍历；龙书"可达定义"框架的反向应用。
- **GVN / CSE**：同操作数同算子 → 同值编号；SSA 上 GVN 简化为"值编号 + 支配"：若 `a=x+y` 支配点可见则复用。Hash-cons 表达式（Shebanow 风格）：树节点驻留哈希表，构造即去重。
- **循环优化**（依赖 L13 可归约 + L14 RPO）：强度削弱 `i=i+1; t=t+4` 中乘法链化加法；归纳变量识别（基归归纳）；循环不变量外提 LICM；软件流水/交换/分块（多面体模型见 MLC 对照）。
- 优化管线是**顺序敏感的不动点过程**：`instcombine → simplifycfg → licm → gvn → dce` 循环至收益<阈值——"pass 顺序即编译器配方"。

## 与前后讲的联系
- 综合课：L12 的 SSA 引介在这里给出算法；L14 的框架在 SSA 上几乎都能"一行可达性"替代；L16 的活跃性在 SSA 上就是"def 到 last use"。
- 向后：优化后程序才是喂给 L15 代码生成的输入；PA5 的自主加分项（循环优化/内联）全部出自本讲菜单。

## 跨课程联系
- **6.006/CS170**：支配树迭代 = 图算法课"半支配/LT 序"的简化版；φ 放置的"沿 DF 扩散"是树+图混合遍历（DSU 优化版本用并查集）。
- **CS242/软件分析**：SSA 与函数式 IR（无赋值）的联系——"版本栈重命名"就是 let-binding 消除赋值；Rust 借用检查直接消费 MIR-SSA。
- **MLC/10-414**：XLA/TVM 的代数重写（fusion、layout 变换）与本讲同源：重写系统 + 代价模型 + 不动点；"机器学习的编译器"优化循环同样先 DCE/GVN 再调度。
- **CSAPP**：`gcc -O2` 打开 GCC 的 100+ pass 管线；`-fopt-info-optimized` 打印实际触发的本讲优化——每条笔记内容都能在真实二进制里找到证据。

## 开源项目中的应用
- **LLVM**：`-instcombine/-licm/-gvn/-dce/-sccp` 每个开关即本讲一节；NewGVN（表达式格+向下兼容支配）是 2016 后的当代 GVN。
- **MLIR**：`-cse/-canonicalize/afflicm` 方言化复用同一批算法；重写规则 DSL（pattern builder）把"翻译模式"升级为规则库。
- **rustc**：MIR 优化管线（const-prop、GVN、DCE）刻意保持精简——IR 语义（drop flag）限制激进重写，"优化必须尊重语言合同"的案例。
- **Z3/CBMC**：优化正确性验证方向（Alive2 用 SMT 证明 peephole/IR 重写等价）——本讲一切重写都可以被"证明"而不仅是"测试"。
- **GCC**：Tree-SSA（2004 起）完整实现 Cytron 式构造 + PHI 传播优化，论文即 GSV 原文级材料。

## 延伸阅读
- Cytron et al. 1991（SSA 原文，φ 放置算法）；Cooper et al. 2001（支配树简易算法）。
- Click 1995 "Efficient Demand-Driven Value Numbering"（gvn 的现代形式）；Shebanow 1992 关于 hash-cons GVN 的工程论文。
- Kennedy & McKinley 1993 循环优化分类综述；LLVM 博客 "NewGVN" 系列文章。
