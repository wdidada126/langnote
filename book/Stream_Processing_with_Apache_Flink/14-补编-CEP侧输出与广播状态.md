# 14 补编：CEP、侧输出与广播状态

> ⚠️ **性质声明与覆盖度**：三者中**只有侧输出（side output）是《Stream Processing with Apache Flink》的正文内容**
> ——出现在第 6 章「向副输出发送数据」（已核实目录，见 [06 章](06-时间与窗口算子.md)）。
> 原书对 FlinkCEP 仅在第 11 章给出一小节定位（「FlinkCEP」），**没有广播状态（broadcast state）的正文** ⚠️
> （全 11 章目录中不存在该主题）。因此本文件是**超出原书范围的备考补编**，
> 内容依据 Flink 官方 CEP / 状态与连接器文档整理；凡版本不确定处均打 ⚠️。
> 核实说明见 [00 总览](00-总览与阅读地图.md)。

## 核心概念速览（中英对照）

- **复杂事件处理** — Complex Event Processing (CEP)：在事件流上匹配「图案 + 时间约束 + 次数约束 + 顺序约束」的计算范式。
- **图案** — Pattern：由若干**图案变量**（pattern vertex）与边（followed by / next / not followed by）构成的序列描述。
- **图案变量** — pattern variable：图案中一步的名字与其条件（`where`/`until`）。
- **量词** — Quantifier：`times(n)`/`oneOrMore`/`timesOrMore`/`greedy`/`consecutive`，控制一步重复几次。
- **时间约束** — within：整段匹配必须落在给定时间跨度内（事件时间靠水位线推进 ⚠️）。
- **可选步骤** — optional：`optional()` 让图案在该步缺失时也能匹配成功。
- **跳过策略** — afterMatchSkipStrategy：匹配成功后从哪继续（`NO_SKIP`/`SKIP_PAST_LAST_EVENT`/
  `FIRST`/`LAST`/`PREVIOUS`，以及 1.10+ 的 `skipTillNextNonDuplicate` ⚠️）——直接决定结果数量与状态规模。
- **NFA** — non-deterministic finite automaton：CEP 把图案编译成状态机；每个部分匹配（partial match）都要保存状态。
- **`PatternProcessFunction`** — 匹配结果函数：输入是「图案变量 → 匹配到的事件列表」的 Map，输出告警/动作。
- **侧输出** — side output：一个算子向多个具名流发射结果（`OutputTag`）；CEP 里用于发「部分匹配」与超时未完成的图案 ⚠️（complement matching）。
- **补集匹配** — complement matching：输出「图案未完整匹配」的情况（如「登录后 30 分钟未下单」）⚠️（引入版本未核实）。
- **广播状态** — broadcast state：把一条控制流（规则、阈值、图案）复制到所有下游子任务，各子任务用
  `MapState` 保存自己那一份，实现**不重启作业的热更新**。
- **`BroadcastProcessFunction`** — 广播处理函数：`processBroadcastElement`（处理规则流，可写广播状态）
  与 `processElement`（处理数据流，**只能读**广播状态）。
- **`MapStateDescriptor` + `broadcast()`** — 广播声明：描述符同时用于数据流与规则流的连接点。
- **动态 CEP** — dynamic CEP：CEP 图案 + 广播状态 = 运行时可增删改图案（官方示例的标准组合）。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 14.1 | 为什么需要 CEP | DataStream 的「一事件↔状态」表达不了序列；窗口又只能给出聚合而非匹配 |
| 14.2 | 图案 DSL 全要素 | 条件、顺序（next/followedBy）、量词、时间、可选、贪心、跳过策略 |
| 14.3 | 执行语义与代价 | NFA + 部分匹配集合：状态规模 = 活跃匹配数，跳过策略是主控阀 |
| 14.4 | 侧输出的三种用法 | 迟到兜底（06 章）、脏数据隔离、CEP 的部分匹配/补集输出 |
| 14.5 | 广播状态机制 | union list state 的用法 + 每子任务一份 MapState + 扩缩容重分布 |
| 14.6 | 动态 CEP 骨架 | 规则流 → 广播 → CEP 图案表，实现在线改规则 |
| 14.7 | 与 SQL/表层的对应 | `MATCH_RECOGNIZE` ⚠️ 是 CEP 的 SQL 表亲，能力与版本相关 |

## 核心精讲

### 14.1 三种表达力的分界

| 需求 | 合适工具 | 理由 |
| --- | --- | --- |
| 「每分钟每个用户的点击数」 | 窗口 + 增量聚合（06 章） | 只要聚合值，不要序列 |
| 「点击后 30 分钟未下单则告警」 | `KeyedProcessFunction` + timer（06 章 6.2） | 单一状态 + 一个计时器，最省 |
| 「A→B→C 顺序出现且 5 分钟内，B 至少 3 次」 | **CEP** | 序列 + 量词 + 时间，手写状态机会失控 |
| 「规则要运营同学随时改」 | **CEP + 广播状态** | 图案可从控制流注入，不需重启作业 |

### 14.2 图案 DSL 🔧

```java
// 🔧 官方风格：条件 + 顺序 + 量词 + 时间 + 跳过策略
Pattern<Event, ?> brute = Pattern.<Event>begin("fail", AfterMatchSkipStrategy.skipPastLastEvent())
    .where(e -> e.type == LOGIN && !e.ok)
    .timesOrMore(3).greedy()                    // 贪心：尽早闭合重复，减少部分匹配数
    .next("success").where(e -> e.type == LOGIN && e.ok)
    .notNext("logout").where(e -> e.type == LOGOUT)   // 中间不许出现登出 ⚠️ 名称以版本为准
    .within(Time.minutes(5));

PatternStream<Event> ps = CEP.pattern(keyedLoginStream, brute);

ps.process(new PatternProcessFunction<Event, Alert>() {
    @Override public void processMatch(Map<String, List<Event>> match, Context ctx, Collector<Alert> out) {
        out.collect(new Alert(ctx.getCurrentKey(),
            match.get("fail").size(), match.get("success").get(0).ts));
    }
});
```

要点清单：

- `keyBy` 是必须的（图案在键内匹配），因此 CEP 是有状态算子，参与检查点（12 补编）。
- `next` 严格相邻，`followedBy` 允许中间有无关事件（性能差别很大：`followedBy` 会产生更多部分匹配）。
- `within` 用**事件时间**时靠水位线清理；水位线卡住 → 部分匹配永不释放（06 章 6.1 的空闲分区问题在这里同样致命）。
- 跳过策略决定「一次事件同时有多少活跃匹配」——`NO_SKIP` 会产生大量重复匹配，生产上几乎总要显式指定。

### 14.3 代价模型与调优旋钮

| 旋钮 | 影响 | 建议 |
| --- | --- | --- |
| `times`/`oneOrMore` + `followedBy` | 部分匹配数可能指数增长 | 加 `greedy()`、收紧 `within`、拆图案 |
| `within` 长度 | 状态保有时长上限 | 只要业务能接受，越短越省 |
| 跳过策略 | 结果重复度 + 匹配数 | 默认 `NO_SKIP` 危险，显式选 `skipPastLastEvent`/`first` |
| 键基数 | NFA 数量 = 活跃键数 | 高基数键（设备 ID）+ 长 `within` = 状态爆炸（07 章 TTL 思路） |
| 并行度 | 与键分布共同决定倾斜 | 看单 subtask 的 CEP 算子 CPU（10 章反压面板） |

### 14.4 侧输出（本书正文的延伸用法）🔧

```java
// 🔧 用法一（06 章）：迟到事件兜底
WindowedStream<...> w = s.keyBy(...).window(TumblingEventTimeWindows.of(Time.minutes(5)));
SingleOutputStreamOperator<R> main = w.allowedLateness(Time.minutes(10))
    .sideOutputLateData(LATE_TAG)                  // OutputTag<R> 需匿名子类保类型
    .apply(myFn);
DataStream<Event> late = main.getSideOutput(LATE_TAG);

// 🔧 用法二：脏数据隔离（解析失败不发主流）
SingleOutputStreamOperator<Rec> parsed = raw.process(new ParseFn());
DataStream<String> poison = parsed.getSideOutput(BAD_RECORD_TAG);   // 送告警 + 单独落文件（08 章）
```

三条纪律：`OutputTag` 要有唯一 id 且类型正确；侧输出仍是 `DataStream`，可继续开窗/入 sink；
侧输出与 `allowedLateness` 的组合是「先重算、后兜底」的标准分层。

### 14.5 广播状态机制 🔧

```java
// 🔧 规则流广播 + 数据流处理
MapStateDescriptor<String, Rule> ruleDesc =
    new MapStateDescriptor<>("rules", Types.STRING, Types.POJO(Rule.class));

DataStream<Rule> ruleStream = env.addSource(ruleSource);            // 来自 Kafka/配置中心
BroadcastStream<Rule> broadcast = ruleStream.broadcast(ruleDesc);

keyedData.connect(broadcast).process(new BroadcastProcessFunction<Event, Rule, Alert>() {
    @Override public void processBroadcastElement(Rule r, Context ctx, Collector<Alert> out) throws Exception {
        BroadcastState<String, Rule> st = ctx.getBroadcastState(ruleDesc);
        if (r.disabled) st.remove(r.id); else st.put(r.id, r);       // 只有这里能**写**广播状态
    }
    @Override public void processElement(Event e, ReadOnlyContext ctx, Collector<Alert> out) throws Exception {
        for (Rule r : ctx.getBroadcastState(ruleDesc).immutableValues()) {  // 数据侧只读
            if (r.matches(e)) out.collect(new Alert(r.id, e));
        }
    }
});
```

机制要点（与 07 章算子状态的关系）：

1. 广播状态是**算子状态**的一种特殊分配方式：每个并行实例都持有全量规则（union list state 语义 ⚠️ 名称以版本为准）。
2. 因此扩缩容安全：新实例从快照里拿到同一份规则表。
3. `processBroadcastElement` 在不同子任务上看到同一事件的顺序**可能不同** ⚠️（官方明确警告），
   规则设计要保证最终一致（例如按规则 id 覆盖写，而不是累加）。
4. 广播的代价：规则条数 × 并行度 = 内存与网络复制成本，别把大字典当广播流。

### 14.6 动态 CEP（广播 + CEP 的官方范式）🔧

```java
// 🔧 把「图案」本身放进广播状态，运行时按 key 取图案匹配
PatternStream<Event> dynamic = CEP.dynamicPatterns(      // ⚠️ 该入口方法的可用版本请核对所用文档
    keyedEvents,
    ruleStream.broadcast(patternDesc),                   // MapStateDescriptor<String, Pattern<Event,?>>
    new PatternRouter<>(),                               // 决定一条事件该试哪些图案
    new PatternProcessFunctionBuilder().withPatternProcessFunction(myFn));
```

意义：风控/营销规则变更从「改代码 → 打包 → 保存点升级（10 章）」变成「往规则 topic 发一条消息」。

### 14.7 与 SQL 层的关系 ⚠️

- SQL 标准的 `MATCH_RECOGNIZE` 是 CEP 的声明式表亲，Flink 各版本对其支持程度逐步补齐 ⚠️（勿假定与 CEP 等价）。
- 表层的序列匹配无法表达时，仍是「下沉到 DataStream/CEP」，与 13 补编 13.6 的判据一致。

## 版本与兼容性 ⚠️

- CEP 的包路径 `org.apache.flink.cep`；`flink-cep` 需显式加依赖（不在 `flink-dist` 里）。
- `AfterMatchSkipStrategy` 各常量与 `skipTillNextNonDuplicate` 的可用版本、`greedy` 与 `times` 的组合限制随版本变化。
- `CEP.dynamicPatterns` 的签名（以及 `PatternProcessFunctionBuilder`）在 1.10/1.13/1.17 之间有过调整 ⚠️。
- 广播状态 1.5 引入，`BroadcastProcessFunction` 至今稳定；`ReadOnlyContext` 与 `Context` 的区分不变。
- Flink 2.x 的 Scala DataStream 削减会同时影响 Scala 版 CEP DSL ⚠️。

## 常见误区

| 误区 | 事实 |
| --- | --- |
| 「CEP 就是复杂点的 filter」 | 差别在**序列 + 时间 + 次数**的组合语义与部分匹配管理；手写会退化成不可维护的多状态机 |
| 「不设跳过策略也行」 | 默认 `NO_SKIP` 会为同一事件产生多个匹配，输出与状态都放大 |
| 「`within` 会保证 5 分钟内一定出结果」 | 事件时间下由水位线驱动；水位线停滞（空闲分区、倾斜）会让匹配永不清理 |
| 「广播状态可以按键存」 | 它是**算子级**状态，所有键共享同一份；按键的数据状态仍用 keyed state |
| 「数据侧可以修正广播状态」 | `processElement` 的上下文是只读的；写只能在 `processBroadcastElement` |
| 「广播元素在所有子任务上顺序一致」 | 官方明确警告顺序可能不同；规则要设计成幂等/可交换 |
| 「侧输出有性能代价所以少用」 | 侧输出就是普通输出流；真正要注意的是别把大量脏数据打进同一作业的输出（改走独立 sink） |
| 「CEP 不需要检查点」 | 它是重状态算子；没有检查点时一次故障就把所有部分匹配丢掉，等于漏报 |

## 与其他章 / 其他书的联系

- 侧输出的原始正文位置 → [06-时间与窗口算子.md](06-时间与窗口算子.md)（6.3）。
- 计时器/超时替代方案 → [06-时间与窗口算子.md](06-时间与窗口算子.md)（6.2）。
- 广播状态的接口谱系（算子状态 / union list state）→ [07-有状态函数与状态管理.md](07-有状态函数与状态管理.md)（7.3）。
- CEP/广播流作为源与汇 → [08-读写外部系统.md](08-读写外部系统.md)。
- CEP 算子的状态与扩缩容/重缩放 → [10-运维监控与调优.md](10-运维监控与调优.md)。
- 原书中 CEP 的唯一正文位置 → [11-生态展望-DataSet_Table_CEP_Gelly.md](11-生态展望-DataSet_Table_CEP_Gelly.md)（11.4）。
- 表层序列匹配对照 → [13-补编-TableAPI与SQL分层.md](13-补编-TableAPI与SQL分层.md)（13.6、14.7）。
- 仓库互链：规则/图案的状态化思路与图计算对照 → [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)；
  Kafka 作为规则 topic → [../Kafka权威指南.md](../Kafka权威指南.md)。
