# CS571 论文与应用清单

## 1. 经典文献/技术资料

| 文献/资料 | 年份 | 主题 | 关联 |
| --- | --- | --- | --- |
| React 官方设计文档（Reconciliation/Hooks RFC #1586/#1508? 总称 RFC 档案） | 2013-2018 | 协调与 Hooks 机制 | W01-W04 |
| "The Reactive Programming" 谱系：Bacon.js/Franz? 更稳妥：Flux 应用架构（Facebook） | 2014 | 单向数据流 | W06 |
| React Navigation 设计文档 | 2017+ | RN 导航范式 | W09 |
| Material Design 规范 | 2014+ | 设计系统 | W07/W12 |
| Nielsen 十大可用性启发式 | 1994 | UX 原则 | W12 |
| Expo/React Native 架构论文性 RFC（Fabric/TurboModules/New Arch） | 2021-2022 | RN 新架构 | W10 |
| Reanimated 2/3 技术白皮书（software-mansion 博文） | 2020+ | 原生线程动画 | W10 |

## 2. 近 5 年（2021-2026）

| 文献/技术 | 年份 | 方向 | 关联 |
| --- | --- | --- | --- |
| React Server Components 官方 RFC 与文档 | 2022-2024 | 渲染模型（阅读对照） | W01-W06 |
| React 18 并发特性（useTransition/useDeferredValue 文档） | 2022 | 并发渲染 | W03/W08 |
| React 19 Actions/use() 新原语 | 2024-2025 | 数据获取范式 | W03/W11 |
| Expo Router（文件路由）发布文档 | 2023-2024 | RN 路由 | W09 |
| Dialogflow CX/Google Chat SDK 文档集 | 2021-2024 | 对话式 UI | W11 |
| 移动端 LLM 应用案例（on-device inference 集成指南） | 2024-2025 | AI×RN | W11/W12 |

## 3. 知识点在开源项目中的应用

| 知识点 | 开源项目 | 体现 |
| --- | --- | --- |
| Hooks/性能 | React DevTools、why-did-you-render | W04/W08 |
| Router | React Router v6/7、Expo Router | W05/W09 |
| 状态管理 | Redux Toolkit、Zustand、Jotai | W06 |
| 样式库 | MUI、Tamagui/NativeWind | W07 |
| 测试 | Jest、React Native Testing Library、Maestro | W08 |
| RN 生态 | Expo 仓库、react-navigation、Reanimated、React Native Paper | W09-W10 |
| 后端/认证 | Firebase、Supabase（RN SDK） | W11 |
| 对话 | Vercel AI SDK（streaming UI，对照 Dialogflow） | W11 |
