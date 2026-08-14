# pogramminglanguage



一个新特性，是语法糖，还是编译器支持的，还是cpu等硬件支持的



关键字
基础数据类型

标准
python2
3

java
8 11

c++
11 14 17

Go

Rust

Ruby

php

标准库 std

虚拟机

操作系统api

跟汇编交互
跟c语言交互

流程
for
while

读写纯文本文件，二进制文件

跟标准库对应的，三方库

应用领域，生态 库，框架





语言提案
标准委员会



你提到的 “JSR” 和 “C++ 标准委员会” 涉及的是不同编程语言的**标准化机制和组织**。我们来分别详细解释：

---

## 🔹 1. **JSR 是什么？**

**JSR = Java Specification Request（Java 规范请求）**

- ✅ **归属**：这是 **Java 语言**的标准化提案机制。
- ✅ **管理组织**：由 **JCP（Java Community Process）** 管理。
- ✅ **目的**：用于提出、讨论和定义 Java 平台的新功能、API 或技术规范。

### 举例：
- **JSR 385**：`Java API for Units of Measurement`（单位制 API）
- **JSR 310**：`Date and Time API`（即 `java.time` 包，Java 8 引入）
- **JSR 371**：`MVC 1.0`（Java EE 的 MVC 框架）
- **JSR 330**：`Dependency Injection`（依赖注入注解，如 `@Inject`）

### 🔄 流程简述：
1. 某人或公司提出 JSR（如 Oracle、IBM、社区）
2. 指定 **Spec Lead**（规范负责人）
3. 经过 **Public Review → Final Release**
4. 被纳入 JDK 或 Java EE 等标准

> 所以，**JSR 是 Java 的“标准提案”系统**。

---

## 🔹 2. **C++ 的标准委员会是什么？**

C++ 没有叫 “JSR” 的机制，它的标准化由 **ISO（国际标准化组织）** 下的专门委员会负责。

### ✅ 正式名称：
> **ISO/IEC JTC1/SC22/WG21**  
> 通常简称为 **WG21**

- **WG21** = Working Group 21
- 负责 **C++ 语言**的国际标准制定。

### 🏢 组织结构：
| 名称     | 职责                                                |
| -------- | --------------------------------------------------- |
| **ISO**  | 国际标准化组织，最终批准标准                        |
| **JTC1** | ISO 下属的“信息技术”联合技术委员会                  |
| **SC22** | JTC1 下属的“编程语言、其环境和系统软件接口”分委员会 |
| **WG21** | SC22 下属的“C++”工作组 ✅ 就是它！                   |

---

### C++ 标准化流程（与 JSR 类比）

| Java（JSR）  | C++（WG21）                        | 说明                                 |
| ------------ | ---------------------------------- | ------------------------------------ |
| 提出 JSR     | 提交 **Paper**（论文）             | C++ 中叫 **P-number**，如 `P0254R2`  |
| JCP 成员投票 | WG21 成员讨论 + 投票               | 在每月会议上讨论                     |
| 发布规范文档 | 发布 **Working Draft**（如 N4950） | 草案不断迭代                         |
| 最终发布标准 | ISO 正式发布 **ISO/IEC 14882**     | 如 C++11, C++14, C++17, C++20, C++23 |

### 📄 C++ 标准命名：
- **ISO/IEC 14882**：C++ 语言国际标准编号
- 版本：
  - C++98（第一版）
  - C++03（小修订）
  - C++11（重大更新）
  - C++14
  - C++17
  - C++20（重大特性：Concepts, Modules, Coroutines）
  - C++23（最新已发布）
  - C++26（正在开发中）

---

### C++ 标准提案（Paper）示例：

| Paper ID    | 内容                                      |
| ----------- | ----------------------------------------- |
| **P0122R7** | `std::filesystem`（文件系统库，C++17）    |
| **P0145R3** | `std::span`（动态视图，C++20）            |
| **P2300R7** | C++23 的 `std::execution`（异步执行模型） |
| **P2164R7** | `std::print`（C++26 预计引入）            |

> 所有提案可在 [https://wg21.link](https://wg21.link) 查看（如 `wg21.link/P0122`）

---

## 对比总结：JSR vs C++ WG21

| 项目     | Java（JSR）                       | C++（WG21）                      |
| -------- | --------------------------------- | -------------------------------- |
| 标准组织 | JCP（Java Community Process）     | ISO/IEC JTC1/SC22/WG21           |
| 提案机制 | JSR（Java Specification Request） | Paper（P-number，如 P1234R5）    |
| 提案示例 | JSR 310（日期时间 API）           | P0122R7（filesystem）            |
| 标准文档 | Java SE Specification             | ISO/IEC 14882                    |
| 版本命名 | Java 8, Java 11, Java 17          | C++11, C++17, C++20, C++23       |
| 是否开放 | 是（但 Oracle 影响大）            | 是（高度开放，社区参与强）       |
| 会议频率 | 不定期                            | 每月线上 + 每年 2-3 次面对面会议 |

---

## ✅ 总结

- ✅ **JSR** 是 **Java** 的标准提案系统，由 **JCP** 管理。
- ✅ **C++** 的标准委员会是 **ISO/IEC JTC1/SC22/WG21**，简称 **WG21**。
- ✅ C++ 没有“JSR”，而是通过提交 **P-number 论文**来推动语言演进。
- ✅ C++ 标准每 3 年发布一次（如 C++20, C++23, C++26…），由 ISO 正式发布。

---

如果你想参与 C++ 标准制定，可以：
1. 访问 [https://wg21.link](https://wg21.link)
2. 阅读 Papers
3. 加入 [Cpp Slack](https://cpplang.slack.com) 或邮件列表
4. 参与会议讨论（开放旁听）

需要我帮你解读某个具体的 C++ 提案（Paper）吗？



|      |        |      |
| ---- | ------ | ---- |
| Java | jsr    |      |
| c++  | isocpp |      |
|      |        |      |





非常棒的问题！你已经从 **Java 的 JSR** 和 **C++ 的 WG21** 出发，进一步问到了主流编程语言的**标准化组织或治理机制**。我们来系统地梳理一下：

> ✅ **目标**：列出每种主流语言的：
> - 标准委员会 / 治理组织
> - 提案机制（如 JSR、P-number）
> - 标准文档或发布方式

---

## 主流编程语言的标准组织与提案机制

| 语言       | 标准组织 / 委员会                                            | 提案机制                               | 标准文档 / 发布                                              |
| ---------- | ------------------------------------------------------------ | -------------------------------------- | ------------------------------------------------------------ |
| **C++**    | **ISO/IEC JTC1/SC22/WG21**（简称 WG21）                      | **Paper（P-number）**，如 `P0254R2`    | **ISO/IEC 14882**（C++11, C++17, C++20, C++23...）           |
| **C**      | **ISO/IEC JTC1/SC22/WG14**（简称 WG14）                      | **Paper / N-number**（如 N2176）       | **ISO/IEC 9899**（C89, C99, C11, C17, C23）                  |
| **Python** | **Python Software Foundation (PSF)** + **BDFL 赋权下的核心开发者** | **PEP（Python Enhancement Proposal）** | PEP 文档集合（如 PEP 8, PEP 484）                            |
| **Go**     | **Go Team（Google 团队）** + 开源社区                        | **Proposal（通过 GitHub Issues）**     | Go 语言规范（[golang.org/ref/spec](https://golang.org/ref/spec)） |
| **Rust**   | **Rust Project**（社区驱动）                                 | **RFC（Request for Comments）**        | Rust RFC Book + The Rust Reference                           |
| **C#**     | **ECMA TC39-TG2** / **ISO/IEC JTC1/SC22/WG22** / **Microsoft + .NET Foundation** | **GitHub Issues & Design Notes**       | **ECMA-334**（C# 语言规范）                                  |
| **Java**   | **JCP（Java Community Process）**                            | **JSR（Java Specification Request）**  | Java SE/EE Specification                                     |

---

### 1. **C++** ✅（已讨论）
- **委员会**：`WG21`（ISO/IEC JTC1/SC22/WG21）
- **提案**：`P-number`（如 `P2300R7`）
- **标准**：`ISO/IEC 14882`
- 🔗 官网：[https://wg21.link](https://wg21.link)

---

### 2. **C 语言**
- **委员会**：`WG14`（ISO/IEC JTC1/SC22/WG14）
- **提案**：技术文件（TD）、N-number 文档（如 N2176）
- **标准**：`ISO/IEC 9899`
  - C89 / ANSI C
  - C99
  - C11
  - C17（ISO/IEC 9899:2018）
  - C23（即将发布）
- 🔗 官网：[https://www.open-std.org/jtc1/sc22/wg14/](https://www.open-std.org/jtc1/sc22/wg14/)

> C 和 C++ 是唯二由 ISO 直接标准化的系统级语言。

---

### 3. **Python**
- **治理组织**：
  - **PSF（Python Software Foundation）**
  - **核心开发团队（core devs）**
  - 曾由 **BDFL（Guido van Rossum）** 领导，2018 年后改为** Steering Council（指导委员会）**
- **提案机制**：**PEP（Python Enhancement Proposal）**
  - PEP 0 是索引
  - PEP 8：代码风格
  - PEP 484：类型提示（`typing` 模块）
  - PEP 572：海象运算符 `:=`
- **标准**：语言行为由 **CPython 实现 + PEP 文档** 共同定义
- 🔗 官网：[https://peps.python.org](https://peps.python.org)

---

### 4. **Go（Golang）**
- **主导组织**：**Go Team（Google 内部团队）**
  - 如 Russ Cox, Ian Lance Taylor, Robert Griesemer
  - 由 **Go Steering Committee** 最终决策
- **提案机制**：
  - 使用 **GitHub Issues** 标记为 `proposal`
  - 流程：`issue → design doc → approval → implementation`
  - 示例：`proposal: map泛型支持` → `issue #43651`
- **标准**：
  - **The Go Programming Language Specification**（官方语言规范）
  - 发布在 [golang.org/ref/spec](https://golang.org/ref/spec)
- **特点**：**Google 主导，社区参与，决策集中**

---

### 5. **Rust**
- **治理组织**：**Rust Project**（社区驱动）
  - 由 **Rust Core Team** 和多个 **Teams**（如 lang, libs, compiler）组成
  - 受 **Rust Foundation**（2021年成立，AWS、Google、Microsoft 等支持）支持
- **提案机制**：**RFC（Request for Comments）**
  - 所有重大变更必须通过 RFC
  - 存储在 GitHub：[github.com/rust-lang/rfcs](https://github.com/rust-lang/rfcs)
  - 示例：
    - RFC 1105：`#[derive]` 机制
    - RFC 2000：`const fn`
    - RFC 2229：`async/await`
- **标准**：
  - **The Rust Reference**
  - **The Rustonomicon**
  - **RFC Book**
- 🔗 官网：[https://rust-lang.github.io/rfcs/](https://rust-lang.github.io/rfcs/)

---

### 6. **C#（C-Sharp）**
- **标准化组织**：
  - **ECMA International**：标准化为 **ECMA-334**
  - **ISO/IEC**：也曾发布 ISO/IEC 23270
  - **Microsoft + .NET Foundation**：实际开发和演进主导
- **提案机制**：
  - **GitHub 仓库**：[github.com/dotnet/csharplang](https://github.com/dotnet/csharplang)
  - 提案以 **Issues 和 Design Notes** 形式提出
  - 示例：
    - `records`（C# 9）：[github.com/dotnet/csharplang/issues/39](https://github.com/dotnet/csharplang/issues/39)
    - `primary constructors`：正在讨论
- **标准文档**：
  - **ECMA-334**（最新版涵盖 C# 10 左右）
  - 实际开发以 **.NET SDK 发布**为准
- **特点**：**微软主导，开源治理，ECMA 标准化备份**

---

### 7. **Java**（补充完整）
- **组织**：**JCP（Java Community Process）**
- **成员**：Oracle、IBM、Red Hat、Google、Eclipse Foundation 等
- **提案**：**JSR（Java Specification Request）**
  - JSR 388：Java SE 11
  - JSR 376：Java Platform Module System（JPMS，Java 9）
- **标准**：**Java SE Specification**
- 🔗 官网：[https://jcp.org](https://jcp.org)

---

## 📊 对比总结表

| 语言       | 治理模式               | 提案机制         | 是否 ISO 标准           | 开放程度          |
| ---------- | ---------------------- | ---------------- | ----------------------- | ----------------- |
| **C++**    | ISO WG21（开放）       | P-number Paper   | ✅ 是（ISO/IEC 14882）   | 高                |
| **C**      | ISO WG14（开放）       | N-number / Paper | ✅ 是（ISO/IEC 9899）    | 高                |
| **Python** | PSF + 指导委员会       | **PEP**          | ❌ 否                    | 高                |
| **Go**     | Google Go Team         | GitHub Proposal  | ❌ 否                    | 中（Google 主导） |
| **Rust**   | 社区 + Rust Foundation | **RFC**          | ❌ 否                    | 非常高            |
| **C#**     | Microsoft + ECMA       | GitHub Issues    | ✅ ECMA-334              | 高（开源）        |
| **Java**   | JCP（企业主导）        | **JSR**          | ✅ ISO/IEC 30107（部分） | 中                |

---

## ✅ 总结一句话：

- **C++**：`WG21` + `P-number` → `ISO/IEC 14882`
- **C**：`WG14` + `N-number` → `ISO/IEC 9899`
- **Python**：`PSF` + `PEP`
- **Go**：`Go Team` + `GitHub Proposal`
- **Rust**：`Community` + `RFC`
- **C#**：`Microsoft` + `ECMA` + `GitHub`
- **Java**：`JCP` + `JSR`

---

如果你想参与这些语言的标准化：
- C/C++：参加 ISO 会议，提交 Paper
- Python：写 PEP
- Rust：提 RFC
- Go：在 GitHub 提 proposal
- C#：参与 dotnet/csharplang 讨论
- Java：加入 JCP，参与 JSR

需要我为你生成一份“如何提交一个 C++ P-number 提案”的指南吗？