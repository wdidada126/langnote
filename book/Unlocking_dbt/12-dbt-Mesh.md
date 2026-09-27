# 12 · dbt Mesh

> Ch 12 pp 407–436 | DOI: 10.1007/979-8-8688-1844-8_12

---

## 学习目标

- 理解 dbt Mesh 的架构理念与解决的问题
- 掌握跨项目依赖 (cross-project dependencies)
- 区分 public / protected / private 模型访问级别
- 了解 Mesh 的组织治理与契约模式

---

## 12.1 为什么需要 dbt Mesh

单体 dbt 项目的问题:
- 团队间冲突频繁 (命名、schema 变更)
- 编译时间随规模线性增长
- 部署耦合——一个团队的变更影响所有人
- 认知负担——每个人需要理解整个项目

> ✅ dbt Mesh 将单体项目拆分为多个独立项目，通过契约协作。

---

## 12.2 Mesh 架构概览

```
[Project: data_platform]     ← 共享基础层
    ├── models/staging/
    └── models/intermediate/
         ↓ (public access)
[Project: analytics_finance]    [Project: analytics_marketing]
    ├── models/marts/finance/       ├── models/marts/marketing/
    └── ...                         └── ...
```

- 每个项目独立开发、测试、部署
- 通过 `ref()` 跨项目引用模型
- 上游项目暴露 `public` 模型供下游消费

---

## 12.3 跨项目 ref

```sql
-- 在 analytics_finance 项目中
SELECT *
FROM {{ ref('data_platform', 'int_customers') }}
```

- 第一个参数是**项目名**，第二个是**模型名**
- 需要在下游项目的 `dependencies.yml` 中声明依赖

---

## 12.4 dependencies.yml

```yaml
# dependencies.yml (下游项目)
projects:
  - name: data_platform
```

```bash
dbt deps    # 拉取上游项目的公共模型定义
```

---

## 12.5 模型访问级别

| 级别 | 跨项目可见性 | 用途 |
|------|-------------|------|
| `public` | 任何项目可引用 | 共享接口模型 |
| `protected` | 同组项目可引用 | 团队内部共享 |
| `private` | 仅本项目可引用 | 内部实现 |

```yaml
# schema.yml
models:
  - name: int_customers
    access: public
    description: "标准化客户维度 — 对外契约"
  - name: int_internal_calc
    access: private
```

> ✅ `access` 是 dbt Mesh 的核心治理机制。

---

## 12.6 契约 (Contracts)

```yaml
models:
  - name: int_customers
    access: public
    config:
      contract:
        enforced: true
    columns:
      - name: customer_id
        data_type: integer
      - name: customer_name
        data_type: varchar
      - name: region
        data_type: varchar
```

- `contract.enforced: true` 强制模型输出符合声明的列名和类型
- 变更契约需要协调下游项目
- 类似 API 版本管理的概念

> ⚠️ 契约是 dbt Mesh 中保证跨项目稳定性的关键机制。

---

## 12.7 Source Overrides

```yaml
# 下游项目覆盖上游 source
sources:
  - name: jaffle_shop
    overrides: data_platform    # 指定被覆盖的上游项目
    tables:
      - name: orders
        # 下游可添加额外的 freshness 配置
```

---

## 12.8 Mesh 的部署模式

| 模式 | 说明 |
|------|------|
| 独立部署 | 每个项目独立 CI/CD |
| 编排器协调 | Airflow/Dagster 编排跨项目依赖 |
| dbt Cloud 多项目 | 原生支持跨项目触发 |

---

## 12.9 迁移策略

从单体到 Mesh 的渐进迁移:

1. **识别边界**: 按业务域划分项目边界
2. **提取公共层**: 将 staging/intermediate 提取为独立项目
3. **设置访问级别**: 标记 public/protected/private
4. **建立契约**: 为 public 模型添加 contract
5. **拆分项目**: 逐步将 marts 层迁移到独立项目
6. **配置跨项目 ref**: 替换内部 ref 为跨项目 ref

---

## 🔧 12.10 DuckDB / SQLite 类比

> 以下类比使用 DuckDB/SQLite 概念辅助理解，**非本书引擎行为**。

| # | dbt 概念 | DuckDB 类比 | SQLite 类比 |
|---|---------|-------------|-------------|
| 1 | 跨项目 ref | DuckDB `ATTACH` 跨 database 引用 | SQLite 跨 database `main.table` 引用 |
| 2 | access level (public/private) | DuckDB 无访问控制（需外部权限） | SQLite 无访问控制 |
| 3 | contract (列类型强制) | DuckDB `CREATE TABLE` 显式类型约束 | SQLite `CREATE TABLE` 弱类型约束 |
| 4 | dependencies.yml 项目依赖 | DuckDB 无项目依赖概念 | SQLite 无项目依赖概念 |

---

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
|------|---------|--------|
| 网格架构 | dbt Mesh | 多项目协作的分布式范式 |
| 跨项目引用 | Cross-project ref | ref('project', 'model') |
| 访问级别 | Access Level | public / protected / private |
| 契约 | Contract | 强制列名和类型的接口保证 |
| 依赖声明 | dependencies.yml | 声明上游项目依赖 |
| Source 覆盖 | Source Override | 下游覆盖上游 source 定义 |

---

## 最新演进与工业实践

- **dbt Mesh GA** (v1.9+): 跨项目 ref 和 contract 正式 GA ⚠️ [docs.getdbt.com/docs/collaborate/govern/about-dbt-mesh](https://docs.getdbt.com/docs/collaborate/govern/about-dbt-mesh)
- **dbt Cloud 多项目支持**: 原生支持跨项目 job 触发和依赖可视化
- **Mesh 治理工具**: dbt-labs 提供 mesh-setup 工具辅助迁移
- **Fusion 引擎**: 跨项目编译优化，多项目场景编译时间大幅缩短 ⚠️ [getdbt.com/blog/dbt-core-v1-11-is-ga](https://www.getdbt.com/blog/dbt-core-v1-11-is-ga)
