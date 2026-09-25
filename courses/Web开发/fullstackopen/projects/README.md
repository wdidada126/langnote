# Full Stack Open 配套项目计划（本轮不写代码）

统一约定：JS→TS 渐进；每个 part 的练习之外另立"个人作品集"线（与课程练习并行复用）；pnpm + docker-compose；只写不编译。

| 章节（part） | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| P0-P2 | JS | 课程主线：电话簿/国家信息站 | vite dev |
| P3-P4 | Node/JS | 博客后端：Express+MongoDB+supertest 全覆盖 | `node --watch` + compose |
| P5 | JS | 前端认证改造 + Playwright E2E 套件 | vite + playwright run |
| P6-P7 | JS | 商城 SPA：Router+Redux Toolkit+自定义 hook | vite |
| P8 | TS | GraphQL 版 Pokedex 客户端+服务端 | pnpm 双包 |
| P9 | TS | 把 P6 商城全栈迁移 TypeScript（含 zod 校验） | pnpm build |
| P10 | TS | React Native 记账 App（Expo，设备 API） | Expo（不编译，配置备查） |
| P11-P12 | TS | CI/CD：GitHub Actions 全流水线 + 分支保护 | 配置文件 |
| P13 | TS | Docker 化全栈 + 部署 Render/Fly 方案文档 | docker-compose 配置 |
| P14-P15 | TS | 终极大项目：团队协作任务板（PG+Prisma+WebSocket+通知） | monorepo(pnpm workspace) |
