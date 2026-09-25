# CS106L 配套项目计划（骨架，本轮不写代码）

| 章节（讲次簇） | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L1–L4 基础语法 | C++17 | 学生成绩 CSV 统计工具（vector/引用传参/auto） | `g++ -std=c++17 -Wall` 单文件 |
| L5 OOP | C++17 | 文本 RPG 角色继承体系 | CMake 多文件 |
| L6–L7 容器与迭代器 | C++17 | 迷你 `MyVector`：自写迭代器 + const 版本 | CMake + GoogleTest |
| L8 lambda | C++17 | 管道式数据处理 DSL：filter/map/reduce 组合 | CMake |
| L9 RAII/智能指针 | C++17 | 文件句柄池 + 自定义删除器的 `shared_ptr` demo | CMake + `-fsanitize=address` |
| L10 移动语义 + 大作业 | C++17 | 复刻课程 Assignment2：`HashMap<K,V>`（含 iterator、异常安全、benchmark） | CMake + Catch2 参数化测试，Release `-O2` 对比 libc++ unordered_map |

约定：只做计划，不产出代码；每个项目目录预留 `build.sh`/`CMakeLists.txt` 骨架位置。
