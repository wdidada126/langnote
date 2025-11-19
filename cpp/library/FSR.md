# FSR

AMD FidelityFX Super Resolution (FSR) 是 AMD 开发的开源图形技术，用于游戏和应用的帧率提升和图像上采样。截至 2025 年 11 月，其开源代码主要托管在 GitHub 的 GPUOpen 组织下，采用 MIT 许可协议，开发者可免费下载、修改和集成。

### 主要开源仓库（按版本分类）
以下是 FSR 各版本的核心开源仓库链接（基于官方 GPUOpen 项目）：

| FSR 版本 | 仓库描述 | GitHub 网址 |
|----------|----------|-------------|
| FSR 1.0 | 基础空间上采样技术，支持 DirectX 和 Vulkan。 | [https://github.com/GPUOpen-Effects/FidelityFX-FSR](https://github.com/GPUOpen-Effects/FidelityFX-FSR) |
| FSR 2.0 | 时空上采样，提升图像质量，支持更多后端。 | [https://github.com/GPUOpen-Effects/FidelityFX-FSR2](https://github.com/GPUOpen-Effects/FidelityFX-FSR2) |
| FSR 3.0 | 添加帧生成（Frame Generation），开源源代码已发布，支持 DLL 集成和调试。 | [https://github.com/GPUOpen-LibrariesAndSDKs/FidelityFX-SDK](https://github.com/GPUOpen-LibrariesAndSDKs/FidelityFX-SDK)（FSR3 分支） |

### 额外资源
- 官方文档和下载页：访问 [GPUOpen FSR 页面](https://gpuopen.com/fidelityfx-super-resolution/)，可获取 SDK、示例代码和集成指南。
- FSR 3 发布公告：详细介绍源代码可用性，[AMD GPUOpen 新闻](https://gpuopen.com/news/fsr3-source-available/)。

这些仓库包含完整源代码、构建脚本和示例。如果你需要特定版本的集成教程或更新，建议直接克隆仓库查看 README。
