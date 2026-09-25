# ch02-bits-float —— 位级整数与 IEEE 754 实验室

**关联讲次**：L02（数据表示·整数/位运算）、L03（浮点与 IEEE 754）。
对应 CSAPP 官方 **Data Lab** 的思想：只用位级操作实现语义，并用无符号模算术
规避有符号溢出等未定义行为。

## 内容

| 文件 | 说明 |
| --- | --- |
| `src/bits.h` / `src/bits.c` | 7 个位级函数：`bit_and`(德摩根)、`bit_count`(分治 popcount)、`bang`(无 `!` 取逻辑非)、`sat_add`(饱和加)、`is_positive`、`float_neg/abs/twice`(浮点位级) |
| `src/main.c` | 自检测试表，对照编译器求值结果与位模式预期 |

## 知识点

- 补码/无符号仅是同一位向量的两种"解释"（bang/is_positive 全部在 unsigned 域运算）。
- `(unsigned)~x + 1` 构造 `-x` 位模式——全程无 UB。
- IEEE 754 三域切分：exp 域的最低位就是 frac 的第 23 位，
  因此非规格化翻倍 `frac << 1` 会"自动"进入规格化（见 main 中 0x00400000 用例）。
- NaN 在 `uf > 0x7F800000` 无符号序判定区——与 L03 数轴图一致。

## 构建与运行

```sh
# Linux/macOS (gcc) 或 Windows (MSVC)：
./build.sh        # → bin/bits_test（Windows 下 bits_test.exe）
# Windows 需在 "x64 Native Tools Command Prompt" 或先 call vcvarsall.bat x64
build.bat
```

GCC 编译建议附 `-Wall -Wextra -std=c99`。
