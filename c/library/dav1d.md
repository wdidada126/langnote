# dav1d

基于C语言的dav1d解码器

`dav1d` 是一个高性能、开源的 AV1 视频解码器库，完全用 C 语言编写，由 VideoLAN（VLC 的开发团队）和 ffmpeg 开发者共同维护。它专注于提供快速、轻量级且无专利问题的 AV1 解码方案。

---

##  一、dav1d 简介

| 特性 | 描述 |
|------|------|
| 编程语言 | C 语言（兼容 C89/C99） |
| 协议 | BSD-2-Clause License（非常宽松） |
| 支持平台 | Linux, Windows, macOS, Android, iOS 等 |
| 多线程 | 支持多线程解码 |
| 硬件加速 | 支持 x86 SSE/AVX、NEON（ARM）、AArch64 |
| 集成支持 | 可与 FFmpeg、GStreamer、VLC 等集成 |

---

##  二、安装 dav1d（Linux 示例）

### 方法 1：使用包管理器安装（推荐）

```bash
# Ubuntu / Debian
sudo apt install libdav1d-dev

# Fedora
sudo dnf install libdav1d-devel
```

### 方法 2：从源码编译安装

```bash
git clone https://code.videolan.org/videolan/dav1d.git
cd dav1d
meson build --prefix=/usr/local
ninja -C build
sudo ninja -C build install
```

>  安装后你会得到 `libdav1d.so` 或 `libdav1d.a`，以及头文件 `dav1d/dav1d.h`

---

##  三、基于 C 语言调用 dav1d 的完整示例

下面是一个简单的 C 程序，演示如何使用 dav1d 解码一个 AV1 帧数据。

>  注意：本示例假设你已经有了 AV1 的 OBU 数据或帧数据，并未处理容器格式（如 IVF、WebM），只关注核心解码逻辑。

###  示例代码：`dav1d_simple_decode.c`

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dav1d/dav1d.h>

#define MAX_FRAME_SIZE (1024 * 1024 * 4) // 4MB max frame size

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <input_file.av1>\n", argv[0]);
        return 1;
    }

    FILE *fp = fopen(argv[1], "rb");
    if (!fp) {
        perror("Failed to open input file");
        return 1;
    }

    Dav1dContext *c = NULL;
    Dav1dSettings settings;
    dav1d_default_settings(&settings);
    settings.n_threads = 4; // 设置解码线程数

    if (dav1d_open(&c, &settings)) {
        fprintf(stderr, "Failed to open dav1d context\n");
        fclose(fp);
        return 1;
    }

    Dav1dData data = { 0 };
    Dav1dPicture p = { 0 };

    // 读取整个文件到内存中（简化处理）
    fseek(fp, 0, SEEK_END);
    size_t size = ftell(fp);
    fseek(fp, 0, SEEK_SET);

    uint8_t *buf = malloc(size);
    fread(buf, 1, size, fp);
    fclose(fp);

    dav1d_data_wrap_external_buffer(&data, buf, size, NULL, NULL);

    int res;

    while ((res = dav1d_decode(c, &p, &data)) == DAV1D_ERR(AGAIN)) {
        // 继续解码
    }

    if (res < 0) {
        fprintf(stderr, "Decode error: %s\n", dav1d_strerror(res));
    } else {
        printf("Decoded frame: %dx%d, format: %d\n",
               p.p.w, p.p.h, p.p.bpc);
        // 此处你可以访问图像数据 p.data[0]、p.stride 等
    }

    dav1d_picture_unref(&p);
    dav1d_data_unref(&data);
    dav1d_close(&c);
    free(buf);

    return 0;
}
```

---

##  四、编译并运行

### 编译命令：

```bash
gcc dav1d_simple_decode.c -o dav1d_simple -ldav1d
```

### 运行命令：

```bash
./dav1d_simple sample.av1
```

>  `sample.av1` 应该是原始的 AV1 比特流文件（OBU 格式）。如果需要从 WebM 提取 AV1 数据，可以使用 `ffmpeg` 或 `ivfenc` 工具。

---

## 五、如何获取 AV1 测试文件？

你可以从以下资源获取 AV1 测试视频：

- [AOMedia Test Data](https://media.xiph.org/video/derf/)
- 使用 `ffmpeg` 转换任意视频为 AV1：

```bash
ffmpeg -i input.mp4 -c:v libaom-av1 -crf 30 -b:v 0 output.av1
```

---

## 六、主要结构体和函数说明

| 类型/函数 | 用途 |
|----------|------|
| `Dav1dSettings` | 初始化解码器设置（如线程数） |
| `dav1d_open()` | 打开解码器上下文 |
| `dav1d_decode()` | 解码一帧数据 |
| `Dav1dData` | 输入比特流数据 |
| `Dav1dPicture` | 输出图像数据 |
| `dav1d_close()` | 关闭解码器 |
| `dav1d_data_wrap_external_buffer()` | 包裹外部缓冲区 |
| `dav1d_picture_unref()` | 释放图像资源 |

---

## 七、进阶建议

如果你希望将 dav1d 集成到更复杂的项目中，比如播放器、嵌入式设备、实时视频传输系统等，可以考虑：

| 功能 | 推荐做法 |
|------|----------|
| 支持 WebM 容器 | 结合 `libwebm` 或 `ffmpeg` 解析容器 |
| 图像显示 | 使用 SDL2、OpenGL 显示解码后的 YUV 数据 |
| 多线程优化 | 利用 dav1d 自带的多线程机制 |
| 性能监控 | 记录每帧解码耗时，统计 FPS |
| 错误恢复 | 对于损坏的数据做容错处理 |

---

## 总结

| 内容 | 说明 |
|------|------|
| 名称 | dav1d |
| 语言 | C |
| 特点 | 快速、轻量、无专利限制 |
| 官网 | https://code.videolan.org/videolan/dav1d |
| 示例 | 上述完整代码展示了如何使用 dav1d 解码 AV1 帧 |
| 编译 | `gcc -o decode dav1d_simple_decode.c -ldav1d` |
| 适用场景 | AV1 解码器、嵌入式系统、播放器、FFmpeg 插件等 |

---

如果你有特定的使用场景，比如：
- 在嵌入式系统中部署
- 与 SDL2 显示图像
- 实现 AV1 实时播放器
- 从 WebM 文件提取 AV1 数据

## rust
Prossimo 公司开发了基于 Rust 的 AV1 解码器 rav1d，其目标是对广泛应用且被认为是最快的基于 C 语言的 dav1d 解码器进行内存安全的重新实现。但目前 rav1d 的性能比 dav1d 慢约 5%。为此 Prossimo 设立了 2 万美元（约合人民币 14.3 万元）的奖金，寻求能让 rav1d 性能达到与 dav1d 同等水平的方法。该计划对参与者有地区限制，仅面向部分国家或地区的开发者。优化需体现在 rav1d 项目本身、Rust 编译器或标准库上，且不能修改底层汇编代码，只能使用 Rust 编写代码。
对此，FFmpeg 以「Rust 真好啊，好到你需要花 2 万美元才能让它跑得和 C 语言一样快」这样略带讽刺的言论，对该悬赏计划进行了评论。
