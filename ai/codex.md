# codex

纯命令行环境，复制auth.json到合适的文件夹下，就可以codex，不用codex login

npm install -g @openai/codex
npm install -g @openai/codex@latest --registry=https://registry.npmmirror.com

codex进入之后，输入
/resume

• 在终端运行：
  codex resume
  会打开历史会话列表；用方向键选择目标会话，按 Enter 即可进入。

  也可以：
  codex resume --last
  直接恢复最近一次会话；或指定会话 ID：
  codex resume <session-id>

当前的 Codex 版本是 0.114.0 ，而最新版本是 0.145.0 （2026年7月21日发布）。版本差距太大，自我更新可能卡住了。

  Update available! 0.145.0 -> 0.146.0


 npm install -g @openai/codex@0.146.0 --registry=https://registry.npmmirror.com 2>&1

ibqo@ibqodeMacBook-Pro test_java_jraft % codex --version
codex-cli 0.146.0
ibqo@ibqodeMacBook-Pro test_java_jraft % 

关于 Codex 模型的 GPT-5.6 系列，你提到的 "medi hith xhigh" 应该是指模型的 "推理强度" (Reasoning Effort) 设置，而不是模型名称。Codex 5.6 系列的三个核心模型是 Sol、Terra 和 Luna，它们和不同的推理强度（如 `medium`, `high`, `xhigh`）是相互独立、可以组合使用的两个概念。

下面是模型与推理强度的详细区别：

### 三大核心模型：Sol、Terra 与 Luna

GPT-5.6 系列采用了新的命名体系，分为三个能力档位。可以按任务需求从这三者中选择：

| 模型 | 定位与特点 | 适用场景 | 价格（每百万Token） |
| :--- | :--- | :--- | :--- |
| Sol | 旗舰型号：能力最强，擅长处理最复杂的任务，但消耗资源也最多。Codex 的 Power 模式默认使用此模型并搭配 `medium` 推理强度。 | 复杂编程、架构设计、大型项目重构、深度研究等对结果质量要求极高的任务。 | 输入 $5 / 输出 $30 |
| Terra | 均衡主力：在能力、速度和成本之间取得了良好平衡，是日常开发的首选。 | 常规代码编写、Bug 修复、代码审查、自动化任务等大多数日常工作。 | 输入 $2.5 / 输出 $15 |
| Luna | 轻量高速：速度最快、成本最低，适合处理大量简单、重复性的任务。 | 文本提取与分类、格式转换、批量生成结构化内容、简单代码修改等。 | 输入 $1 / 输出 $6 |

### 推理强度 (Reasoning Effort)

除了选择模型，你还可以调整一个名为"推理强度"的参数，来控制模型在回答问题前"思考"的深度。这就是你提到的 `medium`、`high`、`xhigh` 这些选项。

*   作用：更高的推理强度会让模型花更多时间进行内部推演，从而提升处理复杂问题的能力，但响应速度会变慢，消耗的token也会更多。
*   建议：官方建议日常交互使用 `medium` 作为不错的平衡点。对于最难的任务，可以使用 `high` 或 `xhigh`。GPT-5.6 系列在 `xhigh` 之上还有一个最高的 `max` 级别。

简单来说，它们的组合逻辑是：
*   追求极致质量：Sol + High / xhigh / Max
*   日常主力使用：Terra + Medium / High
*   追求速度和低成本：Luna + Low / Medium

你在使用 Codex 时主要是处理什么类型的任务？如果告诉我你的具体使用场景，我可以给你更具体的模型和参数搭配建议。
