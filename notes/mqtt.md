# mqtt

## version
The MQTT 3.1.1 standard
http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html


The MQTT 5.0 standard
https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html

## client

https://github.com/eclipse/paho.mqtt.c

An Eclipse Paho C client library for MQTT for Windows, Linux and MacOS. API documentation: https://eclipse.github.io/paho.mqtt.c/

eclipse.org/paho

https://eclipse.github.io/paho.mqtt.c/MQTTClient/html/

1.Paho MQTT C++：Eclipse Paho项目的C++语言实现，提供了面向对象的API，支持多种平台。

## xd
嵌入式硬件肯定选MQTT。AMQP更适合服务端。

MQTT（Message Queuing Telemetry Transport，消息队列遥测传输协议）

MQTT 发布订阅测试，可以在 Chrome 中下载 MQTTBox 插件 或者 命令行安装 mosquitto 工具

MQTT和Websocket的区别是什么？
链接：https://www.zhihu.com/question/21816631/answer/3145022789

引言
工业系统需要确保数据的无缝交换，因此对于高效、安全的通信协议具有极高的依赖性。MQTT Sparkplug 和 OPC UA  是两个经常被提到的工业协议。本文将全面比较 MQTT Sparkplug 和 OPC UA  以及它们的衍生版本，帮助您更清楚地了解哪种协议更适合您的需求。
OPC Classic 和 OPC UA
OPC UA 的前身是 OPC Classic（也称为 OPC DA 或 OPC Data Access），是由 OPC  基金会开发的一套工业自动化标准。OPC Classic 规范于 1996  年首次发布，它定义了一种标准化的方法，用于在软件应用和工业硬件设备（如传感器、控制器和可编程逻辑控制器）之间交换数据。然而，OPC Classic 有个明显缺点：它与微软 Windows 操作系统及其专有的 DCOM 技术紧密耦合。这种依赖性严重影响了协议的可用性、扩展性、互操作性、安全性和平台独立性，这对一个开放标准来说是巨大的制约。为了克服这些限制，OPC 基金会于 2006 年开始开发了 OPC UA (OPC Unified Architecture) 作为  OPC Classic 规范的后继者。这两种规范在功能上是等效的，但使用不同的底层通信技术。此外，OPC Classic DA 3.0  也于同年发布，并且至今仍在使用中。
为物联网而生的协议：MQTT 的演进
在 20 世纪 90 年代末，Andy Stanford-Clark 和 Arlen Nipper  参与了一个关于管道监测的项目，该项目需要一种轻量级协议，用于与远程传感器和设备进行通信。该项目要求在低功耗、低带宽的环境下实现监测功能。然而，当时的消息传输协议，如  HTTP 和 SMTP，被认为过于臃肿和低效，不适合这种特殊的场景。
为了应对这些挑战，一种发布/订阅模式的消息传输协议 MQTT 应运而生。MQTT以其精简的代码和极低的带宽消耗而著称，因此在低功耗、低带宽的场景下具有显著的优势。它的主要目标是实现设备和系统之间的大规模实时数据交换，即使面对不同的数据格式和结构，也能保证数据通信的标准化。这一特点使得  MQTT 成为物联网和机器对机器（M2M）应用的理想选择。
MQTT 于 2010 年被结构化信息标准促进组织（OASIS）发布为开放标准，从而使其成为各个组织和行业可使用的通信协议。随后，在  2014 年发布了 MQTT 3.1.1，引入了一些新的特性，例如改进的错误处理和对服务质量（QoS）级别的支持。再后来，在 2019 年发布了  MQTT 5.0，进行了重大的改进，包括对自定义属性的支持、持久会话的实现以及错误报告的优化。
优势互补：OPC UA over MQTT
MQTT 发布/订阅模型相比经典 OPC UA 客户端-服务器模型有以下几个优势：
可扩展性：发布/订阅模型可以有效地处理大量的设备和系统，非常适合工业自动化和物联网应用。实时数据交换：发布/订阅模型是为实现实时数据交换而专门设计的，它能让设备和系统及时感知和适应环境变化。减少网络流量：发布/订阅模型通过只传递设备和系统需要的数据，而非所有数据，可以有效地降低网络流量。2018 年，OPC 基金会发布了 OPC UA 发布/订阅规范，它为 OPC UA 制定了一种发布/订阅的通信模型，该模型可以采用 MQTT 协议作为传输方式。OPC UA 发布/订阅模型非常强大，为工业自动化和物联网应用带来了巨大的好处。提升工业连接性：MQTT Sparkplug 规范MQTT 协议在物联网场景中取得了巨大的成功，但由于互操作性不足，它在工业自动化系统中的应用受到了限制。为了解决这个问题，Cirrus  Link Solutions 在 2016 年推出了 Sparkplug 规范，旨在简化 MQTT 在工业自动化系统中的部署和使用。该规范为  MQTT 消息定义了一个标准化的格式，使得不同设备和应用之间能够方便地进行数据交换。Sparkplug 的一个显著特点是它支持设备之间的双向通信。这种能力使得设备不仅可以发送命令，还可以接收来自网络中其他设备的反馈。这篇博客通过介绍 5 个关键概念，阐述了为何 MQTT Broker 是实现 Sparkplug 设计原则的理想选择：Sparkplug 规范中关于 MQTT Broker 的 5 个关键概念。OSI 模型概述MQTT 和 OPC UA 是工业自动化和物联网应用中常用的两种协议，它们拥有不同的架构和设计，体现了各自的用途。以下是 MQTT、OPC UA 及其变体在开放系统互联（OSI）模型方面的比较：OSI 模型MQTTOPC UAMQTT SparkplugOPC UA over MQTT应用层发布/订阅机制OPC UA 通信（60 种数据类型）Sparkplug 通信（18 种数据类型）OPC UA发布/订阅通信表示层未定义UA-JSONUA-XMLUA-BinaryProtobufUA-JSONUA-XMLUA-Binary会话层无会话客户端-服务器会话管理Sparkplug 会话感知无会话传输层TCP/IPTCP/IPMQTTMQTT传输层：MQTT 和 OPC UA 都使用 TCP/IP 作为底层通信协议。MQTT Sparkplug 和 OPC UA over MQTT 则使用 MQTT 作为传输协议，它们都采用了 MQTT 的发布/订阅模型。会话层：OPC UA 包含负责管理客户端和服务器之间连接的会话层，处理诸如会话建立、身份验证和加密等任务。相比之下，MQTT 不具备会话层管理功能。然而，MQTT Sparkplug 通过在会话层引入 Sparkplug 会话感知来弥补这个不足。表示层：OPC UA  拥有定义良好的信息模型，该模型定义了客户端和服务器进行数据交换时数据的结构和语义，例如 UA-JSON 和  UA-binary。相比之下，MQTT 缺乏正式的信息模型，而是依赖于基于主题的消息来实现客户端和服务器之间的数据通信。MQTT  Sparkplug 则是通过指定 Google Protobuf 作为消息格式来弥补这一差距，以增强 MQTT 的能力。应用层：MQTT 和 OPC UA 在应用层协议上有明显的区别。MQTT 使用发布/订阅模型，通过主题来组织消息，而 OPC UA 使用客户端/服务器模型，通过分层对象模型来组织数据。OPC UA 发布/订阅规范是对 OPC UA 客户端/服务器模型的一种扩展。MQTT Sparkplug 和 OPC UA 对比MQTT Sparkplug 和 OPC UA 各有优劣，因此在不同的使用场景中，可能会出现某个协议比另一个更加适用的情况。这两种协议及其衍生协议之间的一些主要区别如下：指标MQTTMQTT SparkplugOPC UAOPC UA over MQTT消息传输模型发布/订阅发布/订阅客户端/服务器发布/订阅带宽使用开销最低，低带宽和低功耗开销最低，低带宽和低功耗高代码占用，高带宽高代码占用，高带宽消息载荷未定义轻量级消息，通常小于 OPC UA复杂的数据类型，其消息大小可以远大于 MQTT Sparkplug复杂的数据类型，其消息大小可以远大于 MQTT Sparkplug互操作性不具备互操作性具备互操作性（18 种数据类型）高度互操作性（60 种数据类型）高度互操作性（60 种数据类型）扩展性高度可扩展高度可扩展，每秒能处理百万级消息可扩展性较好，但需要更复杂的架构来处理大量数据比 OPC UA 客户端/服务器模型具有更好的可扩展性集成便利性使用简单，配置要求最少使用简单，配置要求最少需要较多的安装和配置需要较多的安装和配置服务质量QoS 0（至多一次）、QoS 1（至少一次）和 QoS 2（仅一次）QoS 0（至多一次）、QoS 1（至少一次）和 QoS 2（仅一次）提供可靠的传输层，确保消息传递有序且不丢失提供可靠的传输层，确保消息传递有序且不丢失状态感知否是是是自动发现否否是是应用领域物联网、家庭自动化和 M2M 应用工业物联网和 M2M 应用工业自动化工业自动化实时性是是是是安全性安全性不如 OPC-UA安全性不如 OPC-UA数字证书、数字签名、数据加密和安全认证数字证书、数字签名、数据加密和安全认证信息模型不具备内置的信息建模支持支持复杂的信息建模，但不及 OPC UA 多支持复杂的信息建模系统，允许创建复杂的数据结构和模型支持复杂的信息建模系统，允许创建复杂的数据结构和模型简而言之，OPC UA 是一个开放标准，它包含了一套定义明确的数据类型规范。而 MQTT Sparkplug 也是一个开放标准，但它在数据类型的标准化方面做得不够。因此，在数据传输过程中，MQTT Sparkplug 产生的协议开销更小。结语MQTT Sparkplug 使用了轻量级的消息传输协议，非常适合低带宽或不稳定的网络环境。而 OPC UA 使用了更强大的消息传输协议，能够处理更多的数据量，更适合高速和安全的网络环境。OPC UA 和 MQTT 之间的竞争一直持续至今。目前，EMQ 正在推出针对汽车行业的 MQTT over QUIC 协议，而 OPC 基金会也发布了 OPC UA over TSN。OPC UA over TSN 提供了一种在以太网上传输实时数据的标准化方法，旨在简化复杂的工业自动化和控制系统。
https://www.emqx.com/zh/blog/a-comparison-of-iiot-protocols-mqtt-sparkplug-vs-opc-ua

https://mosquitto.org/
IBM 1999年开发的

mqtt java实现

Paho is an Eclipse IoT project.
https://www.eclipse.org/paho/files/javadoc/org/eclipse/paho/client/mqttv3/package-summary.html
https://github.com/mqtt/mqtt.github.io/wiki/SYS-Topics


基于tcp的

MQTT vs WebSocket

跟kafka一样，有topic的概念

MQTT服务器都是叫Broker

### mqtt开源项目
thingsboard
https://github.com/thingsboard/thingsboard

https://mqttx.app/zh

教程
https://blog.csdn.net/qq_26545955/article/details/90346273

MQTT协议是二进制的
HTTP协议是明文的

## 图形工具
MQTT X是一款优雅的跨平台MQTT 5.0桌面客户端工具，它是由杭州映云科技有限公司（也就是 EMQ）开源的。这款工具支持macOS、Linux和Windows三大主流操作系统，其用户界面设计采用了目前非常流行的Electron跨平台技术。

MQTT X以消息聊天的交互形式收发消息，允许同时建立多个连接，这对于需要模拟MQTT消息的发送或者订阅的开发过程来说非常方便。此外，它还支持通过WebSocket连接至MQTT服务器，并采用了树状结构来划分主题，层次分明。

在保障数据传输安全方面，MQTT X支持SSL/TLS传输加密，并能以漂亮的格式显示JSON、XML、MessagePack、十六进制等消息格式。此外，它还能自动解析消息字段并绘制成图表，使得用户可以更直观地理解和分析数据。

值得一提的是，MQTTX还提供了MQTT命令行测试工具，这个强大的工具不仅方便安装，还提供了丰富且完善的各类测试命令和较为完整的MQTT配置参数，可以方便用户快速集成到一些测试脚本中。因此，无论是对于开发人员还是普通用户来说，MQTT X都是一款非常实用的工具。

![MQTT_CONNECT报文协商会话](./imgs/network/mqtt/MQTT_CONNECT报文协商会话.jpg)

Apache ActiveMQ 是一个开源的消息代理（Message Broker），它支持多种协议，包括 MQTT。您可以使用 ActiveMQ 来搭建一个支持 MQTT 协议的消息服务器。

以下是使用 Apache ActiveMQ 搭建 MQTT 服务器的简要步骤：

1. 下载 ActiveMQ：首先，您需要从 Apache ActiveMQ 的官方网站下载 ActiveMQ 的最新版本：[https://activemq.apache.org/](https://activemq.apache.org/)

2. 安装 ActiveMQ：解压下载的 ActiveMQ 压缩包，并根据官方文档中的说明进行安装和配置。

3. 配置 MQTT 协议：在 ActiveMQ 中启用 MQTT 协议，您可以通过修改 ActiveMQ 的配置文件来实现。在 `activemq.xml` 配置文件中添加如下配置：

    ```xml
    <transportConnectors>
        <!-- MQTT -->
        <transportConnector name="mqtt" uri="mqtt://0.0.0.0:1883"/>
    </transportConnectors>
    ```

4. 启动 ActiveMQ：启动 ActiveMQ 服务，确保 MQTT 协议已经启用。

5. Java MQTT 客户端：使用 Java 编写的 MQTT 客户端可以连接到 ActiveMQ 提供的 MQTT 服务，进行消息的发布和订阅等操作。

请注意，Apache ActiveMQ 是一个强大的消息中间件，支持多种协议和功能，包括 JMS、STOMP、OpenWire 等。在您的项目中使用 ActiveMQ 时，可以根据需要选择适合的协议和功能。

希望这些信息能帮助您开始使用 Apache ActiveMQ 搭建一个支持 MQTT 协议的消息服务器。
