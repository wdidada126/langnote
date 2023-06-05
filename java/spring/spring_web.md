spring_web



HandlerMethodArgumentResolver hmar
spring-web这个jar下面的接口
public interface HandlerMethodArgumentResolver {
    boolean supportsParameter(MethodParameter parameter);

    @Nullable
    Object resolveArgument(MethodParameter parameter, @Nullable ModelAndViewContainer mavContainer, NativeWebRequest webRequest, @Nullable WebDataBinderFactory binderFactory) throws Exception;
}

springmvc自带的一些实现：
ServletRequestMethodArgumentResolver和ServletResponseMethodArgumentResolver处理了自动绑定HttpServletRequest和HttpServletResponse
RequestParamMapMethodArgumentResolver处理了@RequestParam
RequestHeaderMapMethodArgumentResolver处理了@RequestHeader
PathVariableMapMethodArgumentResolver处理了@PathVariable
ModelAttributeMethodProcessor处理了@ModelAttribute
RequestResponseBodyMethodProcessor处理了@RequestBody
https://www.cnblogs.com/wangjing666/p/10770726.html


https://tomcat.apache.org/lists.html
dev-subscribe@tomcat.apache.org

debug tomcat source code
https://blog.csdn.net/wangjunjie0817/article/details/102944338
https://juejin.cn/post/6844903859828031501



org.springframework.beans.factory.Aware

Spring实现Aware接口，完成对IOC容器的感知
https://blog.csdn.net/ilovejava_2010/article/details/7953582

BeanNameAware，可以在Bean中得到它在IOC容器中的Bean的实例的名字。
BeanFactoryAware，可以在Bean中得到Bean所在的IOC容器，从而直接在Bean中使用IOC容器的服务。
ApplicationContextAware，可以在Bean中得到Bean所在的应用上下文，从而直接在Bean中使用上下文的服务。
MessageSourceAware，在Bean中可以得到消息源。
ApplicationEventPublisherAware，在bean中可以得到应用上下文的事件发布器，从而可以在Bean中发布应用上下文的事件。
ResourceLoaderAware，在Bean中可以得到ResourceLoader，从而在bean中使用ResourceLoader加载外部对应的Resource资源。
ImportAware
EmbeddedValueResolverAware
EnvironmentAware
BootstrapContextAware
BeanClassLoaderAware
LoadTimeWeaverAware
NotificationPublisherAware
ServletConfigAware




MapMethodProcessor (org.springframework.web.method.annotation)
SortArgumentResolver (org.springframework.data.web)
    SortHandlerMethodArgumentResolver (org.springframework.data.web)
        HateoasSortHandlerMethodArgumentResolver (org.springframework.data.web)
ErrorsMethodArgumentResolver (org.springframework.web.method.annotation)
PathVariableMapMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
AbstractNamedValueMethodArgumentResolver (org.springframework.web.method.annotation)
    RequestHeaderMethodArgumentResolver (org.springframework.web.method.annotation)
    RequestAttributeMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
    RequestParamMethodArgumentResolver (org.springframework.web.method.annotation)
    AbstractCookieValueMethodArgumentResolver (org.springframework.web.method.annotation)
        ServletCookieValueMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
    ExpressionValueMethodArgumentResolver (org.springframework.web.method.annotation)
    SessionAttributeMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
    MatrixVariableMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
    PathVariableMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
RequestHeaderMapMethodArgumentResolver (org.springframework.web.method.annotation)
ModelMethodProcessor (org.springframework.web.method.annotation)
ModelAttributeMethodProcessor (org.springframework.web.method.annotation)
    ServletModelAttributeMethodProcessor (org.springframework.web.servlet.mvc.method.annotation)
    ProxyingHandlerMethodArgumentResolver (org.springframework.data.web)
ServletResponseMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
SessionStatusMethodArgumentResolver (org.springframework.web.method.annotation)
RequestParamMapMethodArgumentResolver (org.springframework.web.method.annotation)
PrincipalMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
ContinuationHandlerMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
AbstractMessageConverterMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
    RequestPartMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
    AbstractMessageConverterMethodProcessor (org.springframework.web.servlet.mvc.method.annotation)
        RequestResponseBodyMethodProcessor (org.springframework.web.servlet.mvc.method.annotation)
        HttpEntityMethodProcessor (org.springframework.web.servlet.mvc.method.annotation)
AbstractWebArgumentResolverAdapter (org.springframework.web.method.annotation)
    ServletWebArgumentResolverAdapter (org.springframework.web.servlet.mvc.method.annotation)
PageableArgumentResolver (org.springframework.data.web)
    PageableHandlerMethodArgumentResolver (org.springframework.data.web)
PagedResourcesAssemblerArgumentResolver (org.springframework.data.web)
UriComponentsBuilderMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
HandlerMethodArgumentResolverComposite (org.springframework.web.method.support)
ServletRequestMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
RedirectAttributesMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
MatrixVariableMapMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
QuerydslPredicateArgumentResolver (org.springframework.data.web.querydsl)



RequestParamMapMethodArgumentResolver rp ear



ModelAndViewContainer


函数调用栈
org.springframework.web.method.support.InvocableHandlerMethod#invokeForRequest()

这个函数很重要
