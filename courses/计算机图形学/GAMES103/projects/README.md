# GAMES103 配套项目计划（本轮不写代码）

统一约定：与官方作业一致用 C#（.NET/Unity 风格 starter 均可）；FEM/流体附加题允许 C++/Taichi 对照实现；只写不编译，构建方式列出备查。

| 章节（讲次） | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L02-L07 刚体 | C# | 弹球塔模拟器：四元数刚体积分 + GJK 碰撞 + 顺序冲量 | `dotnet build` / Unityasmdef |
| L08-L10 布料 | C# | 质点弹簧披风 + PBD/XPBD 距离约束 + 简单自碰 | `dotnet build` |
| L11-L13 弹性体 | C# 或 C++ | 四面体线弹 FEM 方块（掉落挤压），进阶：共旋非线性 | `dotnet build` / CMake(C++) |
| L14 流体 | C# | 2D Stable Fluids（半拉格朗日 + 投影），渲染为纹理 | `dotnet build` |
| L15 流体 II | C#/Python(Taichi) | 2D SPH  dam break 粒子水槽 | `dotnet build` / taichi JIT |
| L16 综合 | C# | 刚体-布料-流体小场景（旗杆+水花），附性能/稳定性剖析 | Unity Editor 工程或 CMake |
