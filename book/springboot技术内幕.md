springboot技术内幕

朱智胜
Spring Boot的布道者、技术专家，畅销书作者，技术专栏作者，国内知名技术论坛博客专家，现任某跨境支付公司技术负责人。
精通Spring Boot框架及其源代码，具有多年的Spring Boot框架使用经验。曾基于Spring Boot搭建风控反洗钱系统，支持1.5亿用户及3000亿交易的风控反洗钱数据处理。
精通Java语言，擅长Spring系列框架的使用，对其源码进行过深入研究，拥有10余年Java开发经验。
乐于分享，曾自主录制多套畅销技术视频教程，累计播放超2万人次。通过微信公众号分享的Spring Boot源码解析系列文章，累计阅读量达30万人次，广受读者好评。

★部分　准备篇

第1章　阅读代码前的准备 2
1.1　获取和调试Spring Boot源代码  2

1.1.1　获取Spring Boot的源代码  2

1.1.2　调试Spring Boot的源代码  3

1.2　Spring Boot源代码的目录结构  3

1.2.1　Spring Boot的整体项目结构  4

1.2.2　spring-boot-project项目结构  5

1.3　源代码阅读工具  5

1.4　Spring Boot的设计理念和目标  6

1.4.1　设计理念  7

1.4.2　设计目标  7

1.5　Spring Boot的整体架构  7

 

★第二部分　原理篇

第2章　Spring Boot核心运行原理 10
2.1　核心运行原理  10

2.2　运作原理源码解析之@EnableAuto-Configuration  11

2.2.1　入口类和@SpringBootApplication注解  11

2.2.2　注解@EnableAutoConf?iguration功能解析  14

2.3　AutoConf?igurationImportSelector源码解析  15

2.3.1　@Import注解  16

2.3.2　ImportSelector接口  16

2.3.3　AutoConf?igurationImportSelector功能概述  17

2.3.4　@EnableAutoConf?iguration自动配置开关  18

2.3.5　@EnableAutoConf?iguration加载元数据配置  19

2.3.6　@EnableAutoConf?iguration加载自动配置组件  21

2.3.7　@EnableAutoConf?iguration排除指定组件  24

2.3.8　@EnableAutoConf?iguration过滤自动配置组件  25

2.3.9　@EnableAutoConf?iguration事件注册  32

2.4　@Conditional条件注解  33

2.4.1　认识条件注解  33

2.4.2　条件注解的衍生注解  34

2.5　实例解析  39

2.6　小结  41

第3章　Spring Boot构造流程源码分析 42
3.1　SpringApplication的初始化简介  42

3.2　SpringApplication实例化流程  43

3.3　SpringApplication构造方法参数  44

3.4　Web应用类型推断  45

3.5　ApplicationContextInitializer加载  47

3.5.1　源码解析  47

3.5.2　实例讲解  49

3.6　ApplicationListener加载  50

3.7　入口类推断  51

3.8　SpringApplication的定制化配置  52

3.8.1　基础配置  52

3.8.2　配置源配置  53

3.9　小结  54

第4章　Spring Boot运行流程源码分析 55
4.1　run方法核心流程  55

4.2　SpringApplicationRunListener监听器  57

4.2.1　监听器的配置与加载  57

4.2.2　SpringApplicationRunListener源码解析  59

4.2.3　实现类EventPublishingRun-Listener  60

4.2.4　自定义SpringApplicationRun-Listener  62

4.3　初始化ApplicationArguments  63

4.4　初始化Conf?igurableEnvironment  63

4.4.1　获取或创建环境  65

4.4.2　配置环境  66

4.5　忽略信息配置  68

4.6　打印Banner  68

4.7　Spring应用上下文的创建  69

4.8　Spring应用上下文的准备  70

4.8.1　应用上下文准备阶段  71

4.8.2　应用上下文加载阶段  73

4.9　Spring应用上下文的刷新  75

4.10　调用ApplicationRunner和CommandLineRunner  77

4.11　小结  78

 

★第三部分　内置组件篇

第5章　Spring Boot外化配置源码解析 80
5.1　外化配置简介  80

5.2　ApplicationArguments 参数处理  81

5.2.1　接口定义及初始化  81

5.2.2　使用实例  85

5.3　命令参数的获取  86

5.4　配置文件的加载  88

5.5　基于Prof?ile的处理实现  93

5.6　综合实战  97

5.7　小结  102

第6章　Spring Boot Web应用源码解析 103
6.1　遗失的web.xml  103

6.2　Web应用的自动配置  104

6.2.1　DispatcherServlet自动配置  105

6.2.2　DispatcherServletRegistrationBean自动配置  108

6.3　Spring MVC的自动配置  111

6.3.1　ViewResolver解析  112

6.3.2　静态资源的支持  114

6.3.3　静态index.html  115

6.4　综合实战  117

6.5　小结  120

第7章　Spring Boot 内置Servlet容器源码解析 121
7.1　Web容器自动配置  121

7.1.1　Servlet Web服务器概述  121

7.1.2　自动配置源码分析  122

7.2　WebServer初始化过程  128

7.3　DispatcherServlet的加载过程  134

7.3.1　DispatcherServlet的获取  134

7.3.2　DispatcherServlet的加载  138

7.4　综合实战  140

7.5　小结  141

第8章　Spring Boot 数据库配置源码解析 142
8.1　自动配置注解解析  142

8.2　自动配置内部实现解析  150

8.2.1　EmbeddedDatabase-Configuration  151

8.2.2　PooledDataSource-Configuration  155

8.3　JdbcTemplateAutoConfiguration  157

8.4　异常案例分析  159

8.5　小结  159

第9章　Spring Boot 消息源码解析 160
9.1　JMS基础自动配置  160

9.1.1　JmsAutoConf?iguration的注解  160

9.1.2　JmsAutoConf?iguration内部实现  164

9.2　ActiveMQ自动配置  166

9.3　@JmsListener注解解析  173

9.4　小结  175

第10章　Spring Boot Cache源码解析 176
10.1　Cache简介  176

10.2　Cache自动配置  177

10.3　默认Cache配置  183

10.4　小结  188

第11章　Spring Boot 日志源码解析 189
11.1　LoggingApplicationListener的触发  189

11.2　LoggingApplicationListener的执行  191

11.2.1　ApplicationStartingEvent事件处理  192

11.2.2　ApplicationEnvironment-PreparedEvent事件处理  196

11.3　小结  203

第12章　实战：创建Spring Boot自动配置项目 204
12.1　自定义Spring Boot Starter项目  204

12.2　Starter测试使用  207

12.3　小结  208

 

★第四部分　外置组件篇

第13章　Spring Boot单元测试 210
13.1　Spring Boot对单元测试的支持  210

13.2　常用单元测试注解  211

13.3　JUnit5单元测试示例  212

13.4　Web应用单元测试  214

13.5　MockMvc的自动配置  217

13.5.1　AutoConf?igureMockMvc注解  217

13.5.2　MockMvcAutoConf?iguration自动配置  219

13.6　小结  221

第14章　Spring Boot打包部署解析 222
14.1　Spring Boot的jar包  222

14.1.1　jar包的生成  222

14.1.2　jar包的结构  227

14.2　Launcher实现原理  227

14.2.1　JarLauncher  228

14.2.2　WarLauncher  232

14.3　小结  234

第15章　Spring Boot 应用监控解析 235
15.1　Actuator简介  235

15.2　Actuator自动配置  237

15.2.1　HealthEndpoint自动配置  237

15.2.2　HealthIndicator实现  240

15.3　Actuator端点展示  244

15.4　小结  247

第16章　Spring Boot Security支持 248
16.1　Security自动配置  248

16.2　SecurityAutoConfiguration详解  249

16.3　SecurityFilterAutoConfiguration详解  255

16.4　小结  257

