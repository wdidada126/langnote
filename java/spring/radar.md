# radar

Radar 是国内目前最主流、最容易上手的 Java 开源实时风控/反欺诈引擎，专为金融、支付、电商等场景设计，核心优势是 可视化配置 + Groovy 动态规则 + 毫秒级响应，开箱即用。


### 一、基本信息
- 定位：轻量级、实时反欺诈、规则引擎
- 语言/栈：Java + Spring Boot + MyBatis + MongoDB + Groovy + Redis + Elasticsearch
- 作者：wfh45678（GitHub）
- 开源地址
  - GitHub：https://github.com/wfh45678/radar
  - Gitee：https://gitee.com/freshday/radar
- 适用场景
  - 交易风控、支付反欺诈、盗卡/盗号
  - 注册/登录安全、营销防刷
  - 信贷申请、额度风控、账户异常

### 二、核心架构（分层）
- API 层：提供 HTTP 风控接口（客户端/网关接入）
- 风控引擎（核心）
  - 规则解析（Groovy 动态脚本）
  - 指标计算、时间窗口、频次统计
  - 决策引擎：通过/拒绝/人工审核/加验
- 管理后台（React）
  - 可视化规则配置、模型管理、字段管理
  - 命中日志、监控、白/黑名单
- 数据层
  - MySQL：配置、用户、日志
  - MongoDB：规则、指标、事件（高频读写）
  - Redis：缓存、窗口计数
  - Elasticsearch：日志检索


### 三、核心能力（面试/选型重点）
1. 动态规则（Groovy 脚本）
   - 无需重启、秒级生效
   - 支持：`if/else`、`&&/||`、`>`/`<`/`>=`/`in`/`contains`
   - 时间窗口：近5分钟/1小时/24小时 频次/金额统计
2. 可视化规则编辑器（中文友好）
   - 业务人员可直接配规则
   - 支持：字段、运算符、分值、权重、阈值
3. 毫秒级响应
   - 典型 <100ms，高并发稳定
4. 多场景模型
   - 登录、注册、支付、提现、转账、营销活动等
   - 每个模型独立规则、独立分值
5. 插件化 & 易扩展
   - 可接入：设备指纹、第三方风控、知识图谱、AI 模型
6. 完整闭环
   - 事件上报 → 规则执行 → 决策返回 → 命中日志 → 策略迭代

### 四、典型规则示例（Groovy）
```groovy
// 1. 近10分钟登录失败≥5次 → 高风险
if(login_fail_count_10m >= 5) {
    score = 100;
    decision = "REJECT"; // 拒绝
}

// 2. 异地+大额交易
if(is_remote == true && trans_amount > 50000) {
    score += 80;
    decision = "REVIEW"; // 人工审核
}

// 3. 新设备+非白名单IP
if(is_new_device == true && !ip_white_list.contains(client_ip)) {
    score += 60;
    decision = "SMS"; // 短信验证
}
```

### 五、技术栈一览
- 后端：Spring Boot 2.x/3.x + MyBatis + tkMapper + Maven
- 规则引擎：Groovy（动态脚本）
- 数据库
  - MySQL：配置、用户、日志
  - MongoDB：规则、指标、事件（核心）
- 缓存/计算：Redis（窗口计数、高频）
- 检索：Elasticsearch（日志、命中记录）
- 前端：React + Ant Design（管理后台）

### 六、为什么选 Radar（对比 Drools）
- Radar
  - 轻量、开箱即用、中文友好
  - 可视化、业务人员可配
  - Groovy 灵活、动态生效
  - 适合：快速搭建、反欺诈、交易风控
- Drools
  - 重、工业级、学习曲线陡
  - 偏向复杂决策表/评分卡
  - 适合：银行授信、保险核保、强合规场景

### 七、部署与接入（极简）
1. 环境：JDK 8+/Maven 3+/MongoDB/MySQL/Redis
2. 拉代码 → 执行 SQL → 修改 application.yml → 启动
3. 客户端 POST 到 `/radar/api/risk`
```json
// 上报事件
{
  "modelId": "login",
  "userId": "1001",
  "ip": "123.45.67.89",
  "deviceId": "abc123",
  "amount": 1000,
  "isRemote": true
}
```
```json
// 返回决策
{
  "code": 200,
  "score": 85,
  "decision": "REJECT", // PASS/REJECT/REVIEW/SMS
  "hitRules": ["异地登录频繁"]
}
```

### 八、一句话总结
Radar = Java 生态 + 可视化配置 + Groovy 动态规则 + 毫秒级风控，是中小团队快速搭建反欺诈/交易风控系统的首选开源方案。

要不要我给你一份 Radar 本地快速部署脚本 + 可直接运行的 Java 客户端 Demo，你5分钟就能跑起来？