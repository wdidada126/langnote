# 第 11 章 SpringMVC

> `DispatcherServlet` 请求全流程：`HandlerMapping` → `HandlerAdapter` → `Handler`（`@Controller`）→ `ModelAndView` → `ViewResolver` → 视图渲染；`HandlerInterceptor`、`HandlerExceptionResolver`、`@RequestBody` 消息转换。本章是 Web 层核心。

## 一、核心精讲

### 11.1 🔧 请求九大组件与流程
- `doDispatch`：`getHandler`（`HandlerMapping`）→ `getHandlerAdapter` → 执行 `preHandle` → `handle`（调 Controller）→ `postHandle` → `processDispatchResult`（渲染/异常解析）→ `afterCompletion`（🔧 `DispatcherServlet` 初始化时用 `initStrategies` 加载九大组件，缺省策略在 `DispatcherServlet.properties`）。

### 11.2 注解驱动
- `@RequestMapping` 由 `RequestMappingHandlerMapping` 注册；`@ResponseBody` 由 `RequestResponseBodyMethodProcessor` + `HttpMessageConverter`（Jackson）序列化（🔧 参数解析/返回值处理都是 `HandlerMethodArgumentResolver`/`HandlerMethodReturnValueHandler` 责任链）。

### 11.3 异常处理
- `@ExceptionHandler`/`@ControllerAdvice` → `ExceptionHandlerExceptionResolver`（🔧 未处理异常交给 `HandlerExceptionResolver` 链或容器错误页）。

## 二、版本演进 / 论文 / 前沿

- 文献：Spring Reference（Web MVC）；Gamma et al. 前端控制器（Front Controller，POSA）；GoF 责任链/适配器（1994）。
- 工业界：Spring MVC；Spring WebFlux（响应式，见 `Java编程方法论_响应式Spring_Reactor3设计与实现.md`）；Spring Boot 3.2+ 支持**虚拟线程**处理请求。
- 开源 stars（2026-09）：spring-framework 61k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "Controller 就是全部" | 前后还有 Mapping/Adapter/Resolver 链 |
| 2 | "@ExceptionHandler 全局生效" | 需 @ControllerAdvice |
| 3 | "拦截器=过滤器" | 拦截器是 Spring 层，Filter 是 Servlet 层 |
