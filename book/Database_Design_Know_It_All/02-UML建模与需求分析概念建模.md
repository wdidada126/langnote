# 02 · UML 数据建模与需求分析/概念建模（合集第 3+4 章）

> **覆盖**：原书 Ch.3 *Data Modeling in UML* + Ch.4 *Requirements Analysis and Conceptual Data Modeling*（✅ 章题实抓）。
> **归源（✅ 已实证，见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 第三节）**：
> - Ch.3 ← Halpin & Morgan《Information Modeling and Relational Databases, 2e》(MK 2008, ISBN 978-0-12-373568-3) 同名章 p.345-397，DOI 10.1016/b978-012373568-3.50013-8；
> - Ch.4 ← Teorey/Lightstone/Nadeau《Database Modeling & Design, 4e》(MK 2006, ISBN 978-0-12-685352-0) 同名章，DOI 10.1016/b978-012685352-0/50004-5。
> 两章并置正好构成**概念建模两大流派**的对台戏：ORM/UML 校验学派 vs ER 工程学派。精读重构，非原书文本。

## 1. Ch.3 · UML 数据建模（Halpin & Morgan 立场 ⚠️ 重构）

### 1.1 ORM 作者的"借船出海"

Halpin 是 **ORM（Object-Role Modeling）** 创始人：模型=事实断言（fact-first），约束用谓词逻辑词表表达（唯一性、强制性、子类型不相交/完备、集合比较、值约束）。他在 IMDR 书里写 UML 章的用意是**翻译学**：让 UML 使用者能把类图无损地读回 ORM/ER 语义，反过来暴露 UML 类图作为数据模型的三处先天不足（书中论证方向，⚠️ 转述）：

1. **类图混装结构与行为**——数据建模只需要名词，UML 却默认你画方法；
2. **约束表达弱**——UML 的 OCL 外挂才是严格约束所在，裸类图的基数常缺失唯一性细节；
3. **子类型机制歧义**——{xor}/{or} 不完全约束靠标记约定，语义校验全靠工具。

### 1.2 概念层校验清单（章的实操价值）

- 每个关联两端写**角色名+基数对**（如 Employee works-for Department，{0,1}/{1,N}）；
- **强制性**（mandatory role）遗漏是需求事故的头号来源："员工必须属于部门吗？"必须在评审会上被问；
- 值类型（value type）先归一：同义字段（cust_no/client_id）建模期就合并；
- 用**填充样例事实**（populate with sample facts）驱动校验：让业务方读一遍生成的人话句子，读不顺=模型错。

### 1.2.1 ORM 约束 → UML/ER 记号对译表（⚠️ 重构对译，非原书表格）

| ORM 概念 | UML 类图记法 | ER 系记法 | 漏掉的下场 |
|---|---|---|---|
| 唯一性 {1} | 属性下划线（键候选） | 键下划线 | 重复事实进库 |
| 可选 {0,1} | 多重度 0..1 | 0:N 可选端 | NULL 泛滥成灾 |
| 强制 {1,1} | 多重度 1..* + 必需导航 | 全参与双框线 | 悬挂子记录 |
| 不相交 {xor} | {xor} 构造型 | ISA 互斥环 | 一行双身份脏数据 |
| 完备 {or} | {complete} | 全特化双线的对应物 | 查询缺默认分支 |
| 子集约束 {subset} | 裸类图**不可表达** | 不可表达 | ——只能靠 OCL/工具 |

末行即 Halpin 的杀手锏论据：子集/相等这类跨谓词约束，类图与 ER 图都画不下，ORM 词表天生放得下——约束表达力的差距不在图上功夫，在语义代数学。

### 1.3 repo 对位

- 5e 的 UML 章（同一作者团的母书演进）：[../Database_Modeling_and_Design_5e/03-UML对象建模.md](../Database_Modeling_and_Design_5e/03-UML对象建模.md)；
- Halpin & Morgan 全本其他章的议题（ER 章 p.305-343、Relational Mapping p.473-526 ✅ Crossref 章页实抓）不在合集内——**读不够就去 5e**；
- 工具落地对照（ER 图生成 DDL 的完整链路）：[../MySQL_Workbench数据建模与开发.md](../MySQL_Workbench数据建模与开发.md)；中文方法论：[../数据建模经典教程.md](../数据建模经典教程.md)。

## 2. Ch.4 · 需求分析与概念数据建模（Teorey 4e 立场 ⚠️ 重构）

### 2.1 章骨架

Teorey 谱系此章的招牌是**把需求访谈变成可检查的建模循环**（与 5e 同名章一脉，对读 [../Database_Modeling_and_Design_5e/04-需求分析与概念建模.md](../Database_Modeling_and_Design_5e/04-需求分析与概念建模.md)）：

1. **需求收集**：用例式短语清单（"供应商可以给多个项目供货"）→ 每短语映射一个联系；
2. **粒度决策（granularity）**：先定"每行是什么"（row fact），再定属性——粒度含糊是后续一切规范化争论的病根；
3. **E/R 草图三圈法**：核心实体圈→扩展圈→外围圈，逐圈与用户确认；
4. **属性归类手术**：把"其实是实体的属性"升格（地址→地址实体+联系），把"派生属性"剔除（年龄=fn(生日)）；
5. **业务规则落约束**：全/偏参与、1:1 强制、时间窗口规则先记录、后映射（CHECK/触发器/应用层三选一留到逻辑层）。

### 2.1.1 三分钟拆解校园需求（重构演示 ⚠️）

输入三短语："教师可教多门课；学生选课带成绩；同一门课每学期重开。"

- 短语 3 触发**粒度事件**："课"是教学大纲（Course）还是开设班次（Offering）？不升格 Offering，"学期"与"成绩"就无处安放——Ch.4 招牌的"实体升格"现场；
- 短语 1 → 教师–Offering 1:N（班次唯一归属教师）或 M:N（合班课）→ 需求复访谈定夺；
- 短语 2 → 学生–Offering M:N → 选课桥表，grade 挂桥上（桥表可带属性是 ER 老手与新手的分水岭）；
- 出口清点：实体集 4、桥 1、强制约束 3 句——每句回写成 ORM 式断言存档，供评审复诵。

### 2.2 与 Ch.3 的方法论张力（编辑并置的用意）

| 维度 | ORM/Halpin（Ch.3） | ER/Teorey（Ch.4） |
|---|---|---|
| 起点 | 形式语义（句子+约束代数） | 业务图景（图形+访谈循环） |
| 校验 | 工具自动生成人话断言 | 样例填充+业务方口读 |
| 长项 | 复杂约束无遗漏 | 大范围沟通与分期建模 |
| 风险 | 学术味重、落地慢 | 基数/约束画漏，留给下游 |

合集把两章放在相邻位置客观上构成"概念建模双轨制"教材——这也是它相对单本教材的**增值点**。

### 2.3 🔧 类比实测：概念约束到 DDL 的最小落地（非本书引擎行为）

用 SQLite 3.45.3（✅ 实跑，E1 全套见 00 §7）：1:N 联系→`REFERENCES`、全参与→`NOT NULL`、1:1 至多→子表主键即外键（`manager.emp_id INTEGER PRIMARY KEY REFERENCES employee(id)`）、值域→`CHECK`。实测确认：删除被引用部门时默认 RESTRICT（FK constraint failed），等价于概念模型"全参与"的工程表达。映射到 §2.1.1 校园模型的形状（仅展示形态，未逐句实跑 ⚠️）：

```sql
-- offering 升格实体的 DDL 落点（复合主键=粒度声明的物化）
CREATE TABLE offering(course_id INTEGER REFERENCES course(id), semester TEXT,
                      PRIMARY KEY(course_id, semester));
CREATE TABLE enrollment(student_id INTEGER, course_id INTEGER, semester TEXT,
                        grade INTEGER CHECK (grade BETWEEN 0 AND 100),
                        PRIMARY KEY(student_id, course_id, semester),
                        FOREIGN KEY(course_id, semester) REFERENCES offering(course_id, semester));
```

桥表带属性（grade）+复合外键指向升格实体（offering）——概念层的两个动作，DDL 层六行字。⚠️ UML 工具到 DDL 的自动映射（ORM 系：Rulemodeler/NF2；ER 系：ERwin 等）未在本机验证，转述 ⚠️。

## 3. 学习检查（重构自章题语义 ⚠️）

1. 给定"每订单可含多种商品，商品跨订单复用"，判断三处粒度陷阱：订单行实体、商品目录实体、价格的时间性（成交价≠目录价）。
2. 用 ORM 句子法给"一名员工至多属于一个部门，部门至少一名员工"写基数+强制性，并指出 ER 图上对应记号。
3. 把 Ch.4 的"升格手术"应用于字段：`customer.tax_id_type`（个人/企业）→ 何时应升为子类型而非枚举列。
4. 子集约束（"退款账户 ⊆ 收款账户"）在对译表末行为什么裸类图画不下？给出 OCL 与 ORM 两种写法思路。
5. 需求访谈中"先记规则、后定机制"（§2.1 第 5 步）避免了什么错误？（概念层过早绑定 CHECK/触发器实现，导致换 DBMS 时模型报废。）

## 核心概念速览（中英对照）

- **对象-角色模型** — Object-Role Modeling (ORM)：以事实断言为一等公民的概念模型，Halpin 创立。
- **事实优先** — Fact-first modeling：先收集业务真句再抽象结构，防"图上无据"。
- **唯一性约束** — Uniqueness Constraint：谓词某参数组合至多一事实——基数校验的最小原子。
- **强制性约束** — Mandatoriness：某角色必须参与；漏画=下游 NULL 泛滥。
- **UML 类图** — UML Class Diagram：结构+行为统一视图；用作数据模型时须剥行为补约束。
- **OCL** — Object Constraint Language：UML 的形式约束外挂，裸类图严格语义的来源（⚠️ 转述）。
- **粒度** — Granularity：每行事实的"单价声明"，概念建模第一决策。
- **需求短语清单** — Requirements by Example/Clarification：自然语言短语→实体/联系的系统映射法。
- **派生属性** — Derived Attribute：可由其他属性算出（年龄/总额），原则上不入存储模式。
- **属性升格** — Promotion/Un-nesting：属性具备独立身份与联系时改写为实体。
- **三圈草图法** — Core-Extended-Peripheral Sketching：分圈确认控制范围蔓延（⚠️ 重构）。
- **概念-逻辑分界** — Conceptual vs Logical：本章产物不得出现外键/表/索引字样。

## 最新演进与工业实践

1. **UML 数据建模退位、逻辑建模代码化**（2026 视角）。类图活成了架构文档图；数据建模的"新代码化载体"是 dbt YAML + 语义层：实体/列/测试写进版本库，文档与血缘自动生成——✅ https://docs.getdbt.com/docs/build/documentation （200）。ER/ORM 的"约束清单"精神由 **data tests**（unique/not_null/relationships）继承——"relationships 测试"就是外键完整性的仓库级重写：对 [../The_Enterprise_Data_Catalog_2e/00-总览与阅读地图.md](../The_Enterprise_Data_Catalog_2e/00-总览与阅读地图.md) 的 catalog 侧叙事。
2. **形式化校验以新面孔回归**：SQL/PGQ（ISO/IEC 9075-16，⚠️ https://www.iso.org/standard/81519.html 403 仅登记）把"角色+基数"查询标准化进 SQL:2023 系；DuckDB 社区扩展 duckpgq 等已在实验性支持图查询——✅ DuckDB 扩展总览 https://duckdb.org/docs/stable/core_extensions/overview （200）。Halpin 若在世大概会欣慰：约束词表进了标准 SQL。
3. **LLM 改变需求访谈**：2024+ 工程实践常用"自然语言 PRD → LLM 抽实体/联系草稿 → 人审"，Ch.4 的短语清单法成为 prompt 模板的骨架；但"业务方口读样例事实"这一校验环节无法外包——它是全书最"人"的一步（⚠️ 实践共识转述）。
4. **概念建模与 NoSQL 分家**：文档数据库的"聚合设计"（embedding vs referencing）实质是在概念层重做 Ch.2 的 M:N 拆分决策，读 [../nosql精粹.md](../nosql精粹.md)；本章 ER/UML 双语仍是关系+图双模时代的通用护照。
5. **工具现状（⚠️ 转述）**：ORM 血统的商业工具（Verity 后继者）几近消失；ER 血统由 erwin/PowerDesigner/DataGrip 模型功能续命；开源侧 dbdiagram.io、draw.io ER 形状为日常主力。选型判据回到本章：能否强制表达**角色基数+唯一性**并导出 DDL。
6. **概念建模在 AI 管道里的新位置**：Text-to-SQL 的生成质量高度依赖"实体-联系-约束"清单的完备度，部分团队把 ORM 式断言表直接当 few-shot 语料——Ch.3/4 的"业务方口读人话句子"第一次有了机器消费者，"口读不顺"如今会让模型答错数（⚠️ 实践综述，无权威 URL 可挂）。
