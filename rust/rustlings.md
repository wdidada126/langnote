# rustlings
https://rustlings.rust-lang.org/usage/

Rustlings 是一个由 Rust 官方团队维护的互动式 Rust 学习工具，专门设计来帮助初学者通过大量小练习快速上手 Rust 语法和核心概念。

简单一句话总结：  
Rustlings = “Rust 的 LeetCode / Rustlings 小练习集合”，但它更专注于“让代码先编译通过 + 通过测试”，而不是算法题。

### 它到底干啥的？

- 给你一堆故意写错的 Rust 文件（.rs），里面有编译错误或测试失败。
- 你需要修改代码让它编译通过（大多数情况），有些还需要让内置测试（tests）通过。
- 边改边学：借用检查器（borrow checker）、所有权、生命周期、泛型、trait、智能指针、错误处理、并发等核心内容都覆盖。
- 它和《The Rust Programming Language》（官方书，俗称 The Book）高度配套，推荐边看书边做 Rustlings。

官网 slogan：  
“Small exercises to get you used to reading and writing Rust code — Recommended in parallel to reading the official Rust book 📚️”

### 典型使用流程（超级友好）

1. 安装 Rust（rustup）后，安装 Rustlings：
   ```bash
   curl -L https://raw.githubusercontent.com/rust-lang/rustlings/main/install.sh | bash
   # 或者 cargo install rustlings --force
   ```

2. 进入练习目录：
   ```bash
   cd rustlings
   rustlings watch   # 启动“监视模式”（最推荐）
   ```

3. 在 watch 模式下：
   - 它会自动给你下一个练习文件。
   - 你打开文件，找到 `// TODO` 或 `todo!()`，改代码。
   - 保存 → 自动重新编译。
   - 编译通过 → 自动跳下一个。
   - 卡住了？按 `h` 看提示（hint）。
   - 想看进度/跳题？按 `l` 打开列表。
   - 想重置某题？选 `r` 重置。

4. 全部做完后：大概 80–100+ 个练习，覆盖从变量到线程、async 的基础。

### 谁适合做 Rustlings？

- Rust 完全新手（学完前几章书后立刻开始最爽）
- 看书看腻了，想动手写代码的人
- 想系统刷一遍 Rust 基础语法和常见错误的人
- 已经会一点 Rust，但 borrow checker / lifetime 还经常犯错，想强化的人

很多人反馈：做完 Rustlings 后，写真实项目时 borrow checker 的报错会少很多，因为你已经“被虐”过无数次了。

一句话：  
Rustlings 是目前公认的最友好、最官方的 Rust 入门动手练习工具，几乎所有 Rust 学习路径都会推荐它。

官网：https://rustlings.rust-lang.org/  
GitHub：https://github.com/rust-lang/rustlings  
（可以 star 一下，项目维护得很活跃）

如果你已经装好 Rust，想现在就开始，我可以给你推荐从哪个练习开始，或者帮你解释某个常见卡点。直接说就行！🦀