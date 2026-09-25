# p02 搜索树（search trees）

- 对应讲次：L14（BST）、L15（平衡化动机）、L16（工程容器对照）、CLRS 14.1（增广/区间树）。
- 知识点：BST 插入/删除（两子用后继顶替）、successor 的父指针上行、中序遍历；**区间树** = BST + 子树 max 增广 + `x.max < lo` / `x.iv[0] > hi` 双剪枝；插入序决定树高（随机 Θ(log n) vs 升序 Θ(n) 退化）。
- 文件：`main.py`（BST、IntervalTree、50+60 轮随机对拍自测、树高实验表）。
- 运行：`run.bat` / `bash run.sh`；手动 `python -m py_compile main.py && python main.py`。
- 预期输出：对拍断言全过；实验表显示 n 增大时随机序树高 ≈ c·log₂n（c<3）而升序树高 = n（链）。
- 延伸：给 BST 加 AVL 平衡因子与旋转即完成 L15 作业；把 key 换成 (low, high) 并改重叠谓词可解 " stabbing query"。
