# Codex 代码审查功能与 Skill

## 本地 Code Review Skill

当前环境中，严格意义上的 Code Review Skill 只有一个：`skill-code-review`。

配置文件：`/Users/ibqo/.agents/skills/ctxr-skill-code-review/SKILL.md`

主要能力：

- 审查两个 Git ref 之间的 diff，或使用 `--full` 审查整个代码库。
- 支持 `standard`、`thorough` 两种审查深度。
- 可以按目录、语言、框架、严重程度、发布门禁和 reviewer 限定范围。
- 自动并行调度专项审查代理。
- 生成固定格式的审查报告和可审计的 `manifest.json`。
- 内含 58 组专项 reviewer。

专项 reviewer 主要覆盖：

- 正确性、并发、内存与性能。
- 安全、注入、密钥、加密、IAM 与隐私。
- 数据库、迁移、缓存、搜索和消息系统。
- 架构、领域驱动设计、事件驱动与设计模式。
- Web、移动端、无障碍和国际化。
- 测试、依赖、构建、容器和持续集成。
- 文档、代码规范和未使用代码。
- 大语言模型、Prompt 与工具调用。

在 Codex TUI 中可以通过 `/skills` 选择，或者直接输入：

```text
$skill-code-review 深度审查 main 到 HEAD 的变化
```

## Codex 内置代码审查

以下属于 Codex 的内置功能或平台集成，不是 Skill：

- `/review`：启动内置审查代理，可以审查未提交修改、指定 commit，或者当前分支与基准分支的差异。默认只报告问题，不修改工作树。
- `codex review`：通过命令行执行非交互式代码审查。
- `@codex review`：在 GitHub Pull Request 评论中触发 Codex 审查。

OpenAI 官方说明：[Code review](https://learn.chatgpt.com/docs/code-review)

## 如何选择

- 未提交修改或快速检查：使用 `/review`。
- 合并前严格审查，需要并行专项 reviewer 和审计报告：使用 `skill-code-review`。
- GitHub Pull Request 自动审查：使用 `@codex review`。
