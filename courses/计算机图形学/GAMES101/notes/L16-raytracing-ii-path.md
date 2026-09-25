# L16 光线追踪（二）：Whitted 光追、加速结构与路径追踪

> 对应 README 讲次 L16；官方 Lecture 18–20（Ray Tracing I–II / Material Models）。
> 阅读：FCG4 Ch.14、Ch.29–30。实践：projects/p4。

## 1. 反向追踪的合法性

L15 结论（L 沿光线不变）允许我们从眼睛发射光线：
像素 → 场景求交 → 交点处"该像素收到多少 L"。每像素多光线 = 抗锯齿/景深/
运动模糊（L09、附录的时间/透镜维度采样——光线追踪的采样天然均匀）。

## 2. Whitted 模型（1980）：递归光线

```
RayColor(ray, depth):
    (t, x, n, material) = ClosestHit(ray)        # 求交取最近
    if none: return background
    c = 局部着色(L14: 直接光 + 环境)
    if depth < Dmax:
        if 反射材质:  c += k_r * RayColor(Reflect(ray,x,n), depth+1)
        if 透明材质:  c += k_t * RayColor(Refract(ray,x,n), depth+1)  # Snell
    return c
```

- 反射方向 $\hat r=\hat d-2(\hat d\cdot\hat n)\hat n$；折射 Snell 定律
  $n_1\sin\theta_1=n_2\sin\theta_2$，全反射在 $\sin\theta_2>1$ 时发生
  （projects/p4 的玻璃球演示）。
- 阴影光线：交点 → 光源单独求交测试，**免费得到精确阴影**——
  光栅化需要 shadow map（GAMES202）才能近似的东西。
- 局限：递归是**确定性的、只按材质分支** → 没有漫反射互照明（间接光），
  因为"该往哪个反射方向发线？"漫反射有无穷多方向。答案：交给蒙特卡洛
  （路径追踪）。

## 3. 加速结构：求交是 O(场景×光线)

- **包围体**：球（2 次平方）/AABB（slab 法：对 3 轴区间求交，分支少、
  SIMD 友好）。空则跳过内部所有图元。
- **BVH**：图元二分树，每个节点一个 AABB。构造：按重心/SAH 选轴切分
  （surface area heuristic：期望代价 ∝ 表面积）。遍历：栈/优先队列 +
  最近命中提前剔除。工业标配：BVH8（AVX）、bvh2/4/8 随硬件演进；
  动态场景用 LBVH/增量重构。
- **规则网格**：均匀/自适应体素 + 3D DDA 步进，适合大场景均质分布。
- 复杂度：$O(\log n)$/光线（vs $O(n)$）——光线追踪从玩具到电影的第一功臣。

## 4. 路径追踪 = 渲染方程的 MC 解（Kajiya 1986 思想，落地于 90 年代）

对每像素每帧生成**一条随机游走的光路**（或每样本一条）：

$$\hat L_o=L_e+\frac{f_r(x,\omega_i,\omega_o)\,L_i(x,\omega_i)\,(\hat n\cdot\omega_i)}{p(\omega_i)}$$

- $\omega_i$ 按密度 $p$ 随机采样（均匀半球 / **cos 加权**：
  $\theta=\arccos\sqrt{1-\xi_1},\ \phi=2\pi\xi_2$，对 Lambert 场景零方差）；
  递归求 $L_i$，到光源或达深度上限。**俄罗斯轮盘赌**控制无偏变长路径。
- 光源采样：直接光单独加一条阴影光线（NEE，next event estimation）
  → 方差骤降；面积光/环境光的按立体角采样（L15 重要性采样的兑现）。
- 收敛表现：低频间接光 $O(1/\sqrt N)$；噪声随 spp 降低而细化（p4 对比图）。
- 与辐射度（L15 对照）：MC 路径追踪支持全部 BRDF/镜面/折射；
  辐射度对纯漫反射大场景的"预计算 + 便宜查询"思想活在 lightmap（GAMES202）。
- 现代延伸：ReSTIR（时空复用样本 reservoir，SIGGRAPH 2020–2023）让
  路径追踪挤进实时；神经降噪（NVIDIA/Intel）用学习先验补 $O(1/\sqrt N)$ 的短板。

## 5. 与光栅化/几何主线的关系

| 维度 | 光栅化（L04–L12） | 路径追踪（本讲） |
| --- | --- | --- |
| 采样对象 | 像素格（规则） | 光线/光路（随机） |
| 可见性 | z-buffer | 求交天然有序 |
| 抗锯齿 | MSAA/Mipmap | 多采样收敛 |
| 间接光 | 近似（探针/SSGI） | 物理正确 |
| 时间预算 | 16 ms | 秒–分钟（离线）/降噪后实时 |

两条主线在混合渲染器（Unreal Lumen、Frostbite ray-traced AA）中正合流。

## 6. 跨课程联系

- **CS149**：光线求交 = 不规则负载 + 指针追逐（BVH 遍历）→ warp divergence
  经典案例；课程作业常以"并行 BVH/光追"为题。
- **DDCA/CSAPP**：BVH 节点布局对缓存行/预取极敏感；SAH 本质是用局部性换算术。
- **数据结构（6.006）**：BVH=平衡二叉搜索的几何版；优先队列遍历、kd-tree 对照。
- **18.06**：反射矩阵 $I-2nn^T$ 是 Householder 变换——线代课堂的几何高光。
- **CS231n/生成模型**：降噪/超分/重光照是条件生成模型的任务空间；
  NeRF 的体积渲染积分与本讲路径积分在数学上同族（传输理论视角）。
- **GAMES202**：光追降噪（SVGF/OIDN）、光线追踪管线（DXR）系统展开。

## 7. 开源项目中的应用

- **raytracing-in-one-weekend(+serious)**：Whitted→路径追踪的最短路径，
  与 projects/p4 完全同构。
- **PBRT-v4 / Blender Cycles / Mitsuba 3**：生产级路径追踪（多光源策略、
  体积、波前/瓦片调度）。
- **Intel Embree / NVIDIA OptiX**：CPU/GPU 光线求交内核库（BVH 工业实现）。
- **小彩虹：`projects/p4`**：单层球 Whitted → Lambertian+镜面路径追踪、
  16 vs 1024 spp 噪声对比，全部标准库 C++17 + PPM 输出。

## 8. 延伸阅读与自查

- 阅读：FCG4 Ch.14、29–30；Whitted 1980、Kajiya 1986、Goldsmith-Salmon 1987
  原文；Veach 1997 博士论文（N EE/轮盘赌/MIS 的出处）；《RTW 三部曲》。
- 自查：
  1. 手推 Snell 折射方向向量，并给出全反射判据（用 $\hat d,\hat n,n_1/n_2$ 表达）。
  2. 为什么 cos 半球采样对 Lambert 材质零方差，对镜面却爆炸？
  3. 画一个两球互遮挡场景，说明 BVH 遍历顺序与最近命中剔除的交互。
  4. 16→256 spp 噪声理论上降几倍？若用 4×4 分层采样呢？
