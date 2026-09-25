# GAMES202 配套项目计划（本轮不写代码）

统一约定：语言 C++（OpenGL 3.3+/Vulkan 可选），构建 CMake（复用 GAMES101 作业框架风格），渲染结果存 PNG 比对；全部代码只写不编译，集中编译由用户执行。

| 章节（讲次） | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L01-L02 | C++ | 迷你延迟管线：G-buffer 生成 + 简单合成 pass | CMake + GLFW/GLAD |
| L03-L04 阴影 | C++/GLSL | Shadow Mapping → PCSS → VSM 三档软阴影对比 | CMake 子目录 `p1_shadow` |
| L05+L09 IBL/PBR | C++/GLSL | Cook-Torrance GGX 材质球 + split-sum IBL（含 BRDF LUT） | CMake 子目录 `p2_pbr` |
| L06-L08 GI | C++/GLSL | SSAO + 辐照度探针插值 + SH9 环境光烘焙器 | CMake 子目录 `p3_gi` |
| L10-L11 材质 | C++/GLSL | 屏幕空间 SSS + 各向异性金属 + 多层涂层测试床 | CMake 子目录 `p4_materials` |
| L12-L13 光追 | C++ (OptiX 或 CPU BVH) | 混合渲染器：光栅 G-buffer + 每像素 ≤1 反射光线 + 时域降噪 | CMake + SDK 路径（只配置不编译） |
| L14 超分 | C++/GLSL | TAA 实现 + FSR(EASU+RCAS) 单文件接入 demo | CMake 子目录 `p5_upscale` |
| L15 综合 | C++ | 综合渲染器：CSM + IBL + SSGI + 光追反射 + TAA，附帧预算剖析表 | CMake `final` |
