# 02 Python 对象模型

> 原书 pp. 第 2 章（具体页码以实体书为准 🔧）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| PyObject 头部 | refcnt + ob_type | 一切对象都有公共头 |
| PyVarObject | 变长 + ob_size | 列表/字符串等 |
| 类型对象 | PyTypeObject | 方法/槽位表，实现多态 |
| 引用计数 | 生命周期 | Python 内存管理基石 |
| 对象分类 | 定长/变长、可变/不可变 | 决定 API 设计 |

## 核心精讲

**1. 公共头部**。每个对象都以 `PyObject_HEAD`（引用计数 `ob_refcnt` + 类型指针 `ob_type`）开头。变量传的是 `PyObject*` 泛型指针，真正类型靠 `ob_type` 运行时判断 → 这就是 Python 动态多态的代价来源。

**2. 变长对象**。`PyVarObject` 在头部多加 `ob_size`（元素个数），`len()` 是 O(1)。`list`/`str`/`dict` 都是变长。

**3. 类型对象**。每个类型是一个 `PyTypeObject` 实例，持有 `tp_as_number`/`tp_as_sequence`/`tp_as_mapping`/`tp_dealloc` 等槽位函数指针。运算符 `a + b` 实际是查 `ob_type` 的 `tp_as_number->nb_add` 并调用——比 C 多两次查找 + 一次函数调用。

**4. 引用计数**。对象创建 `ob_refcnt=1`，赋值/传参 +1，`del`/出作用域 -1，归零即释放。循环引用靠第 10 章的循环 GC 兜底。

## 版本演进

- 3.12 起 **immortal 对象（PEP 683）**：小整数、常量字符串、`True/None` 等标记「永生」，引用计数不再变动，利于 no-GIL 构建免原子操作。
- 3.10+ 类型槽位逐步「永久化」、减少运行期字典查找。
- 3.12 `InternalDocs/` 新增对象系统文档。

## 经典论文与原始文献

- `Include/object.h`（PyObject/PyVarObject 定义）、`Objects/typeobject.c`。
- PEP 683（Immortal Objects，3.12）。

## 近年研究与工业界开源实践（2015–2026）

- immortal 对象是 no-GIL 构建（PEP 703）的前置依赖，避免对每个常量做原子引用计数。
- 对象头在 3.11+ 因帧对象瘦身而整体更紧凑。

## 常见误区与本书需修正之处

- 🔧 误：原书（3.10 基线）未含 immortal 对象与 no-GIL 背景；2026 读对象模型必须带上 PEP 683/703。
- 误：以为「引用计数 = 没有 GC」——循环引用仍需第 10 章的循环收集器。
- 误：`id()` 是内存地址——在 debug/非默认构建下确实是对象地址，但不应依赖。

## 与其他章 / 其他书的联系

- 引用计数细节 → [concepts/PyObject与对象头.md](concepts/PyObject与对象头.md)。
- 类型与描述符 → 第 08 章（类与对象机制）。
- 对照 [`Python学习手册（第5版）/00-总览与阅读地图.md`](../Python学习手册（第5版）/00-总览与阅读地图.md) 的数据模型章。
