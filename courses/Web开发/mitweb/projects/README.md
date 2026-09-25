# MIT WebLab 配套项目计划（本轮不写代码）

统一约定：JS/TS + Node（npm/pnpm 管理），每阶段项目独立仓库式目录；部署到免费托管平台；只写不编译，运行方式列出备查。

| 章节（讲次） | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L01-L03 | HTML/CSS | 个人主页：语义化 + Flex/Grid 响应式，GitHub Pages 上线 | 静态，`npx serve` |
| L04-L05 | JavaScript | 交互应用：TODO/天气 API 小站（fetch + DOM） | vite dev |
| L06 | Node/JS | 书签短链服务：Express 路由 + 内存存储 | `node server.js` |
| L07 | Node+Mongo/PG | 笔记站数据层：CRUD API + 索引优化报告 | docker-compose 起库 |
| L08 | Node+JS | 注册/登录：JWT + 密码哈希 + 受保护路由 | 同上 |
| L09 | React/JS | SPA 改造：把笔记站迁到 React + Router | vite build |
| L10 综合 | 全栈 | 迷你视频站（仿 weblab 结课项目）：上传/播放/评论/部署+HTTPS | Vercel/Render 部署脚本 |
