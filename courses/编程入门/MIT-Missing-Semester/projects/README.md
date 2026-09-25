# MIT Missing Semester — 配套项目计划（骨架）

> 本轮只列计划不写代码。原则：每讲结束立刻用一个小脚本/小工具固化该讲知识点，最终全部纳入自己的 dotfiles 仓库并用 Git+CI 管理。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L1 Shell | Bash | `bulk-rename.sh`：批量重命名/归档下载目录的脚本（glob + for 循环） | `chmod +x` 后直接 `./bulk-rename.sh` |
| L2 命令行环境 | Bash + tmux | 个人 tmux 配置（会话/窗格布局）+ 一键 ssh 别名集 | `tmux new -A -s work` |
| L3 开发环境 | Vimscript/Lua | 最小可用 Vim 配置：状态栏、搜索、宏录制练习集 | `vim` 加载 `~/.vimrc` |
| L4 调试与性能 | Python | 给一段故意写慢的代码写 pdb 调试记录 + cProfile/py-spy 报告 | `python -m cProfile target.py` |
| L5 Git | Git | 用 `git bisect` 定位一个模拟仓库中的 bug；写规范提交历史 | 纯 Git CLI |
| L6 打包发布 | Python + Make | 把 L1-L5 产物打包成可 `pipx install` 的 CLI 工具 + GitHub Actions 自动发布 | `make package` / Actions |
| L7 Agentic Coding | 任意 | 用编码代理完成前 6 讲某个任务，记录提示词与人审 diff 报告 | 代理 CLI + `git diff` |
| L8/L9 代码质量 | Python | 给整个 dotfiles 仓库加 ruff/black/pre-commit/CI 测试门禁 | `pre-commit run --all-files` |

## 验收清单
- [ ] 一个 Git 管理、CI 通过、README 完整的个人工具仓库（即本课程毕业项目）。
