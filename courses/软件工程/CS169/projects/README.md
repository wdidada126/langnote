# CS169 配套项目计划（骨架，本轮不写代码）

主语言：Ruby 3.x + Ruby on Rails（与课程一致），前端按需引入 Hotwire/React。
组织方式：整门课做成**一个持续演进的 SaaS 应用**（对应原版 homeworks + capstone），按讲次里程碑推进；每个里程碑一个目录/标签，含 `build.sh`（bundle + db:prepare + 测试），本轮只写不编译。
项目主题建议：`StudyBuddy` —— 学习小组预约与自习室座位 SaaS（含日历、通知、指标看板），够跑完 14 讲的所有实践。

| 章节（讲次） | 建议语言 | 小项目 / 里程碑 | 编译方式 |
| --- | --- | --- | --- |
| L1–L3 团队与流程 | Markdown + GitHub | 团队章程 + Issue 看板 + 分支保护规则；仓库内记录 DoD 与 review SLA | 无编译（GitHub Settings + PR 模板） |
| L4 第一次部署 | Rails 7 | 脚手架应用上线：Procfile、环境变量、健康检查路由 `/up` | `build.sh`: `bundle install && bin/rails db:prepare && foreman start -f Procfile.dev` |
| L5 MVC 与 ActiveRecord | Rails | 领域建模：User/Group/Booking/Room 模型 + 迁移 + 资源路由 + 表单 | `bundle exec rails test`；`build.sh` 同上 |
| L6 TDD | Ruby + Minitest/RSpec | 预约冲突检测逻辑：先写 12 个失败用例再实现（含时区边界） | `bundle exec rails test:system` + 覆盖率 `simplecov` |
| L7 结对与审查 | — | 两次强制结对会话 + 每人 ≥5 次 PR 审查记录（模板化评论） | 无编译；`docs/reviews/` 存档 |
| L8 估点与迭代 | 表格/看板 | 3 个迭代的规划扑克记录、速度趋势与燃尽图（CSV 导出） | 无编译；脚本 `scripts/velocity.rb` 生成 CSV |
| L9 CI/CD | GitHub Actions + Ruby | 流水线：lint(RuboCop) + test + build + 自动部署 staging；加特性开关 | `.github/workflows/ci.yml`（本地等价 `./build.sh ci`） |
| L10 重构 | Ruby | 把胖控制器抽成 Service Object/Form Object；前后 diff + 基准测试不变 | `bundle exec rails test`（全绿）+ `rubocop --autocorrect` 报告 |
| L11 性能与队列 | Ruby + Redis/Sidekiq | N+1 消除 + 片段缓存 + 异步邮件通知；慢查询看板 | `build.sh`: `bundle && rails db:prepare && sidekiq -c 3`（ Procfile 多进程） |
| L12 数据模型取舍 | Ruby + MongoDB(可选) | 把"事件流/活动日志"迁到文档存储，写迁移与一致性对比报告 | Docker Compose 起 Mongo；`bundle exec rails test:integration` |
| L13 安全加固 | Ruby | 引入 Devise + 授权策略(Pundit)、CSRF/XSS/越权回归测试、依赖扫描 | `bundle exec brakeman -A` + `bundle audit check --update`；测试门禁 |
| L14 运营与实验 | Ruby + JS | 埋点与看板（留存/漏斗）、A/B 分流特性开关、SLO 与错误预算文档 | `build.sh release`：`rails assets:precompile && rails test && deploy --canary 20%` |

> Capstone 验收清单（结课演示）：真实用户 ≥3 人、有可回滚的发布流程、有指标看板、有安全回归测试、有迭代回顾记录。
> 迁移备忘：原版课程依赖 Heroku 免费档（已于 2022-11 关闭），本项目所有 `build.sh` 必须能在本地 Docker 与 Fly.io/Render 任一路径跑通，并把平台差异写进 `notes/L4`。
