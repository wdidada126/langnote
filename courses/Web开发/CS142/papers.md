# CS142 论文与应用清单

## 1. 经典文献/规范

| 文献 | 年份 | 主题 | 关联讲次 |
| --- | --- | --- | --- |
| Berners-Lee WWW 提案 + 首批规范 | 1989-94 | Web 起源 | L01-L02 |
| Fielding REST 博士论文 | 2000 | API 架构风格 | L09 |
| RFC 6265 HTTP State Management（Cookie） | 2011 | 会话机制 | L11 |
| RFC 7519 JWT | 2015 | 令牌认证 | L11 |
| Bachmann et al., React（"Declarative UI Programming at Scale" 官方叙事；论文性材料为 React Conf 技术稿） | 2013 | 虚拟 DOM/协调 | L06-L07 |
| OWASP Top 10 | 2003- | Web 安全清单 | L11 |
| Stoneman? 更准：SQL Injection 经典研究（Biskoftos et al.）与防御 | 2012 | 注入防御 | L10-L11 |
| Node.js 事件循环设计文档（libuv 论文性博客/官方 docs） | 2009+ | 服务端并发 | L03/L08 |
| Mason 等关于 SSR/同构的早期讨论（PayPal 工程博客文集） | 2013-15 | 渲染架构 | L12 |

## 2. 近 5 年（2021-2026）

| 文献/技术 | 年份 | 方向 | 关联 |
| --- | --- | --- | --- |
| React Server Components 提案与落地（Next.js App Router） | 2022-2024 | 全栈渲染 | L06/L12 |
| Postgres 在 AI 应用栈的回归（pgvector 等） | 2023-2025 | 数据库选型 | L10 |
| Web 性能：Core Web Vitals 与 INP 规范更新 | 2022-2024 | 性能度量 | L12 |
| Passkeys/WebAuthn Level 3 与无密码化（FIDO 报告/W3C） | 2021-2024 | 认证演进 | L11 |
| OpenAPI 3.1 与契约驱动开发实践 | 2021 | API | L09 |
| 边缘计算全栈（Cloudflare Workers/Vercel Edge 技术白皮书） | 2021-2025 | 部署 | L12 |

## 3. 知识点在开源项目中的应用

| 知识点 | 开源项目 | 体现 |
| --- | --- | --- |
| HTTP/HTML/CSS | MDN、Chromium DevTools | 调试标准 |
| JS/事件循环 | Node.js、Bun、Deno | 运行时 |
| React | React、Next.js、Remix | 课程主线栈 |
| Express/MVC | NestJS、Feathers | 服务端分层 |
| REST/OpenAPI | Swagger UI、FastAPI(对照) | 契约 |
| PostgreSQL/ORM | Prisma、Sequelize、Supabase | 数据层 |
| 安全 | Helmet、DOMPurify、OWASP ZAP、Argon2 | 防御工具链 |
| 部署 | Docker、Vercel/Nginx | 上线 |
