# 08 Snowflake Security Overview（pp.129–145 ✅ Crossref）

> 章定性：安全总览章——网络/加密/认证/访问控制/数据防护的五层心智，2019 时点恰逢"secure view
> 时代"向"策略时代"过渡的前夜。章题/页码 ✅ Crossref `_8`；小节 ⚠️ 推定；SQL 自拟示意；
> 机制 ⚠️ 转述 + ✅ curl-200 URL；本章无独立 🔧（RBAC 无本地引擎可比面，避免误导）。

## 1. 章节定位与叙事线

本章把云数仓安全拆成可记忆的纵向分层：①网络层（无入站端口、出站单向、私网连接可选）；②加密
（传输 TLS、静态 AES-256 体系与密钥轮换 ⚠️ 官方口径）；③认证（账密→MFA→SSO/SAML→密钥对→
OAuth 的强度阶梯）；④授权（07 章角色金字塔的语义深化：特权、所有权 TRANSFER、GRANT 继承边界）；
⑤数据级防护（2019 主流做法=**安全视图藏列藏行**、脱敏以视图 CASE 手搓 ⚠️ 时代原话）。作者
强调"安全是共享与协作的前提"——为 10 章共享铺心理地基。

## 2. 知识提纲（⚠️ 推定小节）

| # | 推定小节 | 2019 形态 | 现状锚点（✅ curl-200） |
| --- | --- | --- | --- |
| 1 | 网络隔离与连通 | 无监听端口/代理白名单 | security-access-control-overview 族 |
| 2 | 加密与密钥体系 | 全量默认加密、无用户配置 | user-guide/security-encryption |
| 3 | 认证强度阶梯 | SSO 已 GA、MFA 内建 | access-control-overview ⚠️ |
| 4 | RBAC 与对象授权 | 角色+GRANT 双轴 | access-control-overview |
| 5 | 所有权与特权 | OWNERSHIP/TRANSFER | access-control-overview |
| 6 | 行/列级防护（时代做法） | 安全视图包装 | user-guide/views-secure |
| 7 | 审计萌芽 | ACCOUNT_USAGE 视图族 | sql-reference/account-usage |

## 3. 深读与机制重构

**（a）默认即安全的边界（⚠️ 转述）**：加密对用户不可配也不可关——这是与自建数据库最大的
文化差异；可配的是**接入路径**（网络/私有链接）与**身份强度**（MFA/SSO）。锚点：✅
https://docs.snowflake.com/en/user-guide/security-encryption、✅
https://docs.snowflake.com/en/user-guide/security-access-control-overview。

**（b）授权语义的三个"不可"（2019 至今稳定 ✅ access-control-overview）**：权限不跨库级联
（每库每 schema 单独 GRANT ⚠️ 粒度细节以现文为准）；OWNERSHIP 唯一且只能 TRANSFER；角色继承
经 GRANT OF ROLE 而非通配。样板（自拟示意，非书中原文）：

```sql
GRANT USAGE ON DATABASE sales TO ROLE analyst_ro;
GRANT USAGE ON SCHEMA sales.core TO ROLE analyst_ro;
GRANT SELECT ON VIEW sales.core.v_orders_masked TO ROLE analyst_ro;  -- 视图藏敏：时代做法
-- 2019 手搓脱敏（反面教材，2026 已退役 ⚠️）：
CREATE SECURE VIEW sales.core.v_orders_masked AS
SELECT id, CASE WHEN CURRENT_ROLE()=' pii_auditor ' THEN ssn
                ELSE 'XXX-XX-'||RIGHT(ssn,4) END AS ssn, amount
FROM sales.core.orders;
```

**（c）安全视图的历史位置**：`views-secure` 页今天仍在 ✅
https://docs.snowflake.com/en/user-guide/views-secure（已标"被策略取代"语义 ⚠️），本章的
"以视图为策略载体"在 2020+ 被 ** masking policy + row access policy** 结构化取代（演进节）——
读本章时最有价值的不是做法而是问题清单：谁能看哪几行、哪几列、什么场景（列/行/场景三问）。

**（d）审计的地基**：2019 可自证的审计面=ACCOUNT_USAGE 视图族（LOGIN/QUERY/ACCESS 雏形）✅
https://docs.snowflake.com/en/sql-reference/account-usage；成熟的 ACCESS_HISTORY 血缘审计是
后续年份补齐 ⚠️。

## 4. 深读问答（自拟）

**Q1：为什么"无入站端口"降低一整类风险？** A：攻击面收敛到认证与授权两层，网络渗透需先过
身份；反向出站+单向隧道也让数据外流路径可见 ⚠️+✅ access-control-overview。
**Q2：SECURE VIEW 与 MASKING POLICY 的本质差别？** A：前者把策略**编译进 SQL**（每表一套视图、
策略变更=改视图），后者把策略**挂到列/标签**上（策略与查询解耦、可随角色/标签翻转）✅
views-secure / ✅ tag-based-masking-policies。
**Q3：本章最该带走的心智？** A："纵深=每层各挡一类敌"：网络挡扫描、加密挡拖库、认证挡冒充、
授权挡越权、数据策略挡合法但危险的目光。

## 5. 与其他书/章联系

- 07（组织角色图）→ 08（本章语义层）→ 10（共享把两者外推到跨账号）。
- 09 章半结构化列的脱敏在 2026 也由标签+策略覆盖（提前引用本章 §演进）。
- [../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md](../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md)：授权矩阵全表（波1 ✅）；[../Tuning_the_Snowflake_Data_Cloud/00-总览与阅读地图.md](../Tuning_the_Snowflake_Data_Cloud/00-总览与阅读地图.md)：安全特性对性能/成本的隐性影响（波8 ✅）；[../Advanced_Snowflake/00-总览与阅读地图.md](../Advanced_Snowflake/00-总览与阅读地图.md) ⚠️ 降级册仅辨析。

## 6. 本章检验点

1. 复述五层纵深各挡什么、各配什么对象。
2. 写出列脱敏的"时代做法 vs 现行做法"两句 SQL 对照。
3. 说明 OWNERSHIP 与普通 PRIVILEGES 的关系差异。
4. 解释为何 MFA/SSO 是"认证"而网络策略是"接入"——两者不可互替。

## 7. 认证方式速查卡（2019→2026）

| 方式 | 2019 状态 | 2026 状态 |
| --- | --- | --- |
| 用户名+密码 | 默认 | 仍支持，建议禁用 |
| MFA（内建/Okta) | 可用 | 标配 ✅（现行文档线 ⚠️） |
| SSO/SAML 2.0 | GA | 企业默认 ⚠️ |
| 密钥对 JWT | 面向程序化 | 服务账号主流（05 章呼应） |
| OAuth | 生态早期 | 授权码/细粒度令牌成熟 ⚠️ |

## 8. 取证与标注说明

章题/页码 ✅ Crossref `_8`（pp.129–145）；✅ URL（curl-200）：security-access-control-overview、
security-encryption、views-secure、tag-based-masking-policies、tag-based-row-access-policies、
account-usage；AES/密钥轮换细节与 2019 认证矩阵 ⚠️ 转述；SECURE VIEW 示例为**自拟教学反面
教材**（现建议用策略），非书中原文。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话释义 |
| --- | --- | --- |
| 纵深防御 | defense in depth | 网络/加密/认证/授权/数据五层 |
| 静态加密 | encryption at rest | 默认全量、用户不可关 |
| 传输加密 | encryption in transit | TLS 通道 |
| 单点登录 | SSO / SAML 2.0 | 身份外部化 |
| 多因子认证 | MFA | 密码之上的第二凭证 |
| 特权 | privilege | 对对象的一种可授动作 |
| 所有权 | ownership | 唯一、可转授不可并存的特殊权 |
| 安全视图 | secure view | 行/列策略的 SQL 化（时代做法） |
| 掩码策略 | masking policy | 列级动态脱敏（现行做法 ✅） |
| 行访问策略 | row access policy | 行级过滤绑定表/标签（现行 ✅） |

## 最新演进与工业实践

- **策略化取代视图化（本章第一改写）**：动态脱敏与行过滤成一对可组合对象，并支持**标签绑定**
  批量下发 ✅ https://docs.snowflake.com/en/user-guide/tag-based-masking-policies ✅
  https://docs.snowflake.com/en/user-guide/tag-based-row-access-policies。
- **网络面产品化**：私有链接/VPce、网络策略与 Network Policy Advisor（2026-03 GA ⚠️ 品牌级
  证据见发布说明索引；专页 URL 本目录未逐一验真）。
- **统一治理目录**：Horizon 把身份/策略/分类集中（2025+ ⚠️；实证锚点 ✅
  https://docs.snowflake.com/en/release-notes/2026/other/2026-07-21-delta-sharing-horizon-catalog-ga）。
- **数据保护新形态**：数据保护策略 UI 化预览（2026-05 发布说明 ✅ sitemap 在录 ⚠️ 未逐一验真）、
  端到端加密选项 ✅ https://docs.snowflake.com/en/user-guide/security-encryption-end-to-end。
- **工业实践**：零信任口径下"共享/协作先过策略关"成默认流程——直接呼应 10 章；审计侧
  ACCESS_HISTORY+事件表进 SIEM ⚠️ 转述（✅ account-usage 为地基）。
