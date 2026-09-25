# projects/ — MIT 6.050J 配套小项目计划（本轮只列计划，不写代码）

语言：**Python**（numpy / matplotlib / scipy），官方 MATLAB 作业全部改写为 Python；纠错码部分可选 **Julia/C** 以贴近系统实现。

| 章节 | 建议语言 | 小项目 | 编译 / 运行方式 |
| --- | --- | --- | --- |
| L2–L4 熵 | Python | `entropy_lab.py`：统计英文语料的字符/双字熵率，比较定长码与理论下界 | `python entropy_lab.py` |
| L7 Huffman | Python | `huffman.py`：实现 Huffman 编码/解码并压缩一个文本文件，报告平均码长 vs 熵 | `python huffman.py input.txt` |
| L8 压缩对比 | Python | `compress_bench.py`：同一组文件跑 gzip / lz4 / zstd，画压缩比-速度散点图 | `python compress_bench.py`（依赖 python-zstandard、lz4） |
| L9–L12 信道 | Python | `bsc_sim.py`：蒙特卡洛模拟 BSC 上重复码/汉明码的误码率曲线，对照香农容量线 | `python bsc_sim.py` |
| L13–L14 纠错码 | Python / C | `hamming74.c` 或 `hamming74.py`：编码 + 伴随式译码 + 单比特纠错演示 | `gcc -O2 hamming74.c -o hamming74 && ./hamming74` / `python hamming74.py` |
| L15 密码 | Python | `otp_entropy.py`：一次性便笺的密钥量与冗余度实验，暴力破解英文密文估计 H(P\|C) | `python otp_entropy.py` |
| L16–L18 物理熵 | Python | `landauer_calc.py`：由 kT ln2 反推不同工艺（1 pJ/bit）距离热力学下限几个数量级，画功耗墙趋势 | `python landauer_calc.py` |
| 综合 | Python | `information_scavenger.py`：测量一段视频/音频/文本的实际冗余，估计其"可压缩上限" | `python information_scavenger.py` |

约定：
- 依赖写入 `projects/requirements.txt`（numpy、matplotlib、zstandard、lz4）；
- 每个脚本顶部注释标明对应讲次与教材章节；
- **本轮不写代码、不编译**，由用户后续集中执行。
