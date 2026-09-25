# CS148 配套项目计划（本轮不写代码）

统一约定：语言 Python（numpy + matplotlib/PIL），对应届次直接以 HW 风格实现软渲染器主线；只写不编译，运行环境用 venv+requirements 备查。

| 章节（讲次） | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L02 | Blender/py | 建模一个场景并导出 .blend/USD 说明文档 | Blender CLI `blender -b` |
| L03-L04 | Python | 场景图 + 变换栈：层次太阳系渲染为线框图 | `python sol.py`（venv） |
| L05 | Python | 图像合成器：alpha 混合、gamma 正确混合对比 | venv |
| L06-L07 | Python | 软光栅器 v1：三角形重心插值 + Lambert/Phong + 双线性纹理 | venv |
| L08 | Python | 光线投射器 v2：球/三角求交 + 平面/棋盘场景 | venv |
| L09 | Python | 反走样与软阴影：像素/光源蒙特卡洛采样 | venv |
| L10 | Python | BVH 光追 v3：反射/折射 + 加速，对比无 BVH 计时 | venv |
| Final | Python/Blender | 短片：建模→材质→渲染→合成 全流程作品 | Blender + Python 管线 |
