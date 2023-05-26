# esb


https://gitee.com/mirrors/WSO2-ESB

wso2 ha
https://blog.csdn.net/baidu_25117757/article/details/123736178

WSO2 ESB 5.0.0 一些组件的使用教程
https://blog.csdn.net/baidu_25117757/article/details/127943704
ws2 develop studio
https://github.com/wso2/integration-studio/#Installation-and-Run
https://wso2.com/micro-integrator/integration-studio/

WSO2 ESB 5.0.0 一些组件的使用教程
https://blog.csdn.net/baidu_25117757/article/details/127943704


WSO2 ESB 3.1 linux教程
https://blog.csdn.net/weixin_45669656/article/details/108798095?spm=1001.2014.3001.5502


https://github.com/jeffreyning/nhEsb
https://gitee.com/mirrors/nhEsb


[几种ESB（企业服务总线）介绍](https://blog.csdn.net/yinni11/article/details/81070062)


原来深圳智莱使用的是esb，传统行业不使用spring那一套？
esb是一套企业解决方案，不同企业it系统之间集成的
企业原有it系统跟新建设it项目交互数据，走什么协议?http？
数据格式 xml json？
开放接口如何保证安全不被未授权方调用?

[Apache CXF 例子](https://www.cnblogs.com/zuiyirenjian/p/3280236.html)
[CXF简单例子](https://blog.csdn.net/JXH118/article/details/83284346)


著名的非开源 ESB 产品，诸如 WebSphere，Tibco，Sonic 等
https://www.infoq.cn/article/ESB-Tijs-Rademakers-Jos-Dirksen

Mule ESB（MuleSoft）
Talend ESB
Apache ServiceMix和Camel （Apache）   https://servicemix.apache.org/docs/7.x/quickstart/index.html
WSO2 ESB（WSO2）
OpenESB（Sun/Oracle）
JBoss ESB（JBoss）
UltraESB

https://blog.csdn.net/linlzk/article/details/25036069



整体的一些总结
Mule ESB：强在Http Rest接口适配和诸多适配器集成，消息映射和转换能力。对于SOAP WebService的支持一般，对于DB适配的支持也一般。同时注意社区版缺少很多功能，包括集群能力，管控治理平台，类似transform等component组件等。企业稍微对ESB可靠性和管控要求较高的场景用社区版一般搞不懂，而企业版收费不菲，不比oracle ,tibco,ibm的ESB便宜多少。
Talend ESB: 是最近试用的几个开源ESB里面最好的，包括各种服务集成场景，对SOAP, Rest的服务支持，对DB适配的支持（talend 本身也是ETL起家的），消息映射mapping能力，诸多的component组件的提供，同时还支持对于camel的可视化设计。对于企业集成场景，社区版的能力足够丰富，缺少SAM管控治理平台，但是社区版本有开放的接口完全可以自己定制。对于企业版本来说收费也比Mule ESB便宜一些。
ServiceMix：对于Talend ESB部分能力也基于Camel，而对于ServiceMix则是完全基于karaf+camel搭建的一个足够开放的ESB平台，当前的redhat Fuse企业版可以看做是ServiceMix的一个商业实现。其底层能力相当强，但是由于缺乏设计器，本身可配置和可视化的Mapping能力较弱，对于服务管控治理能力也较弱。如果是想自己灵活定制这些内容，且企业具备一定的开发能力，完全可以选择ServiceMix进行二次开发和集成。



如同Apache ServiceMix一样,Open ESB也实现了JBI规范

WSO2有实践



esb http协议转soap

ESB通常用于连接不同的系统与应用,将不同协议的数据进行转化是一个常见任务。
对于需要将HTTP请求转化为SOAP请求的场景,ESB可以通过以下方式实现:
1. 配置HTTP监听端口
首先,我们需要在ESB上配置一个HTTP监听端口,用于接收HTTP请求。
2. 定义消息转化路由
然后,我们需要定义一个消息路由,用来将传入的HTTP请求转化为SOAP请求。
3. 实现消息转化逻辑
消息路由中的转化逻辑主要做以下事情:
- 解析HTTP请求,获取相关信息如URL参数、Header信息、请求Body等
- 根据这些信息,构造一个SOAP请求。包括soap:Envelope根节点,methodName等。
- 将构造的SOAP请求作为转发目标。
4. 发送SOAP请求
构造完SOAP请求后,ESB可以采用不同的方式发送SOAP请求:
- 直接使用SOAP连接,如JAX-WS
- 使用HTTP POST,将SOAP请求发送到目标URL
- 发往消息总线,使用消息代理模式
5. 接收SOAP返回结果
一旦ESB接收到SOAP返回结果后,同样需要实现转化逻辑:
- 解析SOAP返回结果,获取返回值
- 构造HTTP相应,设置响应码和响应Body
- 返回HTTP响应给原始请求方
总的来说,通过在ESB上实现HTTP监听和消息路由,定义好消息转化逻辑,就可以将HTTP请求转化为SOAP请求,最终将SOAP结果再转化为HTTP响应返回。
主要涉及解析请求、构造请求、发送请求和解析结果四个环节。希望可以为您提供参考!如果还有其他疑问,欢迎随时提出,我会尽量为您解答。



WSO2 ESB可以用于执行不同协议的转换,包括HTTP to SOAP协议转换。

配置HTTP监听端口:

```xml
<http.listener port="9000" stats="enable" trace="enable" ... >  
   <server-mappings>  
       <server url-mapping="/service/*"/>
   </server-mappings> 
</http.listener>
```

定义HTTP到SOAP的转换逻辑:

```xml
<proxy name="ConvertToSoap" transports="http" startOnLoad="true" trace="enable">
  
   <target>
       <inSequence>
           ... 解析HTTP请求,获取URL、参数、Body ...
           <!-- 构造SOAP请求 -->
           <property name="messageType" value="text/xml"/>
           <payloadFactory media-type="xml">  
               <format>  
                   <soap:Envelope ...>  
                       <soap:Body>
                           <m:methodName> ... </m:methodName>    
                       </soap:Body>
                   <soap:Envelope>
               </format>                 
           </payloadFactory> 
           <!-- 发送SOAP请求 -->  
           <send>
               <endpoint>
                  <address uri="http://soap.service.com/service" />
               </endpoint>  
           </send> 
       </inSequence> 
       <outSequence>
           ... 解析SOAP响应,并构造并返回HTTP响应 ... 
       </outSequence>
   </target>
</proxy>
```

主要步骤:

- 定义HTTP监听端口
- 通过XML配置定义转换逻辑的Proxy
- 在`<inSequence>`中解析HTTP请求和构造SOAP请求
- 使用`<send>`发送SOAP请求
- 在`<outSequence>`解析SOAP响应并构造HTTP响应

主要元素:

- `<property>` - 设置消息类型
- `<payloadFactory>` - 构造SOAP请求
- `<send>` - 发送SOAP请求
- `Synapse Constants` - 存放解析出的HTTP信息

WSO2 ESB通过简单 yet 强大的XML配置,可以实现不同协议之间的转换。

从WSO2 ESB源码来看,协议转换逻辑主要在以下几个类中:
1. SynapseMessageReceiver:
负责接收不同协议的消息,例如HTTP请求。它会对不同类型的消息进行封装,生成相应的SynapseMessage。
2. SynapseMessage:
封装了消息的各个属性,如消息内容、消息头、携带的属性等。SynapseMessage封装不同协议的消息的公共属性。
3. AbstractHandler:
负责执行消息路由和转换的具体逻辑。它实现了Mediator接口,从而可以作为Mediator注入到路由中。
4. PayloadFactoryMediator:  
具体实现Payload Factory 功能,用于构造 neue 消息内容。主要用于消息体的转换。
5. SendMediator:
发送转换后的消息内容给目标地址。
6. RespondMediator:
根据返回结果构造新的响应消息。
7. RespondMediator:
用于解析返回结果,提取数据,并构造新的响应消息。
总的来说:
- SynapseMessageReceiver和SynapseMessage负责封装不同协议的消息。
- AbstractHandler实现了转换逻辑,是路由的主线。
- PayloadFactoryMediator用于构造新的消息体。
- SendMediator发送转换后的消息。
- RespondMediator解析结果并构造响应。
它们共同协作,实现了WSO2 ESB中的协议转换功能。
SynapseMessage类似于传统的Message对象,统一封装不同协议的消息。
AbstractHandler中调用具体的Mediator实现转换。
希望这能清楚地说明在WSO2 ESB源码中,协议转换主要的角色类。


