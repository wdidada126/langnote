# L22 哲学与 AI 伦理：图灵测试、意识与 AI Safety

> 对应 AIMA Ch.26-27（历史与哲学/伦理）+ Klein 结课讨论。无公式，但给全课"为什么"收尾。

## 1. 核心概念

- **图灵测试（1950）**："机器能思考吗"不可操作 → 换成"模仿游戏能否骗过裁判"；
  - 中文房间（Searle 1980）反驳：句法 ≠ 语义（符号操纵无理解）；
  - 当代变体：LLM 通过聊天测试 ⟹ 测试从"能力判据"退化为"表现判据"——引发"理解 vs 模拟理解"的再辩论（Chomster/Steedly 等 2023 往返）。
- **强 AI / 弱 AI / AGI**：工具智能（窄域）vs 通用智能；当前 LLM 处于哪一格是开放问题。
- **意识的难问题**（Chalmers）：功能解释 vs 现象体验；AI 福利（model welfare）成为新兴研究领域。
- **AI 安全（本课程定义的"理性 agent"视角）**：
  - **规格问题（specification）**：MEU 的 U 写错 → 奖励黑客/回形针 maximizer（Bostrom）；L12 的 R 设计在真实世界是头号风险源。
  - **控制问题（control）**：能力超过人类监督后如何保持纠错权（scalable oversight，弱-to-strong 泛化 2023）。
  - **对齐（alignment）**：RLHF/ Constitutional AI = 把 L15-L16 的效用/信息框架反向用于训练目标本身。
- **伦理与社会**：算法偏见（训练数据分布 × L11 MLE 放大歧视）、可解释性（BN/L10 的可解释 vs 深度网络黑箱）、就业与再分配、深度伪造与信息生态、隐私（VoI 视角下的数据收集边界）。

## 2. 关键论证（结构化整理）

```
图灵测试 → 行为主义判据     中文房间 → 句法不充分
规则伦理 vs 后果伦理        ↔  L15 效用主义 = 后果论的数学化
对齐三难：不可完全指定 U / 可优化 / 可控，三者最多取二
```

## 3. 直觉例子

- 推荐系统局部效用（点击率）≠ 全球效用（用户福祉）→ 标题党 = 教科书级 reward hacking（L12 的 R 设计失误）。
- LLM"拒绝回答"是 RLHF 后验分布偏移（L11/L19 的判别面）——伦理约束可追溯到本课全部技术机制，本讲因此成为"总复习的应用场"。

## 4. 前后讲联系

- 全课终点回扣 L01：理性 agent 框架的隐含假设（度量可定义、环境可建模、计算无限）在哲学与现实层逐条被审视。
- 技术挂钩：L12（奖励设计）、L15（效用公理）、L16（信息价值→隐私）、L19-20（偏见与黑箱）、L21（多智能体安全）。

## 5. 跨课程联系

- **CS229/CS231n**：模型卡/数据集卡、公平性度量（equalized odds）是工程落地物。
- **MIT6.824**：安全（safety）与容错（fault tolerance）对比——恶意智能体 vs 故障节点。
- **DDCA**：硬件侧伦理（稀土/能耗/算力正义）；侧信道攻击让"模型保密"成物理问题。
- 通识：哲学课 (心智哲学)、科技伦理、法学（AI 法案）接口课。

## 6. 开源项目应用

- **Model Cards for Model Reporting（ Mitchell 2019）+ huggingface model-card 模板**；**Foolmap**。
- **EleutherAI lm-evaluation-harness / HELM**：能力与偏见的标准化评测。
- **Constitutional AI（llama 系 open 实现）、TRL/OpenRLHF**：对齐训练开源栈。
- **AI 安全红队**：promptfoo/guardrails 类工具。

## 7. 延伸阅读

- AIMA 4e Ch.26-27（4e 新增伦理章）；Turing "Computing Machinery and Intelligence" (1950)；Searle "Minds, Brains, and Programs" (1980)。
- Russell《Human Compatible》(2019)；Bender 等"On the Dangers of Stochastic Parrots" (2021)；Ng 等更平衡的争议回应（2023）。
