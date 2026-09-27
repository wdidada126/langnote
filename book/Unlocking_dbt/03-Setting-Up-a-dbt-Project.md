# 03 · Setting Up a dbt Project

> Ch 3 pp 97–133 | DOI: 10.1007/979-8-8688-1844-8_3

---

## 学习目标

- 掌握 `dbt init` 创建项目的完整流程
- 理解 `dbt_project.yml` 核心配置项
- 配置 profiles.yml 连接目标数据仓库
- 建立项目目录结构规范

---

## 3.1 dbt init 流程

```bash
dbt init my_project
# 交互式选择:
#   - 数据库适配器 (snowflake/bigquery/redshift/...)
#   - 认证方式
#   - 项目名
```

生成的项目骨架:

```
my_project/
├── dbt_project.yml
├── profiles.yml        # 通常放 ~/.dbt/profiles.yml
├── models/
│   └── example/
│       ├── my_first_dbt_model.sql
│       ├── my_second_dbt_model.sql
│       └── schema.yml
├── macros/
├── tests/
├── seeds/
├── snapshots/
└── analyses/
```

---

## 3.2 dbt_project.yml 核心配置

```yaml
name: 'my_project'
version: '1.0.0'
config-version: 2

profile: 'my_profile'     # 对应 profiles.yml 中的 key

model-paths: ["models"]
seed-paths: ["seeds"]
test-paths: ["tests"]
analysis-paths: ["analyses"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"      # 编译输出
clean-targets: ["target", "dbt_packages"]

models:
  my_project:
    staging:
      +materialized: view
    intermediate:
      +materialized: view
    marts:
      +materialized: table
```

> ✅ `config-version: 2` 是当前标准，旧版 `config-version: 1` 已弃用。

---

## 3.3 profiles.yml 与连接配置

```yaml
my_profile:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: xxx.snowflakecomputing.com
      user: my_user
      password: "{{ env_var('DBT_PASSWORD') }}"
      role: TRANSFORMER
      database: ANALYTICS
      warehouse: COMPUTE_WH
      schema: DBT_DEV
      threads: 4
    prod:
      type: snowflake
      # ... 生产环境配置
```

> ⚠️ 密码等敏感信息应使用 `env_var()` 或环境变量，**切勿明文提交 Git**。

---

## 🔧 3.4 DuckDB / SQLite 类比

> 以下类比使用 DuckDB/SQLite 概念辅助理解，**非本书引擎行为**。

| # | dbt 概念 | DuckDB 类比 | SQLite 类比 |
|---|---------|-------------|-------------|
| 1 | profiles.yml 连接配置 | DuckDB connection string + `ATTACH` | SQLite `.open` + PRAGMA |
| 2 | dbt_project.yml 项目配置 | DuckDB 无对应（需外部脚本） | SQLite 无对应 |
| 3 | `dbt init` 脚手架 | 无直接对应 | 无直接对应 |
| 4 | target-path 编译输出 | DuckDB `EXPORT` 输出目录 | SQLite `.output` 文件 |

---

## 3.4 环境管理策略

| 策略 | 说明 | 适用场景 |
|------|------|---------|
| Schema 隔离 | dev/prod 用不同 schema | 最常用 ✅ |
| Database 隔离 | dev/prod 用不同 database | 强隔离需求 |
| Account 隔离 | 不同云账号 | 企业级 |
| `dbt run --target` | CLI 切换 target | 日常开发 |

---

## 3.5 包管理 (packages.yml)

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: "1.1.1"
  - package: calogica/dbt_expectations
    version: "0.10.1"
  - git: "https://github.com/my-org/my-dbt-macros.git"
    revision: main
```

```bash
dbt deps    # 安装依赖到 dbt_packages/
```

---

## 3.6 版本控制最佳实践

- ✅ `dbt_project.yml`, `models/`, `macros/`, `seeds/`, `snapshots/` → **纳入 Git**
- ❌ `profiles.yml`, `target/`, `dbt_packages/`, `logs/` → **Git 忽略**
- ✅ 使用 `.gitignore` 模板:

```
target/
dbt_packages/
logs/
profiles.yml
*.pyc
```

---

## 3.7 第一个 dbt run

```bash
cd my_project
dbt debug          # 验证连接
dbt deps           # 安装依赖
dbt run            # 执行所有模型
dbt test           # 运行测试
dbt docs generate  # 生成文档
dbt docs serve     # 本地预览
```

---

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
|------|---------|--------|
| 项目配置 | dbt_project.yml | 项目元数据与默认设置 |
| 连接配置 | profiles.yml | 数据仓库连接凭证 |
| 目标环境 | Target / Output | dev/prod 环境切换 |
| 包管理 | Package Management | 复用社区宏与测试 |
| 脚手架 | Scaffolding (dbt init) | 项目初始化模板 |
| 依赖安装 | dbt deps | 下载 packages.yml 声明的包 |

---

## 最新演进与工业实践

- **dbt Fusion 引擎** (2025 beta): 项目配置中可通过 `flags` 启用 Fusion 编译路径 ⚠️ [docs.getdbt.com/docs/dbt-versions/2025-release-notes](https://docs.getdbt.com/docs/dbt-versions/2025-release-notes)
- **VS Code 扩展** (2025-05 beta): 官方扩展提供项目初始化向导和 profiles.yml 验证
- **JSON Schema 严格校验** (v1.11): dbt_project.yml 现在支持 JSON Schema 验证，减少配置错误
- ⚠️ 本书 Ch3 的 `dbt init` 交互流程在 VS Code 扩展中已有图形化替代
