# esb



[几种ESB（企业服务总线）介绍](https://blog.csdn.net/yinni11/article/details/81070062)


原来深圳智莱使用的是esb，传统行业不使用spring那一套
[Apache CXF 例子](https://www.cnblogs.com/zuiyirenjian/p/3280236.html)
[CXF简单例子](https://blog.csdn.net/JXH118/article/details/83284346)



著名的非开源 ESB 产品，诸如 WebSphere，Tibco，Sonic 等
https://www.infoq.cn/article/ESB-Tijs-Rademakers-Jos-Dirksen

Mule ESB（MuleSoft）
Talend ESB
Apache ServiceMix和Camel （Apache）
WSO2 ESB（WSO2）
OpenESB（Sun/Oracle）
JBoss ESB（JBoss）
UltraESB

https://blog.csdn.net/linlzk/article/details/25036069



整体的一些总结
Mule ESB：强在Http Rest接口适配和诸多适配器集成，消息映射和转换能力。对于SOAP WebService的支持一般，对于DB适配的支持也一般。同时注意社区版缺少很多功能，包括集群能力，管控治理平台，类似transform等component组件等。企业稍微对ESB可靠性和管控要求较高的场景用社区版一般搞不懂，而企业版收费不菲，不比oracle ,tibco,ibm的ESB便宜多少。
Talend ESB: 是最近试用的几个开源ESB里面最好的，包括各种服务集成场景，对SOAP, Rest的服务支持，对DB适配的支持（talend 本身也是ETL起家的），消息映射mapping能力，诸多的component组件的提供，同时还支持对于camel的可视化设计。对于企业集成场景，社区版的能力足够丰富，缺少SAM管控治理平台，但是社区版本有开放的接口完全可以自己定制。对于企业版本来说收费也比Mule ESB便宜一些。
ServiceMix：对于Talend ESB部分能力也基于Camel，而对于ServiceMix则是完全基于karaf+camel搭建的一个足够开放的ESB平台，当前的redhat Fuse企业版可以看做是ServiceMix的一个商业实现。其底层能力相当强，但是由于缺乏设计器，本身可配置和可视化的Mapping能力较弱，对于服务管控治理能力也较弱。如果是想自己灵活定制这些内容，且企业具备一定的开发能力，完全可以选择ServiceMix进行二次开发和集成。



