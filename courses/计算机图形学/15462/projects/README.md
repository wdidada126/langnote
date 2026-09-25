# 15-462 配套项目计划（本轮不写代码）

统一约定：主线 C++（CMake + Eigen + libigl），图像实验类用 Python(numpy/matplotlib) 对照；每个小项目独立可构建；只写不编译。

| 章节（讲次） | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L01-L03 | C++ | 齐次变换库：复合/求逆/法向变换 + 单元测试 | CMake |
| L04-L06 | Python+C++ | 采样-混叠-重建实验台：sinc vs 帐篷 vs Mipmap，附 2D FFT 频谱图 | venv |
| L07-L08 | C++ | 软光栅器：三角形→z-buffer→纹理；画家/BSP/z-buffer 可见性对比 | CMake |
| L09-L12 | C++(libigl) | 半边网格编辑器 + Loop 细分 + marching cubes(SDF→mesh) | CMake+libigl |
| L13-L15 | C++ | 路径追踪 v1：球/网格、Whitted→简化渲染方程 | CMake |
| L16-L17 | C++ | MC 积分器：均匀/余弦/GGX 重要性采样 + MIS，收敛曲线报告 | CMake |
| L18 | Python | 薄透镜相机 + 景深渲染；光场 4D 重放小实验 | venv |
| L19-L20 | C++ | 弹簧-质点+半隐式积分布料；显式 vs 隐式稳定性对比 | CMake |
| L21-L22 | C++/Python | 阻尼 IK 双臂抓取 demo + DFT 图像压缩小工具 | CMake/venv |
| Final | C++ | 综合渲染器：光栅化 G-buffer + BVH 光追 + 降噪，渲染官方场景 | CMake |
