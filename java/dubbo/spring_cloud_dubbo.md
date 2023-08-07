# spring_cloud_dubbo

```xml
		<dependency>
			<groupId>com.alibaba.cloud</groupId>
			<artifactId>spring-cloud-starter-dubbo</artifactId>
            <version>2.2.6.RELEASE</version>
		</dependency>
```

## 源代码分包解析



https://javadoc.dev/online/api/com.alibaba.cloud/spring-cloud-starter-dubbo/2.2.6.RELEASE/index.html





### com.alibaba.cloud.dubbo.actuate



| com.alibaba.cloud.dubbo.actuate        |      |      |
| -------------------------------------- | ---- | ---- |
| DubboMetadataEndpointAutoConfiguration |      |      |
|                                        |      |      |
|                                        |      |      |

##### com.alibaba.cloud.dubbo.actuate.endpoint



| Classes                   |      |      |
| ------------------------- | ---- | ---- |
|                           |      |      |
| DubboDiscoveryEndpoint    |      |      |
| DubboExportedURLsEndpoint |      |      |
| DubboRestMetadataEndpoint |      |      |





### com.alibaba.cloud.dubbo.annotation



| com.alibaba.cloud.dubbo.annotation |      |      |
| ---------------------------------- | ---- | ---- |
| DubboTransported                   |      |      |
|                                    |      |      |
|                                    |      |      |

### com.alibaba.cloud.dubbo.autoconfigure









| com.alibaba.cloud.dubbo.autoconfigure                      |      |      |
| ---------------------------------------------------------- | ---- | ---- |
| Classes                                                    |      |      |
|                                                            |      |      |
| DubboLoadBalancedRestTemplateAutoConfiguration             |      |      |
| DubboMetadataAutoConfiguration                             |      |      |
| DubboOpenFeignAutoConfiguration                            |      |      |
| DubboServiceAutoConfiguration                              |      |      |
| DubboServiceDiscoveryAutoConfiguration                     |      |      |
| DubboServiceRegistrationAutoConfiguration                  |      |      |
| DubboServiceRegistrationNonWebApplicationAutoConfiguration |      |      |



#### com.alibaba.cloud.dubbo.autoconfigure.condition



| com.alibaba.cloud.dubbo.autoconfigure.condition   |      |      |
| ------------------------------------------------- | ---- | ---- |
| MissingSpringCloudRegistryConfigPropertyCondition |      |      |
|                                                   |      |      |
|                                                   |      |      |





### com.alibaba.cloud.dubbo.bootstrap



| com.alibaba.cloud.dubbo.bootstrap    |      |      |
| ------------------------------------ | ---- | ---- |
| DubboBootstrapStartCommandLineRunner |      |      |
| DubboBootstrapWrapper                |      |      |
|                                      |      |      |



##### com.alibaba.cloud.dubbo.bootstrap.event



DubboBootstrapStartedEvent



### com.alibaba.cloud.dubbo.client.loadbalancer



| com.alibaba.cloud.dubbo.client.loadbalancer |      |      |
| ------------------------------------------- | ---- | ---- |
| DubboMetadataInitializerInterceptor         |      |      |
| DubboTransporterInterceptor                 |      |      |
|                                             |      |      |


### com.alibaba.cloud.dubbo.context



| com.alibaba.cloud.dubbo.context                       |      |      |
| ----------------------------------------------------- | ---- | ---- |
| DubboServiceRegistrationApplicationContextInitializer |      |      |
|                                                       |      |      |
|                                                       |      |      |


### com.alibaba.cloud.dubbo.env



| com.alibaba.cloud.dubbo.env                    |      |      |
| ---------------------------------------------- | ---- | ---- |
| DubboCloudProperties                           |      |      |
| DubboNonWebApplicationEnvironmentPostProcessor |      |      |
|                                                |      |      |


### com.alibaba.cloud.dubbo.http



| com.alibaba.cloud.dubbo.http |           |                             |
| ---------------------------- | --------- | --------------------------- |
| ByteArrayHttpInputMessage    |           |                             |
| DefaultHttpRequest           |           |                             |
| DefaultHttpRequest Builder   |           |                             |
| HttpServerRequest            | interface |                             |
| MutableHttpServerRequest     |           | HttpServerRequest接口实现类 |
|                              |           |                             |



MutableHttpServerRequest



### com.alibaba.cloud.dubbo.metadata



| com.alibaba.cloud.dubbo.metadata |      |      |
| -------------------------------- | ---- | ---- |
|                                  |      |      |
|                                  |      |      |
|                                  |      |      |


### com.alibaba.cloud.dubbo.openfeign





| com.alibaba.cloud.dubbo.openfeign |      |      |
| --------------------------------- | ---- | ---- |
|                                   |      |      |
| DubboInvocationHandler            |      |      |
| TargeterBeanPostProcessor         |      |      |



### com.alibaba.cloud.dubbo.registry





| com.alibaba.cloud.dubbo.registry              |      |      |
| --------------------------------------------- | ---- | ---- |
|                                               |      |      |
| ServiceInstanceChangeListener                 |      |      |
|                                               |      |      |
| Classes                                       |      |      |
|                                               |      |      |
| AbstractServiceSubscribeHandler               |      |      |
| AbstractSpringCloudRegistry                   |      |      |
| DubboCloudRegistry                            |      |      |
| DubboServiceRegistrationEventPublishingAspect |      |      |
| GenearalServiceSubscribeHandler               |      |      |
| MetadataServiceSubscribeHandler               |      |      |
| ReSubscribeManager                            |      |      |
| SpringCloudRegistry                           |      |      |
| SpringCloudRegistryFactory                    |      |      |



#### com.alibaba.cloud.dubbo.registry.event



| Classes                             |      |      |
| ----------------------------------- | ---- | ---- |
|                                     |      |      |
| ServiceInstancePreDeregisteredEvent |      |      |
| ServiceInstancePreRegisteredEvent   |      |      |
| ServiceInstanceRegisteredEvent      |      |      |
| ServiceInstancesChangedEvent        |      |      |
| SubscribedServicesChangedEvent      |      |      |



### com.alibaba.cloud.dubbo.service



| com.alibaba.cloud.dubbo.service            |           |                                |
| ------------------------------------------ | --------- | ------------------------------ |
| DubboGenericServiceExecutionContext        |           |                                |
| DubboGenericServiceExecutionContextFactory |           |                                |
| DubboGenericServiceFactory                 |           |                                |
| DubboMetadataService                       | interface |                                |
| DubboMetadataServiceExporter               |           |                                |
| DubboMetadataServiceInvocationHandler      |           |                                |
| DubboMetadataServiceProxy                  |           |                                |
| IntrospectiveDubboMetadataService          |           | DubboMetadataService接口实现类 |
| MetadataServiceRevisionRouterFactory       |           |                                |





#### com.alibaba.cloud.dubbo.service.parameter



| Interfaces                                   |      |      |
| -------------------------------------------- | ---- | ---- |
|                                              |      |      |
| DubboGenericServiceParameterResolver         |      |      |
|                                              |      |      |
| Classes                                      |      |      |
|                                              |      |      |
| AbstractDubboGenericServiceParameterResolver |      |      |
| AbstractNamedValueServiceParameterResolver   |      |      |
| PathVariableServiceParameterResolver         |      |      |
| RequestBodyServiceParameterResolver          |      |      |
| RequestHeaderServiceParameterResolver        |      |      |
| RequestParamServiceParameterResolver         |      |      |



### com.alibaba.cloud.dubbo.util



| Classes             |      |      |
| ------------------- | ---- | ---- |
|                     |      |      |
| DubboCloudConstants |      |      |
| DubboMetadataUtils  |      |      |
| JSONUtils           |      |      |