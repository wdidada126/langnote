# L12 纹理映射（Textures）

> 对应 README 讲次 L12；官方 Lecture 07、11。阅读：FCG4 Ch.12。实践：projects/p2。

## 1. 纹理 = 定义在曲面上的函数

给每个表面点配一个 $(u,v)\in[0,1]^2$ 参数（UV 映射），把图像"贴"上去。
本质：**用 2D 函数给 3D 表面赋属性**（颜色、粗糙度、法线、金属度…）。
UV 展开（L11 网格参数化）是美术工作流：接缝（seam）、拉伸、Texel 密度均匀性
是三大痛点；unwrap 后打包到 [0,1] 方格。

## 2. 采样与滤波：从 texel 到颜色

片元拿到 $(u,v)$ 后是连续值，需从离散 texel 重建：

- **最近邻**：放大出马赛克（放大问题）。
- **双线性插值（bilinear）**：四邻域两次线性插值 → 连续但梯度不连续；
  缩小问题依旧：一个像素覆盖多个 texel 时闪烁/走样（minification aliasing）。

## 3. Mipmap：预计算 LOD 金字塔

**问题**：透视下远处表面纹素密度远超采样率 → 缩小走样（L09 频域分析再现）。
**解法**（Williams 1983）：为纹理预建 $n\times n \to 1\times1$ 的二分金字塔，
每层已做平均（低通）。运行时估计屏幕空间纹理频率（相邻像素的 UV 差 $u_x,u_y$，
解析三角式或硬件梯度单元）：

$$\mathrm{LOD}=\log_2\max(\lVert\nabla_u\rVert,\lVert\nabla_v\rVert),\quad
\text{颜色}=\mathrm{trilinear}(\mathrm{level})$$

**Trilinear**：相邻两层各做一次双线性再 lerp。**各向异性过滤（AF）**：
斜视长方形 footprint 时沿主轴多次采样——地面纹理远端的清晰度救星。
内存代价 +33%，带宽换质量。

## 4. 透视 correct 纹理插值

L06 的债在此偿还：屏幕空间线性插值 UV 会导致**纹理在斜面上拉伸错乱**。
修正（L08 重心坐标推广）：

$$\alpha'=\frac{\alpha}{z},\ \beta'=\frac{\beta}{z},\ \gamma'=\frac{\gamma}{z},
\quad u(P)=\frac{\alpha' u_A+\beta' u_B+\gamma' u_C}{\alpha'+\beta'+\gamma'}$$

（$z$ 为视深）。GPU 光栅化器自动做这件事；软件光栅化器（projects/p2）
故意先错后对，出图对比。

## 5. 法线/凹凸/置换：骗过光照而非颜色

纹理作用于**法线**而非颜色时，视觉细节远超分辨率本身：

- **Bump mapping**（Blinn 1978）：高度场 $h(u,v)$ → 扰动法线 $\hat n+\epsilon\nabla h$。
- **Normal mapping**（Kimling 2004）：直接存 $\hat n$（切线空间 RGB），游戏工业标准；
  高模烘焙进低模，省几何不省"看起来的细节"。
- **Parallax/relief mapping**：沿视线偏移 UV，模拟真实高度（自遮挡需 raymarch）。
- **Displacement/POM**：真改几何（细分 + 置换）或真 raymarch——离线/高端实时。

## 6. 与前后续讲的联系

- 依赖 L08（重心坐标）、L09（滤波/频率）、L11（UV 参数化）。
- L14 着色将把纹理从"颜色贴图"泛化为"材质贴图集"（albedo/roughness/normal/AO）。
- L15–L16 光线追踪里纹理即"求交后对 $(u,v)$ 的函数求值"；
  光追的 footprint 估计 = 锥形追踪（Igehy 1999，进阶内容）。
- 神经新贵：NeRF/3DGS 可视为"用 MLP/高斯基元替代手工 UV+纹理"（跨课联系）。

## 7. 跨课程联系

- **信号处理**：mipmap = 多尺度金字塔，与小波/尺度空间（图像处理）同构。
- **CS149**：纹理访问是 GPU 带宽的头号大户，texel 缓存/各向异性/压缩纹理
  （BCN/ASTC）都是存储层次设计（DDCA 的 cache 视角）。
- **DDCA/CSAPP**：GPU 纹理单元做双线性/三线性是固定功能"查表插值器"，
  类比协处理器指令。
- **CS231n**：程序化纹理与风格迁移的"纹理统计"（Gatys）视角：纹理是
  二阶统计量，内容是一阶——有趣旁支。

## 8. 开源项目中的应用

- **glTF 2.0**：标准 PBR 材质槽（baseColorTexture/normalTexture/occlusionTexture…），
  即本讲纹理家族的产品化。
- **Three.js/Filament**：`texture.generateMipmaps/anisotropy` 一行开关背后全链路。
- **Blender Shader Editor**：Image Texture/Bump/Normal Map 节点。
- **DirectXTex / ASTC encoder**：压缩纹理工具链。
- **projects/p2**：程序化 checker 纹理 + 透视 correct/incorrect 对比输出。

## 9. 延伸阅读与自查

- 阅读：FCG4 Ch.12；Williams 1983《Pyramidal Parametrics》；Heckbert 1989
  《Fundamentals of Texture Mapping and Image Warping》（透视 correct 插值名文）。
- 自查：
  1. 为什么 mipmap 用"层内 lerp"而非直接取最近层？（连续性/梯度。）
  2. 斜视地面 100 米外纹理消失成灰 —— 用频率分析解释，并给出 AF 能救哪部分。
  3. 推导透视 correct 插值中为何权重与视深 $z$ 成反比（面积论证或代数推导）。
