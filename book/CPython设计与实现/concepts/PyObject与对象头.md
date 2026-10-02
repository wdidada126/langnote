# 概念专篇：PyObject 与对象头

> 跨章概念：与第 02 章（对象模型）、第 03/04 章（内置对象）、第 09 章（内存）、第 10 章（GC）强相关。
> 校准到 2026（含 immortal 对象 PEP 683、3.11+ 紧凑帧）。

## 1. 公共头部 PyObject_HEAD

```c
// 教学示意，不参与构建（C 伪代码）
typedef struct _object {
    PyGC_Head *gc;        // 仅参与 GC 的对象有（变长/容器）
    Py_ssize_t ob_refcnt; // 引用计数
    PyTypeObject *ob_type;// 类型指针
} PyObject;
```

每个对象都以该头开头。变量存的是 `PyObject*`，真正类型靠 `ob_type` 查——这是动态多态的代价（每次运算多两次查找 + 一次函数调用）。

## 2. 变长头 PyVarObject

多 `Py_ssize_t ob_size`（元素个数）。`list`/`str`/`dict`/`tuple` 是变长，`len()` 为 O(1)（直接读 `ob_size`）。

## 3. 引用计数（第 10 章详述）

- 创建 +1，赋值/传参 +1，`del`/出作用域 -1，归零即释放（确定性）。
- 循环引用由循环 GC 兜底。
- 3.12 **immortal 对象（PEP 683）**：小整数、`None`/`True`/`False`、常量字符串等把引用计数冻结为「永生」，不再原子增减——no-GIL 构建（PEP 703）的关键使能，避免对海量常量做原子操作。

## 4. 类型对象 PyTypeObject

持有 `tp_as_number`/`tp_as_sequence`/`tp_as_mapping`/`tp_dealloc`/`tp_init` 等槽位函数指针。运算符 `a + b` 实际是 `ob_type->tp_as_number->nb_add` 调用。每个内置类型是一个 `PyTypeObject` 实例（也是对象，其 `ob_type` 是 `type`）。

## 5. 常见误区

- 误：`id()` 是稳定地址——在默认构建下确实是对象地址，但不应依赖它做逻辑。
- 误：引用计数 = 无 GC——循环引用仍需循环收集器。
- 误：对象头对所有对象大小相同——变长对象多 `ob_size`；GC 跟踪对象多 `PyGC_Head`。
