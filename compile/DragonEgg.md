# DragonEgg

有用LLVM做GCC后端的项目，DragonEgg，最近一次更新在5年前了，估计想用的人不多。
是的，DragonEgg（也叫DragonEgg-3.x）确实是那个经典的用LLVM替换GCC后端的项目：它作为一个GCC插件，让GCC的前端（解析C/C++/Fortran/Ada等）输出LLVM IR，然后用LLVM的优化器和代码生成器来处理，目标是x86/ARM等架构。2010年左右LLVM社区推这个玩意儿，本意是让GCC用户尝鲜LLVM的优化（比如更好的向量化、调试支持），而不必全盘切换Clang。

### 更新情况确认
你说5年前（2020年）最后更新——基本对得上，但更精确点：官方最后稳定版是DragonEgg-3.3（对应LLVM 3.3，2013年左右），之后是零星的社区补丁和移植：
- 2017年，有人（Leslie Zhai）把代码迁到GCC 8 + LLVM 6（Phoronix报道过），能编译简单C代码，但不稳定。
- GitHub上的llvm-mirror/dragonegg仓库是LLVM项目的遗留镜像，最后commit在2018年左右，之后就没动静了（现在是只读状态，指向llvm-project主仓库）。
- 2025年现状：完全停更，没人维护。Fedora/FreeBSD等发行版早在2015-2018年就删包了，因为Clang成熟了（支持Ada/Fortran的移植也跟上）。想用？得自己hack老GCC（4.5-4.8），兼容性烂，调试info也差（Java/Fortran勉强跑）。

用的人确实不多——Reddit/StackExchange上偶尔有人怀旧（2023年帖子提过“DragonEgg halfway there”），但主流项目早抛弃它，转Clang或纯LLVM IR。维护成本高（GCC插件API变了，LLVM IR不兼容），加上GPL+Apache双许可纠缠，社区懒得碰。

### 类似/替代项目
如果想玩LLVM替换GCC后端的把戏，现在没直接继承者（DragonEgg的“混合体”理念被Clang取代），但有几个变体或间接方案。基于2025年搜索，列几个活跃/相关的：

| 项目/方案 | 描述 | 最后更新 | 活跃度/适用 | 为什么替代DragonEgg |
|-----------|------|----------|-------------|---------------------|
| Clang/LLVM (主流) | GCC前端太老？直接用Clang的前端+LLVM后端。支持C/C++/Fortran（via Flang），优化比GCC强。 | 2025年活跃（LLVM 19.x） | 高，Rust/Swift/Haskell全用 | 不用插件，直接编译。想“GCC味”？用Clang的-GNU模式。 |
| libFirm | 简单IR中间层，类似LLVM但轻量（<10万行C代码）。可接GCC前端或自定义。 | 2022年后小更新 | 中等，嵌入式/DSP项目 | Reddit上推为“LLVM简化版”，支持VLIW架构，不复杂。 |
| GCC to LLVM IR (自定义) | 前端输出C--或GIMPLE，然后转LLVM IR（用llvm-gcc遗留工具）。 | 散见2015-2023 Reddit | 低，自建 | 像DragonEgg的“手动版”，但得写转换器。Haskell GHC有LLVM后端，但慢于GCC。 |
| GNU Lightning / libJIT | GCC的轻JIT库，输出C-like IR到LLVM/GCC。 | 2020年后停 | 低，JIT实验 | 老古董，Reddit 2015帖提过，作为“no-backend”备选。 |

- 为什么没人接盘？ LLVM/Clang生态太强（7M+行代码，但模块化好），GCC后端API不友好（C++重，绑定差）。新语言直接LLVM IR（Rust/Swift），老项目迁Clang（Ada via GNAT-LLVM，2025活跃）。
- 想试？ 克隆llvm-mirror/dragonegg，配GCC 4.8+LLVM 3.3，跑`gcc -fplugin=dragonegg.so hello.c`——但2025年环境兼容性0，建议虚拟机。

如果你是想复活DragonEgg或找具体代码示例，说一声，我帮挖！否则，Clang才是正道。