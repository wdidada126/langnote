# MIT Missing Semester（IAP 2026）— 笔记大纲（骨架）

## L1 课程概览与 Shell 入门
- 课程定位：大学课堂不教但对 CSer 至关重要的工程技能。
- shell 是什么：命令解释器；常见 shell（bash/zsh/fish）与终端模拟器的区别。
- 基本 shell 语法：路径、`$PATH`、权限位、glob 通配符。
- shell 编程：变量、引号、花括号展开、命令替换、函数与脚本参数。
- 要点：能用 `for/while` + 管道完成一次批量文件处理。

## L2 命令行环境
- job control：前台/后台、`Ctrl-Z`、`fg/bg`、挂起与恢复。
- 进程视图：`ps`、`htop`、信号（`kill -9` 与 `kill -15` 的区别）。
- 终端复用：tmux 的 session/window/pane 三层模型。
- ssh 基础：远程登录、密钥认证、端口转发概念。
- Dotfiles：用版本控制管理个人配置的思路。

## L3 开发环境与工具
- 编辑器谱系：Vim（模式编辑）与 Emacs 的哲学差异。
- Vim 最小可用集：移动、插入、可视模式、查找替换、宏。
- shell 效率：补全、历史、快捷键、prompt 定制。
- 工具选型：`fzf`、`ripgrep`、`jq` 等现代 CLI 工具。

## L4 调试与性能分析
- 调试器：pdb/lldb/gdb 的断点、单步、栈帧检查。
- 系统化调试：最小复现、假设-验证、二分定位（git bisect 预告）。
- 性能分析：profiler 的概念（采样 vs 插桩）、先测量后优化。
- `strace`/系统调用追踪定位"程序卡在哪"。
- 日志（logging）优于 print 的原则。

## L5 版本控制与 Git
- 分布式模型：工作区/暂存区/HEAD 三棵树。
- 日常命令：`add/commit/branch/merge/log/diff`。
- 进阶：`rebase`、`stash`、`bisect`、`cherry-pick`。
- 多人协作：远程、PR、冲突解决；`.gitignore`。
- 心智模型：Git 是内容寻址的文件系统快照。

## L6 代码打包与发布
- Python 生态打包：venv、requirements、`pyproject.toml`。
- 通用构建：Makefile 最小示例；CI（GitHub Actions）概念。
- 可复现环境：锁文件与依赖固定。
- 从"能跑"到"别人也能跑"：README、许可证、版本号。

## L7 代理式编程（2026 新增）
- AI 编码代理（Copilot/agent CLI）的工作方式与能力边界。
- 提示词与上下文管理：仓库级上下文、任务拆分。
- 人机协作流程：代理写码 + 人审查 + 测试兜底。
- 与本课程其他工具的结合：git diff 审查代理改动。

## L8 代码之外
- 工程协作：代码评审文化、提交信息规范。
- 文档与沟通：README/CHANGELOG/设计文档的最小集。
- 自动化哲学：重复三次就脚本化（cron、pre-commit）。
- 数据安全：备份、误删恢复思路。

## L9 代码质量
- 风格与静态检查：linter/formatter（ruff、black、shellcheck）。
- 测试金字塔：单测为主、Mock 的适用边界。
- 覆盖率与 CI 门禁的组合拳。
- 重构信号：坏味道识别与最小化改动。
