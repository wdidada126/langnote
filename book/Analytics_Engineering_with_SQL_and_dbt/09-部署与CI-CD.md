# 09-部署与CI-CD

> **对应章节**: Ch9 — Deploying dbt Projects
> **核心命题**: CI/CD 管道、dbt Cloud 部署、编排集成、生产最佳实践

---

## 9.1 dbt 部署模式

### 三种部署方式

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| **本地开发** | `dbt run` 在开发者笔记本 | 开发/调试 |
| **CI 部署** | GitHub Actions / GitLab CI | 测试 PR、自动检查 |
| **生产调度** | dbt Cloud / Airflow / cron | 定时运行 |

✅ 最佳实践：**本地开发 → CI 验证 → 生产调度**的三阶段管道。

---

## 9.2 dbt Cloud 部署

### dbt Cloud 核心功能

| 功能 | 说明 |
|------|------|
| **托管 IDE** | 浏览器内 SQL 编辑 + 预览 |
| **调度器** | 定时运行 dbt run/test |
| **CI/CD** | PR 自动创建 slim CI 环境 |
| **文档托管** | 自动发布 dbt docs |
| **告警** | 运行失败通知（Slack/Email） |
| **RBAC** | 角色权限管理 |

### 环境配置

```
Development  → 开发者个人 schema (dev_<name>_)
CI            → PR 专用 schema (dbt_cloud_ci_pr_<id>)
Production   → 生产 schema (analytics)
```

✅ 环境隔离是 dbt Cloud 的**核心安全机制**——开发者不会意外影响生产数据。

---

## 9.3 CI/CD 管道设计

### GitHub Actions 示例

```yaml
# .github/workflows/dbt-ci.yml
name: dbt CI
on: [pull_request]
jobs:
  dbt-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install dbt-snowflake
      - run: dbt deps
      - run: dbt build --select state:modified+
        env:
          DBT_PROFILES_DIR: .
```

### CI 管道阶段

| 阶段 | 命令 | 目的 |
|------|------|------|
| **安装依赖** | `dbt deps` | 安装 packages.yml 中的包 |
| **编译检查** | `dbt compile` | Jinja 语法验证 |
| **构建** | `dbt build --select state:modified+` | 只构建变更模型及下游 |
| **测试** | `dbt test` | 运行所有测试 |
| **Lint** | `sqlfluff lint` | SQL 风格检查 |

✅ `state:modified+` 是 CI 的**关键选择器**——只测试变更影响的模型，大幅节省 CI 时间。

---

## 9.4 编排集成

### dbt + Airflow

```python
# Airflow DAG 中调用 dbt Cloud Job
dbt_run = DbtCloudRunJobOperator(job_id=12345, trigger_rule='all_success')
```

### 编排顺序

```
Extract/Load (Fivetran/Airbyte)
    ↓
dbt run (Transform)
    ↓
dbt test (Quality Check)
    ↓
Reverse ETL (Census/Hightouch)
    ↓
BI Tools (Looker/Tableau)
```

⚠️ dbt 自身不是调度器——生产环境需要外部编排（dbt Cloud 调度器 / Airflow / Dagster）。

---

## 9.5 生产环境最佳实践

### 运行策略

| 实践 | 说明 |
|------|------|
| **分阶段运行** | staging → intermediate → marts 分步执行 |
| **失败快速** | `dbt build --fail-fast` 首个失败即停止 |
| **重试策略** | 网络/临时错误自动重试 1-2 次 |
| **全量刷新周期** | 每周/月执行 `--full-refresh` 清理增量状态 |
| **监控告警** | Slack/Email 通知 + 运行时间趋势 |

### 成本控制

| 策略 | 效果 |
|------|------|
| `--select state:modified+` | CI 只运行变更部分 |
| 合理物化选择 | 减少不必要的 table 重建 |
| 增量模型 | 大表避免全量重建 |
| 开发环境缩小 | dev schema 用 SAMPLE 数据 |

---

## 9.6 🔧 DuckDB / SQLite 类比（部署本地化）

| # | dbt 部署概念 | DuckDB 本地实现 | SQLite 本地实现 | 标注 |
|---|-------------|----------------|----------------|------|
| 1 | `dbt run` 生产执行 | `duckdb analytics.duckdb < run_all.sql` 脚本化执行 | `sqlite3 analytics.db < run_all.sql` | 🔧 非本书引擎行为 |
| 2 | 环境隔离 | 多个 `.duckdb` 文件：`dev.duckdb` / `prod.duckdb` | 多个 `.db` 文件 | 🔧 非本书引擎行为 |
| 3 | CI 检查 | 手动在 `dev.duckdb` 上运行验证查询 | 同 | 🔧 非本书引擎行为 |
| 4 | 调度 | 无内置调度，可用 cron + shell 脚本 | 同 | 🔧 非本书引擎行为 |
| 5 | `dbt build --fail-fast` | 手动脚本中 `set -e` 遇错即停 | 同 | 🔧 非本书引擎行为 |
| 6 | 运行监控 | 无内置监控，需外部日志分析 | 同 | 🔧 非本书引擎行为 |

> 🔧 以上均为**非本书引擎行为**——CI/CD 和调度是 dbt + 外部工具的组合能力。

---

## 9.7 dbt Mesh 与大规模部署

### 多项目架构

```
项目 A (staging) → 项目 B (finance mart)    项目 C (marketing mart)
数据平台团队       财务域团队                  营销域团队
```

| 概念 | 说明 |
|------|------|
| **跨项目 ref** | `{{ ref('project_a', 'stg_orders') }}` |
| **项目契约** | 公共模型接口约定 |
| **独立部署** | 各项目独立 CI/CD |

⚠️ dbt Mesh 适合 10+ 开发者的大型组织——小团队单项目即可。

---

## 核心概念速览（中英对照）

| 中文概念 | English Term | 一句话定义 |
|---------|-------------|-----------|
| 持续集成 | Continuous Integration (CI) | PR 合并前自动运行 dbt 检查和测试 |
| 持续部署 | Continuous Deployment (CD) | 代码合并后自动部署到生产环境 |
| 编排 | Orchestration | 协调 dbt 与 EL/Reverse ETL 的外部调度 |
| 环境隔离 | Environment Isolation | dev/staging/prod 使用独立 schema |
| 精简 CI | Slim CI | 基于 state:modified 只运行变更部分 |
| dbt 网格 | dbt Mesh | 多个 dbt 项目通过跨项目 ref 协作 |
| 快速失败 | Fail Fast | 遇到首个错误立即停止执行 |

---

## 最新演进与工业实践

| 时间 | 演进 | 影响 |
|------|------|------|
| 2022 | dbt Cloud 调度器 GA | dbt Cloud 成为一站式部署平台 |
| 2023 | dbt-core 1.5 | CI 中 `state:modified+` 性能优化 |
| 2024 | dbt Mesh GA | 跨项目 ref 正式稳定，大规模部署成为可能 |
| 2025 | dbt Cloud AI | AI 辅助 SQL 审查 + 自动优化建议 |
| 2026 | dbt 2.0 | 新部署架构、性能引擎重写 |

> 📖 与 `../Unlocking_dbt/` 关联：
> - Unlocking_dbt Ch11 (dbt in Production) → 生产部署的深度实践
> - Unlocking_dbt Ch12 (dbt Mesh) → 多项目架构的详细指南
>
> 📖 与 `../Data_Mesh/`（#201）关联：
> - #201 Ch4 (自助数据平台) → dbt Mesh 是自助平台的技术实现
> - #201 Ch5 (联邦计算治理) → 多项目 dbt 的治理模型
> - #201 Ch8 (多平面数据平台) → dbt Mesh 架构与多平面架构的对应关系
