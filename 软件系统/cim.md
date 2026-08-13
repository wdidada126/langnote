# cim系统

工厂设备的数据采集系统

CIM（Computer Integrated Manufacturing，计算机集成制造）系统软件供应商在半导体、泛半导体等行业中扮演着至关重要的角色。以下是一些CIM系统软件供应商的相关信息，按照清晰的结构进行分点和归纳：

国产CIM系统软件供应商
哥瑞利
成立时间：2007年
融资情况：已完成D轮融资，由国家级基金、产业方、知名基金共同投资
产品与服务：专注于打造中国自有的泛半导体领域CIM系统，长期服务半导体、面板、光伏、PCB及PCBA等各行业龙头
竞争优势：国内少有的拥有整厂解决方案能力的供应商，具备与头部外资供应商竞争的实力，已完成600多个项目，实现了多个泛半导体行业的端到端全覆盖
赛美特
融资情况：完成超5亿元C轮融资，投后估值超60亿元
技术团队：技术人员占比80%以上，拥有超过700名员工
产品与服务：提供高性能、高可用性、高可靠性的一站式国产CIM解决方案，覆盖生产管理、品质管理、物流管理、经营管理等领域
成功案例：自研的CIM解决方案已在7家12吋晶圆厂得到验证，协助解决高工艺、高成本、高良率、高产量等挑战
国外CIM系统软件供应商
IBM
成立时间：1911年
CIM系统产品：推出了POSEIDEN系统和基于POSEIDEN系统的SiView系统，可实现全自动化的单晶圆控制，并处理在同一产线中多批次的产品
市场地位：在半导体CIM领域占据重要地位，其SiView系统被格芯、台积电等厂商所采用
Applied Materials（应用材料）
成立时间：1967年
CIM系统产品与服务：作为全球最大的半导体设备和服务供应商，应用材料在CIM系统领域也有布局，但具体产品与服务信息在提供的参考文章中未详细提及
总结
CIM系统软件供应商在半导体和泛半导体行业中发挥着关键作用，国内外均有领先的供应商。国产供应商如哥瑞利和赛美特在政策和资本的支持下，正逐步崛起并与国际巨头竞争。同时，国际供应商如IBM和应用材料凭借其强大的技术实力和丰富的行业经验，在市场上仍占据重要地位。

## Intel CIM 与 Applied Materials 产品辨析（截至 2026-08）

### 结论

- 原文将 CIM 写成“工厂设备的数据采集系统”过于狭窄。CIM 是制造执行、设备自动化、物料搬运、工艺与质量数据等环节组成的工厂级集成体系；设备数据采集只是基础能力，通常由 EAP、SECS/GEM、FDC 等组件承担。
- 不能根据公开资料把“Intel 的 CIM 系统”直接认定为 Applied Materials（AMAT）的某一个产品。Intel 公开材料说明其各工厂使用 MES 跟踪设备和物料状态，并由 MES 协调其他自动化系统，但没有披露 MES 的产品名或供应商。因此，“Intel CIM = FAB300”或“Intel CIM = PROMIS”都不应当作为事实写入笔记。
- 若问题是“应用材料历史上用于晶圆厂 CIM/MES 的产品叫什么”，最接近的产品名是 **FAB300**。它源自 AMAT 于 1998 年收购的 Consilium；2000 年发布的 FAB300 2.0 面向 300 mm 晶圆厂，属于 fab management / MES 产品，覆盖晶圆管理、派工、工艺和设备管理等能力。
- AMAT 当前对外使用的是 **Applied SmartFactory CIM Solution** 这一解决方案名称，而非一个名为“Intel CIM”的单品。其中 **PROMIS** 是其 MES 产品；解决方案还覆盖制造执行、工艺质量、工厂生产率和供应链四个域。历史系统、版本和客户现场部署不能仅凭当前产品页反推。

### 名称与边界

| 名称 | 所属方 | 定位 | 与“Intel CIM”的关系 |
| --- | --- | --- | --- |
| FAB300 | Applied Materials 历史产品线 | 面向 300 mm 晶圆厂的 fab management / MES | 是 AMAT 历史上最接近 CIM/MES 的产品名；没有公开证据证明 Intel 使用它 |
| PROMIS | Applied SmartFactory / AMAT | 当前 MES 产品 | 可作为 AMAT CIM 方案中的 MES 候选，不等同于 Intel 的已确认部署 |
| Applied SmartFactory CIM Solution | Applied SmartFactory / AMAT | CIM 整体解决方案 | 是当前解决方案总称，包含 MES、质量、生产率和供应链能力 |
| Intel Automated Factory Solutions | Intel | 工厂数字孪生、仿真和优化能力 | 是 Intel 自己对外介绍的工厂自动化产品组合，不是 AMAT CIM 产品 |

### Intel 公开描述的 CIM 结构

Intel 的公开智能工厂资料可归纳为下列链路，具体实现供应商需以项目合同、现场系统界面或运维资料为准：

```text
计划/排产
    -> MES：维护批次、工艺路线、设备与物料生产状态，编排制造活动
    -> EAP/设备自动化：通过 SECS/GEM 等接口下发配方、采集设备状态和事件
    -> AMHS/MCS：搬运晶圆盒并回传物料位置、任务状态
    -> FDC/SPC/APC/良率分析：发现异常、控制漂移、反馈工艺调整
    -> 数据平台/数字孪生：分析瓶颈、验证调度策略和优化方案
```

MES 是中心编排层，不等于数据采集系统；CIM 则是上述系统及其业务、数据和自动化接口组成的整体。Intel 当前公开的 Factory Pathfinder、Recon、Optimizer、Adapter 等，更偏向工厂数字孪生、数据接入与优化，不能据此替代或推断其底层 MES/CIM 厂商。

### 如何确认某个 Intel 现场的实际产品

1. 优先查看采购合同、软件许可、项目验收资料和运维服务单，其中应包含产品名称、版本与供应商。
2. 查看系统登录页、帮助页面、部署包、数据库 schema、接口文档和服务进程名称，区分 MES、EAP、MCS、FDC 等不同层次。
3. 对历史项目同时确认投产年份和升级记录。AMAT 曾在 2006 年宣布收购 Brooks Software，其后产品组合和名称发生过演变；不能用今天的产品页直接给早期项目定名。

### 参考资料

- Applied Materials：Consilium 发布 FAB300 2.0 的新闻稿（2000），说明其 300 mm fab management/MES 定位及 SEMI CIM Framework 兼容性：<https://ir.appliedmaterials.com/news-releases/news-release-details/consilium-launches-semiconductor-industrys-most-advanced-fab/>
- Applied SmartFactory：当前 CIM Solution 的四个能力域：<https://appliedsmartfactory.com/semiconductor-blog/manufacturing-execution/cim-solution/>
- Applied SmartFactory：PROMIS MES 产品页：<https://appliedsmartfactory.com/manufacturing-execution-solutions/promis/>
- Intel IT：MES 在工厂中跟踪设备和物料状态、协调自动化系统的说明：<https://www.intel.com/content/dam/www/public/us/en/documents/best-practices/using-big-data-in-manufacturing-at-intels-smart-factories-paper.pdf>
- Intel：Automated Factory Solutions 概览：<https://www.intel.com/content/www/us/en/content-details/789047/intel-automated-factory-solutions-overview.html>
