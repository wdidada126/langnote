# 第 3 章 Java 内存模型（JMM）

> 从计算机运行模型（CPU/主存/外设/总线）讲到 Java 内存模型：主内存 vs 工作内存、可见性/有序性/原子性、happens-before、`volatile`。本书图解硬件→JMM 抽象。详见《之美》concepts/JMM与happens-before/volatile与内存可见性、深度解析 3 章。

## 一、核心精讲

### 3.1 🔧 硬件矛盾 → JMM 抽象
- CPU 与主存速度差 → 缓存 → 可见性问题；编译/CPU 重排 → 有序性问题（🔧 JMM 用 happens-before 统一抽象，屏蔽硬件差异）。

### 3.2 happens-before 八条
- 程序序、volatile、锁、start/join、传递性（🔧 是可见性判定依据，非时间先后，见《之美》JMM 专篇）。

### 3.3 volatile
- 可见 + 有序，不保原子；DCL 必加（🔧 见《之美》volatile 专篇）。

## 二、版本演进 / 论文 / 前沿

- 论文：JSR 133（Manson-Pugh-Adve POPL'05）、Adve-Hill DRF-SC（TPDS'93）、x86-TSO（Sewell CACM'10）。
- 工具：JOL、jcstress、herd7。

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "volatile 原子" | 仅可见+有序 |
| 2 | "DCL 不加 volatile" | 半初始化 |
| 3 | "x86 跑过即安全" | ARM 弱内存仍崩 |
