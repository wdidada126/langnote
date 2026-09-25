# MIT Missing Semester — 论文与工程实践对照（骨架）

> 本课程偏工程工具，"经典论文"取工具/系统领域与课程内容直接相关的奠基文献。

## 一、经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| The UNIX Time-Sharing System（Ritchie & Thompson） | 1974 | 确立 Unix 哲学：小工具、组合、一切皆文件，是现代 shell 的源头 | L1/L2 |
| An Introduction to Programming Language Design（或 Unix 管道前身： Pipes and Filters 相关文献） | 1960s-70s | 管道-过滤器模型，`cmd1 | cmd2` 组合思想的来源 | L1 |
| gprof: A Call Graph Execution Profiler（Graham et al.） | 1982 | 经典采样式性能分析器，"先测量再优化"的方法论原型 | L4 |
| Git 官方设计文档（不是论文，视作一手资料） | 2005 | 内容寻址快照模型，解释 Git 一切命令的心智基础 | L5 |
| Why Programs Fail（Zeller，专著） | 2009 | 系统化调试方法论：观察-假设-最小化复现 | L4 |
| GNU Make Manual（免费手册，视作一手资料） | 1990s | 增量构建与依赖图，L6 打包发布的基础 | L6 |

## 二、近 5 年论文（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Evaluating Large Language Models Trained on Code（Codex/HumanEval） | 2021 | 证明模型可端到端生成可用代码，开启 AI 结对编程时代 | L7 |
| SWE-bench: Can Language Models Resolve Real-World GitHub Issues? | 2023 | 以真实仓库 issue+PR 为基准评测编码代理，定义 agentic coding 评测范式 | L7/L8 |
| Large Language Models are Zero-Shot Reasoners / Chain-of-Thought 系列 | 2022 | 提示技术演进，直接指导与编码代理的交互方式 | L7 |
| MetaGPT / Generative Agents（多智能体软件工程） | 2023 | 用角色扮演多代理流水线模拟软件团队工作流 | L7/L6 |

## 三、知识点在开源项目中的应用

| 课程知识点 | 开源项目案例 | 说明 |
| --- | --- | --- |
| Shell 脚本 + 管道 | Neovim 插件生态、`dotfiles` 万星仓库（如 mathiasbynens/dotfiles） | 用 shell 组合小工具定制环境 |
| tmux/ssh 工作流 | GitHub Codespaces、tmux 插件 tpnpm/tmux | 远程开发会话保持 |
| Git 进阶（bisect/rebase） | Linux 内核、Git 自身协作流程 | 邮件列表 + 严格 rebase 工作流 |
| 打包与 CI | GitHub Actions 市场、pypa/pipx | Python 工具发布与自动化安装 |
| 调试与 profiling | py-spy、perf、bpftrace | 现代采样分析器实践 L4 概念 |
| Agentic Coding | OpenAI Codex CLI、Aider、OpenHands | L7 的直接工程化身 |
