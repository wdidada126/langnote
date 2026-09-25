# L07 图形管线概览：可见性、z-buffer 与着色流水线

> 对应 README 讲次 L07；官方 Lecture 05。阅读：FCG4 Ch.6、Ch.10。实践：projects/p2。

## 1. 渲染管线全景

```
顶点数据(3D, 模型系) ──MVP──▶ 裁剪空间 ──÷w──▶ NDC ──viewport──▶ 屏幕坐标
      │  顶点着色器（可编程：动画、变换）
      ▼
图元装配（三角形）──▶ 光栅化：哪些像素被覆盖？(L08)
      ▼
片元/像素处理 ──▶ 深度测试(z-buffer) ──▶ 混合/输出合并 ──▶ 帧缓冲 framebuffer
      纹理采样 + 光照计算（片元着色器，L12/L14）
```

三个固定思想：**几何用矩阵搬运，颜色用函数计算，可见性用逐像素竞争解决**。

## 2. 可见性问题（Hidden Surface）

画家算法（按深度排序后从远到近画）：O(n log n) 排序、对相交三角形无解。
逐多边形扫描线、BSP 树各有局限。**z-buffer（深度缓冲）** 的解法朴素而伟大：

```
初始化: color[i][j] = 背景;  depth[i][j] = +∞
对每个三角形、每个覆盖像素 (i,j):
    if z_fragment < depth[i][j]:        # 深度测试
        depth[i][j] = z_fragment
        color[i][j] = shade(fragment)   # 先写颜色再算或先算再写(硬件预剔除)
```

- 复杂度 O(像素数 × 平均覆盖层数)，**无需排序**，允许三角形任意相交、
  以任意顺序提交——这是对并行渲染友好的关键（CS149 视角：无全局同步点，
  仅原子性深度测试）。
- 内存代价：每像素一个深度值（24/32-bit）。现代 GPU 用 **early-z / Hierarchical-Z**
  在光栅化阶段就剔除被遮挡片元，省去片元着色开销（DDCA 的流水线思想）。
- 历史：Catmull 1974 博士论文（帧缓冲 + z-buffer），他后来创办皮克斯。

## 3. 管线哪些阶段可编程？

| 阶段 | 性质 | 内容 |
| --- | --- | --- |
| 顶点着色 | 可编程 | MVP、蒙皮、置换 |
| 图元装配/裁剪 | 固定 | 三角形出屏怎么处理 |
| 光栅化/插值 | 固定 | 重心坐标插值（L08） |
| 片元着色 | 可编程 | 纹理、光照（L12/L14） |
| 输出合并 | 固定+可配 | 混合、MSAA 解析（L09） |

"固定功能 + 可编程插槽"的结构让驱动能把可编程部分映射到不同硬件
（Vulkan/Metal/DX12 的显式管线即该结构的直接暴露）。

## 4. 与前后续讲的联系

- 本讲是 L04–L06 变换与 L08–L09 光栅化之间的"总装车间"。
- z-buffer 依赖 L06 的深度非线性映射；深度值又将在 L09 的 MSAA 中保持逐样本、
  颜色保持逐像素——两者的分离正是 MSAA 可行性的前提。
- 本讲"像素最终颜色"悬而未决 → L13–L14 着色的登场；可见性的另一条路（光线追踪）
  在 L16 回马枪：它**用求交顺序天然解决 z-buffer 要解决的问题**。

## 5. 跨课程联系

- **DDCA/CSAPP**：渲染管线 = 硬件流水线（分段、寄存器、吞吐 vs 延迟）；
  early-z ≈ 分支预测失败时的浪费剔除；帧缓冲 ≈ 内存映射 I/O（CSAPP Ch.9 页表视角）。
- **CS149**：z-buffer 的深度测试是"无序生产者 + 每像素局部归约（min）"，
  可 lock-free 原子实现——课程并行模式（reduction）的图形学原型。
- **18.06 复用**：视口变换（NDC→像素）只是一次仿射（L04 的 S/T 复合）。
- **GAMES202**：deferred rendering 把"颜色"延后、先存 G-buffer——本讲管线
  的现代变体；occlusion query 把可见性测试做成异步查询。

## 6. 开源项目中的应用

- **Mesa/Vulkan（RADV）**：`vkCmdDraw` 提交的正是本讲管线；驱动/硬件调度器
  把三角形分给多个 rasterizer 单元。
- **Three.js/Filament**：`renderer.render(scene,camera)` 背后是整条管线；
  Filament 的 `material.frameUniform` 演示顶点/片元两端的可编程接口。
- **tinyrenderer（dgoyette/dBuramku）**：70 行 C++ 复刻本讲管线 + L08 光栅化，
  与 projects/p2 同构。
- **Blender EEVEE**：合成前向管线，G-buffer/early-z 优化的教科书用户。

## 7. 延伸阅读与自查

- 阅读：Fabian Giesen《A trip through the Graphics Pipeline》（第 1、4–5 篇）；
  Catmull 1974 论文；Vulkan 官方规范"Rendering Architecture"章（可只读图）。
- 自查：
  1. 为什么 z-buffer 不需要全局排序？画家算法失败的反例（三角形相交/循环遮挡）。
  2. early-z 为什么能安全跳过被深度测试淘汰的片元着色？它对半透明物体为何失效？
  3. 深度值写 16/24/32-bit 的画质差异出现在屏幕何处？（提示：L06 非线性。）
