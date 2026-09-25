# Spring 系列·总索引

> 本文件是 `book/` 根下 Spring 系列大纲单文件的总索引。仓库中的 Spring 笔记有两种形态：
> ① **大纲式单文件**（本索引收录的主体，含目录摘抄与读书摘记）；
> ② **章节目录**（已拆分为 `book/<书名>/NN-章节.md` 的深度笔记，见「与已建章节目录的互链」一节）。
> 元数据状态标注：✅ 已核实（联网核对）｜📄 来自笔记（以笔记内记录为准）｜⚠️ 待核验。

### 使用约定

- 本索引只做导航与元数据归档，**不改动任何原笔记文件**；重复笔记只标注、待清理时再人工处理。
- 表内「文件」列使用相对链接，在仓库内（含 Obsidian 等工具）可直接跳转。
- 每张表后的「补充备注」逐本记录笔记实况（行数量级、目录覆盖、延伸线索），供快速判断是否值得重读或升级为章节目录。
- 新增 Spring 大纲笔记时，按四组分表追加一行，并在「收录统计」同步计数；若建成章节目录，则移入「互链」一节。

## 阅读路线（分层）

1. **框架本体入门**：`Spring实战5.md` / `Spring揭秘.md` 打底 → 进 `Spring源码深度解析（第2版）.md`（已有章节目录，优先读目录版）啃源码。
2. **Boot 线**：`SpringBoot实战.md`（Walls，薄而经典）→ `springboot从入门到实战.md` / `Springboot应用开发实战.md` 上手 → 原理进阶读 `SpringBoot源码解读与原理分析.md`、`springboot技术内幕.md`、`Springboot揭秘.md`。
3. **Cloud / 微服务线**：`Spring微服务架构设计.md`（架构观）→ Alibaba 系三本（`原理与实战` / `微服务实战` / `架构实战派`）按 Nacos、Sentinel、Seata、RocketMQ、Gateway 逐组件对照读。
4. **Security / Data 专题**：`深入浅出Spring_Security.md` + `SpringSecurity实战.md` + `SpringSecurity原理与实战.md`；数据层读 `SpringDataJPA入门实战与进阶.md`；设计模式视角补 `spring5设计模式.md`、`Spring5核心原理与30个类手写实战.md`。

> **时序提示**：Spring 5 / Boot 2 时代（javax.\* 命名空间）的书籍在 Spring 6 / Boot 3 时代需注意 javax→jakarta 迁移与 AOT / GraalVM Native Image 等变化，老书源码示例需自行换算。

## 一、Spring 框架本体

| 文件 | 书名 | 作者/译者 | 出版社·年份 | ISBN | 一句话定位 | 状态 |
|---|---|---|---|---|---|---|
| [Spring实战5.md](Spring实战5.md) | Spring实战（第5版） | [美]Craig Walls 著；张卫滨 译 | 人民邮电·2020-02 | 9787115527929 | 经典入门，覆盖 Spring 5 / Boot 2 / WebFlux / 微服务 | ✅ |
| [Spring实战4.md](Spring实战4.md) | Spring实战（第4版） | [美]Craig Walls 著（译者待核验） | 人民邮电·2016-04 | 9787115417305 | 上一代经典，针对 Spring 4，与第5版对照读 | ✅（译者⚠️） |
| [Spring揭秘.md](Spring揭秘.md) | Spring揭秘 | 王福强 著 | 人民邮电·2009 | 9787115209429 | 对应 Spring 2.5 时代，IoC/AOP 原理讲得最透的中文老书 | ✅ |
| [Spring源码深度解析（第2版）.md](Spring源码深度解析（第2版）.md) | Spring源码深度解析（第2版） | 郝佳 著 | 人民邮电·2019-01 | 9787115499141 | 中文 Spring 源码第一入口；**已升级为章节目录**，见互链一节 | ✅ |
| [Spring深度分析.md](Spring深度分析.md) | 同上（早期废弃大纲） | 郝佳 著 | 人民邮电·2019 | 9787115499141 | 笔记自标「废弃」，章节结构与《源码深度解析(第2版)》一致，属同一本书的旧笔记 | 📄（重复） |
| [Spring5核心原理与30个类手写实战.md](Spring5核心原理与30个类手写实战.md) | Spring 5核心原理与30个类手写实战 | 谭勇德(Tom) 著 | 电子工业·2019-07 | 9787121367410 | 咕泡学院丛书，手写 30 个核心类还原 Spring 设计 | ✅ |
| [spring5设计模式.md](spring5设计模式.md) | Spring 5 Design Patterns（中译） | [印]Dinesh Rajput 著；梁桂钊/程超/祝坤荣 译 | 中国水利水电·2020-11 | 9787517090557 | 从设计模式视角理解 Spring 框架 | 📄 |
| [学透Spring.md](学透Spring.md) | 学透Spring：从入门到项目实战 | 丁雪丰 著 | 人民邮电·2023-02 | 9787115609113 | 图灵原创，一站式覆盖 Framework/Boot/Cloud 全家桶 | ✅ |
| [看透springmvc.md](看透springmvc.md) | 看透Spring MVC：源代码分析与实践 | 韩路彪 著 | 机械工业·2016-01 | ⚠️待核验 | Spring MVC 九大组件源码分析 | ✅（ISBN⚠️） |
| [Springboot揭秘.md](Springboot揭秘.md) | SpringBoot揭秘：快速构建微服务体系 | 王福强 著 | 机械工业·2016-05 | 9787111536642 | Boot 1 时代的原理科普 | 📄 |

### 补充备注（框架本体）

- `Spring实战5.md`：笔记含完整 5 部分 19 章目录（豆瓣 34949443），第 1 部分「Spring 基础」起步；与第 4 版笔记对照可见 Spring 5 新增响应式与微服务部分。
- `Spring实战4.md`：笔记记录 2016-4 出版、第 5 版 2020 年出版的时间线，含作者 Craig Walls（Pivotal）简介与豆瓣 26767354 链接；正文摘记覆盖第 1 部分「Spring 的核心」。
- `Spring揭秘.md`：豆瓣 3897837；笔记对应 Spring 2.5 时代，摘记覆盖第 1 章「Spring 框架的由来」、IoC 三种注入方式（接口/构造方法/setter）等。
- `Spring源码深度解析（第2版）.md`：豆瓣 30452948，2019 年出版；笔记另含 Spring 5 源码编译踩坑记录（JDK 8/11 环境变量、`repo.spring.io` 插件仓库报错）。
- `Spring深度分析.md`：84 行早期大纲，标题作「Spring源码深入分析」，含两个豆瓣链接（30452948 / 25866350），14 章结构＝第 2 版目录，首行自标「废弃」。
- `Spring5核心原理与30个类手写实战.md`：笔记标注「鼓泡学院（咕泡学院）」，豆瓣 34466260；电子工业出版社官网确认作者谭勇德(Tom)。
- `spring5设计模式.md`：笔记自带完整版权页信息（原作名 Spring 5 Design Patterns，定价 79.00，2020-11）。
- `学透Spring.md`：仅 6 行（豆瓣 36247031 + ISBN 9787115609113），经核实为丁雪丰 2023 年新书；作者亦是《Spring Boot实战》译者与极客时间《玩转Spring全家桶》讲师。
- `看透springmvc.md`：10 行，仅豆瓣 26696099 链接；核实为韩路彪著、机械工业出版社、四篇 22 章（含 Tomcat 实现与九大组件源码）。
- `Springboot揭秘.md`：豆瓣 26808298，出版年 2016-5；笔记定位 spring boot 1，目录自「第 1 章 了解微服务」起。

## 二、Spring Boot

| 文件 | 书名 | 作者/译者 | 出版社·年份 | ISBN | 一句话定位 | 状态 |
|---|---|---|---|---|---|---|
| [SpringBoot实战.md](SpringBoot实战.md) | Spring Boot实战 | [美]Craig Walls 著；丁雪丰 译 | 人民邮电·2016-09 | 9787115433145 | Boot 最薄最经典的入门（图灵）；笔记另含知乎电子书记录 | ✅ |
| [SpringBoot开发实战.md](SpringBoot开发实战.md) | Spring Boot开发实战 | 陈光剑 著 | ⚠️待核验（电子版见知乎读书/得到，2018-08） | ⚠️待核验 | Boot 2.0 + Gradle/Kotlin 视角的综合实战 | 📄（社/ISBN⚠️） |
| [SpringBoot技术实践.md](SpringBoot技术实践.md) | Spring Boot技术实践 | 张子宪 编著 | 清华大学·2021-06 | 9787302577324 | 短平快（149 页），REST+OAuth2+ES+监控 | ✅ |
| [SpringBoot源码解读与原理分析.md](SpringBoot源码解读与原理分析.md) | SpringBoot源码解读与原理分析 | LinkedBear 著 | 人民邮电·2023-02 | 9787115601377 | 基于 Boot 2.3 源码，启动流程/自动装配讲得细 | 📄 |
| [Springboot应用开发实战.md](Springboot应用开发实战.md) | Spring Boot应用开发实战 | 饶仕琪 著 | 清华大学·2021-03 | 9787302575269 | Boot 2.3，含聊天/商城/云盘三个实战项目 | ✅ |
| [springboot2实战之旅.md](springboot2实战之旅.md) | Spring Boot 2实战之旅 | 杨洋(大老杨) 著 | 清华大学·2019-07 | 9787302531623 | 基于 Boot 2.0.3 的坑点实录型入门 | ✅ |
| [springboot从入门到实战.md](springboot从入门到实战.md) | Spring Boot从入门到实战 | 章为忠 著 | 机械工业·2021-11 | 9787111694021 | 「知识点+实例」17 章企业级开发 | 📄 |
| [springboot实战派.md](springboot实战派.md) | Spring Boot实战派 | 龙中华 著 | 电子工业·2019（ISBN 版次见书） | 9787121377365 | 大而全的 Boot + DDD/CQRS 视角实战 | 📄 |
| [springboot技术内幕.md](springboot技术内幕.md) | Spring Boot技术内幕：架构设计与实现原理 | 朱智胜 著 | 机械工业·2020-06 | 9787111657088 | 源码分析系列，Boot 内置/外置组件逐个拆 | ✅ |

### 补充备注（Boot 线）

- `SpringBoot实战.md`：81 行。前半为 Walls 版 8 章目录摘记（第 2 章自动配置原理、属性源优先级 9 条、Actuator）；末尾 2023-09 日常笔记引用了《Spring Boot 编程思想（核心篇）》链接，属延伸线索，未单独建笔记。注意笔记首部「知乎电子书 2016-9」一行与 Walls 纸书并存，章节内容经比对为 Walls 版。
- `SpringBoot开发实战.md`：129 行。陈光剑著，2018 年，代码示例为 Groovy；笔记含三大部分 20 章完整目录（框架基础 / 项目综合实战 / 监控测试运维），知乎读书与微信读书均有电子版。
- `SpringBoot技术实践.md`：笔记自带出版社内容简介与 7 章梗概（Initializr、RESTful、Swagger 2、OAuth 2、Elasticsearch、前后端分离、监控），149 页。
- `SpringBoot源码解读与原理分析.md`：笔记含豆瓣 36244230、ISBN、出版年 2023-2-1 与作者 LinkedBear 简介；另附作者掘金小册课程目录（启动引导 / IOC / 自动装配等）及配套 Gitee 仓库；源码基于 Spring Boot 2.3.11.RELEASE。
- `Springboot应用开发实战.md`：笔记含知乎电子书入口、Gitee 配套代码（spring-boot_app_dev_in_action）、ISBN 与出版年 2021-3。
- `springboot2实战之旅.md`：345 行，笔记以完整 14 章目录为主体（第 1 章 Spring Boot 概述起，含 Boot 版本发展史 1.0–2.0）；作者简介（杨洋/大老杨）取自笔记。
- `springboot从入门到实战.md`：笔记含作者章为忠、2021-11、豆瓣 35676004 与 Gitee 配套代码；面向 Boot 2.x，「知识点+实例」17 章。
- `springboot实战派.md`：豆瓣 34894533；作者龙中华简介（DDD/CQRS 背景）取自笔记，目录自「第 1 章 进入Spring Boot世界」起。
- `springboot技术内幕.md`：318 行，作者朱智胜简介取自笔记（与百度百科/馆藏一致）；笔记含四部分完整目录（准备篇 / 原理篇 / 内置组件篇 / 外置组件篇，共 16 章）。

## 三、Spring Cloud / 微服务

| 文件 | 书名 | 作者/译者 | 出版社·年份 | ISBN | 一句话定位 | 状态 |
|---|---|---|---|---|---|---|
| [Spring微服务架构设计.md](Spring微服务架构设计.md) | Spring微服务架构设计 | [阿联酋]Rajesh R V 著 | 人民邮电·2020-03 | 9787115533753 | 航空公司首席架构师写的微服务架构观 | 📄 |
| [SpringCloudAlibaba微服务原理与实战.md](SpringCloudAlibaba微服务原理与实战.md) | Spring Cloud Alibaba微服务原理与实战 | 谭锋(Mic) 著 | 电子工业·2020-04 | 9787121388248 | 咕泡学院丛书，「场景→原理」讲 Nacos/Sentinel/Seata/RocketMQ | ✅ |
| [SpringCloudAlibaba微服务实战.md](SpringCloudAlibaba微服务实战.md) | Spring Cloud Alibaba微服务实战 | 周仲清 著 | 清华大学·2021-07 | 9787301322710 | 全组件上手手册（含 SkyWalking、XXL-JOB） | 📄 |
| [SpringCloudAlibaba微服务架构实战派.md](SpringCloudAlibaba微服务架构实战派.md) | Spring Cloud Alibaba微服务架构实战派 | 胡弦 著 | 电子工业·2022-01 | 9787121423130 | 篇幅最大（500+ 页）的 Alibaba 组件实战派 | 📄 |
| [Spring_Cloud_Alibaba微服务架构实战派.md](Spring_Cloud_Alibaba微服务架构实战派.md) | —（空壳笔记） | — | — | — | 仅 2 行标题，**判定为上一条的重复笔记**，见重复清单 | 📄（重复） |

### 补充备注（Cloud / 微服务）

- `Spring微服务架构设计.md`：笔记含豆瓣 35018058、ISBN、出版年 2020-3-30 与作者 Rajesh R V（阿联酋航空首席架构师）简介；2024-02 日常笔记中延伸引用了 Sam Newman《微服务设计》。
- `SpringCloudAlibaba微服务原理与实战.md`：24 行，豆瓣 35041576 + ISBN 9787121388248，标注「咕泡学院Java架构师成长丛书」；笔记目录重点在第 4–10 章（服务治理、Nacos、Sentinel、分布式事务、RocketMQ、Gateway）；2023-06 日常笔记另引网关主题延伸阅读。
- `SpringCloudAlibaba微服务实战.md`：23 行，豆瓣 35548919 + ISBN 9787301322710 + 出版年 2021-7，作者周仲清简介取自笔记；目录覆盖第 4–14 章（Nacos、Ribbon、Sentinel、OpenFeign、Dubbo Spring Cloud、Gateway、Seata、Stream、SkyWalking、XXL-JOB、部署）。
- `SpringCloudAlibaba微服务架构实战派.md`：67 行，豆瓣 35671963 + ISBN 9787121423130 + 出版年 2022-1；作者胡弦（杭州电子科技大学硕士，公众号「架构治理之道」）简介取自笔记；目录含基础篇（第 1–9 章）与高级篇（第 10 章起 SkyWalking），篇幅度最大。
- `Spring_Cloud_Alibaba微服务架构实战派.md`：全文仅标题一行 + 空行，无任何内容，判定为重复笔记壳文件。

## 四、Security / Data 专题

| 文件 | 书名 | 作者/译者 | 出版社·年份 | ISBN | 一句话定位 | 状态 |
|---|---|---|---|---|---|---|
| [深入浅出Spring_Security.md](深入浅出Spring_Security.md) | 深入浅出Spring Security | 王松(江南一点雨) 著 | 清华大学·2021-03 | 9787302572763 | 15 章从认证授权讲到 OAuth2，配源码 | ✅ |
| [SpringSecurity实战.md](SpringSecurity实战.md) | Spring Security实战（Spring Security in Action） | [罗]劳伦斯·斯皮尔卡 著；蒲成 译 | 清华大学·2022-01 | 9787302594246 | Manning 引进版，从基础到 OAuth2/K8s 场景 | ✅ |
| [SpringSecurity原理与实战.md](SpringSecurity原理与实战.md) | Spring Security原理与实战（疑） | ⚠️待核验（疑为郑天民，人民邮电·2022，9787115577894） | ⚠️待核验 | ⚠️待核验 | 笔记标注「知乎电子书」，与上述纸书对应关系待核验 | ⚠️ |
| [ProSpringSecurity.md](ProSpringSecurity.md) | Pro Spring Security | ⚠️待核验（Apress；初版 Carlo Scarioni 2013，第2版 Scarioni & Nardone 2019，第3版 Nardone & Scarioni 2024） | Apress | ⚠️待核验 | 英文原版笔记，笔记内另引 Spring Security Essentials，具体版次未定 | ⚠️ |
| [SpringDataJPA入门实战与进阶.md](SpringDataJPA入门实战与进阶.md) | Spring Data JPA：入门、实战与进阶 | 张振华 著 | 机械工业·2021-10 | 9787111692201 | 「语法+源码+原理+实战」四模块 33 章 | ✅ |

### 补充备注（Security / Data）

- `深入浅出Spring_Security.md`：216 行，豆瓣 35383505，笔记标注「知乎电子书」；正文含第 1 章「Spring Security 架构概览」起的目录与摘记（认证、授权、Web 安全）。核实后确认纸质版由清华大学出版社 2021-03 出版，作者王松（江南一点雨），两者为同一本书的不同载体记录。
- `SpringSecurity实战.md`：30 行，含两个豆瓣链接（35682757 / 34910069）与「2021 年原版、2022 年翻译」的记录；核实为 Manning《Spring Security in Action》中译本（清华 2022-01，蒲成译），笔记首句摘录与该书中译版前言一致。
- `SpringSecurity原理与实战.md`：13 行，仅豆瓣 35814597 + 知乎电子书链接（zhihu.com/pub/book/120288138），2020-02 日常笔记延伸引用《Spring 实战》；作者信息暂无法从笔记与公开检索中确证对应关系，列待核验。
- `ProSpringSecurity.md`：9 行英文笔记，含两个豆瓣链接（20780552 / 27603777）并提及《Spring Security Essentials》；Apress 官网确认《Pro Spring Security》存在 2013 初版（Carlo Scarioni）、2019 第 2 版（Scarioni & Nardone）、2024 第 3 版（Nardone & Scarioni，覆盖 Spring Framework 6 / Boot 3）三个版次，笔记未标明具体对应哪一版。
- `SpringDataJPA入门实战与进阶.md`：49 行，豆瓣 35659940；笔记目录覆盖第 1–9 章及以上（Repository 命名语法、@Query、@Entity 注解、QueryByExampleExecutor 等），与张振华书目录吻合；笔记另含与 JdbcTemplate 对比的摘记。

## 重复笔记清单（只标注，不动文件）

- `Spring_Cloud_Alibaba微服务架构实战派.md`：全文仅 2 行（标题），为 [SpringCloudAlibaba微服务架构实战派.md](SpringCloudAlibaba微服务架构实战派.md) 的空壳重复笔记，内容以下者为准。
- `Spring深度分析.md`：笔记自标「废弃」，章节结构与《Spring源码深度解析（第2版）》完全一致（含 2019-1-2 版与豆瓣 30452948 链接），为同一本书的早期大纲；正式笔记见 [Spring源码深度解析（第2版）.md](Spring源码深度解析（第2版）.md)。

## 与已建章节目录的互链

以下书籍已升级为「章节目录」形态的深度笔记：

- [Spring源码深度解析第2版/00-总览与阅读地图.md](Spring源码深度解析第2版/00-总览与阅读地图.md) —— 与 `Spring源码深度解析（第2版）.md` 同书，单文件为总纲、目录版为逐章笔记。
- [深入理解高并发编程/](深入理解高并发编程/) —— 高并发专题目录（与 Spring 线互补，Boot/Cloud 应用的并发基础）。
- [软件架构设计/](软件架构设计/) —— 架构设计专题目录（与 Spring 微服务线配套）。
- [打造敏捷开发模式/](打造敏捷开发模式/) —— 工程效能专题目录。

## 待核验清单

1. `Spring实战4.md`：中文版译者（网络来源仅确认作者/出版社/ISBN，译者未确认）。
2. `看透springmvc.md`：ISBN（作者韩路彪、机械工业 2016 已核实，条码号未确认）。
3. `SpringBoot开发实战.md`：出版社与 ISBN（陈光剑、2018-08、知乎读书/得到电子版已确认）。
4. `SpringSecurity原理与实战.md`：笔记仅记「知乎电子书 + 豆瓣 35814597」，疑似郑天民《Spring Security原理与实战》（人民邮电 2022，9787115577894），对应关系待核验。
5. `ProSpringSecurity.md`：具体版次与作者（笔记同时引用 Pro Spring Security 与 Spring Security Essentials 两个豆瓣条目）。
6. `springboot实战派.md`、`SpringCloudAlibaba微服务架构实战派.md` 等 📄 条目的出版年份为笔记记录，未联网复核。

## 收录统计

- 收录大纲单文件 **29** 个（含 2 个重复/废弃壳文件：`Spring_Cloud_Alibaba微服务架构实战派.md`、`Spring深度分析.md`）。
- 元数据状态分布：✅ 已核实 16 本（其中 `Spring实战4` 译者、`看透springmvc` ISBN 两项为部分核实）｜📄 来自笔记 10 本｜⚠️ 整体待核验 2 本（`SpringSecurity原理与实战`、`ProSpringSecurity`）＋另含待核验字段若干。
- 待核验条目共 **6** 项，见上清单。
- 已升级章节目录 1 部（Spring源码深度解析第2版/，15 个文件）；关联专题目录 3 部。
