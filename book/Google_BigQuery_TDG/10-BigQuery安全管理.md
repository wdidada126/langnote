# 10 BigQuery安全管理（原书第 10 章 · Securing BigQuery）

> 章首注：原书页区间 ⚠️ 推定 p.371–420；一级章题 ✅ 目录实抓（配套仓库 `10_securing` ✅）；
> **本章二级小节 ⚠️ 推定**——按配套代码 `10_securing/` ✅ 实抓文件族（IAM 策略 JSON、
> 列级/行级安全 DDL、CMEK 配置）与官方 access-control / data-governance 文档页组织。
> BigQuery 的安全面覆盖 IAM/数据级加密/列级行级安全/审计日志/组织策略多层。

## 本章地图（⚠️ 推定结构，锚点为 ✅ 配套文件 + 官方文档主题）

| 组 | 小节主题 | 锚点 |
| --- | --- | --- |
| IAM 基础 | 角色/成员/策略绑定、预定义 vs 自定义角色 | ⚠️ 官方 IAM 页 |
| 数据集级权限 | 数据集 ACL、授权范围 | ⚠️ |
| 列级安全 | 列级 IAM 策略、敏感列隔离 | ✅ 配套仓库 DDL |
| 行级安全 | 行级过滤策略、多租户隔离 | ✅ 配套仓库 DDL |
| 数据脱敏 | 动态脱敏策略（masking） | ⚠️ |
| 加密 | 默认加密 / CMEK（客户管理密钥）/ CSEK | ✅ 配套仓库 CMEK 配置 |
| 网络隔离 | VPC Service Controls、私有 IP 访问 | ⚠️ |
| 审计与合规 | 审计日志、INFORMATION_SCHEMA 安全视图 | ⚠️ |
| 组织策略 | 组织级约束、数据驻留 | ⚠️ |

## 核心精讲

### 1. IAM 三要素：角色 × 成员 × 资源（⚠️ 转述）

BigQuery 的权限模型遵循 GCP IAM 统一框架：

| 要素 | 含义 | 示例 |
| --- | --- | --- |
| 角色 (Role) | 权限集合 | `roles/bigquery.dataViewer`、`roles/bigquery.jobUser` |
| 成员 (Member) | 被授权主体 | 用户/组/服务账号/域 |
| 资源 (Resource) | 被保护对象 | 项目/数据集/表/列 |

⚠️ 预定义角色层级（粗→细）：Owner > Editor > Viewer > bigquery.admin > bigquery.dataEditor 等。
自定义角色可按需组合权限——生产环境**最小权限原则**的落地工具。
总入口：✅ docs.cloud.google.com/bigquery/docs/access-control。

### 2. 列级安全：敏感列隔离（✅ 配套仓库 DDL）

```sql
-- 自拟教学示意（非原书文本）：列级 IAM 策略
ALTER TABLE dataset.sensitive_table
SET IAM POLICY
  (SELECT * WHERE TRUE)
  COLUMNS salary, ssn
  ADD GROUP 'data-science@company.com':roles/bigquery.dataViewer;
```

⚠️ 列级安全使**同一张表的不同列可有不同的访问控制**——
薪资/SSN 等敏感列可限制为仅特定组可见，无需拆表。

### 3. 行级安全：多租户隔离（✅ 配套仓库 DDL）

```sql
-- 自拟教学示意（非原书文本）：行级过滤策略
CREATE ROW ACCESS POLICY region_filter ON dataset.multi_tenant
GRANT SELECT ON
FILTERING USING (region = SESSION_USER());
```

⚠️ 行级安全使**同一查询对不同用户返回不同行**——
多租户 SaaS 场景、区域合规场景的核心隔离机制。
对读 Snowflake 行级安全 [../Snowflake_The_Definitive_Guide/10-安全数据共享.md](../Snowflake_The_Definitive_Guide/10-安全数据共享.md)（⚠️ 若盘上对应笔记存在）。

### 4. 数据脱敏（⚠️ 转述）

动态脱敏策略使敏感数据在查询时自动遮蔽：

```sql
-- 自拟教学示意（非原书文本）
CREATE MASKING POLICY email_mask ON (email STRING)
  USING (CASE WHEN HAS_ROLE('roles/hr_admin') THEN email
              ELSE REGEXP_REPLACE(email, r'(.).*(@)', '\\1***\\2') END);
```

⚠️ 脱敏策略可绑定到列→查询时自动生效→无需修改 SQL。
这是"数据可用但不可见"的工程化落地。

### 5. 加密：三层密钥模型（⚠️ 转述 + ✅ 配套仓库）

| 层级 | 密钥管理 | 适用 |
| --- | --- | --- |
| Google 管理 (默认) | Google 自动轮换 | 大多数场景 |
| CMEK | 客户在 Cloud KMS 管理密钥 | 合规/金融/医疗 |
| CSEK | 客户完全自持、Google 不可见 | 极端合规（⚠️ 以官方文档为准） |

✅ 配套仓库 `10_securing/` 含 CMEK 配置示例——
CMEK 使 BigQuery 存储加密的密钥由客户控制→密钥撤销即数据不可恢复。

### 6. 网络隔离与审计（⚠️ 转述）

- **VPC Service Controls**：定义安全边界→阻止数据外泄（BigQuery→非授权网络/服务）；
- **私有 IP 访问**：BigQuery 可通过 VPC 私有连接访问（无公网出口 ⚠️）；
- **审计日志**：所有数据访问/管理操作写入 Cloud Audit Logs→合规审计链；
- **INFORMATION_SCHEMA**：SQL 可查审计元数据（查询日志/作业历史/权限变更 ⚠️）。

### 7. 组织策略与数据驻留（⚠️ 转述）

组织级策略可约束：
- 数据集的**地理区域**（数据驻留合规：EU-only / US-only ⚠️）；
- 是否允许导出到 GCS / 是否允许未加密传输；
- 默认加密级别 / CMEK 强制要求。

⚠️ 组织策略 > 项目策略 > 数据集策略——层级覆盖关系是治理设计的关键。

## 常见误区（⚠️ 转述）

| 误区 | 事实 |
| --- | --- |
| 项目 Owner 能做一切 | 组织级策略可覆盖项目级权限（组织 > 项目 > 数据集） |
| 列级安全需拆表 | 列级 IAM 策略可在同表不同列设不同权限 |
| 默认加密不够安全 | Google 管理密钥自动轮换，大多数场景已足够；CMEK 是合规加码 |
| 行级安全影响性能 | 行级策略在编译期注入 WHERE→对查询透明（⚠️ 复杂策略可能有额外成本） |
| 审计日志需额外配置 | Cloud Audit Logs 默认开启管理事件；数据访问事件需显式启用（⚠️） |
| VPC 隔离=零信任 | VPC SC 是边界防护；零信任还需 IAM 最小权限 + 审计闭环 |

## 与其他章、其他书联系

- IAM 基础与 GCP 统一框架 → [05-使用BigQuery进行开发.md](05-使用BigQuery进行开发.md)（认证三件套）；
  架构层的网络隔离 → [06-BigQuery架构.md](06-BigQuery架构.md)。
- 列级/行级安全的数据面 → [04-将数据加载到BigQuery.md](04-将数据加载到BigQuery.md)（数据接入面的权限管控）。
- ML 模型权限 → [09-BigQuery中的机器学习.md](09-BigQuery中的机器学习.md)（模型是数据集内对象，受 IAM 管控）。
- 治理与数据网格：[../Data_Mesh/00-总览与阅读地图.md](../Data_Mesh/00-总览与阅读地图.md)（域自治 × 联邦治理）。
- 云仓治理对读：[../Snowflake_The_Definitive_Guide/10-安全数据共享.md](../Snowflake_The_Definitive_Guide/10-安全数据共享.md)（⚠️ 若盘上对应笔记存在）。
- 合规底座：[../设计数据密集型应用/05-复制.md](../设计数据密集型应用/05-复制.md)（数据驻留/一致性视角）。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| IAM | Identity and Access Management | GCP 统一权限框架 |
| 预定义角色 | predefined role | Google 预设的权限集合（bigquery.dataViewer 等） |
| 自定义角色 | custom role | 按需组合权限的角色 |
| 列级安全 | column-level security | 同表不同列的不同访问控制 |
| 行级安全 | row-level security | 同查询不同用户的不同行可见性 |
| 数据脱敏 | data masking | 查询时自动遮蔽敏感数据 |
| CMEK | Customer-Managed Encryption Key | 客户管理的加密密钥 |
| CSEK | Customer-Supplied Encryption Key | 客户完全自持密钥（⚠️ 极端合规） |
| VPC Service Controls | VPC-SC | 安全边界，防数据外泄 |
| 审计日志 | audit log | Cloud Audit Logs，数据/管理操作记录 |
| INFORMATION_SCHEMA | INFORMATION_SCHEMA | SQL 可查的元数据/审计视图 |
| 数据驻留 | data residency | 数据集地理区域约束（合规要求） |
| 组织策略 | organization policy | 组织级约束，覆盖项目/数据集策略 |

## 最新演进与工业实践

- **数据治理产品化（2024-2026 ✅ 版本说明实抓）**：BigQuery 的治理面从"IAM + 手动策略"
  演进为"Data Catalog + DLP + 自动分类 + 策略即代码"的完整治理栈。
- **敏感数据保护（DLP）集成**：自动检测 PII/敏感列→推荐脱敏策略→减少人工审计成本（⚠️ 以官方文档为准）。
- **Policy Tags 统一分类**：列级安全从 IAM 策略扩展到 taxonomy→一次分类、多策略复用（⚠️）。
- **Iceberg 托管表的治理面（2026 GA ✅）**：开放格式表同样受 IAM/列级/行级安全管控——
  "开放 ≠ 无管控"的治理一致性得到保证。
- **工业实践**：金融/医疗场景的典型治理栈——CMEK 加密 + 列级脱敏 + 行级区域隔离 + VPC-SC 边界 +
  审计日志全量归档。对读 Snowflake 同题治理
  [../Snowflake_The_Definitive_Guide/10-安全数据共享.md](../Snowflake_The_Definitive_Guide/10-安全数据共享.md)（⚠️ 若盘上对应笔记存在）。
- **合规认证**：BigQuery 通过 SOC 1/2/3、ISO 27001、HIPAA、PCI DSS 等认证（⚠️ 认证清单以 Google Cloud 合规页为准）——
  原书 2019 的合规面在 2026 已大幅扩展。
