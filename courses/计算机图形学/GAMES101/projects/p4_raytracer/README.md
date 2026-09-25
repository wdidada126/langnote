# p4 — Whitted 光线追踪 → 简单路径追踪（GAMES101 L15–L16；官方 Lecture 15–20）

> 对应课程 Assignment 4 的核心思想（球体版）。仅标准库 C++17，输出 PPM。

## 覆盖讲次

- L15：辐射度量（线性域累加/tonemap 的动机）、蒙特卡洛积分（半球采样估计器）、渲染方程。
- L16：Whitted 递归（反射/Snell 折射/全反射）、阴影光线、路径追踪
  （Lambertian+镜面、cos 加权与均匀半球采样、NEE、俄罗斯轮盘赌）。
- L13 收尾：Reinhard 色调映射 + gamma 编码；L09：像素内分层多采样 = 抗锯齿。

## 场景

3 个漫反射/金属球 + 1 个玻璃球 + 半空间棋盘地面（L10 的两种隐式图元）。

## 两种模式

### `whitted`（确定性，无噪声）

$$C = \text{localShade} + k_r C(\text{反射线}) + k_t C(\text{折射线})$$

局部 Blinn-Phong + 点光源阴影光线；镜面球里能看见漫反射球的"假"互照明
（其实只是镜面映像）。

### `path`（蒙特卡洛，收敛到物理解）

渲染方程逐样本估计（L15 推导）：

$$\hat L_o = L_e + \frac{f_r(\omega_i,\omega_o)\,\hat L_i(\omega_i)\,\cos\theta}{p(\omega_i)}$$

- Lambert：$f_r=\frac{alb}{\pi}$；**cos 加权采样** $p=\frac{\cos\theta}{\pi}$ → 权重=alb（零方差）；
  换 `mode=pathuni`（均匀半球 $p=\frac1{2\pi}$）权重 $2\,alb\cos$，噪声略大——对照实验。
- 金属：镜面 δ 方向，$f$/权重退化为 albedo。
- 玻璃：按 Snell 折射弹射（不采样，保持简单）。
- **NEE**：每个交点向点光源补一条阴影光线（L16 降噪第一招）。
- 深度 >2 后无偏俄罗斯轮盘赌（存活 0.8，throughput ×1/0.8）。
- 像素 4×4 分层抖动（stratified）：抗锯齿 + 降低聚簇噪声。

## 构建与运行

```sh
./build.sh
./bin/p4 path   16   512 path_16.ppm          # 低采样：明显噪声
./bin/p4 path   1024 512 path_1024.ppm        # 高采样：干净参考
./bin/p4 path   16   512 path_16_blur.ppm blur # 朴素 3×3 箱式降噪
./bin/p4 whitted 1   512 whitted.ppm           # 秒出，对比"假全局光照"
```

```bat
build.bat
bin\p4 path 16 512 path_16.ppm
bin\p4 path 1024 512 path_1024.ppm
bin\p4 whitted 1 512 whitted.ppm
```

## 降噪对比（README 即实验说明）

按 $O(1/\sqrt{N})$，16→1024 spp 噪声应降 ~8 倍。三图对照：

| 图 | 期望观察 |
| --- | --- |
| `path_16.ppm` | 椒盐噪声；间接光区域（红球旁的微红反弹）糊成一团 |
| `path_1024.ppm` | 锐利干净；角点色溢（color bleeding）清晰 |
| `path_16_blur.ppm` | 噪声被抹平，但**边缘/高光也被抹糊**——朴素降噪"作弊"的代价； |
|  | 现代做法（OPTIX Denoiser/SVGF，GAMES202）用反照率/法线/运动矢量引导保边滤波 |

## 参数与实验

- `spp` 2 的幂逐级翻倍：亲测收敛率。
- 改 `Scene::spheres` 的 `type/albedo`：全场景金属 / 加一个"光源球"（发射材质）。
- 给 `Scene` 加 AABB 包围体列表 → 选做 BVH（L16 加速；官方 Assignment 4 拓展）。
- `randomCosineHemisphere` 的推导（$\theta=\arccos\sqrt{\xi_1}$）见 notes/L15。

## 已知局限

- 玻璃折射不采样、无菲涅尔加权（Whitted 模式里有近似）→ 路径模式下玻璃偏"水"。
- 地面半空间不参与反弹（避免无限弹射的额外方差），间接光只剩球-球互照明。
- 球体暴力求交（4 个无所谓；>100 个物体请上 BVH，选做）。
