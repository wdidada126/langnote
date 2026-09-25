# 卷2·可见性与有序性的原理（JMM）（尼恩）

> 卷2 第 4 章。Java 内存模型、可见性（volatile/锁）、有序性（重排序）、happens-before、DCL。详见《之美》concepts/JMM与happens-before.md 与 concepts/volatile与内存可见性.md（更细，含 DRF-SC 与屏障成本）。

## 一、核心精讲

### 1.1 三大特性
- **原子性**（锁/原子类）、**可见性**（volatile/锁使本地缓存失效）、**有序性**（volatile/acquire-release 禁重排）（🔧 synchronized 三者都保，但重；volatile 仅可见+有序，不保复合原子）。

### 1.2 happens-before（8 条）
- 程序序、volatile 写-读、锁释放-获取、线程 start/join、传递性（🔧 是「可见性保证」的判定依据，非时间先后）。

### 1.3 DCL 必须 volatile
- 单例 `instance = new Singleton()` 可能重排（分配→引用暴露→初始化），其他线程取到半初始化对象（🔧 `instance` 加 `volatile` 禁止该重排；或用「静态内部类」懒加载，JLS 保证类初始化锁的 happens-before）。

## 二、版本演进 / 论文 / 前沿

- 论文：JSR 133（Manson-Pugh-Adve POPL'05）、Pugh《The Java Memory Model is Fatally Flawed》(2000)、Adve-Hill DRF-SC（TPDS'93）、x86-TSO（Sewell CACM'10）。
- 工具：jcstress、JOL、herd7。

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "volatile 原子" | 仅可见+有序 |
| 2 | "DCL 不加 volatile" | 半初始化，必加 |
| 3 | "x86 跑过即安全" | ARM 弱内存仍可能崩 |
