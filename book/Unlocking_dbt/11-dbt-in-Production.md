# 11 · dbt in Production

> Ch 11 pp 381–406 | DOI: 10.1007/979-8-8688-1844-8_11

---

## 学习目标

- 掌握 dbt 从开发到生产的部署流程
- 理解 CI/CD 管道设计 (GitHub Actions / GitLab CI)
- 掌握 dbt Cloud 的 Job 调度与通知
- 了解环境管理 (dev / staging / prod) 策略

---

## 11.1 部署模式

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| dbt Cloud | 全托管 SaaS | 企业级首选 |
| CLI + CI/CD | GitHub Actions / GitLab CI | 成本敏感 / 定制需求 |
| CLI + 编排器 | Airflow / Dagster / Prefect | 复杂依赖编排 |

---

## 11.2 dbt Cloud Jobs

```yaml
# dbt Cloud Job 配置
Job: "Production Run"
  Schedule: "0 6 * * *"   # 每天 6:00 AM
  Commands:
    - dbt build --select state:modified+
  Environment: Production
  Triggers:
    - on_schedule: true
    - on_merge: false
```

### Slim CI

```bash
# dbt Cloud CI Job
dbt build --select state:modified+ --defer
```

- `state:modified+`: 仅构建受代码变更影响的模型
- `--defer`: 未变更的模型引用生产环境的结果

> ✅ Slim CI 大幅缩短 PR 检查时间，只测试受影响的部分。

---

## 11.3 GitHub Actions CI/CD

```yaml
# .github/workflows/dbt-ci.yml
name: dbt CI
on:
  pull_request:
    branches: [main]

jobs:
  dbt-ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install dbt-snowflake
      - run: dbt deps
      - run: dbt build --target ci
        env:
          DBT_PASSWORD: ${{ secrets.DBT_PASSWORD }}
```

---

## 11.4 环境管理策略

| 环境 | Schema/Database | 用途 | 数据 |
|------|----------------|------|------|
| dev | `dbt_<user>` | 个人开发 | 子集/采样 |
| staging | `dbt_staging` | 集成测试 | 全量 |
| prod | `analytics` | 生产消费 | 全量 |

### 环境切换

```bash
dbt run --target dev      # 开发
dbt run --target prod     # 生产
```

---

## 11.5 生产最佳实践

### 运行策略

```bash
# 生产环境推荐: build = run + test + snapshot
dbt build --target prod
```

- ✅ `dbt build` 按依赖顺序执行 run → test → snapshot
- ✅ 测试失败时下游模型不执行 (fail-fast)

### 错误处理

| 策略 | 说明 |
|------|------|
| `--fail-fast` | 首个错误即停止 |
| `--warn-error` | 将警告视为错误 |
| `--continue-on-error` | 跳过失败继续执行 |

---

## 11.6 监控与告警

### dbt Cloud 通知

- Slack 集成: run 成功/失败通知
- Email 通知
- Webhook: 自定义集成

### 外部监控

```python
# 通过 Discovery API 监控
import requests
query = """
{
  jobRuns(accountId: 123, environmentId: 456) {
    status
    completedAt
  }
}
"""
```

---

## 11.7 性能优化

| 策略 | 说明 |
|------|------|
| 合理物化 | staging=view, marts=table |
| 增量模型 | 大表使用 incremental |
| 并行度 | `threads: N` 控制并发 |
| Slim CI | 仅处理变更部分 |
| 仓库分区 | 利用仓库的 clustering/partitioning |

---

## 11.8 安全与权限

- ✅ 生产环境使用专用 service account
- ✅ 遵循最小权限原则
- ✅ 密码/密钥使用环境变量或 Secret Manager
- ✅ 定期轮换凭证
- ⚠️ 避免在 dev 环境使用生产凭证

---

## 🔧 11.9 DuckDB / SQLite 类比

> 以下类比使用 DuckDB/SQLite 概念辅助理解，**非本书引擎行为**。

| # | dbt 概念 | DuckDB 类比 | SQLite 类比 |
|---|---------|-------------|-------------|
| 1 | dbt build (run+test+snapshot) | DuckDB 脚本串联多步 SQL | SQLite 脚本串联多步 SQL |
| 2 | slim CI (state:modified+) | 无直接对应（需自建 diff 逻辑） | 无直接对应 |
| 3 | 多环境 target 切换 | DuckDB 多 `ATTACH` 切换 database | SQLite 多 `.open` 切换 database |
| 4 | threads 并行度 | DuckDB 自动并行（内部线程池） | SQLite 单线程（WAL 模式有限并发） |

---

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
|------|---------|--------|
| 持续集成 | CI (Continuous Integration) | PR 自动测试 |
| 持续部署 | CD (Continuous Deployment) | 自动部署到生产 |
| 精简 CI | Slim CI | 仅构建受影响的模型 |
| 构建命令 | dbt build | run + test + snapshot 一体化 |
| 环境管理 | Environment Management | dev/staging/prod 隔离 |
| 监控告警 | Monitoring & Alerting | 运行状态追踪 |

---

## 最新演进与工业实践

- **dbt Cloud CI/CD 增强** (2025): 支持 GitHub Checks API 直接在 PR 中显示 dbt 结果 ⚠️ [docs.getdbt.com/docs/deploy/ci-cd](https://docs.getdbt.com/docs/deploy/ci-cd)
- **Fusion 引擎**: 生产 run 性能大幅提升，大项目从小时级降到分钟级 ⚠️ [getdbt.com/blog/dbt-core-v1-11-is-ga](https://www.getdbt.com/blog/dbt-core-v1-11-is-ga)
- **dbt MCP Server** (2025-10 GA): 可通过 AI Agent 触发和监控 dbt 运行
- **Dagster + dbt**: 深度集成，dbt assets 直接映射为 Dagster software-defined assets
