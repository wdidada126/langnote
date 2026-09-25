# GAMES202 逐讲要点（骨架）

> 每讲 3-5 条要点，全文笔记后续填充。

## L01 实时渲染概述
- 实时渲染定义：>30/60 FPS 的帧预算（16-33ms）下追求最高画质，一切方法都是时间预算的产物。
- 与离线渲染（路径追踪）的根本差异：单帧样本数从上万降到个位数，必须靠"近似+滤波+时域复用"补偿。
- 课程地图：阴影 → 环境光照 → GI → 着色 → 光追 → 抗锯齿/超分。

## L02 回顾：渲染管线/着色语言/渲染方程
- 现代管线：VS → 光栅化 → PS → OIT/后处理；shader program 在 GPU 上的执行模型。
- 渲染方程 L = Le + ∫ f L cosθ dω 的逐项含义；实时渲染 = 用各种手段近似该积分。
- 微积分与概率基础：立体角、余因子的重要性；蒙特卡洛估计器与方差。

## L03 实时阴影 1
- Shadow Map 原理：光源视角深度图 + 比较，硬件一次管线即可实现。
- 核心问题：acne 与 peter-panning 的 bias 权衡、阴影贴图分辨率与 3D 纹理级联（CSM）。
- 点光源/方向光/聚光的贴图布局（cube map、tiling）。

## L04 实时阴影 2
- 硬阴影不真实：软阴影需要光源面积/遮挡物距离信息。
- PCSS：两遍（penumbra estimation + 增加样本）；VSM/ESSM：存深度矩做高斯滤波。
- 现代方案：游标阴影贴图、ANN/光线检测混合、时域降噪。

## L05 实时环境光照（IBL）
- 环境光不是常数：irradiance environment map 预积分漫反射；镜面用 prefiltered radiance mip。
- Split-sum 近似（Epic）：BRDF LUT 把几何遮蔽-粗糙度项与积分项分离。
- 实时更新环境的代价与替代（探针、SH 压缩）。

## L06 实时全局光照 1（屏幕空间）
- SSAO/HBAO：从深度缓冲估计环境可见度，廉价遮蔽近似。
- SSR：屏幕空间光线步进，局限在屏内数据。
- SSGI/SPAR：屏幕空间辐射度传播 + 时域复用与降噪。

## L07 实时全局光照 2（空间类）
- Light Probe（辐照度探针）+ 四面体化插值（Unity/Unreal 探针布局）。
- SDF/距离场 GI：用包围体贴图（Zenith）做廉价多次弹射。
- 预计算辐射传输与运行时探针的权衡：动态场景适配。

## L08 实时全局光照 3（预计算与烘焙）
- 球谐函数（SH）：投影低频光照，9 系数即可表示辐照度；旋转与压缩。
- PRT：把光照与物体传递函数分离，可实时换光。
- Lightmap 烘焙：UV 展开、方向光照贴图（directional LM）、商用管线实践。

## L09 实时高质量着色 1
- 微表面理论：GGX 法线分布 + Smith 阴影遮蔽 + Fresnel（Schlick 近似）= Cook-Torrance。
- 能量守恒与多重散射补偿；metal/roughness 与 specular-glossiness 工作流。
- 重要性采样与预滤波：为什么 IBL 与 PBR 必须成套使用。

## L10 实时高质量着色 2
- 次表面散射 SSS：扩散近似（d'Eon）、屏幕空间 separable SSS、曲率补偿。
- 各向异性（Aniso GGX）、清漆（coat）、透明度与厚度（refraction）。
- 风格化渲染：卡通描边、色阶化光照——BRDF 的非物理用法。

## L11 实时高质量着色 3
- 复杂材质：织物（fiber 模型）、多层堆叠（layered BRDF）与归一化。
- 参数空间一致性：保证材质"物理可信"（F0 区间、能量守恒）。
- 影视级材质标定（Disney BRDF 参数表、MERL 数据库）迁移到实时。

## L12 实时光线追踪 1
- 硬件光追接口：DXR/Vulkan RT 的 BLAS/TLAS、ray query 与 SBT。
- 混合渲染：光栅化做 G-buffer + 光追做反射/阴影/Occlusion。
- 低采样光追的噪声问题：滤波与时域累积的必要性。

## L13 实时光线追踪 2
- 降噪：SVManifolds/Bilateral GPU 滤波 → 学习式降噪器（NVIDIA SDK/OIDN）。
- ReSTIR：时空重要性重采样，把每个像素的样本"借"给邻域，实现实时 GI 光追。
- 光线预算调度：反射/阴影/GI 的 rays per pixel 分配与性能剖析。

## L14 实时抗锯齿与超采样
- 时域抗锯齿 TAA：历史帧重投影、抖动、ghosting 与解法。
- DLSS/FSR/XeSS：ML 超分与空间超分的管线；与相机随机采样配合。
- Kajiya 84"渲染方程的时域解"思想源头。

## L15 工业界常用技术
- 管线级优化：deferred/tilered deferred、集群前向、GPU 驱动管线（mesh shader）。
- LOD/HLOD/剔除（GPU driven culling）、带宽意识设计。
- 从"单点技术"到"整帧预算"：引擎渲染架构综合案例。
