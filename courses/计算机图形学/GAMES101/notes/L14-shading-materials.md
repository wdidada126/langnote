# L14 几何着色（Shading and Geometry / 光照模型）

> 对应 README 讲次 L14；官方 Lecture 13–14。阅读：FCG4 Ch.10–11。实践：projects/p2。

## 1. 着色三件套：环境 + 漫反射 + 镜面

对局部光源 $i$、表面点 $x$、法线 $\hat n$、视线 $\hat v$、光向 $\hat l$：

$$\text{color}=\underbrace{k_a\,c_a}_{\text{环境}}+\sum_i\Big(\underbrace{k_d\,c_d\,(\hat n\cdot\hat l)\,\frac{\Phi}{4\pi r^2}}_{\text{Lambert 漫反射}}+\underbrace{k_s\,c_s\,(\hat r\cdot\hat v)^p}_{\text{Phong 镜面}}\Big)$$

- **Lambert**：粗糙表面各方向均匀散射，能量 ∝ $\cos\theta$（辐照度投影，
  L15 将解释为何是 $\cos$ 而不是别的）。
- **Phong**：$\hat r$ 为 $\hat l$ 关于 $\hat n$ 的镜像；高光"看起来在镜面方向"
  的经验幂函数，$p$ 越大越光滑。
- **Blinn-Phong**（工业默认）：用半角 $\hat h=\widehat{\hat l+\hat v}$ 替代 $\hat r$，
  $(\hat n\cdot\hat h)^{p'}$——避免反射向量计算、无"背面高光"缺陷、$p'\approx p/4\cdot2$。
  一次点积 + 幂，SIMD 极友好（DDCA 视角）。

衰减 $\frac{\Phi}{4\pi r^2}$ 来自点光源能量球面守恒（L15 辐射度量学的预告）。

## 2. 逐顶点（Gouraud）vs 逐片元（Phong shading）

- **Phong 光照模型**（本讲公式）逐像素算：需要逐像素法线 → 重心坐标
  插值顶点法线并**透视 correct**（L08/L12 的债）+ 归一化。
- **Gouraud 明暗处理**：顶点算颜色、片元插值颜色——高光会丢失/偏移，
  但 1971 年是革命。
- 注意术语撞车：Phong 反射模型（1975）≠ Phong 明暗处理（1975，法线插值）。
  两者常合称 "Phong shading"，考试与论文里务必区分。

## 3. 法线与着色质量

- 共享顶点法线（平滑/软着色）vs 面法线（平直/低多边形风）——
  同一个网格两种法线即两种外观（projects/p3/p2 可视化）。
- 法线变换矩阵：$\hat n'=(M^{-1})^T\hat n$（L04 预告的逆转置，此处兑现）。
  非均匀缩放时忘记逆转置 → 高光漂移，是新手第一大 bug。

## 4. BRDF 初探

双向反射分布函数 $f_r(l,v)$：入射方向辐照度 → 出射方向 radiance 的比例密度。
形式要求（能量守恒、互易性 Helmholtz）：

$$\int_{\Omega} f_r(l,v)(\hat n\cdot\hat v)\,d\omega \le 1,\qquad f_r(l,v)=f_r(v,l)$$

- Lambert BRDF 是常数 $f_r=\frac{c_d}{\pi}$（$\pi$ 来自半球积分归一，L15 严格推导）。
- 各向同性假设：$f_r$ 只依赖相对角度。
- **Cook-Torrance 微表面模型预告**：把表面看成微观镜面小平面（microfacet）
  集合 → $f=\frac{DFG}{4(\hat n\cdot\hat l)(\hat n\cdot\hat v)}$，D=法线分布（GGX）、
  G=遮蔽阴影、F=菲涅尔。L14 只讲思想，公式在 GAMES202/《RTR》第 9 章展开；
  L16 的"材质模型"讲将回到 BRDF 与光线追踪的组合。

## 5. 与前后续讲的联系

- 需要 L12（albedo/normal 纹理喂给它）、L13（颜色在哪个空间相乘）、
  L08（逐片元插值）。
- 本讲是**局部光照**的顶点：反射/折射/阴影/间接光无法用局部模型表达
  → L15 渲染方程统一收编；L16 光线追踪逐一实现。
- projects/p2 用 Blinn-Phong + 点光源 + 棋盘 albedo 完成"第一个像样的渲染图"。

## 6. 跨课程联系

- **DDCA/CSAPP**：Blinn-Phong 的指令剖面（3 点积 + 幂，pow 用 exp2/log2 近似）
  是着色器 ALU 规划的入门案例。
- **18.06**：逆转置来自"切空间基变换、法线余变"的对偶观点（线性代数进阶）。
- **CS231n/生成模型**：神经渲染（NeRF 的 view-dependent color、Dreamer 的
  渲染头）学的就是本讲 BRDF 的替代物——MLP 直接回归 $c(l,v)$。
- **CS149**：片元着色是"规整（regular）数据并行"的极致：每像素独立、
  同一程序、海量实例。
- **GAMES202**：PBR 工作流（metallic-roughness、Ibl、DDA）= 本讲微表面预告的工程化。

## 7. 开源项目中的应用

- **glTF/Filament/UE**：metallicRoughness 材质 = Cook-Torrance GGX 的参数化。
- **Three.js**：`MeshPhongMaterial/MeshStandardMaterial` 正好对应本讲的
  经验模型 → 物理模型演化。
- **Shadertoy**：Blinn-Phong 是新手第一个 shader；`pow(NdotH, shininess)` 随处可见。
- **PBRT**：`Twosided/MeasuringMaterial` 与 LUT 实测 BRDF（MERL 数据库）。

## 8. 延伸阅读与自查

- 阅读：FCG4 Ch.10–11；Phong 1975、Blinn 1977、Cook-Torrance 1982 原文
  （见 papers.md）；《RTR》Ch.8–9 速览。
- 自查：
  1. 推导 Blinn-Phong 半角向量公式并说明它为何比 Phong 项更"温和"。
  2. Gouraud 下高光在三角形中心的"滑移/消失"实验如何复现（p2 选做）？
  3. 非均匀缩放 (2,1,1) 下，球顶点的法线该乘什么矩阵？算一个具体点。
  4. 为什么 Lambert 的 BRDF 常数是 $c_d/\pi$ 而不是 $c_d$？
