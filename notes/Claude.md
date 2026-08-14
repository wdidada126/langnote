# Claude

Claude由OpenAI前副总裁离职创立的和chatGPT对位的AI机器人，号称是chatGPT一生的对手！目前已开放测试申请入口，不过要排队等待。据网上了解，有可能是申请人数过多，很多人等了几天毫无反应。

https://zhuanlan.zhihu.com/p/621460269

slack，add apps中搜索Claude，“add to Slack”按钮是灰色的
Unfortunately, Claude is only available in certain regions right now. Please

Claude在slack中也被限制了，只能特定地区能访问，大陆ip不能直接访问了

https://www.anthropic.com/claude-in-slack

Switched to Claude 3 HaikuDue to high demand, Claude 3.5Sonnet is temporarily unavailable forfree plans. Claude 3 Haiku is fasterbut may provide less detailedresponses.

## Claude Fable 5（截至 2026-08）

### 定位与更正

Claude 是 Anthropic 的模型与产品系列，不是一个由 OpenAI 直接创建的机器人。Anthropic 的创始团队中包含前 OpenAI 员工；上面的早期记录可作为当时的使用见闻，但不应把 Claude 的公司归属写成 OpenAI。

Claude Fable 5 是 Anthropic 于 2026-06-09 发布、面向公开客户的高能力模型，API 模型标识为 `claude-fable-5`。官方将它定位为高难度推理和长周期 Agent 工作模型：适合把复杂目标拆成多个阶段、调用工具、持续检查进度并完成异步任务。它不意味着“一次 API 调用可以无限运行”；长任务的状态持久化、工具权限、预算、超时、人工审批和恢复仍由调用方的 Agent harness 负责。

| 项目 | 公开信息 |
| --- | --- |
| 可用性 | Claude API、Amazon Bedrock、Claude Platform on AWS、Google Cloud、Microsoft Foundry 已公开提供；具体区域、配额和准入条件以云平台控制台为准。 |
| 上下文与输出 | 默认 1M token 上下文，单次请求最多 128k token 输出。 |
| 输入输出 | 支持文本、图像、PDF 输入，输出为文本；可结合视觉、代码执行、工具调用、记忆和上下文压缩能力构建 Agent。 |
| 推理控制 | adaptive thinking 始终启用，不能通过 `thinking: {"type": "disabled"}` 关闭；通过 `effort` 控制思考深度和成本。原始 chain of thought 不返回，`thinking.display` 只能返回可读摘要或省略。 |
| 数据边界 | Fable 5 属于 Covered Model，官方说明具有 30 天数据保留要求，不能按 zero data retention 使用。涉及生产数据、源代码、个人信息或受监管数据时，先完成数据分类和平台合规审查。 |

与仅限批准客户的 Claude Mythos 5 相比，Fable 5 具有相同能力档位，但加入了安全分类器，因此整合方必须处理“拒绝”和 fallback。不要把这一点误解为模型故障或服务不可用。

### 拒绝、fallback 与 DLQ 的关系

Fable 5 的安全分类器拒绝请求时，Messages API 返回的是成功 HTTP 响应，并使用 `stop_reason: "refusal"` 标识；响应中还会给出触发拒绝的分类器信息。这与网络超时、429 限流、5xx、工具执行失败是不同类别，处理策略也不同。

| 情况 | 推荐动作 | 不应做什么 |
| --- | --- | --- |
| `stop_reason: "refusal"` | 记录请求分类与 trace；确认任务是否允许切换到其他模型；使用服务端、SDK 或业务侧 fallback。 | 对同一模型、同一提示词无上限重试，或试图通过改写绕过安全限制。 |
| 429、网络抖动、短暂 5xx | 有上限的指数退避与抖动；遵守平台配额和调用超时。 | 立即并发重试，放大限流和成本。 |
| 工具调用失败 | 记录工具输入输出、错误码和可重试性；修复权限、参数或依赖后从检查点继续。 | 把工具异常误判成模型拒绝。 |
| Agent 任务多次失败或需要人工判断 | 写入任务失败队列，保留任务状态、上下文引用、工具日志和重试记录；人工修复或批准后受控恢复。 | 直接无限重启整段 Agent，或把上下文丢弃后无法复现。 |

Fable 5 的 fallback **不是 DLQ**：前者是单次模型请求被拒绝后的同步模型路由，目标是继续完成可安全处理的请求；后者是异步任务经过有限重试仍失败后的持久化隔离与人工处置。两者可以组合：Agent 的某一模型调用被拒绝时先做合规 fallback；整个任务仍无法完成、或工具副作用处于不确定状态时，才进入类似 DLQ 的失败任务队列。

```text
提交 Agent 任务
    -> 调用 Fable 5
       -> 正常输出 / 工具调用成功：写检查点，继续下一步
       -> refusal：按策略 fallback 到允许的模型，记录模型路由
       -> 临时 API 故障：有限退避重试
       -> 工具或业务步骤失败：从检查点有限重试
       -> 超过任务预算、重试阈值或需要人工授权：任务 DLQ
任务 DLQ -> 聚合错误 -> 人工修复/审批 -> 限速恢复或终止并审计
```

### Agent 工程实践

1. 以任务状态机而非单次对话实现长任务。至少保存 `task_id`、目标、当前阶段、输入版本、模型版本、工具调用、检查点、预算、操作者和最终状态；不要依赖聊天窗口保留全部执行状态。
2. 明确工具最小权限。只读检索、代码修改、执行命令、访问生产系统、对外发送和资金/数据写入应是不同权限级别；高风险副作用需要人工批准点和可撤销/补偿路径。
3. 为模型和工具分别设预算。限制总 token、最大轮次、最长墙钟时间、单工具超时、并发数和最大重试次数；达到预算时暂停并把可恢复状态交给人工，而不是默默截断任务。
4. 用真实任务做评测。关注成功率、人工接管率、工具失败率、拒绝率、端到端时延、token/工具成本、代码测试通过率和副作用错误率，而不是只比较一次性问答效果。
5. 区分“可重试”和“需要变更”。缺少凭据、权限拒绝、输入不完整、外部系统非幂等、需求矛盾、策略拒绝通常不会因原样重试而解决；应转为补充输入、调整权限、走 fallback 或进入任务 DLQ。

### 最小处理伪代码

```text
result = call_model(model="claude-fable-5", task, checkpoint)

if result.stop_reason == "refusal":
    audit_refusal(task, result.classifier, trace_id)
    return call_allowed_fallback_or_escalate(task, checkpoint)
if result.is_transient_api_error:
    return retry_with_backoff_within_budget(task, checkpoint)
if result.tool_failed:
    return retry_from_checkpoint_or_escalate(task, checkpoint)
if task.exhausted_budget or task.requires_human_approval:
    return move_to_task_dlq(task, checkpoint, result.logs)
return persist_checkpoint_and_continue(task, result)
```

这里的 `call_allowed_fallback_or_escalate` 必须由业务策略决定。fallback 模型也可能在能力、可用区域、数据保留、工具支持和安全策略上不同，不能为了“任务必须完成”而默认将敏感请求路由到未经批准的平台或模型。

### 参考资料

- Anthropic：Fable 5、Mythos 5、拒绝、fallback、计费、推理与支持功能说明：<https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5>
- Google Cloud：模型 ID、输入输出、token 上限、数据保留、能力与可用性：<https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude/fable-5>
- AWS：长周期 Agent、异步任务和 Bedrock 可用性说明：<https://www.aboutamazon.com/news/aws/claude-fable-5-anthropic-available-amazon-bedrock>
