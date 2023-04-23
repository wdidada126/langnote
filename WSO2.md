# WSO2

- wso2 开发ide wso2 Integration Studio，基于eclipse定制的
- 可运行程序 


E:\wso2esb-5.0.0\bin 运行时？

ps运行

cd E:\wso2esb-5.0.0
.\bin/wso2server.bat


.\bin/wso2server.bat
JAVA_HOME environment variable is set to D:\Java\jdk1.8.0_231
CARBON_HOME environment variable is set to E:\wso2esb-5.0.0\bin\..
Java HotSpot(TM) 64-Bit Server VM warning: ignoring option MaxPermSize=256m; support was removed in 8.0
[2023-04-22 23:50:25,406]  INFO - CarbonCoreActivator Starting WSO2 Carbon...
[2023-04-22 23:50:25,414]  INFO - CarbonCoreActivator Operating System : Windows 10 10.0, amd64
[2023-04-22 23:50:25,414]  INFO - CarbonCoreActivator Java Home        : D:\Java\jdk1.8.0_231\jre
[2023-04-22 23:50:25,414]  INFO - CarbonCoreActivator Java Version     : 1.8.0_231
[2023-04-22 23:50:25,414]  INFO - CarbonCoreActivator Java VM          : Java HotSpot(TM) 64-Bit Server VM 25.231-b11,Oracle Corporation
[2023-04-22 23:50:25,415]  INFO - CarbonCoreActivator Carbon Home      : E:\wso2esb-5.0.0\bin\..
[2023-04-22 23:50:25,415]  INFO - CarbonCoreActivator Java Temp Dir    : E:\wso2esb-5.0.0\bin\..\tmp
[2023-04-22 23:50:25,415]  INFO - CarbonCoreActivator User             : edidada, zh-CN, Asia/Shanghai
[2023-04-22 23:50:25,569]  WARN - ValidationResultPrinter The running OS : Windows 10 is not a tested Operating System for running WSO2 Carbon
[2023-04-22 23:50:25,571]  WARN - ValidationResultPrinter Carbon is configured to use the default keystore (wso2carbon.jks). To maximize security when deploying to a production environment, configure a new keystore with a unique password in the production server profile.
[2023-04-22 23:50:25,696]  INFO - KafkaEventAdapterServiceDS Successfully deployed the Kafka output event adaptor service
[2023-04-22 23:50:25,775]  INFO - ManagementModeConfigurationLoader CEP started in Single node mode
[2023-04-22 23:50:31,207]  INFO - EmbeddedRegistryService Configured Registry in 114ms
[2023-04-22 23:50:31,291]  INFO - RegistryCoreServiceComponent Registry Mode    : READ-WRITE
[2023-04-22 23:50:36,745]  INFO - SolrClient Default Embedded Solr Server Initialized
[2023-04-22 23:50:37,370]  INFO - UserStoreMgtDSComponent Carbon UserStoreMgtDSComponent activated successfully.
[2023-04-22 23:50:44,761]  INFO - TaglibUriRule TLD skipped. URI: http://tiles.apache.org/tags-tiles is already defined
[2023-04-22 23:50:46,340]  INFO - ClusterBuilder Clustering has been disabled
[2023-04-22 23:50:46,646]  INFO - UserStoreConfigurationDeployer User Store Configuration Deployer initiated.
[2023-04-22 23:50:46,646]  INFO - UserStoreConfigurationDeployer User Store Configuration Deployer initiated.
[2023-04-22 23:50:46,660]  INFO - PassThroughHttpSender Initializing Pass-through HTTP/S Sender...
[2023-04-22 23:50:46,671]  INFO - PassThroughHttpSender No proxy configuration found
[2023-04-22 23:50:46,722]  INFO - PassThroughHttpSender Pass-through HTTP Sender started...
[2023-04-22 23:50:46,722]  INFO - PassThroughHttpSSLSender Initializing Pass-through HTTP/S Sender...
[2023-04-22 23:50:46,723]  INFO - PassThroughHttpSSLSender No proxy configuration found
[2023-04-22 23:50:46,725]  INFO - ClientConnFactoryBuilder HTTPS Loading Identity Keystore from : repository/resources/security/wso2carbon.jks
[2023-04-22 23:50:46,732]  INFO - ClientConnFactoryBuilder HTTPS Loading Trust Keystore from : repository/resources/security/client-truststore.jks
[2023-04-22 23:50:46,737]  INFO - PassThroughHttpSSLSender Pass-through HTTPS Sender started...
[2023-04-22 23:50:46,750]  INFO - PassThroughHttpListener Initializing Pass-through HTTP/S Listener...
[2023-04-22 23:50:46,800]  INFO - PassThroughHttpSSLListener Initializing Pass-through HTTP/S Listener...
[2023-04-22 23:50:48,196]  INFO - ModuleDeployer Deploying module: addressing-1.6.1-wso2v19 - file:/E:/wso2esb-5.0.0/bin/../repository/deployment/client/modules/addressing-1.6.1-wso2v19.mar
[2023-04-22 23:50:48,341]  INFO - ModuleDeployer Deploying module: rampart-1.6.1-wso2v18 - file:/E:/wso2esb-5.0.0/bin/../repository/deployment/client/modules/rampart-1.6.1-wso2v18.mar
[2023-04-22 23:50:49,801]  INFO - DeploymentEngine Deploying Web service: org.wso2.carbon.message.processor-4.6.6 -
[2023-04-22 23:50:49,817]  INFO - DeploymentEngine Deploying Web service: org.wso2.carbon.message.store-4.6.6 -
[2023-04-22 23:50:50,637]  INFO - DeploymentInterceptor Deploying Axis2 service: wso2carbon-sts {super-tenant}
[2023-04-22 23:50:50,665]  INFO - DeploymentEngine Deploying Web service: org.wso2.carbon.sts-5.1.1 -
[2023-04-22 23:50:50,759]  INFO - DeploymentEngine Deploying Web service: org.wso2.carbon.tryit-4.5.4 -
[2023-04-22 23:50:50,994]  INFO - CarbonServerManager Repository       : E:\wso2esb-5.0.0\bin\../repository/deployment/server/
[2023-04-22 23:50:51,050]  INFO - TenantLoadingConfig Using tenant lazy loading policy...
[2023-04-22 23:50:51,066]  INFO - PermissionUpdater Permission cache updated for tenant -1234
[2023-04-22 23:50:51,137]  INFO - RuleEngineConfigDS Successfully registered the Rule Config service
[2023-04-22 23:50:51,203]  INFO - ServiceBusInitializer Starting ESB...
[2023-04-22 23:50:51,217]  INFO - ServiceBusInitializer Initializing Apache Synapse...
[2023-04-22 23:50:51,222]  INFO - SynapseControllerFactory Using Synapse home : E:\wso2esb-5.0.0\.
[2023-04-22 23:50:51,229]  INFO - SynapseControllerFactory Using synapse.xml location : E:\wso2esb-5.0.0\.\.\repository\deployment\server\synapse-configs\default
[2023-04-22 23:50:51,230]  INFO - SynapseControllerFactory Using server name : localhost
[2023-04-22 23:50:51,234]  INFO - SynapseControllerFactory The timeout handler will run every : 15s
[2023-04-22 23:50:51,244]  INFO - Axis2SynapseController Initializing Synapse at : Sat Apr 22 23:50:51 CST 2023
[2023-04-22 23:50:51,256]  INFO - CarbonSynapseController Loading the mediation configuration from the file system
[2023-04-22 23:50:51,266]  INFO - MultiXMLConfigurationBuilder Building synapse configuration from the synapse artifact repository at : .\.\repository/deployment/server/synapse-configs\default
[2023-04-22 23:50:51,280]  INFO - XMLConfigurationBuilder Generating the Synapse configuration model by parsing the XML configuration
[2023-04-22 23:50:51,371]  INFO - DependencyTracker Sequence : fault was added to the Synapse configuration successfully
[2023-04-22 23:50:51,387]  INFO - DependencyTracker Sequence : main was added to the Synapse configuration successfully
[2023-04-22 23:50:51,405]  INFO - DependencyTracker API : HospitalServiceApi was added to the Synapse configuration successfully
[2023-04-22 23:50:51,407]  INFO - SynapseConfigurationBuilder Loaded Synapse configuration from the artifact repository at : .\.\repository/deployment/server/synapse-configs\default
[2023-04-22 23:50:51,409]  INFO - DependencyTracker Local entry : SERVER_HOST was added to the Synapse configuration successfully
[2023-04-22 23:50:51,411]  INFO - DependencyTracker Local entry : SERVER_IP was added to the Synapse configuration successfully
[2023-04-22 23:50:51,414]  INFO - Axis2SynapseController Loading mediator extensions...
[2023-04-22 23:50:51,444]  INFO - DeploymentInterceptor Deploying Axis2 service: echo {super-tenant}
[2023-04-22 23:50:51,445]  INFO - DeploymentEngine Deploying Web service: Echo.aar - file:/E:/wso2esb-5.0.0/bin/../repository/deployment/server/axis2services/Echo.aar
[2023-04-22 23:50:51,496]  INFO - DeploymentInterceptor Deploying Axis2 service: Version {super-tenant}
[2023-04-22 23:50:51,497]  INFO - DeploymentEngine Deploying Web service: Version.aar - file:/E:/wso2esb-5.0.0/bin/../repository/deployment/server/axis2services/Version.aar
[2023-04-22 23:50:51,517]  INFO - EventPublisherDeployer Event Publisher deployment held back and in inactive state :MessageFlowConfigurationPublisher.xml, Stream validation exception : Stream org.wso2.esb.analytics.stream.ConfigEntry:1.0.0 does not exist
[2023-04-22 23:50:51,532]  INFO - EventPublisherDeployer Event Publisher deployment held back and in inactive state :MessageFlowStatisticsPublisher.xml, Stream validation exception : Stream org.wso2.esb.analytics.stream.FlowEntry:1.0.0 does not exist
[2023-04-22 23:50:51,590]  INFO - EventPublisherDeployer Event Publisher undeployed successfully : MessageFlowConfigurationPublisher.xml
[2023-04-22 23:50:51,841]  INFO - EventJunction WSO2EventConsumer added to the junction. Stream:org.wso2.esb.analytics.stream.ConfigEntry:1.0.0
[2023-04-22 23:50:51,848]  INFO - EventPublisherDeployer Event Publisher configuration successfully deployed and in active state : MessageFlowConfigurationPublisher
[2023-04-22 23:50:51,849]  INFO - EventStreamDeployer Stream definition is deployed successfully  : org.wso2.esb.analytics.stream.ConfigEntry:1.0.0
[2023-04-22 23:50:51,865]  INFO - EventPublisherDeployer Event Publisher undeployed successfully : MessageFlowStatisticsPublisher.xml
[2023-04-22 23:50:51,870]  INFO - EventJunction WSO2EventConsumer added to the junction. Stream:org.wso2.esb.analytics.stream.FlowEntry:1.0.0
[2023-04-22 23:50:51,873]  INFO - EventPublisherDeployer Event Publisher configuration successfully deployed and in active state : MessageFlowStatisticsPublisher
[2023-04-22 23:50:51,874]  INFO - EventStreamDeployer Stream definition is deployed successfully  : org.wso2.esb.analytics.stream.FlowEntry:1.0.0
[2023-04-22 23:50:51,876]  INFO - Axis2SynapseController Deploying the Synapse service...
[2023-04-22 23:50:51,880]  INFO - Axis2SynapseController Deploying Proxy services...
[2023-04-22 23:50:51,880]  INFO - Axis2SynapseController Deploying EventSources...
[2023-04-22 23:50:51,913]  INFO - API Initializing API: HospitalServiceApi
[2023-04-22 23:50:51,922]  INFO - ServerManager Server ready for processing...
[2023-04-22 23:50:51,978]  INFO - MediationStatisticsComponent Global Message-Flow Statistic Reporting is Disabled
[2023-04-22 23:50:53,126]  INFO - PassThroughHttpListener Starting Pass-through HTTP Listener...
[2023-04-22 23:50:53,147]  INFO - PassThroughListeningIOReactorManager Pass-through HTTP Listener started on 0:0:0:0:0:0:0:0:8280
[2023-04-22 23:50:53,148]  INFO - PassThroughHttpSSLListener Starting Pass-through HTTPS Listener...
[2023-04-22 23:50:53,171]  INFO - PassThroughListeningIOReactorManager Pass-through HTTPS Listener started on 0:0:0:0:0:0:0:0:8243
[2023-04-22 23:50:53,234]  INFO - NioSelectorPool Using a shared selector for servlet write/read
[2023-04-22 23:50:53,306]  INFO - NioSelectorPool Using a shared selector for servlet write/read
[2023-04-22 23:50:53,471]  INFO - TaskServiceImpl Task service starting in STANDALONE mode...
[2023-04-22 23:50:53,523]  INFO - NTaskTaskManager Initialized task manager. Tenant [-1234]
[2023-04-22 23:50:53,620]  INFO - JMXServerManager JMX Service URL  : service:jmx:rmi://localhost:11111/jndi/rmi://localhost:9999/jmxrmi
[2023-04-22 23:50:53,623]  INFO - StartupFinalizerServiceComponent Server           :  WSO2 Enterprise Service Bus-5.0.0
[2023-04-22 23:50:53,626]  INFO - StartupFinalizerServiceComponent WSO2 Carbon started in 36 sec
[2023-04-22 23:50:54,510]  INFO - CarbonUIServiceComponent Mgt Console URL  : https://192.168.56.1:9443/carbon/

访问

https://192.168.56.1:9443/carbon/admin/login.jsp

截图
wso2_esb.PNG
E:\IntegrationStudio  ide


官方教程
https://docs.wso2.com/display/ESB500/Quick+Start+Guide



Axis2网站http://ws.apache.org/axis2/


最近在做一个企业服务总线的系统   技术选型最后选择WSO2
对ESB基础了解后,做了个简单的WSO2汉化版本    相关文件上传至百度网盘
地址:    https://pan.baidu.com/s/1jKeQLSi

wso2esb-5.0.0.zip
https://docs.wso2.com/display/ESB500/About+this+Release

https://blog.csdn.net/Wwl_Java/article/details/79077419

WSO2 ESB 5.0只能是java 1.7

product-esb-5.0.0.zip

https://github.com/wso2-attic/product-esb/releases



WSO2 ESB 5.0部署以及汉化
https://blog.csdn.net/Wwl_Java/article/details/79077419


WSO2 ESB 学习教程 第一章 项目的创建
https://blog.csdn.net/weixin_41195466/article/details/104695367

系列教程
https://so.csdn.net/so/search?q=wso2&t=blog&u=weixin_41195466

通过运行示例从WSO2 ESB开始
https://blog.csdn.net/dnc8371/article/details/106705714

