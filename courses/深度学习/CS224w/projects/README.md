# CS224w 配套项目计划

> 对齐 6 个编程作业 + 3 个书面作业（LaTeX）结构；Python (PyG/DGL) 为主，书面作业以 LaTeX 报告形式产出。本轮只写不编译。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L2 节点嵌入 | Python (numpy) | 手写 DeepWalk+skip-gram，Cora 上可视化/链路预测 | `python emb/deepwalk.py --corpus karate` |
| L3-L4 MPNN/GCN | Python (PyG) | 手写消息传递层（禁用现成 GCNConv）+ 半监督分类 | `python gcn/main.py --dataset citeseer` |
| L5 自监督 | Python (PyG) | DGI 预训练 + 线性探针评测 | `python dgi/train.py` |
| L6 GAT | Python (PyG) | GAT 复现与注意力权重可视化 | `python gat/explain.py` |
| L7 表达力 | Python | WL 测试小实验：GIN vs GCN 区分同构对 | `python expressivity/wl_demo.py` |
| L8 链接预测 | Python (PyG) | GAE 链路预测 + OGB Hits@K | `python gae/train.py --dataset ogbl-collab` |
| L9-L10 图分类与 scaling | Python (PyG) | 分子属性预测（MoleculeNet），采样训练消融 | `python molprop/train.py --sample size` |
| L11-L12 pooling/几何 | Python (PyG) | DiffPool vs mean-readout 对比；简单等变层 | `python diffpool/main.py` |
| L13 图生成 | Python (PyG) | 小 GraphRNN 生成环状分子 toy | `python graphgen/sample.py` |
| L14 评估 | Python | 随机 split vs 时间 split 泄露对比报告（LaTeX） | `make -C report_pdf/` |
| 期末项目 | Python | 自选：GraphRAG 问答 / 分子生成 复现 | `bash final_project/run_all.sh` |
