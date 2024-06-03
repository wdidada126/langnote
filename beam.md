# beam

https://beam.apache.org/

An advanced unified programming model

[Apache Beam指南](https://blog.csdn.net/vinfly_li/article/details/79396948)

分布式数据处理发展迅猛 –> 新的分布式数据处理技术越来越多 –> Hadoop MapReduce，Apache Spark，Apache Storm，Apache Flink，Apache Apex –> 新技术高性能 , 受欢迎,人们喜新厌旧 –> 业务的迁移 –> 迁移条件: 学习新技术,重写业务逻辑 –> 懒 –> 怎么办 ??
Apache Beam 应运而生
贵族身份:
Apache Beam - 原名 Google DateFlow
2016年2月份成为Apache基金会孵化项目
2017年1月10日正式毕业成为顶级项目
继MapReduce，GFS和BigQuery之后，Google在大数据处理领域对开源社区的又一个超级大的贡献

Apache Beam是大数据的编程模型，定义了数据处理的编程范式和接口，它并不涉及具体的执行引擎的实现，但是，基于Beam开发的数据处理程序可以执行在任意的分布式计算引擎上，目前Dataflow、Spark、Flink、Apex提供了对批处理和流处理的支持，GearPump提供了流处理的支持，Storm的支持也在开发中。

综上所述，Apache Beam的目标是：

提供统一批处理和流处理的编程范式
能运行在任何可执行的引擎之上
