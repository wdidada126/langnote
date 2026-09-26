# 06 · API 风格：纯 C、面向对象、模板与数据驱动（原书第 5 章）

> 对应中文目录（已核实）：第 5 章 风格 —— 5.1 纯 C API（5.1.1 ANSI C 特性 / 5.1.2 优点 / 5.1.3 用 ANSI C 编写 API /
> 5.1.4 从 C++ 中调用 C 函数 / 5.1.5 案例研究：FMOD C API）/ 5.2 面向对象的 C++ API（5.2.1 优点 / 5.2.2 缺点 /
> 5.2.3 案例研究：FMOD C++ API）/ 5.3 基于模板的 API（5.3.1 示例 / 5.3.2 模板与宏 / 5.3.3 优点 / 5.3.4 缺点）/
> 5.4 数据驱动型 API（5.4.1 数据驱动型 Web 服务 / 5.4.2 优点 / 5.4.3 缺点 / 5.4.4 支持可变参数列表 /
> 5.4.5 案例研究：FMOD 数据驱动型 API）。
> 英文原章题 ⚠️ 推定："Style"。FMOD 案例为作者（曾在 Crash Technology/FMOD 任职 ⚠️ 履历细节未核实）自带的贯穿样本。

## 核心概念速览（中英对照）

- **API 风格** — API style：接口以何种语言机制承载——C 平铺函数 / C++ 类 / 模板泛型 / 数据描述——四选一的战略立场。
- **纯 C API** — plain C API：`extern "C"` 函数 + 不透明句柄 + 定宽类型的接口面；跨编译器/跨语言的 ABI 公约数。
- **名称改编** — name mangling：C++ 为重载把 `foo(int)` 变成 `_Z3fooi`；不同编译器方案不同 → ABI 不可互认（已实测，见下）。
- **C++ 兼容层** — C++ wrapper over C：在 C ABI 之上用零开销内联类还原易用性——FMOD 双接口路线（5.1.5/5.2.3）。
- **面向对象 API** — OO API：类 + 继承 + 虚函数的接口风格；表达力强但虚表与模板实例化把 ABI 焊死。
- **模板 API** — template-based API：接口即蓝图，代码在使用点生成；灵活极致，但**不可导出符号**（实例化在用户侧）。
- **模板与宏** — templates vs macros：5.3.2 的对比——模板参与类型系统、宏只是文本；两代「泛型复用」的取舍同构。
- **数据驱动 API** — data-driven API：不暴露动作函数，暴露「可读写的数据属性集」，行为由数据配置触发。
- **可变参数列表** — variadic arguments：`...`/va_list 一族的逃生舱；类型不安全，书与当代指南都建议以「属性表/键值对」替代。
- **导出面** — export surface：动态库实际公开的符号集合；风格选择决定它长什么样（07 章手法收口）。

## 动机：风格是「谁能用我」的答案

四种风格各答一道题：C API 答「跨语言/跨编译器/长期二进制兼容」；OO API 答「C++ 用户的心智模型」；
模板 API 答「与用户代码共同演化（自定义类型/编译期多态）」；数据驱动答「运行时可配置、可序列化、可远程」。
5 章的案例研究用**同一个 FMOD**连做三个风格样本，意图明显：问题不变，风格即立场。

## 机制

### 1. 纯 C API 的四件套（5.1.3）

```c
/* 🔧 现代定型版：句柄 + 定宽类型 + 显式错误 + 导出宏 */
#include <stdint.h>
#ifdef _WIN32
#  define FMOD_API __declspec(dllexport)        /* MinGW 实测：仅此标注者进导出表 */
#else
#  define FMOD_API __attribute__((visibility("default")))
#endif
typedef struct FSystem_F* FSystem;               /* 不透明句柄（02 章 3.1.6） */
FMOD_API int    FSystemCreate(FSystem* out);
FMOD_API int    FSystem_SetFrequency(FSystem s, int32_t hz);   /* fmod.h 风格：一函数一意图 */
FMOD_API const char* FSystem_GetError(FSystem s);
```

要点：结构体**不声明成员**（不完整类型 → 布局零承诺）；所有跨边界类型为 `int32_t` 等定宽型；
`extern "C"` 关 mangling。已实测（g++ 15.2 MinGW，DLL 导出表 `objdump -p` 核验）：
导出名恰为 `c_add / widget_create / widget_destroy` 三个 C 符号，
同名 C++ 函数则呈现 `_Z6vis_fnv` 式改编名——「C++ ABI 不互认」的最直白证据。

### 2. OO 与模板的边界决定（5.2/5.3）

OO 风格的两条硬限制（书 5.2.2）：虚表布局进 ABI；**模板无法以虚函数多态**（成员模板不能 virtual）。
模板风格的两条硬限制（5.3.4）：接口在编译期耗尽（无法 dlopen 一个未实例化的模板）；
错误暴露在实例化点（书时代的模板报错天书，C++20 concepts 后大幅缓解——见「最新演进」）。
5.3.2「模板与宏」放在今天仍然有人需要读：头文件里 `#define ADD(a,b) ((a)+(b))` 的宏 API
（如老式 Win32 消息宏）与模板 API 犯同样的错：不可调试、无类型、污染命名。

### 3. 数据驱动 API 的结构（5.4）

```cpp
// 🔧 从"函数每事一个"收敛到"属性表 + 少量动词"
doc->setProperty("page.size", variant{A4});
doc->setProperty("font.embed", variant{true});
int n = doc->query("page.count");
```

5.4.4 批评可变参数（`printf` 风格）后给出的方向——键值属性表——正是此后
JSON/protobuf attribute、渲染引擎 parameter block、甚至 LSP（Language Server Protocol）
`didChangeConfiguration` 的形态。Web 服务小节（5.4.1）在 2012 年看 REST/JSON，今天看 gRPC/GraphQL，结论不变：
**数据驱动接口的兼容性靠字段容忍（未知字段忽略），代码接口的兼容性靠版本流程（09 章）。**

## 权衡

| 风格 | 换来 | 付出 |
| --- | --- | --- |
| 纯 C | 跨编译器/语言、句柄可版本化、导出面小而稳 | 无构造析构/重载/RAII；易用性靠 C++ 兼容层二次加工 |
| OO C++ | 心智模型自然、RAII、可扩展（继承） | 虚表 ABI 债；跨模块 new/delete 运行时配对雷；符号导出面失控诱惑 |
| 模板 | 零开销抽象、用户类型通用、编译期可证 | 不可跨二进制边界；编译时间；报错成本；实现全公开（header） |
| 数据驱动 | 运行时配置、可序列化、前后端分离 | 类型安全后置（运行期才知配错）；IDE 补全难；性能路径间接 |

一个反直觉结论（5.1.4「从 C++ 调用 C」）：**C 风格 API 并不反 C++ 用户**——包一层内联包装类
即可还原值语义，反向（让 C 用户吃 C++ ABI）几乎无解。所以「底层 C ABI + 上层可选 C++ 糖」成为工业标配。

## 相邻概念对比

- **风格 vs 惯用法**：风格是全局立场（本库对外是什么形状），02–04 的模式/惯用法是局部手段；一种风格里混用多模式很正常（C 风格 + 句柄 + 工厂函数）。
- **C ABI vs C++ ABI**：C 的稳定承诺 = 调用约定 + 平坦符号 + POD 布局；C++ 的改编名/虚表/异常表使跨编译器互认基本不可能（Itanium ABI 只是「同一 GCC/Clang 家族」的默契）。
- **模板 API vs 宏 API**：同「复用」，异在「是否进类型系统」。
- **数据驱动 vs 插件**：都「不动代码改行为」；数据驱动改的是**参数**，插件换的是**实现单元**（11 章）。

## 最新演进与工业实践

- **C++20 concepts 重修模板 API 的报错债**：`template <std::ranges::range R>` 的约束把
  「实例化点天书」变「签名即文档」；接口设计首次可以**编译期声明前置条件**——5.3 的直接现代化
  （对照 [../C++20模板元编程.md](../C++20模板元编程.md) 与仓库 concepts 材料）。
- **std::format/`{}` 风格取代可变参数**：`printf` 系 `...` API 被类型安全格式化替代；
  `std::source_location` 取代 `__FILE__/__LINE__` 宏参——5.4.4 的「宏/可变参数之恶」有了标准解。
- **导出宏现代化**：CMake 的 `GenerateExportHeader` + `CXX_VISIBILITY_PRESET hidden` + `run-ld` 版本脚本
  已成为 ELF 库的标准三件套（Windows 用 `WINDOWS_EXPORT_ALL_SYMBOLS=OFF` + 显式 dllexport，与我们的
  MinGW 实测一致：不标不导）。
- **工业样本**：LLVM 的 llvm-c 目录（C API 层生成自 `typedef struct LLVMOpaqueX* LLVMXRef` 家族）、
  Vulkan/OpenGL ES 的纯 C 句柄接口、SQLite 的单头 C API——C 风格「小而稳」路线的当代大成；
  反面，libstdc++/MSVC STL 证明「OO + 模板」风格一旦发布，ABI 演化需要版本符号脚本级的事后手术（09 章）。
- **header-only 是「模板风格 + 数据驱动分发」的合体极端**：cpp-httplib（单头 HTTP 服务/客户端）、
  doctest（单头测试框架）、stb 图像库——放弃二进制兼容换「零构建集成」；
  与 C 风格「二进制稳定、需链接」形成分发策略的两极（对照 [10-文档与测试.md](10-文档与测试.md) 的测试选型）。
- **数据驱动 → 接口即 schema**：protobuf/flatbuffers/capnproto 的 IDL 化，本质是 5.4 的
  「属性表」升级为「带版本规则的类型系统」；gRPC 的 status 模型也回应了 4.7.4 的错误通道问题。

## 与其他章 / 其他笔记的联系

- ← [02-不透明指针与Pimpl.md](02-不透明指针与Pimpl.md)：C 风格句柄 = 不透明指针的 API 全局化。
- ← [05-设计流程与错误处理.md](05-设计流程与错误处理.md)：先定接口形状再落风格语法。
- → [07-C++用法与符号导出.md](07-C++用法与符号导出.md)：风格选定后的语言级手法与导出控制。
- → [09-版本控制与ABI.md](09-版本控制与ABI.md)：四种风格各自的兼容承诺账本。
- → [11-脚本绑定与插件扩展.md](11-脚本绑定与插件扩展.md)：C 风格是所有绑定的落点；数据驱动是插件配置的前半。
- → [../C语言接口与实现.md](../C语言接口与实现.md)、[../C语言接口及实现.md](../C语言接口及实现.md)：HBS「接口即契约」的 C 语言原版教材，与 5.1 同源互补。
- → [../LLVM编译器原理与实践.md](../LLVM编译器原理与实践.md)：读 llvm-c 风格包装的实战样本。
- → [../C++API设计.md](../C++API设计.md)｜[../C++系列·总索引.md](../C++系列·总索引.md)

## 思考题

1. 为同一个「音频播放器」库分别草拟 C / OO / 模板 / 数据驱动四版核心接口（各 ≤5 个入口），标注每版你最难守住的一条兼容性承诺。
2. 为什么「模板 API 的库升级不重编即不可用」？从实例化时机论证，并说明显式实例化（6.4.3）能否救。
3. 你的 C API 用户投诉「没有 RAII」：写一个 20 行的 C++ 包装层草案，要求零额外开销且不透出任何新 ABI。
