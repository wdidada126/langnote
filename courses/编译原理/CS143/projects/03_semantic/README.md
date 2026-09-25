# Stage 03 — 符号表与静态类型检查

- **对应讲次**：`notes/L09`（属性视角）、`notes/L10`（符号表/作用域/类型规则）
- **对应 CS143 PA**：PA3（COOL 语义检查器）。差异：MiniC 无类层次，故没有
  `lub/最小公共祖先` 规则——该规则的完整实现思路见 notes/L10 与 notes/L18。
- **核心代码**：`../common/checker.h`（本阶段新增），驱动 `main.cpp`

## 知识点落点（代码 ↔ 讲义）

| 讲义概念 | 实现位置（checker.h） |
| --- | --- |
| 符号表 = 作用域栈 | `std::vector<std::unordered_map<std::string, Ty>> scopes_` |
| 两遍法（允许互递归/前向引用） | `checkProgram` 先收集 `funcs_` 签名再查体 |
| 类型规则表 = 继承+综合属性 | `checkExpr`：环境向下流（lookup），类型向上汇（`e.type`） |
| 遮蔽 vs 同层重声明 | `declaredHere`（同层报错）与 `lookup`（允许外层遮蔽） |
| 哨兵类型防级联 | 出错节点置 `Ty::Unknown`，后续只与"已知"比较 |
| 初始化式看不到自身绑定 | `int x = x;` 中 x 在 `scopes_.back()[x] = type` **之前**被查——按 C 语义报错 |
| return 可达性 | 只检查函数体最后一条语句（语法近似 → warning，见 notes/L14：真正的路径分析是数据流问题） |

## 构建 / 运行

```sh
./build.sh && ./minic03 ../samples/bad.minic   # 应报告 6 处类型错误
./minic03 ../samples/hello.minic               # PASS
```
```bat
build.bat && minic03.exe ..\samples\bad.minic
```

## 动手实验
1. 把 `print isEven(17);` 改成 `print 1 + true;`：观察 '+' 规则报错。
2. 给 `helper` 增加一个参数，调用端不改：参数个数错误。
3. 在 `main` 里写 `int y = y;`：体会"绑定在初始化之后才可见"。
4. 进阶：实现龙书 5.6 的"函数重载禁止"或"变量必须先声明后使用（无遮蔽）"，只需改两处函数。
