# CS142 逐讲要点（骨架）

## L01 Web 与 HTTP
- Web=应用层协议之上的文档超图；URL/方法/头/状态码四要素。
- 无状态 HTTP 与会话需求的矛盾（为 L11 埋点）。
- DevTools Network 面板读请求。

## L02 HTML/CSS
- 语义化结构 + 盒模型 + Flex/Grid。
- 响应式与媒体查询。
- 浏览器渲染流程：解析→布局→绘制→合成。

## L03 JavaScript 深入
- 词法作用域、闭包、this 绑定规则。
- 事件循环：宏/微任务与异步骨架。
- 模块系统（ESM vs 打包）。

## L04 DOM 与数据获取
- DOM API 与事件委托。
- Fetch/Promise；JSON 作为通用交换格式。
- 从"页面"到"应用"：不刷新更新视图。

## L05 前端工程化
- npm 依赖管理与锁文件；构建（打包/转译/压缩）。
- 源码映射与调试。
- lint/格式化工程基线。

## L06 React
- 声明式 UI 与组件模型；单向数据流。
- JSX 本质 createElement；props 组合。
- Hooks：useState/useEffect 心智模型。

## L07 React 进阶
- 列表 key、受控表单、提升状态。
- Router 与代码分割；Context 管理跨层状态。
- 组件测试（Testing Library）。

## L08 Node/Express
- 事件驱动单线程服务器模型。
- Express 中间件洋葱圈；模板与静态资源。
- MVC 分层与项目结构。

## L09 REST API
- 资源建模、URI/方法/状态码约定。
- 表示（JSON schema）与版本化；分页/过滤。
- 契约测试与文档（OpenAPI）。

## L10 数据库
- 关系模型与 SQL（PostgreSQL）；事务与约束。
- ORM 与迁移（数据不丢失的演进）。
- 索引与 N+1 查询优化。

## L11 认证与安全
- cookie/session 服务端态 vs JWT 自包含态。
- 三大漏洞实操：XSS/CSRF/SQL 注入及防御。
- 密码存储（bcrypt/argon2）与 HTTPS/TLS。

## L12 性能与部署
- 前端性能：瀑布流、懒加载、缓存头、bundle 分析。
- 服务端：反向代理、负载均衡、读写分离初步。
- 上线流程：环境变量、日志、健康检查。
