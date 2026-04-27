# 202003_monthly

## 原有内容


## 原有内容


在家工作
汇编语言
os的相关知识，不应该涉及

java类加载机制 jvm spec

load  link 初始化   Initializing

https://blog.csdn.net/m0_38075425/article/details/81627349

### 1.Loading

```
	类加载器通过双亲委派机制将类的class文件载入内存
```

### 2.Linking

```
	1）Verification:检验载入的class文件是否符合jvm的规范格式
	2）Preparation: 为类的静态变量申请内存并赋默认值（注：默认值不是初始值，并且此时对象的内存还未申请）
	3）Resolution:解析阶段。将二进制文件中的类、方法、属性等符号引用解析为直接引用（成员属性的变量名或空引用等，如int i;Object o；），将常量池中的各种符号引用解析为指针、偏移量等内存地址的直接引用。
```

### 3.Initializing

```
	1）初始化静态成员变量
	2）执行静态代码块
```

mysql index page block

平安面试 必须要离职的，俗称捡漏

## 整理补充

## 本月概览

- 本月共整理 31 篇日记。
- 已结合周报回填当月重点主题，便于后续继续补充。

## 周度脉络

- 202003_week1：- 20200301：周日；3月目标
- 202003_week2：- 20200308：周日；[计算机组成原理](https://www.icourse163.org/learn/PKU-1205809805)；计算机体系结构
- 202003_week3：- 20200315：周日；mysql技术内幕；[postgresssql 51cto](https://edu.51cto.com/center/course/lesson/index?id=42874)
- 202003_week4：- 20200322：周日；腾讯课堂redis；为什么linux开源？
- 202003_week5：- 20200329：周日；早上睡到11点起床；[linux和android开发链接](https://blog.csdn.net/LoongEmbedded/article/details/54016805)

## 本月高频主题

- 周日
- 3月目标
- 整理infoq文章
- 要有大纲
- ppt流程图
- 总结base64异常 it技术相关的
- rust编译时长优化
- 公司 SDK流程
- docker的，先定主节点，然后往集群添加主节点
- 知乎总结中间件
- 编译原理 词法分析
- 平安银行面试

## 整理补充

## 本月概览

- 本月共整理 31 篇日记。
- 已结合周报回填当月重点主题，便于后续继续补充。

## 周度脉络

- 202003_week1：- 20200301：周日；3月目标
- 202003_week2：- 20200308：周日；[计算机组成原理](https://www.icourse163.org/learn/PKU-1205809805)；计算机体系结构
- 202003_week3：- 20200315：周日；mysql技术内幕；[postgresssql 51cto](https://edu.51cto.com/center/course/lesson/index?id=42874)
- 202003_week4：- 20200322：周日；腾讯课堂redis；为什么linux开源？
- 202003_week5：- 20200329：周日；早上睡到11点起床；[linux和android开发链接](https://blog.csdn.net/LoongEmbedded/article/details/54016805)

## 本月高频主题

- 周日
- 3月目标
- 整理infoq文章
- 要有大纲
- ppt流程图
- 总结base64异常 it技术相关的
- rust编译时长优化
- 公司 SDK流程
- docker的，先定主节点，然后往集群添加主节点
- 知乎总结中间件
- 编译原理 词法分析
- 平安银行面试
