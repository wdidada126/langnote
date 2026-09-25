# CS142 配套项目计划（本轮不写代码）

统一约定：对齐官方 8 个 Project 的滚动式大应用（照片社交站 "PhotoApp" 风格），JS/TS + React + Express + PostgreSQL；只写不编译，运行方式列出备查。

| 章节（讲次） | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L01-L02 | HTML/CSS | P1a 静态多页站点 + 响应式评分页 | 静态 `npx serve` |
| L03-L04 | JavaScript | P1b 单页交互：DOM 相册 + fetch JSON 假数据 | vite |
| L05 | TS | 工具链项目：ESLint/Prettier/tsconfig 基线模板（复用全课程） | pnpm scripts |
| L06-L07 | React/TS | P2 前端应用：路由/表单/上传 UI/组件测试 | vite + vitest |
| L08-L09 | Node/TS | P3 后端：Express REST API + OpenAPI 契约 + 集成测试（Jest） | `tsx watch` |
| L10 | Node+PG | P4 数据层：Sequelize/Prisma 迁移 + 索引优化（慢查询报告） | docker compose + PG |
| L11 | 全栈 | P5 认证：session 或 JWT 登录、好友权限模型、安全自检清单 | 同上 |
| L12 | 全栈 | P6 上线：Docker 化、Nginx+HTTPS、Lighthouse 性能优化前后对比 | docker build/仅配置 |
| 综合 | 全栈 | P7-P8 团队协作扩展（评论/标签/搜索/推荐）与压测报告 | pnpm monorepo |
