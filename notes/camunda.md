# camunda

        <dependency>
            <groupId>org.camunda.bpm</groupId>
            <artifactId>camunda-engine</artifactId>
            <version>7.20.0</version>
        </dependency>

### camunda跟activiti的关系 
Camunda和Activiti是两个流程引擎框架，它们有一定的关系。
Activiti是一个开源的BPM（Business Process Management）引擎，最初由Alfresco软件公司开发，后来由于Alfresco将其捐赠给了Apache软件基金会，成为Apache项目之一。Activiti提供了流程定义、执行和管理的功能，可以用于构建和执行业务流程。
Camunda是一个基于Activiti流程引擎的开源项目，它是在Activiti的基础上进行扩展和改进的。Camunda提供了更广泛的功能和工具，包括工作流引擎、决策引擎和案例管理等，以支持更复杂的业务流程管理需求。Camunda也提供了更丰富的API和集成选项，使其更加灵活和可扩展。
可以说，Camunda是在Activiti的基础上进行了进一步的发展和完善，提供了更多功能和扩展性。尽管如此，Activiti仍然是一个成熟且广泛使用的流程引擎，而Camunda则是在Activiti基础上的一种选择，可以根据具体需求选择使用其中之一。

基于camunda开发的工作流web系统--中享思途

http://www.situedu.com/news/uid/2950.html

https://www.cnblogs.com/yscec/p/11562064.html


camunda-modeler
画流程图的工具

https://camunda.com/download/modeler/?__hstc=12929896.eb7fddd2cb015af811484bcc48f563df.1687671971326.1687671971326.1687671971326.1&__hssc=12929896.1.1687671971326&__hsfp=3766048905

Open Source Desktop Modeler
Supports: BPMN, DMN, Forms
Version: 5.12.0
Release Date: June 13, 2023
Platform: Camunda 7 and 8

全亿健康用了

```xml
        <dependency>
            <groupId>org.camunda.bpm.springboot</groupId>
            <artifactId>camunda-bpm-spring-boot-starter-rest</artifactId>
            <version>7.15.0</version>
        </dependency>

        <dependency>
            <groupId>org.camunda.bpm.springboot</groupId>
            <artifactId>camunda-bpm-spring-boot-starter-webapp</artifactId>
            <version>7.15.0</version>
        </dependency>
```


接下来了解比较常见的流程引擎。例如 JBPM 、 Activiti 、 Flowable 、 Camunda 、 Zeebe 。
https://www.cnblogs.com/schaepher/p/12571944.html
https://github.com/meirwah/awesome-workflow-engines
https://camunda.com/

camunda 、activiti 、flowable
三个框架都是从jbpm框架诞生出来的，先是有jbpm4,然后出来了一个activiti5,activiti5发展一段时间，又出来了一个Camunda。activiti5发展了4年，紧接着出来了一个flowable。


官方文档：https://docs.camunda.org
源码地址：https://github.com/camunda/camunda-modeler

https://gitee.com/edidada/testcamunda


https://www.jianshu.com/p/67271eddc95b

https://zhuanlan.zhihu.com/p/376904826

https://docs.camunda.org/manual/latest/user-guide/spring-boot-integration/configuration/#camunda-engine-properties

Camunda 是一套基于 BPMN 2.0、DMN、CMMN 标准的开源流程自动化平台，核心是流程引擎，用于编排、执行、监控业务流程。

下面按 核心概念分层 整理（同时覆盖 Camunda 7 / Camunda 8 通用理解）。

---

## 一、三大标准（建模语言）
Camunda 核心围绕 BPMN / DMN / CMMN 三大OASIS标准：

### 1. BPMN 2.0（核心）
Business Process Model and Notation：业务流程模型与符号
- 用于结构化、可执行流程（固定步骤、明确流转）
- 核心元素：事件(Event)、任务(Task)、网关(Gateway)、序列流(Sequence Flow)

### 2. DMN 1.3
Decision Model and Notation：决策模型与符号
- 用于业务规则/决策表（如审批条件、费率计算、风控规则）
- 可独立执行，也可嵌入 BPMN 流程中

### 3. CMMN 1.1
Case Management Model and Notation：案例管理模型
- 用于非结构化、灵活、以人为中心的场景（如复杂案件、投诉处理）

---

## 二、流程核心概念（BPMN）
### 1. 流程定义（Process Definition）
- 静态模板：`.bpmn` XML 文件，描述流程结构（节点、流转、条件、角色）
- 由 Camunda Modeler 可视化设计
- 唯一标识：`key` + `version`

### 2. 流程实例（Process Instance）
- 流程定义的一次具体执行（动态、运行中/已结束）
- 每个实例有独立 ID、状态、变量、执行路径

### 3. 活动 / 任务（Activity / Task）
流程中最小工作单元：
- 用户任务（User Task）：需要人处理（审批、填写表单）
- 服务任务（Service Task）：自动调用 Java/REST/外部系统
- 脚本任务（Script Task）：执行 Groovy/JavaScript 等脚本
- 业务规则任务（Business Rule Task）：执行 DMN 决策
- 发送/接收任务（Send/Receive Task）：消息交互

### 4. 网关（Gateway）— 控制流转
- 排他网关（Exclusive）：多选一（条件判断）
- 并行网关（Parallel）：分叉/汇合（同时执行多分支）
- 包含网关（Inclusive）：满足条件的分支都走
- 事件网关（Event-based）：等待多个事件之一触发

### 5. 事件（Event）
- 开始事件（Start）：启动流程
- 结束事件（End）：结束流程
- 中间捕获事件（Intermediate Catching）：等待消息、定时器、信号
- 边界事件（Boundary）：挂在任务上，超时/异常/消息中断任务

### 6. 流程变量（Process Variable）
- 流程实例的数据载体（键值对）
- 用于：条件判断、传参、任务表单、业务数据关联

### 7. 执行与令牌（Token）
- 引擎用 Token（令牌） 沿着序列流移动，表示执行位置
- 并行网关会生成多个 Token；汇合网关等待所有 Token 到达

---

## 三、Camunda 平台核心组件
### 1. 流程引擎（Process Engine）
- Camunda 7：嵌入式 Java 引擎（PVM 内核），基于关系库（MySQL/PostgreSQL）
- Camunda 8：分布式引擎 Zeebe，事件流架构、水平扩展、gRPC API

### 2. 核心服务（API）
- RepositoryService：部署/查询流程定义
- RuntimeService：启动实例、触发信号/消息、修改变量
- TaskService：查询/完成用户任务、认领/委派
- HistoryService：查询历史实例、任务、变量
- ManagementService：作业、定时器、异常重试

### 3. Web 应用（7 vs 8）
- Camunda 7
  - Cockpit：监控运行实例、状态、异常
  - Tasklist：用户代办/已办
  - Admin：用户、组、权限
- Camunda 8
  - Operate：监控、故障排查
  - Tasklist：用户任务
  - Modeler：云端建模、协作
  - Optimize：流程分析、瓶颈、报表

### 4. 作业执行器（Job Executor）
- 处理异步、定时、延时任务（定时器、异步继续、外部任务）
- 失败自动重试、死信队列

### 5. 外部任务（External Task）
- 跨语言/跨服务：流程引擎创建 Job，外部 Worker 轮询/订阅 → 执行 → 完成
- Camunda 8 主推模式

---

## 四、Camunda 7 vs 8 核心差异（概念层）
| 维度 | Camunda 7 | Camunda 8 (Zeebe) |
|------|------------|-------------------|
| 引擎架构 | 嵌入式、单库集群 | 分布式、事件流、分区Raft |
| 存储 | 关系型数据库 | Elasticsearch + 流存储 |
| 扩展 | 垂直扩展 | 水平无限扩展 |
| 通信 | Java API / REST | gRPC |
| 事务 | 本地ACID | 最终一致性、Saga |
| 适用场景 | 单体/Java微服务 | 云原生、高吞吐、跨语言 |

---

## 五、核心流程生命周期（一句话）
建模（Modeler）→ 部署（Deployment）→ 启动实例 → 执行（Token/任务/网关/事件）→ 人工/自动处理 → 结束 → 历史归档

---

## 六、常见术语速记
- Deployment：流程定义打包部署
- Incident：流程异常/失败（需人工干预）
- Claim/Complete：认领任务 / 完成任务
- Signal/Message：跨实例/跨流程触发
- Correlation Key：消息关联键（路由到正确实例）

---

如果你需要，我可以帮你画一张 Camunda 核心概念关系图（BPMN元素 + 引擎 + 服务 + 实例/变量/任务），方便你整体记忆。

下面用最清晰、不绕弯的方式，把这四个概念的关系、区别、各自职责一次性讲透，适合面试、架构设计、写文档都能用。

# 一、先一句话总览
- BPM（业务流程管理）：是一套思想+方法论+平台，不是单个引擎。
- 工作流引擎：BPM 的核心执行器，负责按步骤跑流程。
- 决策引擎：BPM 里的“大脑”，负责判断、规则、计算。
- 案例管理引擎：BPM 里的“灵活版工作流”，处理不确定、以人为中心的流程。

它们不是互斥，而是互补、嵌套、协同。

---

# 二、逐个概念精确定义

## 1. BPM（Business Process Management）
不是引擎，是一套体系。

包含：
- 流程建模（BPMN）
- 流程执行（工作流引擎）
- 决策规则（DMN）
- 灵活案例（CMMN）
- 监控、优化、分析

一句话：
BPM = 工作流引擎 + 决策引擎 + 案例管理 + 监控平台 + 建模工具

---

## 2. 工作流引擎（Workflow Engine）
BPM 的“骨架”和“驱动器”。

职责：
- 按固定步骤执行流程
- 流转节点（审批、自动任务、分支、并行）
- 管理任务、权限、待办
- 维护流程状态、变量、历史

典型场景：
- 请假审批
- 采购流程
- 订单履约
- 固定步骤的自动化

特点：
- 结构化强、路径明确
- 先画流程图，再按图执行

代表：Camunda 7/8、Activiti、Flowable、OSWorkflow

---

## 3. 决策引擎（Decision Engine）
BPM 的“大脑”，负责判断与计算。

基于标准：DMN

职责：
- 条件判断
- 规则计算（利率、风控、折扣、额度）
- 分支路由
- 避免代码里写大量 if-else

典型场景：
- 风控规则
- 审批自动通过/拒绝
- 价格计算
- 客户分级

特点：
- 无流程、只做判断
- 规则可热更新，不用改代码
- 可独立调用，也可嵌入工作流

代表：Camunda DMN、Drools、Easy Rules、IBM ODM

---

## 4. 案例管理引擎（Case Management Engine）
BPM 的“灵活版工作流”。

基于标准：CMMN

职责：
- 处理非结构化、不确定步骤的业务
- 以人为中心，步骤可随时加、可跳步
- 围绕一个“案件”展开，而不是固定流程

典型场景：
- 保险理赔调查
- 投诉处理
- 法务案件
- 复杂故障排查

特点：
- 流程不固定、灵活演进
- 没有严格的开始→结束路径
- 强调知识工作、人工决策

代表：Camunda CMMN、FileNet、Pega Case Management

---

# 三、核心关系（最重要）

## 1. 包含关系
BPM 包含：工作流引擎 + 决策引擎 + 案例管理引擎

## 2. 协作关系（真实系统里长这样）
1. 工作流引擎跑主流程
2. 遇到判断 → 调用决策引擎
3. 遇到复杂灵活场景 → 启动案例管理
4. 全部由 BPM 平台统一监控

## 3. 层级关系
- BPM：顶层体系
- 工作流引擎：核心执行
- 决策引擎：逻辑判断
- 案例管理：灵活补充

# 四、区别对比（最直观）

| 维度         | 工作流引擎                     | 决策引擎                 | 案例管理引擎               | BPM                         |
|------------|-----------------------------|-----------------------|-----------------------|-----------------------------|
| 核心定位       | 流程步骤执行器                  | 规则判断计算器            | 灵活案件处理器           | 整体业务流程管理平台           |
| 结构         | 强结构化、固定路径          | 无流程、纯函数式          | 非结构化、动态步骤     | 结构化+非结构化都支持          |
| 驱动方式       | 流程节点驱动                    | 数据/规则驱动             | 人/事件驱动             | 混合驱动                     |
| 典型标准       | BPMN                        | DMN                   | CMMN                  | BPMN+DMN+CMMN               |
| 适合业务       | 审批、固定流程、自动化           | 风控、定价、路由、规则      | 案件、投诉、复杂处理      | 全场景企业流程自动化           |
| 是否可独立存在 | 是                           | 是                     | 是                     | 是（整合所有）|

# 五、用一个生活例子秒懂

假设场景：保险理赔

1. 工作流引擎
   报案 → 初审 → 审核 → 赔付 → 结案
   → 按固定步骤跑。

2. 决策引擎
   金额 < 2000 → 自动通过
   金额 ≥ 5000 → 需人工复核
   酒驾/违规 → 拒绝
   → 纯判断，不关心步骤。

3. 案例管理引擎
   重大事故、多方责任、需要调查、补充材料
   步骤不确定，随时加任务
   → 灵活案件处理。

4. BPM
   把上面三者整合，统一监控、分析、优化整个理赔体系。

# 六、最终极简总结
- BPM：全家桶，一套完整体系
- 工作流引擎：按步骤跑流程
- 决策引擎：做判断、算规则
- 案例管理：灵活、非结构化案件处理

关系：BPM 包含并协调后三者，后三者互相配合完成业务。

如果你需要，我可以再给你画一张架构关系图，或者整理成面试背诵版。
