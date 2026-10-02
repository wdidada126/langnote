# 概念专篇 · 作用域与 LEGB

> 跨章参考：支撑[第10章 Modules and scoping rules](../10-Modules and scoping rules.md)与[第15章 Classes and OOP](../15-Classes and object-oriented programming.md)的名字查找规则。

## LEGB 查找顺序

当引用一个名字，Python 按以下顺序由内向外找：

1. **L**ocal — 当前函数局部
2. **E**nclosing — 外层闭包函数
3. **G**lobal — 模块级
4. **B**uiltin — 内建（`len`/`print` 等）

```
# 教学示意，不参与构建
x = 'global'
def outer():
    x = 'enclosing'
    def inner():
        x = 'local'
        print(x)          # local
    inner()
outer()
```

## 修改外层变量

- 默认赋值创建局部变量；要改外层用 `global`（改全局）或 `nonlocal`（改闭包）。
- `global` 尽量少用，优先返回值/传参。

## 模块即全局作用域

- 每个 `.py` 模块有独立全局命名空间；`import` 引入名字。
- 相对导入（`.`/`..`）仅包内可用。

## 版本与陷阱

- `nonlocal`（PEP 3104，3.0）声明修改闭包变量。
- `from __future__ import annotations`（3.7）延迟标注，缓解导入期开销。
- 循环导入：用 `TYPE_CHECKING` 守卫类型导入，或延迟导入。

## 跨章跨书联系

- 主章：[第10章 Modules and scoping rules](../10-Modules and scoping rules.md)。
- 类属性查找见[第15章 Classes and OOP](../15-Classes and object-oriented programming.md)。
- 风格见 [`Effective Python（第2版）/00-总览与阅读地图.md`](../../Effective Python（第2版）/00-总览与阅读地图.md)。
