# OWASP TimeGap Theory Handbook

## 版本与 ISBN

- 全名：*OWASP TimeGap Theory Handbook — Learn and teach TOCTOU security issues in web applications*
- 作者：Abhi M Balakrishnan（硅谷安全工程师）
- 出版社：**作者自出版**（POD，经 Pothi.com / The Book Patch 印制）
- 出版时间：2020 年 8 月（The Book Patch 记为 2020-08-25）
- 版次：第 1 版，2020
- **ISBN-13：`9789390274611`** → 规范化 `978-93-9027-461-1`（93 = 印度英语出版区）
- **ISBN-10：`9390274613`**
- 页数：153 页（Pothi、Flipkart 均记 153；The Book Patch 记 151，存在一页之差）
- 规格：6" × 9"，全彩内页，平装（Perfect Binding）
- 定价：₹1,567（Pothi，按需印刷）

> 2026-09-25 由 `2026/202609/20260922.md`（TOCTOU 主题）整理。
> ISBN-13 校验位已验证通过（前 12 位加权和 129 → 校验位 1 ✔），书名/作者/ISBN 经 Pothi、Flipkart、The Book Patch、timegaptheory.com 四方交叉确认。

## 笔记

- **目前唯一一本以 TOCTOU 为主题的独立公开出版物**——这点很关键，TOCTOU 文献里论文很多，成书的只有这一本。
- 全书围绕 OWASP 的 **TimeGap Theory** 开源项目展开，该项目是一个**夺旗赛（CTF）**式的 Web 应用，专门用来演示和利用 TOCTOU 竞态漏洞。书按 CTF 通关攻略的形式写。
- **恐龙主题**，风格轻松，全彩。定位是「给完全没接触过 TOCTOU 的人」或「刚入门 Web 应用安全的人」的入门手册。
- 明确反驳三个常见误解：
  1. 以为 TOCTOU 只发生在转账/支付页面
  2. 以为挖 TOCTOU 必须靠高精尖工具（书里只用**浏览器开发者工具、cURL** 等免费开源工具）
  3. 以为 TOCTOU 是边角案例、现实中很难利用
- 作者创作动机挺有意思：在一次威胁建模会议上，他指出某设计可能存在 TOC/TOU 问题，**在场一半人不知道 TOCTOU 是什么**，还有人认为新一代数据库已内置防护。于是他花了一年半做了这个项目 + 写了这本书。
- 配套项目用 **Docker + Heroku** 部署，成本极低、可移植。

## 获取与配套

| 项目 | 链接 |
|------|------|
| 项目官网 | https://timegaptheory.com/ |
| Pothi（POD 购买） | https://store.pothi.com/book/abhi-m-balakrishnan-owasp-timegap-theory-handbook/ |
| The Book Patch | http://app.thebookpatch.com/BookStore/owasp-timegap-theory-handbook/ |

作者的其他 OWASP / 安全项目：OWASP Mantra、Matriux、ExploitMe REST、Alert Labs、OWASP Bricks、Snow、Brick Town，以及《web app security testing with browsers》。

## 备注

- 自出版 + 按需印刷，无传统出版社与书号体系，**印量与流通都很少**，国内基本买不到。
- 页数的 153 / 151 两说并存，以 Pothi 与 Flipkart 的 153 为准（与源笔记记录一致）。

## 关联

- `paper/20260922.md` — 同批整理的 TOCTOU 论文清单（3 篇）
- `paper/toctou_ieee_access_2022.md` — IEEE Access 综述，学术侧的 TOCTOU 全景（本书是实践/CTF 侧）
- `book/软件安全工程.md`、`book/计算机安全导论.md`、`book/CISSP认证考试指南.md` — 同一来源笔记中提到的另外三本安全书
