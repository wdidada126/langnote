# asg

你说的“ASG”如果是编译原理语境，那指的就是 Abstract Syntax Graph（抽象语法图） 或 Abstract Semantic Graph（抽象语义图），现在主流编译器前端基本都用 AST（Abstract Syntax Tree，抽象语法树） 了，但某些现代编译器/静态分析工具为了支持更复杂的语义查询和跨语言分析，会把 AST 进一步提升为 ASG（带语义边、作用域边、数据流边的图结构）。

下面是目前几个最知名的开源编译器/静态分析项目中明确实现了 ASG（或类 ASG） 的项目和网址（截至2025年11月都活跃维护）：

| 项目名称                  | ASG 类型                     | 语言支持          | 核心仓库地址（GitHub）                                      | 备注                                      |
|---------------------------|------------------------------|-------------------|-------------------------------------------------------------|-------------------------------------------|
| Joern                 | Code Property Graph (CPG) = AST + CFG + PDG + ASG | C/C++, Java, Kotlin, Python, JavaScript, LLVM-IR | https://github.com/joernio/joern                           | 目前最强大的开源 ASG 实现，安全圈标配     |
| CodeQL (开源部分)     | 类似 ASG 的语义数据库        | Java, C#, Python, JS, Go, C/C++, Ruby               | https://github.com/github/codeql                            | GitHub 自己的，查询语言超强                |
| Semgrep (核心引擎)    | 轻量级 Semantic Graph        | 20+ 语言          | https://github.com/semgrep/semgrep                          | 规则用 AST + 少量语义边，速度极快          |
| Tree-sitter + custom  | 可扩展为 ASG                 | 50+ 语言          | https://github.com/tree-sitter/tree-sitter                  | 配合额外 pass 可以生成完整 ASG            |
| Spoon (Java)          | 程序元模型（接近 ASG）       | Java              | https://github.com/INRIA/spoon                                      | 学术圈最爱，Java 程序分析神器              |
| Roslyn (.NET)         | Syntax Tree + Semantic Model | C#, VB.NET        | https://github.com/dotnet/roslyn                                    | 微软官方，语义模型已经非常接近 ASG         |
| Babel + Babylon + ESTree | 可扩展为 ASG              | JavaScript/TypeScript | https://github.com/babel/babel                              | JS 生态最全                                |
| PhASAR                | LLVM-based ASG (IFDS/IDE)    | C/C++ (LLVM)      | https://github.com/pdschubert/PhASAR                                | 学术界数据流分析标杆                       |
| Ghidra SRE Framework  | P-Code → ASG                 | 多语言反编译      | https://github.com/NationalSecurityAgency/ghidra            | NSA 开源，逆向工程里 ASG 做得最完整        |

最推荐上手的前三名（真正能直接玩到 ASG）：

1. Joern（强烈推荐）  
   一行命令就能把 C/Java/Python 代码变成可查询的图数据库：  
   ```bash
   ./joern --script examples/all.sc
   ```  
   然后用 Gremlin 或自带的查询语言直接问“所有从 user.input 流到 sink 的路径”。

2. CodeQL  
   直接在 VS Code 里写 QL 查询，GitHub 已经把上万仓库的 ASG 建好了。

3. Semgrep Pro + OSS 引擎  
   如果你只想快速写规则，Semgrep 的 semantic mode 已经接近轻量 ASG。

