# LangChain

https://github.com/tmc/langchaingo

langchain最大问题是不支持中文

 在 LLM （大规模语言模型）应用开发领域，开源框架扮演着至关重要的角色，为广大开发者提供了强大的工具支持。作为这一领域的领军者，LangChain 凭借其创新设计和全面功能赢得了广泛赞誉。但与此同时，一些替代框架也应运而生，为不同场景下的需求提供了更优选择。

https://www.langchain.com/langchain

The largest community building the future of LLM apps
LangChain’s flexible abstractions and AI-first toolkit make it the #1 choice for developers when building with GenAI.

https://python.langchain.com/v0.2/docs/introduction/

LangChain is a framework for developing applications powered by large language models (LLMs).

LangChain simplifies every stage of the LLM application lifecycle:

Development: Build your applications using LangChain's open-source building blocks and components. Hit the ground running using third-party integrations and Templates.
Productionization: Use LangSmith to inspect, monitor and evaluate your chains, so that you can continuously optimize and deploy with confidence.
Deployment: Turn any chain into an API with LangServe.

https://github.com/langchain-ai/langchain
python的

LangChain是一个基于语言模型开发应用程序的框架，旨在帮助开发人员使用语言模型构建端到端的应用程序。它提供了一套工具、组件和接口，可简化创建由大型语言模型（LLM）和聊天模型提供支持的应用程序的过程。LangChain可以轻松管理与语言模型的交互，将多个组件链接在一起，并集成额外的资源，例如API和数据库。
要使用LangChain，开发人员需要导入必要的组件和工具，如LLMs、chat models、agents、chains和内存功能。这些组件组合起来创建一个可以理解、处理和响应用户输入的应用程序。LangChain为特定用例提供了多种组件，例如个人助理、文档问答、聊天机器人、查询表格数据、与API交互、提取、评估和汇总等。
LangChain还提供了一些用于向系统添加Memory的封装，其中ChatMessageHistory是成熟的Memory之一。Memory用于记录对话的上下文信息，并在需要时补充到用户的提问中去。例如，当用户输入一个问题时，系统首先从Memory中读取相关的上文信息（历史对话信息），然后组装成一个Prompt，调用大模型进行回答。大模型的回复会作为历史对话信息保存在Memory中，供之后的对话使用。
LangChain的应用案例广泛，可以用于医疗领域的语言翻译、商务交流中的跨国企业合作、旅游业中的旅游指南翻译、电子商务中的跨国电商平台翻译等场景。这些应用案例展示了LangChain在不同领域中的实用性和灵活性。
总的来说，LangChain是一个功能强大的框架，能够帮助开发人员更高效地构建基于语言模型的应用程序。通过提供丰富的组件和接口，LangChain简化了开发过程，并使得开发人员能够更轻松地实现各种复杂的语言处理任务。

## api

https://api.python.langchain.com/en/latest/langchain_api_reference.html

## blog
https://blog.langchain.dev/



在 LLM （大规模语言模型）开发和应用的热潮中，评估和权衡不同工具平台的优劣将是一个至关重要的环节。基于提示工程、数据集成、工作流程编排、调试可视化、评估指标、生产就绪性以及生态系统集成等七个关键维度进行全方位解析，无疑是一个极具前瞻性和系统性思路及方向。
接下来，我们一一具体展开分析:

1. Prompt Engineering - 提示工程
毫无疑问，高质量的提示工程是充分挖掘 LLM 潜能的前提和基石。理想的工具平台不仅应当提供简洁、灵活的提示构建界面，更应整合自然语言理解、语义解析等先进技术，实现提示的自动生成优化，最大限度贴合具体任务语境，减轻人工干预成本。
此外，对于复杂的多步骤任务，能否支持对提示进行参数化管理、版本控制也将是一项重要考量。
2. Data Retrieval and Integration - 数据检索和集成
RAG范式的兴起使得高效的外部知识库集成功能成为工具平台的必备能力。优秀的平台不仅应当能够轻松连接和导入各类异构数据源，更需具备强大的数据预处理和质量控制能力，确保知识注入的准确性和连贯性。除此之外，对海量检索结果的可视化分析和优化调优，也将大幅提升开发者的工作效率。
3. Model Orchestration and Chaining - 模型编排和链
面对现实世界中的复杂任务需求，单一的 LLM 通常很难独立完成。因此，能够灵活编排多个模型模块的工作流程，通过参数控制实现差异化组合，将成为工具平台的核心竞争力所在。
同时，对工作流程的版本管理、参数调优、可重复性等特性的良好支持，也将大幅提升开发效能。
4. Debugging and Observability - 调试和可观测性
LLM 系统作为一个典型的"黑箱"AI，其内部机理向来令人摸不透头绪。优秀的工具平台应当着力打破这一局限，通过诸如注意力分布可视化、推理路径追踪等手段，为模型内部状态提供洞见，同时，支持更精准的错误排查、偏差修正和性能优化，从而真正提升系统的可解释性和可信赖性。
5. Evaluation - 评估
严格的评估流程是确保 LLM 应用质量的关键一环。在这一点上，不同平台所提供的评估基础架构、涵盖的指标维度、自动化水平以及与人工评估的融合程度，将直接决定评估结果的客观性和权威性。
通常而言，一个成熟的评估体系，必将为最终产品的实际落地提供坚实的质量保证。
6. Deployment and Production-Readiness - 部署和生产就绪性
对于面向生产环境的工业级应用而言，工具平台的部署和运维能力将是一项核心考量。完善的上线机制、支持的部署选项(云端、边缘设备等)、安全合规、性能优化、监控告警等产品化保障，都将直接影响着 LLM 系统的最终可用性和可靠性。
7. Ecosystem and Integration - 生态系统和集成
作为前沿创新技术，LLM平台与现有企业技术栈的无缝集成是确保其广泛应用的前提。一个庞大的第三方应用商店和合作伙伴资源库，将有助于构建一个丰富的生态系统，覆盖更广泛的行业场景和差异化需求，从而推动LLM技术的大规模普及和创新应用。


Prompt Engineering - 提示工程
https://github.com/CatherineLiyuankun/prompt-engineering-for-developers

[论文阅读] Prompt Engineering综述
https://zhuanlan.zhihu.com/p/682352630

ChatGPT 上线至今，已经快 5 个月了，但是不少人还没真正掌握它的使用技巧。
其实，ChatGPT 的难点，在于 Prompt（提示词）的编写，OpenAI 创始人在今年 2 月时，在 Twitter 上说：「能够出色编写 Prompt 跟聊天机器人对话，是一项能令人惊艳的高杠杆技能」。
因为从 ChatGPT 发布之后，如何写好 Prompt 已经成为了一个分水岭。熟练掌握 Prompt 编写的人，能够很快让 ChatGPT 理解需求，并很好的执行任务。
目前你在网上看到的所有 AI 助理、智能翻译、角色扮演，本质上还是通过编写 Prompt 来实现。
只要你的 Prompt 写的足够好，ChatGPT 可以帮你快速完成很多工作，包括写爬虫脚本、金融数据分析、文案润色与翻译等等，并且这些工作还做的比一般人出色。
为了帮助大家能更好的掌握 Prompt 工程，DeepLearning.ai 创始人吴恩达与 OpenAI 开发者 Iza Fulford 联手推出了一门面向开发者的技术教程：《ChatGPT 提示工程》。

https://github.com/GitHubDaily/ChatGPT-Prompt-Engineering-for-Developers-in-Chinese