# Full Stack Open 逐部分要点（骨架）

## P0 Web 基础
- 浏览器-服务器请求往返与 DevTools Network 视角。
- HTML/CSS/JS 分工与页面事件。
- 工具链：node/npm、Git 工作流。

## P1 React 入门
- 组件树与 props 向下流动；state 向上提升。
- 列表渲染与 key；事件处理函数。
- 不依赖后端的纯前端应用（phonebook 雏形）。

## P2 服务端通信与样式
- useEffect + fetch/axios 的异步数据获取。
- 表单受控组件与校验。
- CSS 模块/内联/Bootstrap 方案对比。

## P3 Node/Express
- 从 fs 到 http：手写服务器理解抽象。
- Express 路由、中间件、错误处理。
- REST API：URL/状态码/JSON 约定；代理与 CORS。

## P4 数据库与测试
- MongoDB 文档模型 + Mongoose schema/校验。
- 单元/集成测试（jest + supertest）。
- 环境管理（dotenv）、登录初探。

## P5 认证与 E2E
- token 认证流程：登录→存储→Authorization 头。
- 前端受保护视图与路由守卫。
- Cypress/Playwright E2E 测试方法论。

## P6 Redux
- 单向数据流 + reducer 纯函数；store/dispatch。
- redux-toolkit（createSlice）现代用法。
- 与 React 内置状态的选择边界。

## P7 进阶 React
- React Router：URL 即状态。
- 自定义 Hooks 复用逻辑；Context 替代层层 props。
- webpack/babel 构建心智（类组件仅史学）。

## P8 GraphQL
- schema/type/resolver；查询形状客户端决定。
- 与 REST 的取舍：N+1、批量、缓存（Apollo/urql）。

## P9 TypeScript
- 静态类型对 React/Express 全栈的意义。
- 泛型工具类型与 API 边界校验。

## P10 React Native
- Expo 工程结构与跨平台组件。
- 设备 API（相机/定位/传感器）与调试。

## P11 状态专题（Redux 进阶/查询库）
- 服务器状态 vs 客户端状态（React Query 思想）。
- 复杂应用的 reducer 设计模式。

## P12 CI/CD
- GitHub Actions 流水线：lint→test→build→deploy。
- 迁移策略与回滚；环境变量与密钥。

## P13 容器
- Dockerfile 与镜像分层；compose 编排应用+数据库。
- 云平台部署与日志监控（Betterstack 等）。

## P14 PostgreSQL/Prisma
- 关系建模 vs 文档建模；外键与联结查询。
- Prisma schema/迁移；多对多实践。

## P15 WebSockets/消息
- HTTP 之上长连接：ws/socket.io。
- 广播、房间与水平扩展（Redis pub/sub）。
