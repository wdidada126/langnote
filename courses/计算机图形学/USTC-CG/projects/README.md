# USTC CG 配套项目计划（本轮不写代码）

统一约定：C/C++（CMake + Eigen/libigl），对齐官网 9 HW + 1 Project 的题量；每题独立构建；只写不编译。

| 章节（讲次） | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L02-L03 | C++ | 2D 绘图库：Bresenham 线/圆 + 多边形扫描填充，输出 BMP/SVG | CMake |
| L04-L05 | C++ | 软渲染管线 v1：z-buffer 多边形消隐 + alpha 混合 | CMake |
| L06-L07 | C++ | 着色与纹理：Gouraud/Phong + 双线性纹理 + Mipmap | CMake |
| L08 | C++ | 光线追踪器：球/网格、反射折射 + BVH 加速 | CMake |
| L09 | C++/GLSL | SDF 字体渲染器：距离场生成 + GPU 平滑采样 | CMake+GLFW |
| L10 | Python | 曲线拟合工具：样条/Bézier 交互编辑与 SVG 导出 | venv |
| L11-L12 | C++(libigl) | 网格分析器：曲率可视化 + Loop 细分 + QEM 简化 | CMake+libigl |
| L13 | C++ | 参数化实验：LSCM 共形展平 + 纹理重投影 | CMake+libigl |
| L14 | C++/Python | 泊松图像编辑：克隆/接缝修补（OpenCV 对照实现） | venv/CMake |
| L15 | C++(PCL) | 点云→曲面：法向估计 + Poisson 重建 | CMake+PCL |
| Project | C++ | 自选大项目（渲染器/几何管线），附 README 与对比报告 | CMake |
