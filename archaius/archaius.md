# archaius

中间
https://github.com/Netflix/archaius

配置文件

hystrix用到了

Spring Cloud中用到了Hystrix

公司封装了，弃用

首先来看看Archaius解决了什么问题，在大型分布式系统中，在大型分布式系统中经常会存在下面的几类问题：
1.需用从配置中新获取配置，加载到本地内存。
2.配置中心的配置发生变化，需要动态更新本地内存中的配置。
3.配置中心的配置发生变换，需要接收通知。

archaius如何解决上面的问题：
其实archaius解决方法很简单，就是定时从配置中心去读取数据，并且更新内存中相关配置，并且通知监听的监听器更新内容。
通过archaius我们就可以实现动态配置了

Archaius 是一个开源的Java配置管理库，由Netflix开发并开源。它主要用于管理应用程序的配置信息，支持动态配置更新和多种配置源。Archaius 是 Netflix 在构建大规模分布式系统时，为了更好地管理配置信息而开发的工具，它提供了灵活的配置管理功能，能够适应快速变化的配置需求。
Archaius 的主要功能
动态配置更新：
Archaius 支持动态更新配置信息，而无需重启应用程序。这对于需要实时调整配置参数的分布式系统非常有用。
多种配置源：
Archaius 支持从多种配置源加载配置信息，包括：
本地文件：从本地的属性文件（如 .properties 文件）加载配置。
远程配置中心：从远程配置中心（如 Consul、Etcd、Zookeeper 等）加载配置。
环境变量：从环境变量中加载配置。
系统属性：从系统属性中加载配置。
配置监听器：
Archaius 提供了配置监听器机制，允许应用程序在配置信息发生变化时，自动接收到通知并进行相应的处理。
配置优先级：
Archaius 支持配置优先级，允许从多个配置源加载配置信息，并根据优先级规则决定最终的配置值。
集成简单：
Archaius 提供了简单的API，方便开发者在应用程序中集成配置管理功能。
Archaius 的使用场景
分布式系统：
在分布式系统中，配置信息可能需要根据不同的环境（如开发、测试、生产）进行动态调整。Archaius 提供了灵活的配置管理机制，能够满足这种需求。
微服务架构：
在微服务架构中，每个微服务可能需要独立的配置管理。Archaius 可以帮助微服务动态加载和更新配置信息，而无需重启服务。
云原生应用：
在云原生应用中，配置信息可能需要根据不同的部署环境进行动态调整。Archaius 提供了与云原生环境（如 Kubernetes）的集成能力，能够更好地支持云原生应用的配置管理。
Archaius 的基本使用
以下是一个简单的示例，展示如何在Java应用程序中使用Archaius进行配置管理。

1. 添加依赖

在pom.xml文件中添加Archaius的依赖：

```xml复制
<dependencies>
    <!-- Archaius Core -->
    <dependency>
        <groupId>com.netflix.archaius</groupId>
        <artifactId>archaius-core</artifactId>
        <version>0.7.6</version>
    </dependency>

    <!-- Archaius Commons Configuration -->
    <dependency>
        <groupId>com.netflix.archaius</groupId>
        <artifactId>archaius-api</artifactId>
        <version>0.7.6</version>
    </dependency>
</dependencies>
```

2. 创建配置文件
创建一个本地配置文件application.properties，并添加一些配置项：
properties复制
# application.properties
app.name=MyApp
app.version=1.0.0
3. 加载配置
在Java代码中加载配置文件，并获取配置值：
java复制
import com.netflix.config.ConfigurationManager;
import com.netflix.config.DynamicPropertyFactory;

public class ArchaiusExample {
    public static void main(String[] args) {
        // 加载配置文件
        ConfigurationManager.loadPropertiesFromResources("application.properties");

        // 获取配置值
        String appName = DynamicPropertyFactory.getInstance().getStringProperty("app.name", "default").get();
        String appVersion = DynamicPropertyFactory.getInstance().getStringProperty("app.version", "default").get();

        // 输出配置值
        System.out.println("App Name: " + appName);
        System.out.println("App Version: " + appVersion);
    }
}

总结
Archaius 是一个功能强大的配置管理库，特别适合分布式系统和微服务架构。它支持动态配置更新、多种配置源、配置监听器等功能，能够帮助开发者更好地管理应用程序的配置信息。通过简单的集成，你可以在Java应用程序中使用Archaius进行灵活的配置管理。
