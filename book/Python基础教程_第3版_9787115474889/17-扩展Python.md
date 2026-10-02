# 第 17 章 扩展Python（原书 pp.286–299）

> 一句话定位：本章回答「Python 不够快 / 用不上某个 C 库时怎么办」——从换解释器到写 C 扩展，再到今天更省力的ctypes/Cython/Rust 路线。基线：原书 Python 3.5；本目录按 3.12+ 校验。
> 对应英文章名：**Extending Python**。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 17.1 鱼和熊掌兼得 | 为什么扩展：① 性能 ② 复用既有 C/C++ 资产 ③ 专有闭源算法 ④ 与宿主环境（JVM/.NET）互操作 | 「易用」与「快」不必二选一：把热路径下沉，其余留在 Python |
| 17.2 Jython 和 IronPython | 运行在 JVM / .NET 上，直接调用 Java / C# 库 | 🔧 2026 年两者都已边缘化；JVM 路线看 **GraalPy** |
| 17.3 SWIG | 用接口描述文件自动生成包装代码 | 仍在维护，但新项目更常用 Cython / pybind11 / PyO3 |
| 17.3 手工编写扩展 | `Python.h` + `PyArg_ParseTuple` + 方法表 + `PyInit_xxx` | 最贴近 CPython 实现，也最易出错（引用计数、异常约定） |
| 17.4 小结 | 先确认真的需要扩展；能不写 C 就别写 C | 见「常见误区」表 |

## 核心精讲

> 以下均为**教学示意，不参与构建**：本目录不编译真实扩展模块，示例用于对齐概念与命令。

### 1. 扩展的四种动机与对应方案（原书 17.1）

| 动机 | 首选方案（2026） | 说明 |
| --- | --- | --- |
| 热点函数太慢 | 先 `cProfile` 定位 → `numpy` 向量化 → Numba / Cython / mypyc | **别一上来写 C**；90% 的「慢」是算法与数据结构问题 |
| 要调用已有 C/C++ 库 | `ctypes`（无编译器）→ `cffi` → Cython → pybind11 | `ctypes` 只适合简单 ABI；复杂 API 用 cffi/Cython |
| 要调用 Rust | PyO3 + maturin | 内存安全 + 单一命令发布 |
| 要与 JVM/.NET 互操作 | GraalPy / pythonnet | 原书的 Jython / IronPython 定位已被这两个替代 🔧 |

### 2. Jython 与 IronPython 的今日状态（原书 17.2）

| 实现 | 原书说法 | 2026 现状 |
| --- | --- | --- |
| Jython | 「让你在 JVM 上运行 Python 并调用 Java」 | 🔧 长期停留在 **2.7 分支**（Python 2 语法），发布节奏很慢，**不支持 Python 3**；新项目不要选 |
| IronPython | 「在 .NET 上运行 Python」 | 🔧 3.4 系列面向 **Python 3.4 语法**，进度缓慢；.NET 互操作今天更常用 **pythonnet** |
| GraalPy | 原书未涉及 | 🔧 JVM 上的现代 Python 实现（GraalVM），语法代次远高于 Jython，且支持 C 扩展的受限兼容；**以官方站点为准** |

### 3. 手工编写 C 扩展（原书 17.3）

`spam.c`（教学示意，不参与构建；需要 C 编译器与 Python 头文件）：

```c
/* spam.c —— 教学示意，不参与构建 */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

/* 1) 包装函数：Python 对象 ↔ C 值 */
static PyObject *spam_gcd(PyObject *self, PyObject *args)
{
    long a, b;
    if (!PyArg_ParseTuple(args, "ll", &a, &b))   /* 失败时已设置异常，返回 NULL */
        return NULL;
    while (b != 0) { long t = b; b = a % b; a = t; }
    return PyLong_FromLong(a < 0 ? -a : a);      /* 返回新引用 */
}

/* 2) 方法表 */
static PyMethodDef SpamMethods[] = {
    {"gcd", spam_gcd, METH_VARARGS, "Return the greatest common divisor."},
    {NULL, NULL, 0, NULL}                        /* 哨兵，必须有 */
};

/* 3) 模块定义 */
static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT, "spam", NULL, -1, SpamMethods
};

/* 4) 初始化函数：名字必须是 PyInit_<模块名> */
PyMODINIT_FUNC PyInit_spam(void)
{
    return PyModule_Create(&spammodule);
}
```

用 PEP 517 口径构建（**不要用原书的 `distutils`**，见 [18-程序打包.md](18-程序打包.md)）：

```toml
# pyproject.toml —— 教学示意，不参与构建
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "spam"
version = "0.1.0"
requires-python = ">=3.12"

[tool.setuptools]
ext-modules = [{ name = "spam", sources = ["spam.c"] }]
```

```bash
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install .            # 会调用本机编译器构建 spam 扩展
python -c "import spam; print(spam.gcd(12, 18))"     # 6
```

三条铁律：**返回 `NULL` 前必须已 `PyErr_SetString`**；**引用计数借/还分清**
（`PyArg_ParseTuple` 借、`PyLong_FromLong` 还给你一个新引用）；**`-1` 的 `m_size`**
表示模块不支持子解释器（默认值，最省心）。

### 4. 不用编译器的方案：`ctypes`（原书未强调，2026 年首选轻量方案）

```python
# ctypes_demo.py —— 教学示意，不参与构建（仅用标准库）
import ctypes
import sys
from ctypes.util import find_library

if sys.platform == "win32":
    libc = ctypes.CDLL("msvcrt")
else:
    libc = ctypes.CDLL(find_library("c") or "libc.so.6")

libc.sqrt.argtypes = [ctypes.c_double]      # 不声明 argtypes 会按 int 传参，结果错误
libc.sqrt.restype = ctypes.c_double
print(libc.sqrt(2.0))                        # 1.4142135623730951
```

`ctypes` 的价值：**零构建步骤、纯 Python 分发**；代价是手工维护类型声明与结构体布局，
ABI 复杂时（回调、C++ 类模板）应升级到 `cffi`（ABI/API 双模式，`pip install cffi`）或 Cython。

### 5. 三条主流「写扩展」路线对比

| 路线 | 语言 | 适合场景 | 成本 |
| --- | --- | --- | --- |
| CPython C API | C | 需要极致控制、要进 CPython 生态核心 | 最高：手写引用计数与异常 |
| Cython | Python 语法超集 + 类型注解 | 把现有 Python 热点逐步编译成 C | 中：改 `.pyx`，可选 `pip install cython` |
| pybind11 | C++ | 包装现代 C++ 库（智能指针、STL 自动转换） | 中：头文件库 + 编译器 |
| PyO3 + maturin | Rust | 新写高性能模块、想要内存安全 | 中：`maturin develop` 一条命令 |

### 6. 编译器都不想碰的性能替代

```bash
pip install numba          # JIT 编译数值函数，加个 @njit 装饰器
pip install mypyc          # 把带类型注解的 Python 编译成 C 扩展（mypy 同源）
python -m mypyc app.py     # 产出可直接 import 的 .so / .pyd
```

- **Numba**：`@numba.njit` 对 NumPy 循环效果最好，但对纯 Python 对象支持有限。
- **mypyc**：把**已有带注解的 Python** 编译成 C 扩展，无需改写语言，典型加速 1.5–4 倍 🔧（视代码而定）。
- **Codon**：类 Python 语法的 AOT 编译器，🔧 与 CPython 的兼容程度随版本变化，以官方为准。

### 7. free-threading（PEP 703）对扩展模块的要求

```c
/* 多阶段初始化时声明「本模块不需要 GIL」——🔧 字段名以当前官方文档为准 */
static PyModuleDef_Slot slots[] = {
    {Py_mod_multiple_interpreters, Py_MOD_PER_INTERPRETER_GIL_SUPPORTED},
#ifdef Py_mod_gil
    {Py_mod_gil, Py_MOD_GIL_NOT_USED},
#endif
    {0, NULL}
};
```

要点：3.13 提供**实验性** free-threaded 构建，3.14 提供**官方支持**的 free-threaded 构建；
判断当前解释器有无 GIL 用 `sys._is_gil_enabled()`。扩展模块只有在显式声明
`Py_MOD_GIL_NOT_USED`（🔧 名称以文档为准）时才会被判定为「无 GIL 安全」，
否则安装时会被拒绝或强制回到有 GIL 模式。**未做线程安全改造的 C 扩展仍是 Python 并行的最大障碍。**

## 版本演进

| 版本 | 与本章相关的变化 |
| --- | --- |
| 3.5（原书基线） | 手工 C 扩展、`distutils` 编译、`ctypes`/`cffi` 均已可用 |
| 3.6–3.9 | C API 逐步收紧：引入 `Py_ssize_t` 相关清理、`Py_LIMITED_API` 可用面扩大 |
| 3.10 | 🔴 稳定 ABI / 有限 API 相关整理持续；SWIG 与 Cython 跟进较慢 |
| 3.11 | C 扩展加载机制改进；错误提示更友好 |
| 3.12 | 🔴 **`distutils` 被移除（PEP 632）**：原书的扩展编译示例必须改用 `setuptools` 或 `pyproject.toml`；🔧 稳定 ABI（有限 API）相关 PEP 编号以官方文档为准 |
| 3.13 | 🔴 **free-threaded 构建实验性引入（PEP 703）**；未适配 GIL 假设的 C 扩展会出问题；`ctypes`/`cffi` 等受影响的库陆续适配 |
| 3.14 | 🔴 free-threaded 构建**官方支持**；多解释器 API 正式化；注解延迟求值（PEP 649 系）对依赖注解的扩展有影响 🔧 |

## 经典论文与原始文献

> Python 生态以 PEP 与官方文档为准（规范文档，非同行评审论文）。

| 编号 / 来源 | 标题 | 年份 | URL |
| --- | --- | --- | --- |
| PEP 703 | Making the Global Interpreter Lock Optional in CPython | 2023（3.13 实验 / 3.14 官方支持） | https://peps.python.org/pep-0703/ |
| PEP 632 | Deprecate distutils module | 2021（3.12 移除） | https://peps.python.org/pep-0632/ |
| PEP 484 | Type Hints（mypyc / Cython typed 语法的共同基础） | 2014（3.5） | https://peps.python.org/pep-0484/ |
| 官方文档 | Extending and Embedding the Python Interpreter | 持续更新 | https://docs.python.org/3/extending/index.html |
| 官方文档 | Python/C API Reference Manual | 持续更新 | https://docs.python.org/3/c-api/index.html |
| 🔧 官方文档 | Stable ABI / Limited API | 持续更新 | https://docs.python.org/3/c-api/stable.html （相关 PEP 编号以官方文档为准） |

> 说明：Jython / IronPython / Cython / pybind11 均为实现与工具，**没有对应 PEP**，
> 以其官方仓库与文档为口径。本目录不编造论文与 DOI。

## 近年研究与工业界开源实践（2015–2026）

- **Cython**（`cython/cython`）：最成熟的「Python 语法 → C」方案；pandas、scikit-learn 等大量项目使用。
- **pybind11**（`pybind/pybind11`）：C++11 头文件库，是包装现代 C++ 库的事实标准。
- **PyO3 / maturin**（`PyO3/pyo3`）：Rust 生态绑定；`maturin` 把构建 + 打包 + 发布压成一条命令，
  近年多个高性能库（如部分 tokenizer、polars 生态组件）走这条路。
- **nanobind**（`wjakob/nanobind`）：pybind11 作者的后续作品，面向 C++17，二进制更小、调用更快。
- **Numba**（`numba/numba`）：LLVM JIT，数值循环加速；对纯 Python 对象支持有限，是它的明确边界。
- **mypyc / Codon**：把「编译」做成可选开关而非重写项目的两种路线；mypyc 已被 mypy 自身用于加速。
- **GraalPy**（`oracle/graalpython`）：JVM 上的现代 Python 实现，接管了原书 Jython 的定位 🔧。
- **受限 API 与 wheel 分发**：工业界趋势是「**一次编译、多个 Python 版本可用**」
  （有限 API + `abi3` wheel），直接降低 C 扩展的维护成本。
- **研究侧**：关于 Python 性能的工作近年集中在 **JIT（copy-and-patch 路线）**、
  **free-threading 下的并发正确性验证**、以及 **跨语言 FFI 的安全边界**；
  这类工作多以 CPython issue 与基准仓库形式出现，非同行评审论文，🔧 以官方为准。

## 常见误区与本书需修正之处

| # | 原书说法 / 常见想法 | 问题 | 2026 正确写法（🔧 = 需修正） |
| --- | --- | --- | --- |
| 1 | 「Python 慢，所以热点要写 C」 | 多数慢源于算法/数据结构或未向量化 | 🔧 先 profile（见 [16-测试基础.md](16-测试基础.md)），再 numpy 向量化，最后才考虑 C |
| 2 | 用 `distutils` 编译扩展 | `distutils` 已于 **3.12 移除（PEP 632）** | 🔧 用 `setuptools` 的 `ext-modules`（见 [18-程序打包.md](18-程序打包.md)）或 meson-python |
| 3 | 用 Jython 在 JVM 上跑 Python | 🔧 Jython 停在 2.7 分支，是 Python 2 | 🔧 选 GraalPy 或 JPype；原书 17.2 整节需按现状重写 |
| 4 | 用 IronPython 做 .NET 互操作 | 🔧 语法代次落后，进度缓慢 | 🔧 选 `pythonnet`（`pythonnet/pythonnet`） |
| 5 | SWIG 是包装 C 库的首选 | 接口文件维护成本高、报错难读 | 🔧 新项目优先 Cython / pybind11 / nanobind；SWIG 只用于既有 `.i` 资产 |
| 6 | 手工 C 扩展是「标准做法」 | 引用计数与异常约定最容易出错 | 🔧 默认选 Cython/pybind11；确实要手写时逐条对照 C API 文档 |
| 7 | 扩展天然能享受多核 | CPython 有 GIL；扩展不释放 GIL 就仍是串行 | 长时间计算用 `Py_BEGIN_ALLOW_THREADS` / 在 C 层自行加锁 |
| 8 | free-threading 时代扩展「自动更快」 | 恰恰相反：未声明/未适配会被挡回有 GIL | 🔧 用 `Py_MOD_GIL_NOT_USED`（🔧 名称以文档为准）声明；`sys._is_gil_enabled()` 判断 |
| 9 | 🔧 原书未涉及 | 原书没讲 `ctypes`/`cffi` 这条「免编译器」路线 | 补：简单 C ABI 用 `ctypes`；复杂用 `cffi`（API 模式最稳） |
| 10 | 🔧 原书未涉及 | 原书没讲 Rust / PyO3 / maturin | 补：新写高性能模块时，PyO3 + maturin 的维护成本通常低于手写 C |
| 11 | 🔧 原书未涉及 | 原书没讲稳定 ABI / `abi3` wheel | 补：面向分发时用有限 API 产出 `abi3` wheel，避免每版本重编 |
| 12 | 「扩展一次写好就不动了」 | CPython 每年改 C API，扩展需持续跟进 | 把扩展模块的编译放进 CI，每版 Python 都跑一遍 |

## 与其他章 / 其他书的联系

- 本册：第 16 章 [16-测试基础.md](16-测试基础.md)（先 profile 再优化）、
  第 18 章 [18-程序打包.md](18-程序打包.md)（扩展的构建与 wheel 分发）、
  第 10 章 [10-开箱即用.md](10-开箱即用.md)（`ctypes` 与标准库边界）。
- 跨语言：本仓库 [C++并发编程实战2/](../C++并发编程实战2/) 可与「GIL 与线程安全」一节对照；
  Java 目录可与 Jython/GraalPy 的互操作代价对照。
- 他册：《流畅的Python》关于 C API 与内存布局的讨论可作为进阶读物 🔧（本仓库暂无笔记）。
- 回到总览：[00-总览与阅读地图.md](00-总览与阅读地图.md)
