# libear

```
dpkg -L libear
/.
/usr
/usr/lib
/usr/lib/x86_64-linux-gnu
/usr/lib/x86_64-linux-gnu/bear
/usr/lib/x86_64-linux-gnu/bear/libear.so
/usr/share
/usr/share/doc
/usr/share/doc/libear
/usr/share/doc/libear/changelog.Debian.gz
/usr/share/doc/libear/copyright
```

### libear 库介绍

libear（全称 EBU ADM Renderer Library）是一个开源的 C++14 库，专为音频渲染设计，用于根据 ITU-R BS.2127 推荐标准 处理和渲染 ADM（Audio Definition Model） 内容。它是 EBU（European Broadcasting Union，欧洲广播联盟） 的核心组件之一，主要用于 下一代音频（Next Generation Audio, NGA） 的实现，如沉浸式音频、空间音频渲染等。 该库于 2019 年由 BBC R&D（英国广播公司研发部门） 和 IRT（德国广播技术研究所） 联合开发，旨在提供高效的实时音频渲染算法。

#### 核心功能与特点
- 渲染类型支持：
  - 通道基音频（Channel-based）：传统多声道渲染。
  - 场景基音频（Scene-based）：支持 3D 场景音频。
  - 对象基音频（Object-based）：动态对象定位和混音。
- 算法核心：计算增益（gains）和应用 DSP（数字信号处理）组件，实现 ADM 元数据的解释和音频输出。
- 不包含的文件 I/O：libear 只处理渲染逻辑；推荐结合 libbw64（BW64 文件读写）和 libadm（ADM XML 解析）使用，以实现完整管道。
- 性能：实时应用友好，API 稳定（从发布起未重大变更），支持嵌入式集成。
- 局限性（截至 2025 年）：部分高级参数（如某些对象元数据）尚未完全支持，但核心功能已成熟；未来版本计划完善。

#### 许可与开源
- 许可证：Apache 2.0（宽松许可），允许商业和非商业使用、修改和分发。
- 仓库：GitHub - [ebu/libear](https://github.com/ebu/libear)（星标 100+，活跃维护）。
- 文档：官方 ReadTheDocs - [libear.readthedocs.io](https://libear.readthedocs.io/en/latest/index.html)，包含 API 参考和示例。

#### 安装与使用
libear 使用 CMake 构建系统，集成简单。以下是典型步骤（基于官方指南）：

1. 克隆并构建：
   ```
   git clone --recursive https://github.com/ebu/libear.git
   cd libear
   mkdir build && cd build
   cmake ..
   make -j$(nproc)  # 或 cmake --build .
   sudo make install
   ```

2. CMake 项目集成（示例）：
   ```cmake
   cmake_minimum_required(VERSION 3.5)
   project(MyProject LANGUAGES CXX)
   find_package(ear REQUIRED)  # 如果已安装
   # 或 add_subdirectory(submodules/libear)  # 如果用子模块
   add_executable(myapp main.cpp)
   target_link_libraries(myapp PRIVATE ear)
   ```

3. 简单 C++ 示例（渲染 ADM 音频）：
   ```cpp
   #include <ear.h>  // libear 头文件
   #include <iostream>

   int main() {
       // 假设已加载 ADM 数据
       ear::Renderer renderer;  // 创建渲染器
       // 配置 ADM 元数据...
       // renderer.process(audio_buffer);  // 应用渲染
       std::cout << "Rendering complete!" << std::endl;
       return 0;
   }
   ```

#### 应用场景（2025 年现状）
- 广播与媒体：集成到 DAW（数字音频工作站，如 Reaper 或自定义插件）中渲染 NGA 内容，用于 TV/广播沉浸式音频。
- 实时应用：游戏引擎、VR/AR 音频系统、直播工具。
- 生态：与 EBU 的其他工具（如 EAR Python 原型）互补；2025 年已广泛用于欧洲公共广播系统（如 BBC、ARD），并扩展到亚洲/美洲的音频生产链。
- 社区：EBU 维护活跃，定期更新以匹配 ITU 标准演进；适合音频工程师和开发者。

一句话总结：libear 是 2025 年构建 ADM/NGA 音频渲染器的首选开源库，轻量高效、标准合规。如果您是音频开发者，强烈推荐从 GitHub 示例起步！
