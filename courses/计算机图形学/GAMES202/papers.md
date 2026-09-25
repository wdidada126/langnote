# GAMES202 论文与应用清单

## 1. 经典论文（课程直接引用）

| 论文 | 年份 | 关联讲次 | 一句话贡献 |
| --- | --- | --- | --- |
| Williams, Casting curved shadows on curved surfaces | 1978 | L03 | Shadow Mapping 开山 |
| Heckbert-Salesin, Fast rendering of antialiased and accurate images | 1994 | L14 | 像素中心与抗锯齿实践 |
| Kajiya, The rendering equation | 1984 | L02/L14 | 全局光统一方程；时域解思想 |
| Cook-Torrance, A reflectance model for computer graphics | 1982 | L09 | 微表面 BRDF 奠基 |
| Walter et al., Microfacet models for refraction through rough surfaces | 2007 | L09 | GGX 分布 |
| Pharr-Jakob, Nonlinear spatial filters with variance | 2012 | L11 | 非线性滤波预滤波辐射度 |
| Ramamoorthi-Hanrahan, Frequency-space environment lighting | 2001 | L08 | 光照的 SH 低频可预计算理论 |
| Sloan et al., Precomputed radiance transfer | 2002 | L08 | PRT |
| Donnelly-Lauritzen, Vitamin shadow maps / variance shadows | 2006/2010 | L04 | 软阴影滤波族 |
| Lauritzen, Water-like RIP: annihilation filtering（VSM 改进）等 | 2010 | L04 | 现代阴影综述 |
| Aila et al., Understanding the latency of simple ray tracing workloads（GPU 光追硬件） | 2010 | L12 | GPU 光线追踪体系 |
| McAdams et al., Marling（各向异性 GGX 实时） | 2013 | L10 | Karis SIGGRAPH PBR 课程同源 |
| Karis, Real shading in UE4（SIGGRAPH PBR course） | 2013 | L05/L09 | split-sum IBL 工业化 |
| Schied et al., Spatiotemporal minimal image filters SSGI | 2017 | L06 | 屏幕空间 GI 代表 |
| Bitterli et al., Spatiotemporal variance-guided filtering | 2016 | L13 | 实时光追降噪经典 |

## 2. 近 5 年论文（2021-2026）

| 论文 | 年份 | 方向 | 与课程联系 |
| --- | --- | --- | --- |
| ReSTIR GI / ReSTIR PT（Lin et al.; Lee et al.） | 2021-2022 | 实时 GI 光追 | L13 时空重采样主线 |
| Ray Tracing: The Next Generation（NVIDIA Research 系列） | 2020-2023 | 硬件光追生态 | L12 |
| 3D Gaussian Splatting（Kerbl et al., SIGGRAPH） | 2023 | 神经渲染表示 | 点 splatting 光栅化与 L15 管线新分支 |
| Mip-NeRF 360 / Instant-NGP | 2022 | 神经渲染 | 与 SH 预积分/体渲染对照 |
| Nanite（Karras? 实为 Graham Wihlidal/Karras 报道，SIGGRAPH 2021） | 2021 | GPU 驱动几何 | L15 mesh cluster/剔除 |
| DLSS 3 帧生成 / Optical Flow Multi Frame（NVIDIA） | 2023 | 时域超分/生成 | L14 超采样前沿 |
| Hash blend / Material Graph 自动化标定（Disney/MERL 后续） | 2021+ | 材质 | L11 |
| SVOGI→Lumen（Epic 技术文档与论文化报告） | 2021-2023 | 实时 GI 软件光追 | L06-L07 工业落地 |
| Differentiable MC rendering（Zhang/Nimier-David 系列） | 2021-2023 | 可微渲染 | 渲染方程与蒙特卡洛的延伸 |

## 3. 知识点在开源项目中的应用

| 课程知识点 | 开源项目/产品 | 具体体现 |
| --- | --- | --- |
| PBR (GGX) + IBL | Three.js / Filament / Bevy | MeshStandardMaterial、KHR_materials_* 扩展、IBL 管线 |
| Shadow Mapping/CSM | Mesa(Vulkan)/bgfx/Unity(URP 源码分析) | depth bias、级联、VSM 实验分支 |
| SSAO/SSR/SSGI | Godot 4、SpartanEngine、PlayCanvas | 屏幕空间效果 pass |
| 球谐/烘焙 GI | Godot lightmap baking、Blender bake | SH 探针、方向光照贴图 |
| 实时光追 | Blender Cycles（CPU/GPU RT）、Mesa ray tracing vulkan、LVP/Lumen 开源复刻 | BLAS/TLAS、降噪 |
| ReSTIR/降噪 | NVIDIA NRDE 公开接口、Open Image Denoise(OIDN) | 生产降噪器 |
| TAA/DLSS | FSR 2/3（AMD 开源）、XeSS 参考实现、Intel | 时域超分完整开源参考 |
| Splatting/GS | gsplat、Nerfstudio、Polycam | 神经渲染开源栈 |
| SDF 渲染 | tinyexr? 更准确：Frostbite/SDFGI（Godot 实现）、rpg_SDFGI | 距离场 GI |
