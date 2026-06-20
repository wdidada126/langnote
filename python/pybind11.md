# pybind11

非常酷啊，先用Python写一遍，再优化性能。后面优化不动了，就让GPT给我生成一个pybind11的C++版本，自己矫正下逻辑，测试后，直接就上线了，飞起

我用最简单、最直白的方式给你讲清楚，不绕弯子：

# 1. `pybind11_add_module` 作用（一句话）
它是 pybind11 提供的 CMake 函数，专门用来把 C++ 代码编译成 Python 可直接 import 的扩展模块（.so/.pyd 文件）。

## 详细作用
1. 自动处理编译参数
   帮你自动找到 Python 头文件、链接 Python 库，不用手动写 `-I` `-L`。

2. 自动生成符合 Python 规则的动态库
   编译出来的文件可以直接：
   ```python
   import 你的模块名
   ```
   不需要任何额外配置。

3. 自动处理 pybind11 绑定代码
   你写的 C++ 绑定代码：
   ```cpp
   PYBIND11_MODULE(xxx, m) { ... }
   ```
   它能自动识别并正确编译。

4. 跨平台兼容
   Windows / macOS / Linux 都能用，自动生成对应格式：
   - Linux: `模块名.cpython-xxx.so`
   - macOS: `模块名.cpython-xxx.so`
   - Windows: `模块名.pyd`

# 2. CMake 自定义函数 完整流程（超清晰）
CMake 自定义函数 = 自己写一个可复用的 CMake 指令。

## 流程一共 4 步
### ① 定义函数
```cmake
function(函数名 参数1 参数2 ...)
  # 函数内部逻辑
endfunction()
```

示例：
```cmake
function(my_add target source)
  # 内部可以调用任意 cmake 命令
  add_executable(${target} ${source})
endfunction()
```

### ② 调用函数
```cmake
my_add(myapp main.cpp)
```

### ③ 函数内部可使用的变量
- `${ARGV}`：所有参数
- `${ARGC}`：参数个数
- `${ARG0}, ${ARG1}`：第1、2个参数

### ④ 作用域规则
- 函数内默认不修改外部变量
- 想修改外部变量用：
  ```cmake
  set(变量名 值 PARENT_SCOPE)
  ```

# 3. 最实用的小例子（一看就懂）
```cmake
# 定义函数
function(compile_py_module mod_name)
  pybind11_add_module(${mod_name} ${mod_name}.cpp)
endfunction()

# 使用函数
compile_py_module(example)
compile_py_module(utils)
```

作用：自动批量生成 Python 扩展模块。

# 极简总结
- `pybind11_add_module`：把 C++ 编译成 Python 可导入的库。
- CMake 自定义函数：`function() ... endfunction()`，定义 → 调用，用于复用逻辑。

需要我给你一个可直接运行的 pybind11 + CMake 最小模板吗？你直接编译就能用。
