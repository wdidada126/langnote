# Full Stack Open 论文与应用清单

## 1. 经典文献/规范

| 文献 | 年份 | 主题 | 关联 |
| --- | --- | --- | --- |
| Fielding REST 论文 | 2000 | API 风格 | P3 |
| Facebook GraphQL 规范与博客 | 2015 | 查询语言 | P8 |
| Redux（Dan Abramov 提出，flux 谱系）技术文 | 2015 | 可预测状态容器 | P6/P11 |
| React 协调（Reconciliation）官方设计文档 | 2013-17 | 虚拟 DOM | P1-P7 |
| MongoDB Data Model 指南 | 2014+ | 文档建模 | P4 |
| The Twelve-Factor App | 2012 | 应用部署方法论 | P12-P13 |
| Docker/OCI 容器规范 | 2013-15 | 容器 | P13 |
| SQL-92/RFC 7519/OWASP（同 CS142 清单，作为复习） | — | DB/认证/安全 | P5/P9 |

## 2. 近 5 年（2021-2026）

| 文献/技术 | 年份 | 方向 | 关联 |
| --- | --- | --- | --- |
| React Server Components 与"服务器状态"讨论（TanStack Query 生态） | 2021-2023 | 状态管理前沿 | P11 |
| TypeScript 5.x 装饰器/const 类型参数规范摘要 | 2023-2024 | 类型系统 | P9 |
| CI/CD-as-Code：GitHub Actions 最佳实践白皮书 | 2021-2024 | 流水线 | P12 |
| Supabase/Neon 等 Serverless Postgres 技术报告 | 2021-2024 | 数据层 | P14 |
| Expo SDK 新架构（Fabric/Turpan? 准确：React Native New Architecture 官方 RFC） | 2023-2024 | 移动端 | P10 |

## 3. 知识点在开源项目中的应用

| 知识点 | 开源项目 | 体现 |
| --- | --- | --- |
| React Hooks/路由 | React Router、TanStack Query | 标准生态 |
| Express/Mongoose | Strapi、Keystone | Node CMS/后台 |
| GraphQL | Apollo Server/Client、Hasura | P8 生产形态 |
| Redux Toolkit | React-Redux 官方示例生态 | 大厂后台常用 |
| TypeScript | 全站 TS 化开源（VS Code 本体即 TS 最大案例） | 工程基线 |
| Docker/compose | 各 OSS 仓库（Superset/n8n 等） | P13 实操模板 |
| GitHub Actions | 任意主流 OSS 的 CI 配置 | P12 临摹对象 |
| Prisma+PostgreSQL | Cal.com、Typeform 开源栈 | 现代关系栈范例 |
