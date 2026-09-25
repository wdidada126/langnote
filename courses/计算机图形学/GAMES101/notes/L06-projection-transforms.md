# L06 投影变换：视锥体、正交投影与透视投影

> 对应 README 讲次 L06；官方 Lecture 04（后半）。阅读：FCG4 Ch.5。实践：projects/p1、p2。

## 1. 投影 = 降维 + 规范化

相机视锥体（frustum：上/下/左/右/近/远六面）内可见。投影做两件事：
把视锥体**压成** $[-1,1]^3$ 的规范立方体（NDC, normalized device coordinates），
之后统一走 L08 的光栅化。两种压缩：正交（保平行）与透视（近大远小）。

## 2. 正交投影（Orthographic）

参数：l, r, b, t, n, f（左右下远近）。两步复合：平移到原点 → 缩放到单位立方体：

$$M_{ortho}=\begin{bmatrix}\frac{2}{r-l}&0&0&-\frac{r+l}{r-l}\\0&\frac{2}{t-b}&0&-\frac{t+b}{t-b}\\0&0&-\frac{2}{f-n}&-\frac{f+n}{f-n}\\0&0&0&1\end{bmatrix}$$

注意 z 用**负缩放**：相机看向 $-z$，而 NDC 深度约定越大越远（OpenGL 惯例，
Vulkan/D3D 为 $[0,1]$）。用途：CAD、2D 游戏、阴影贴图（GAMES202 的 shadow map 从光
的视角做的正是正交/透视投影）。

## 3. 透视投影（Perspective）

先"压扁"：把视锥体映射为长方体。$z'=\frac{n}{-z}z$（x、y 同除 $-z/n$），
即小孔成像的相似三角形：$x_{near}=x\cdot\frac n{-z}$。写成齐次矩阵

$$M_{persp\toortho}=\begin{bmatrix}1&0&0&0\\0&1&0&0\\0&0&\frac{f}{f-n}&-\frac{fn}{f-n}\\0&0&-1&0\end{bmatrix}$$

第四列的 $-1$ 使输出 $w=-z$。随后接正交投影（l,b,r,t 替换为按 $n$ 平面与 $f_{ovy}$
算出的尺寸）。**齐次坐标在管线中一路保留到这一步才做除法**：

$$\text{perspective divide: }\ (x,y,z,w)\mapsto(x/w,\,y/w,\,z/w)$$

这就是"齐次坐标为何必要"的终极答案——线性部分（含 $w=-z$）用矩阵表达，
非线性部分（除以 $z$）交给一次硬件除法。GPU 中固定功能单元完成该除法。

## 4. 透视 correct 插值的伏笔

透视除法后，屏幕空间里均匀的参数不再对应世界空间均匀的位置 →
直接线性插值纹理/法线会**畸变**（近处被拉伸）。修正：插值属性除以 $z$ 再加权
（$\alpha/z$ 权重，L08 重心坐标 + L12 纹理一起给出公式）。projects/p2 中
checker 纹理的对比图即该问题的可视化。

## 5. 与前后续讲的联系

- MVP 到此集齐：$M_{clip}=P\cdot V\cdot M$（L04–L06）。
- 投影完 → 视口变换（viewport）→ NDC 进 L07/L08 光栅化。
- 相机参数（FOV、n/f）是附录讲"运动模糊/景深"里唯一被时间扩展的量。
- $z$ 的非线性映射是 L07 深度精度问题（z-fighting）的根源：近处精度极高、
  远处极粗 → 需要 24-bit 深度缓冲、reversed-Z 等工程对策。

## 6. 跨课程联系

- **DDCA/CSAPP**：固定功能除法是流水线里典型的高延迟单元；GPU 用倒数近似表
  （RSQ）实现 $1/z$——CSAPP 浮点章节的现实版。
- **18.06**：透视→正交矩阵可逆（$w=-z$ 只是记录视深，未丢信息），但最后的
  透视除法是真正的信息丢失步骤——NDC 深度可从投影矩阵参数反解回视深，
  这正是深度缓冲重建 3D 位置（deferred shading、深度图）的数学依据。
- **CS231n/NeRF**：针孔相机模型 = 本讲小孔成像 + 内参矩阵 $K$
  （焦距/主点），NeRF 的 rays 生成完全照抄；FOV 变化即内参变化。
- **GAMES202**：lightmap/阴影贴图的 UV 变换、CSM 的分裂 sphere 都绕不开投影矩阵逆。

## 7. 开源项目中的应用

- **GLM**：`glm::perspective(radians(45.f), aspect, .1f, 100.f)`、`glm::ortho`。
- **WebGL/Three.js**：`PerspectiveCamera.fov/near/far` 直接决定矩阵参数；
  `camera.updateProjectionMatrix()` 即重算 $P$。
- **Filament**：`Camera::setProjectionFromCone/FromValues`。
- **Mesa llvmpipe / tinyrenderer**：软件管线中手写 $P\cdot V\cdot M$ 后做齐次除法，
  与 projects/p2 流程一致。

## 8. 延伸阅读与自查

- 阅读：FCG4 Ch.5.3–5.4；Fabian Giesen 名文《A trip through the Graphics Pipeline》
  系列第 1–3 篇（NDC 与视口的硬件细节）。
- 自查：
  1. 推导 $M_{persp\toortho}$ 第三行为何是 $(0,0,\frac{f}{f-n},-\frac{fn}{f-n})$。
  2. 为什么把 near 从 0.1 改到 1.0 能显著缓解 z-fighting？
  3. 正交投影下，三角形面积在 NDC 中是常数吗？透视呢？
