# LlamaIndex

llamaindex适合rag，langchain适合agent
玩多模态
idea插件
用云资源

`llamaindex` 和 `langchain` 是两个不同的工具，它们在构建和管理大型语言模型（LLMs）驱动的应用程序中扮演着不同的角色。

**LlamaIndex** 是一个用于构建和管理知识库的工具，它可以帮助开发者创建、查询和管理文档的索引。LlamaIndex 通常与检索增强的生成（Retrieval-Augmented Generation，简称 RAG）模型一起使用，这种模型结合了检索和生成技术，以提供更准确和相关的信息。在RAG模型中，LlamaIndex 可以用来检索与用户查询相关的文档片段，然后将这些片段作为上下文提供给生成模型，以生成更准确的回答。

**LangChain** 则是一个用于构建和部署由LLMs驱动的代理（agents）的框架。LangChain 提供了构建模块、组件和第三方集成，用于开发复杂的LLM应用程序。LangChain 的一个关键特性是它允许开发者创建有状态的代理，这些代理可以记住之前的交互并据此做出决策。LangChain 也支持将代理部署为REST API，以便可以轻松地将它们集成到其他应用程序中。

因此，可以认为 `llamaindex` 更适合用于RAG模型，因为它专注于文档索引和检索，而 `langchain` 更适合用于构建代理，因为它提供了构建有状态代理和部署API的能力。

