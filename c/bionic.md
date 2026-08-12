# bionic

Bionic 是 Android 系统中使用的 C 标准库（C library），它是 Android 操作系统的重要组成部分之一。与常见的 GNU C 库（glibc）或 musl、uClibc 等标准库不同，Bionic 是 Google 专门为 Android 定制开发的轻量级 C 库。

---

## 一、什么是 Bionic？

###  名称来源：
“Bionic” 来自 “bionic man”，是科幻电视剧《The Six Million Dollar Man》中的主角，Google 内部曾以此命名项目。

###  主要作用：
- 提供 POSIX 和 ISO C 标准函数接口（如 `malloc`, `printf`, `open`, `read`, `write` 等）
- 与 Linux 内核交互
- 提供 Android 特有的扩展功能（如 `android_get_device_api_level()`）

---

##  二、Bionic 的特点

| 特点 | 描述 |
|------|------|
| 轻量高效 | 只实现了 Android 需要的部分标准库功能，去掉了冗余代码 |
| 不完全兼容 glibc | 缺少一些 glibc 支持的功能（如 `gethostbyname_r` 的某些变种） |
| 基于 BSD libc 衍生 | 初始代码来自 FreeBSD 的 libc，而非 glibc |
| 紧密集成 Linux 内核 | 使用 `__bionic_open_etc()`、`__bionic_recv_bug_32937345()` 等内部机制 |
| 支持 Android 特有功能 | 如 log、属性服务、设备 API 级别获取等 |

---

##  三、Bionic 的源码结构（AOSP 中）

你可以在 AOSP 中找到 Bionic 的源码路径：

```
https://android.googlesource.com/platform/bionic/
```

主要目录如下：

| 目录 | 功能说明 |
|------|----------|
| `libc/` | C 标准库实现，包含系统调用封装、字符串处理、文件 I/O 等 |
| `libm/` | 数学库（浮点运算、三角函数等） |
| `libdl/` | 动态链接库加载支持（`dlopen`, `dlsym` 等） |
| `libcutils/` | Android 常用工具函数（如原子操作、线程相关） |
| `libbase/` | Android 基础库（文件读写、字符串处理等） |
| `tests/` | 单元测试 |
| `include/` | 公共头文件（如 `<stdio.h>`, `<unistd.h>`） |

---

##  四、Bionic 与其他 C 标准库对比

| 项目 | Bionic | glibc | musl |
|------|--------|-------|------|
| 开发者 | Google | FSF/GNU | Rich Felker |
| 设计目标 | 轻量、Android 定制 | 全面支持标准、兼容性高 | 小巧、标准兼容 |
| 适用平台 | Android | Linux 桌面/服务器 | 嵌入式/Linux |
| 许可证 | Apache-2.0 | LGPL | MIT |
| 是否完整支持 POSIX |  大部分 |  完整 |  完整 |
| 是否支持 Android 特有功能 |  是 |  否 |  否 |

---

##  五、Bionic 的使用场景

1. Android Framework 层：Java/Kotlin 通过 JNI 调用到 Native 时最终会调用 Bionic。
2. Native App 开发：使用 NDK 编写 C/C++ 代码时，默认使用 Bionic。
3. 系统级开发：Android 系统组件（如 Zygote、init、SurfaceFlinger）都依赖 Bionic。
4. 内核驱动调试：在编写用户空间工具时，需要调用 Bionic 接口访问硬件。

---

## 六、NDK 中如何使用 Bionic？

当你使用 Android NDK 开发 C/C++ 代码时，编译器会自动链接 Bionic 库。

### 示例代码：

```cpp
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <android/api-level.h>

void print_info() {
    printf("PID: %d\n", getpid());
    printf("Running on Android API level %d\n", android_get_device_api_level());
}
```

### CMakeLists.txt 示例：

```cmake
add_library(native-lib SHARED native.cpp)
find_library(log-lib log)
target_link_libraries(native-lib ${log-lib})
```

---

##  七、常见问题 & 注意事项

###  不支持的 glibc 函数示例：

| glibc 函数 | 在 Bionic 中是否可用 |
|------------|---------------------|
| `gethostbyname_r`（非标准变体） |  |
| `crypt()` |  |
| `fts_*` 文件树遍历系列函数 |  |
| `strptime` | （但部分格式可能不支持） |
| `pthread_condattr_setclock` |  |
| `realpath` | （但行为略有不同） |

你可以参考官方文档了解哪些函数被支持：
🔗 [https://android.googlesource.com/platform/bionic/+/refs/heads/main/docs/status.md](https://android.googlesource.com/platform/bionic/+/refs/heads/main/docs/status.md)

---

## 八、Bionic 的发展与现状

- 持续更新：随着 Android 新版本发布，Bionic 也在不断更新以支持新特性（如 C++20、TLSv1.3 等）。
- 安全强化：增加了 ASLR、Stack Protector、Fortify 等安全机制。
- 对 ARM64/x86_64 支持完善：适配多种架构和 ABI。
- 与 ART 运行时深度整合：为 Java/Kotlin 提供底层支撑。

---

## 九、推荐阅读资料

| 资源 | 地址 |
|------|------|
| AOSP Bionic GitHub | https://android.googlesource.com/platform/bionic/ |
| Bionic 文档 | https://android.googlesource.com/platform/bionic/+/main/docs/ |
| Android NDK 官方文档 | https://developer.android.com/ndk |
| Bionic vs glibc 对比 | https://wiki.debian.org/ArmEabiPort/BionicComparison |
| Android API Level 获取方法 | https://developer.android.com/ndk/reference/group___a_p_i.html#ga52ef55e7f0ac932d8c32fb5e1dfbaeb3 |

---

## 十、总结

| 维度 | Bionic |
|------|--------|
| 所属 | Android 系统核心组件 |
| 功能 | 提供 C 标准库 + Android 扩展 |
| 架构支持 | ARM, x86, MIPS 等 |
| 开发语言 | C |
| 开发者 | Google |
| 优势 | 轻量、快速、Android 专用优化 |
| 劣势 | 不兼容 glibc，缺少部分标准函数 |

---

如果你正在做 Android NDK 开发、定制 ROM 或系统级调试，理解 Bionic 的工作原理将非常有帮助。

