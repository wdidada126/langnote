# 01 · Introduction to dbt

> Ch 1 pp 1–43 | DOI: 10.1007/979-8-8688-1844-8_1

---

## 学习目标

- 理解 dbt 在现代数据栈中的定位与价值主张
- 区分 dbt Core（开源）与 dbt Cloud（商业）
- 掌握 ELT vs ETL 范式转换的核心理念
- 了解 dbt 项目的典型生命周期

---

## 1.1 dbt 是什么

dbt (data build tool) 是一个 **SQL-first 的数据转换工具**，将软件工程最佳实践（版本控制、测试、文档、CI/CD）引入数据分析领域。

### 核心定位

- **不做数据摄入 (extraction/loading)** — 只负责 **T (transformation)**
- 输出 SQL → 发送到数据仓库执行
- 管理模型之间的 **依赖关系 (DAG)**

### ELT vs ETL

| 维度 | ETL | ELT (dbt 范式) |
|------|-----|----------------|
| 转换位置 | 专用引擎 | 数据仓库内部 |
| 计算弹性 | 受限 | 利用仓库算力 |
| 可调试性 | 黑盒 | SQL 透明 |
| 增量策略 | 引擎特定 | 仓库原生 |

> ✅ dbt 官方定义: "dbt compiles and runs SQL against your data warehouse"

---

## 1.2 dbt Core vs dbt Cloud

| 维度 | dbt Core | dbt Cloud |
|------|----------|-----------|
| 性质 | 开源 CLI (MIT) | 商业 SaaS |
| 部署 | 本地 / CI / 自建编排 | 托管服务 |
| IDE | 本地编辑器 + VS Code | 浏览器 Web IDE |
| 调度 | 需外部 (Airflow 等) | 内置 Scheduler |
| 协作 | Git-only | Git + 代码审查 + 通知 |
| Discovery API | ❌ | ✅ GraphQL |
| 适合场景 | 小团队 / 成本敏感 | 企业级 / 需要全托管 |

> ⚠️ dbt Cloud 有免费开发者层 (Free plan)，个人学习可用。

---

## 🔧 1.3 DuckDB / SQLite 类比

> 以下类比使用 DuckDB/SQLite 概念辅助理解，**非本书引擎行为**。

| # | dbt 概念 | DuckDB 类比 | SQLite 类比 |
|---|---------|-------------|-------------|
| 1 | dbt DAG 编译 | DuckDB 的 `CREATE VIEW` 链式依赖解析 | SQLite 的视图依赖追踪 |
| 2 | ELT: 先 load 再 transform | DuckDB `COPY INTO` + SQL 转换 | SQLite `IMPORT` + SQL |
| 3 | dbt 适配器模式 | DuckDB 的 `ATTACH` 多引擎 | SQLite 的 VFS 层 |
| 4 | ref() 依赖声明 | DuckDB 跨 schema 引用 | SQLite 跨 database 引用 |

---

## 1.4 dbt 项目生命周期

```
dbt init → dbt run → dbt test → dbt docs generate → dbt deploy
```

1. **init**: 脚手架创建项目结构
2. **run**: 编译 Jinja → SQL → 发送到仓库执行
3. **test**: 运行 schema test + data quality test
4. **docs generate**: 生成 lineage + 文档站点
5. **deploy**: CI/CD 管道推送到生产

---

## 1.5 现代数据栈中的 dbt

```
[Source Systems] → [Fivetran/Airbyte] → [Raw Data in Warehouse]
                                                  ↓
                                            [dbt Transformations]
                                                  ↓
                                   [Analytics-Ready Models in Warehouse]
                                                  ↓
                              [BI Tools / Semantic Layer / Reverse ETL]
```

dbt 位于 **Raw → Analytics-Ready** 的核心位置，是现代数据栈的 "transform" 层标准工具。

---

## 1.6 关键目录结构

```
project_name/
├── dbt_project.yml      # 项目配置
├── models/              # SQL 模型
│   ├── staging/         # 贴源层
│   ├── intermediate/    # 中间层
│   └── marts/           # 集市层
├── tests/               # 自定义数据测试
├── macros/              # Jinja 宏
├── seeds/               # CSV 种子数据
├── snapshots/           # 快照 (SCD2)
├── analyses/            # 不物化的分析 SQL
└── packages.yml         # 依赖包
```

---

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
|------|---------|--------|
| 数据转换 | Data Transformation | dbt 的核心职责 |
| 依赖图 | DAG (Directed Acyclic Graph) | 模型间 ref 关系 |
| 适配器 | Adapter | 连接不同仓库的插件 |
| 物化 | Materialization | 模型在仓库中的存储方式 |
| 编译 | Compilation | Jinja → 纯 SQL 的过程 |
| 开源/商业 | Core / Cloud | 两种使用形态 |

---

## 最新演进与工业实践

- **dbt Fusion 引擎** (2025 beta): 新一代执行引擎，性能大幅提升 ⚠️ [docs.getdbt.com/docs/dbt-versions/2025-release-notes](https://docs.getdbt.com/docs/dbt-versions/2025-release-notes)
- **dbt MCP Server** (2025-10 GA): Model Context Protocol 集成，支持 AI Agent 调用 dbt 元数据
- **VS Code 扩展** (2025-05 beta): 官方 dbt 编辑器体验
- **Copilot 集成**: dbt Cloud 内置 AI 辅助，要求 UTF-8 编码
- ⚠️ 本书 Ch1 的 Core vs Cloud 对比在 Fusion 引擎推出后需要更新：Fusion 同时适用于 Core 和 Cloud
