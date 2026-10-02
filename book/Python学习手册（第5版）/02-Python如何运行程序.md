# 2 Python如何运行程序（原书 pp. 英文 5e 第 2 章，中文版页次以实体书为准 🔧）

## 本章地图
| 节 | 内容 | 结论 |
| --- | --- | --- |
| 解释器简介 | CPython 把源码编为字节码 | 源码 → .pyc → PVM |
| 程序员视角 | 模块即对象，import 即运行 | `import` 触发执行 |
| 执行模型变体 | CPython/Jython/IronPython/PyPy | 字节码 + 各自 VM |
| 优化工具 | Cython/Shed Skin/Psyco | 加速或冻结二进制 |
| 冻结二进制 | PyInstaller/cx_Freeze | 打包成可执行文件 |

## 核心精讲
核心模型：`源码 .py → 编译为字节码 .pyc（仅一次，按 mtime 缓存）→ Python 虚拟机(PVM) 解释执行`。

```
教学示意，不参与构建
# 运行模块时实际发生的事
python hello.py
# 1) 编译 hello.py -> __pycache__/hello.cpython-312.pyc
# 2) PVM 从 __pycache__ 加载字节码执行
```

- `import` 与 `reload`：3.x 用 `importlib.reload(mod)` 代替 2.x 的 `reload(mod)`。
- 实现分支：CPython（标准 C）、Jython（JVM）、IronPython（.NET）、Stackless（并发）、PyPy（JIT）。

## 版本演进
- 3.8 起 `.pyc` 带源文件哈希、区分优化级别目录（`__pycache__`）。
- 3.12 引入「per-instigator」专用化自适应字节码（Faster CPython 一期）。

## 经典论文与原始文献
- PEP 3147 *PYC Repository Directories*（3.2，定义 `__pycache__`）。
- PEP 552 *Deterministic pyc*（3.7，源哈希 vs 时间戳）。
- 官方 *Python Language Reference*「Execution model」。

## 近年研究与工业界开源实践（2015–2026）
- PyInstaller、Nuitka（把 Python 编译为 C）、Codon 等冻结/编译工具流行。
- Cinder（Meta 内部版 CPython）回馈部分补丁给上游。

## 常见误区与本书需修正之处
| 误区 | 修正 |
| --- | --- |
| 原书讲 `reload()` 内置 | 3.x 中 `reload` 已移入 `importlib.reload` |
| Shed Skin / Psyco 仍推荐 | 二者基本停止维护；优先 PyPy 或 Cython |
| `.pyc` 仅按 mtime | 3.7+ 还支持源哈希模式（可复现构建） |

## 与其他章 / 其他书的联系
- `import` 机制深挖见 [22-模块大图景](22-模块大图景.md)、[23-模块代码基础](23-模块代码基础.md)。
- 性能对照 [21-基准测试说明](21-基准测试说明.md)。
