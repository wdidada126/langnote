# p1 — 向量/矩阵库与变换演示（GAMES101 L02–L06）

## 覆盖讲次

本目录 README 讲次 **L02（向量）、L03（矩阵/齐次坐标）、L04（2D 变换与复合）、
L05（3D 旋转/视图/求逆）、L06（投影）**。对应官方 23 讲制的 Lecture 02–04。

## 算法要点

- `src/geom.hpp`：Vec2/3/4、`Mat4`（行主序、列向量约定 `v' = M v`）、
  平移/缩放/旋转、`lookAt`、`ortho`、`perspective`（透视除法 `perspDiv`）、
  刚体求逆 `inverseRigid`（L05 捷径）。
- `src/main.cpp`：
  1. **2D 仿射演示**：以"小房子"线段模型过 8 种矩阵（I、T、R、S、复合 T·R·S、
     绕定点旋转、剪切、R·T），验证"复合从右往左消费"（L04）。
  2. **MVP 线框**：4 个非均匀缩放+旋转相位的立方体，经
     `proj * view * model` → 透视除法 → NDC → 屏幕映射，输出线框（Bresenham）。
  3. 自检：`view * inverseRigid(view)` 与单位阵的最大偏差打印到 stdout。

## 构建与运行

```bat
:: Windows（MSVC，任意 x64 Native Tools 命令行）
build.bat        :: 生成 bin\p1.exe
bin\p1.exe
```

```sh
# Linux/macOS/WSL
./build.sh       # g++ -std=c++17 -O2
./bin/p1
```

## 输出图像说明

- `transforms_2d.ppm`：800×800，2×4 网格。观察：`T.R.S` 与 `R(90)T` 姿态不同
  → 矩阵乘法不交换（L03）；剪切格子里房子歪斜但面积比变化符合 det 直觉（L03）。
- `mvp_cube.ppm`：400×400 四宫格线框，近大远小（透视除法生效，L06）；
  压扁的 y 缩放让旋转呈现"果冻感"——非均匀缩放 + 旋转的复合直观。
- PPM 为 P3 文本格式，任意看图软件/`eog`/`IrfanView` 可开；也可
  `python -c` 一行转 png。

## 练习衔接

- 在 2D 演示里加 `S·R·T` 与 `T·R·S` 对比图；
- 把线框改成只画正面 3 个面（提示：视空间 z 排序即可，z-buffer 留给 p2/L07）。
