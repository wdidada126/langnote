# L06 约束满足问题 CSP：回溯、MRV/LCV、AC-3

> 对应 AIMA Ch.6；Klein 讲义 "CSP I/II"。把 L02 搜索的"状态=部分赋值"推到极致。

## 1. 核心概念

- **CSP 三元组**：变量 X、域 D、约束 C；解 = 满足全部约束的完整赋值。
  - 与 L02 对比：状态空间固定 n 个槽位、目标 = 全约束满足、路径无序化（组合而非排列）。
- **回溯搜索** = DFS + 单元传播：每次只扩展一个变量赋值，冲突即剪。最坏 O(d^n)。
- **智能排序**：
  - **MRV**（minimum-remaining-values）：选域最小的变量——"失败先发生"。
  - **LCV**（least-constraining-value）：选对其他变量约束最少的值。
- **推理加速**：
  - **FC**（forward checking）：赋值后即时删除邻居未赋值变量的冲突值。
  - **AC-3**（arc consistency）：反复对每条弧 (Xi,Xj) 做 revise——Xi 中无支持值的元素删除；队列驱动 O(n²d³)。
  - **CJ**（constraint joining）合并二元约束；高阶约束降元。

## 2. 关键伪码

```
function AC-3(csp):
    queue ← all arcs
    while queue:
        (Xi,Xj) ← pop()
        if REVISE(Xi,Xj):           # 删除 Xi 中无支持的值
            if |Di|==0: return false
            queue += arcs(Xk,Xi) for all k≠j
function BACKTRACK(csp, var_order=MRV, prune=FC):
    if complete: return assignment
    v ← SELECT-VAR(MRV); for val in ORDER(LCV):
        if consistent: assign; recurse; undo
```

## 3. 直觉例子

- 地图着色（WA/NT/SA…）：AC-3 一步就能把 SA 域收缩；数独 = CSP 圣杯（MRV+AC 求解器秒解 9x9）；8-queens 用"列=变量，行=值"编码后 n-queens 局部搜索与 CSP 两路都能解（对照 L04）。
- 排课/频段分配（frequency assignment）是 CSP 工业主场。

## 4. 前后讲联系

- 前承 L02-L04（搜索+局部视角：min-conflicts 即 CSP 爬山）；后接 L07（结构性突破：树分解）、L9-L10（CSP 是贝叶斯网络推断的特例——证据为 0/1 的硬约束）、L18 采样（推断难 ⟹ 采样）。

## 5. 跨课程联系

- **6.006/CS61B**：d^n 指数下界与 SAT NP 完全性（CSP ⊇ k-coloring）；6.006 "不可解问题"讲座的实例库。
- **CS229**：结构化预测 CRF 的解码 = CSP/DP（Viterbi 同 L17）。
- **MIT6.824**：分布式约束满足（DCSP）用于多机器人协同——共识问题可写成一致性约束。
- **DDCA**：组合测试/时钟网表验证本质是 SAT/CSP；FPGA 布线 = 资源约束满足。

## 6. 开源项目应用

- **python-constraint**（教学级 AC-3+回溯，与本课程项目风格完全一致）；**OR-Tools CP-SAT**（工业级：传播+搜索+SAT 混合，调度冠军）。
- **MiniZinc**：约束建模语言 + 一堆后端求解器；**Z3**（SMT，程序验证版 CSP）。
- 数独求解器：`projects/planning` 邻近——可把 sudoku 作为 AC-3 演示扩展。

## 7. 延伸阅读

- AIMA 4e §6.1-6.5；CS188 Note "CSPs"。
- Mackworth "Consistency in Networks of Relations" (1977, AC 算法)；Haralick & Elliott "Foward Checking" (1980)；Dechter《Review of AI: Constraint Networks》。
