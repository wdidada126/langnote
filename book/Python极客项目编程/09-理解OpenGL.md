# 09 章 理解 OpenGL（原书 pp.133–157）

## 本章地图

| 节 | 内容 | 结论 |
|---|---|---|
| 渲染管线 | 顶点→片元 | 数据经着色器到屏幕 |
| PyOpenGL | Python 绑定 | `from OpenGL.GL import *` |
| 着色器 GLSL | 顶点/片元着色器 | 现代 OpenGL 必写 |
| VBO/VAO | 上传顶点缓冲 | 用 `numpy` 提供数据 |
| 变换矩阵 | 模型/视图/投影 | 旋转立方体 |
| 上下文 | GLUT/SDL 窗口 | 🔧 现代系统搭建繁琐 |

## 核心精讲

现代 OpenGL 是「着色器驱动」：你把顶点数组上传到 GPU（VBO），用 GLSL 写顶点/片元着色器，再发绘制命令。

```python
# 教学示意，不参与构建
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

VERT = b"""
#version 330 core
in vec3 aPos;
uniform mat4 uMVP;
void main(){ gl_Position = uMVP * vec4(aPos, 1.0); }
"""
FRAG = b"""
#version 330 core
out vec4 frag;
void main(){ frag = vec4(0.4, 0.7, 1.0, 1.0); }
"""

def make_program():
    return compileProgram(
        compileShader(VERT, GL_VERTEX_SHADER),
        compileShader(FRAG, GL_FRAGMENT_SHADER))

# 立方体顶点用 numpy 数组，dtype=np.float32，np.frombuffer 上传 VBO
```

> 要点：`np.float32` 连续数组 + `glBufferData` 上传；`uMVP` 是模型-视图-投影合成矩阵（可用 `pyrr`/`glm` 计算）。

## 版本演进

- 原书用**旧式** OpenGL（固定管线 `glBegin/glVertex`），现代已废弃，必须写 GLSL 着色器（Core Profile 3.3+）。
- 上下文创建：原书用 GLUT；现代更稳的是 SDL2 / GLFW + `PyOpenGL`。
- `PyOpenGL` 在 3.12+ 基本可用，但驱动/上下文是主要痛点（🔧）。

## 经典论文与原始文献

- OpenGL 官方规范（Khronos Group）：https://www.khronos.org/opengl/ 。
- GLSL 规范同站；「渲染管线」概念见实时图形学教材（如 *Real-Time Rendering*, Akenine-Möller 等）。
- Python 侧：`PyOpenGL` 文档；矩阵库 `pyrr`/`PyGLM`。
- 无专属 PEP（图形 API 不在 Python 语言层）。

## 近年研究与工业界开源实践（2015–2026）

- WebGL / WebGPU 让图形进浏览器；Python 侧有 `vispy`、`moderngl`（更 Pythonic 的 OpenGL 封装）、`pyglet`。
- 科学可视化：`vtk`、`pyvista`（体渲染/3D 数据）。
- GPU 计算：`cupy`、`pytorch` 张量即 GPU 缓冲，常用于非图形并行。

## 常见误区与本书需修正之处

| 误区 | 修正 |
|---|---|
| 照搬 `glBegin/glVertex` | 现代 Core Profile 用 VBO + GLSL 着色器 |
| 用 GLUT 当生产窗口 | 现代用 GLFW/SDL2，GLUT 停滞维护 |
| 顶点数组 dtype 非 float32 | 必须 `np.float32` 且 C 连续 |
| 忽视矩阵乘法顺序 | MVP = Projection·View·Model，顺序反则错位 |

## 与其他章 / 其他书的联系

- 接 [10-粒子系统.md](10-粒子系统.md)（着色器粒子）、[11-体渲染.md](11-体渲染.md)（3D 纹理/光线投射）。
- numpy 缓冲上传范式见 [04-Karplus-Strong弦合成.md](04-Karplus-Strong弦合成.md)、[05-Boids鸟群模拟.md](05-Boids鸟群模拟.md)。
- 可视化进阶见 [../Python数据科学手册2e.md](../PythonDataScienceHandbook2e.md)、[../高性能Python（第2版）.md](../高性能Python（第2版）.md)。
