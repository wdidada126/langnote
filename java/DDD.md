# DDD



https://github.com/heynickc/awesome-ddd
https://zhuanlan.zhihu.com/p/97680152
https://blog.csdn.net/m0_37055174/article/details/102656194
https://zhuanlan.zhihu.com/p/32459776
[DDD解决扩展性问题](https://www.douban.com/doulist/113575586/)




极客时间有



DO
DTO
是模型

领域模型又是？


我们还是来看看《阿里开发手册》提供的分层领域模型规约参考：

DO(Data Object)：此对象与数据库表结构一一对应，通过DAO层想上传输数据源对象。
DTO(Data Transfer Object)：数据传输对象，Service或Manager向外传输的对象。
BO(Business Object)：业务对象，由Service层输出的封装业务逻辑的对象。
AO(Application Object)：应用对象，在Web层与Service层之间抽象的复用对象模型，极为贴近展示层，复用度不高。
VO(View Object)：显示层对象，通常是Web向模版渲染引擎层传输的对象。
Query：数据查询对象，各层接收上层的查询请求。注意超过2个参数的查询封装，禁止使用Map类来传输。


一般的工作流程 写概要设计文档 数据库表 -> 
MyBatais也是基于

领域驱动设计
假设内存无限大，数据不需要存在数据库

[阿里盒马领域驱动设计实践](https://www.infoq.cn/article/alibaba-freshhema-ddd-practice)



在非 DDD 设计思路下的项目，我们一般先根据需求做数据库表的设计，然后根据表结构设计推导出相应的实体对象，这样的实体对象是数据模型转换的结果。此时，这些对象只是数据的载体，是没有行为的。在这种设计模式下，业务流程实现上仍旧是面向过程式，是一种以数据为中心的过程式思想，其开发过程可以理解为是对数据移动、处理和实现的过程。而如果采用 DDD 的思想去设计，我们将建立一个基于面向对象设计的系统

[领域驱动设计（DDD）在有赞教育线索资源管理的实践](https://www.infoq.cn/article/HVTWari0Ru4MSSGPvkYv)

[基于DDD的微服务设计和开发实战](https://weibo.com/ttarticle/p/show?id=2309404386442074813348&sudaref=www.google.com&display=0&retcode=6102)





