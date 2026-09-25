# AP1400-2 配套项目计划（骨架，本轮不写代码）

以 csdiy 推荐的 7 个 homework 为原型，改为自研小项目；语言均为 C++17。

| 章节 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L1 Matrix | C++17 | 轻量矩阵库：四则运算+转置+单元测试 | `g++ -std=c++17 -Wall -Wextra` + CMake（Catch2 测试） |
| L2 加密货币 | C++17 | 内存版钱包/交易模拟器（账户、转账、余额校验） | CMake + ctest |
| L3 BST | C++17 | 带迭代器的通用 BST 模板库 | CMake + GoogleTest |
| L4 智能指针 | C++17 | 自实现 `MySharedPtr`/`MyUniquePtr` + 循环引用检测 demo | CMake + Sanitizer (`-fsanitize=address,undefined`) |
| L5 多态 | C++17 | 迷你图形渲染器：Shape 继承体系 + 序列化 | CMake |
| L6 STL | C++17 | 词频统计/TopK 等 4 个 STL 解题集 | 单文件 `g++ -std=c++17` |
| L7 Python | Python 3 | 用 Python 重写 L3 BST 并对比代码量 | `python3` 直接运行 |

约定：每个项目独立目录，附 `build.sh`（Linux/Windows 各一版），本轮只列计划不产出代码。
