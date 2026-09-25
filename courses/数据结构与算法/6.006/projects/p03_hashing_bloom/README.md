# p03 哈希表与 Bloom filter

- 对应讲次：L07（开放寻址/墓碑/负载因子）、L17（双重哈希派生 k 个函数、Bloom 数学）、L19（倍增重建的摊还拷贝计数）。
- 知识点：线性探测 + 墓碑 + 0.5 负载倍增重建；splitmix64/FNV 确定性哈希（不吃 PYTHONHASHSEED 的随机盐）；Bloom filter 无假阴性、FPR 理论式 (1−e^{−kn/m})^k 与最优 k*=(m/n)ln2。
- 文件：`main.py`（HashTable、BloomFilter、4000 操作对拍 dict、6 组 k 的 FPR 表）。
- 运行：`run.bat` / `bash run.sh`；手动 `python -m py_compile main.py && python main.py`。
- 预期输出：重建总拷贝 ≤ 2.5n（几何级数账）；实测 FPR 贴合理论曲线、k=7 附近最低。
- 延伸：把 m 换成 `array('Q')` 位数组可省 8 倍内存；加计数 Bloom 支持删除（L17 讨论）。
