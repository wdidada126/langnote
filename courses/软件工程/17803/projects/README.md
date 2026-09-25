# 17-803 配套项目计划（骨架，本轮不写代码）

课程作业与期末项目未公开，自学替代方案是**"复现一篇实证论文 + 提出自己的研究设计"**。
主语言：R（统计建模主线，tidyverse + lme4/fixest）与 Python（数据获取与网络/文本分析），Markdown/LaTeX 写研究材料与报告。
约定：每个项目独立目录（`r01_xxx/` 或 `p01_xxx/`），含 `README.md`（研究问题-数据-方法-效度威胁）、`analysis.Rmd` 或 `notebook.ipynb`、`data/README.md`（数据来源与快照日期）与 `build.sh`（R 用 `Rscript -e "rmarkdown::render('analysis.Rmd')"`；Python 用 `python -m compileall` + `jupyter nbconvert --to html`）。本轮只写不编译。

| 章节（讲次） | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L1–L4 研究设计与综述 | Markdown/LaTeX | 一篇 EMSE 论文的拆解报告 + 迷你检索方案（检索式、纳入排除、PRISMA 草图） | `latexmk -pdf`（或 pandoc → html） |
| L5–L7 定性编码 | Python + 工具 | 用 20 条 Stack Overflow 回答做开放编码：写代码本（定义/正例/反例），双人编码算 Cohen's κ | `build.sh`: `python scripts/label.py --pairs 2 && Rscript kappa.R` |
| L8–L9 问卷设计 | Markdown + R | 设计 12 题"开发者工具使用"问卷 + 认知访谈记录；模拟一次响应偏差分析 | pandoc 生成问卷 PDF；`Rscript bias.R` |
| L10 描述统计与清洗 | R | 抓取一个仓库的提交历史，产出分布图/缺失报告与可复现清洗管线（tidyverse） | `Rscript -e "rmarkdown::render('clean.Rmd')"` |
| L11–L12 检验与功效 | R | 效应量表（Cohen's d / 比值比 / IRR）+ `pwr`/`simr` 做混合模型的模拟式功效分析 | `Rscript power.R --sims 2000`（输出表格） |
| L13–L14 回归建模 | R | 缺陷预测基线：OLS + 逻辑回归 + 负二项（计数提交/缺陷），含诊断图与稳健标准误 | `Rscript -e "rmarkdown::render('reg.Rmd')"` |
| L15 混合效应模型 | R | 开发者嵌套于项目的生产力模型：随机截距/斜率选择、ICC 报告、收敛诊断 | `Rscript lmer.R`（`lme4`/`fixest`，环境用 `renv` 锁定） |
| L16–L17 仓库挖掘 | Python + SQL | 用 GHTorrent/GH Archive/BigQuery 构一张"PR 周期时间"面板表：身份归并、窗口对齐、度量 lineage 文档 | `python -m compileall` + `sqlite3 < metrics.sql`；快照日期入库 |
| L18–L19 因果推断 | R 或 Python | 某工具/流程"上线前后"的效果评估：DID + 事件研究图 + 平衡性检验；再写一份"识别策略与威胁" | `Rscript did.R`（`fixest`/`MatchIt`）或 `python causal.py`（`DoWhy`） |
| L20 实验与预注册 | Markdown + R | 写一份预注册报告（研究问题/主分析/停止规则）+ 一个随机化脚本（可复现 seed） | pandoc → PDF；`Rscript randomize.R --seed 20260101` |
| L21 社交网络分析 | Python | 代码评审/共同修改网络：度/介数中心性、社区检测、同质性置换检验（NetworkX + igraph） | `python sna.py --perm 1000`（输出图与表格） |
| L22 文本与序列分析 | Python | PR 标题/评论的主题模型 vs 嵌入聚类对比；n-gram 序列分析提交流程 | `jupyter nbconvert --to html text.ipynb`（gensim/BERTopic） |
| L23 伦理与数据治理 | Markdown | 一份可提交的 IRB 材料包：知情同意模板、去标识方案、数据留存与共享计划 | pandoc → PDF；附 `checklist.md` |
| L24 复现与传播（期末） | R + Python | **复现一篇论文的一张主表/一张主图**：数据+代码+环境全部开源（Docker 或 renv/uv lock），写复现差异报告 | `./build.sh all`（拉数据 → 清洗 → 模型 → 图表），产出 `output/` 与 `REPRODUCE.md` |

> 建议数据集（免申请、可公开）：GitHub GH Archive / GHTorrent 快照、Software Heritage、Apache DevLake 示例仓库、公开 SE 基准数据集（Defects4J、SZZ 类缺陷标注数据）、Stack Overflow 年度开发者调查数据。
> 所有 `build.sh` 必须"只读源码 + 输出到 `output/`"，不改系统状态，便于后续集中验证与 artifact 评审。
