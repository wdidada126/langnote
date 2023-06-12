# 深入浅出Spring Security

https://book.douban.com/subject/35383505/


知乎电子书





## 第1章 Spring Security架构概览 1
1.1 Spring Security简介 1
1.2 Spring Security核心功能 2
1.2.1 认证 3
1.2.2 授权 3
1.2.3 其他 3
1.3 Spring Security整体架构 4
1.3.1 认证和授权 4
1.3.2 Web安全 6
1.3.3 登录数据保存 9
1.4 小结 9
## 第2章 Spring Security认证 10
2.1 Spring Security基本认证 10
2.1.1 快速入门 10
2.1.2 流程分析 11
2.1.3 原理分析 12
2.2 登录表单配置 19
2.2.1 快速入门 19
2.2.2 配置细节 23
2.3 登录用户数据获取 39
2.3.1 从SecurityContextHolder中获取 41
2.3.2 从当前请求对象中获取 59
2.4 用户定义 64
2.4.1 基于内存 64
2.4.2 基于JdbcUserDetailsManager 65
2.4.3 基于MyBatis 68
2.4.4 基于Spring Data JPA 74
2.5 小结 77

org.springframework.security.core.context.SecurityContextHolder


org.springframework.security.provisioning.JdbcUserDetailsManager


## 第3章 认证流程分析 78
3.1 登录流程分析 78
3.1.1 AuthenticationManager 78
3.1.2 AuthenticationProvider 79
3.1.3 ProviderManager 86
3.1.4 AbstractAuthenticationProcessingFilter 89
3.2 配置多个数据源 94
3.3 添加登录验证码 95
3.4 小结 99
## 第4章 过滤器链分析 100
4.1 初始化流程分析 100
4.1.1 ObjectPostProcessor 101
4.1.2 SecurityFilterChain 102
4.1.3 SecurityBuilder 103
4.1.4 FilterChainProxy 117
4.1.5 SecurityConfigurer 120
4.1.6 初始化流程分析 128
4.2 ObjectPostProcessor使用 136
4.3 多种用户定义方式 137
4.4 定义多个过滤器链 141
4.5 静态资源过滤 144
4.6 使用JSON格式登录 146
4.7 添加登录验证码 150
4.8 小结 152
## 第5章 密码加密 153
5.1 密码为什么要加密 153
5.2 密码加密方案进化史 154
5.3 PasswordEncoder详解 154
5.3.1 PasswordEncoder常见实现类 155
5.3.2 DelegatingPasswordEncoder 156
5.4 实战 159
5.5 加密方案自动升级 161
5.6 是谁的PasswordEncoder 166
5.7 小结 168
## 第6章 RememberMe 169
6.1 RememberMe简介 169
6.2 RememberMe基本用法 170
6.3 持久化令牌 172
6.4 二次校验 174
6.5 原理分析 176
6.6 小结 189
## 第7章 会话管理 190
7.1 会话简介 190
7.2 会话并发管理 191
7.2.1 实战 191
7.2.2 原理分析 194
7.3 会话固定攻击与防御 206
7.3.1 什么是会话固定攻击 206
7.3.2 会话固定攻击防御策略 207
7.4 Session共享 208
7.4.1 集群会话方案 208
7.4.2 实战 210
7.5 小结 212
## 第8章 HttpFirewall 213
8.1 HttpFirewall简介 213
8.2 HttpFirewall严格模式 215
8.2.1 rejectForbiddenHttpMethod 216
8.2.2 rejectedBlacklistedUrls 217
8.2.3 rejectedUntrustedHosts 218
8.2.4 isNormalized 219
8.2.5 containsOnlyPrintableAsciiCharacters 220
8.3 HttpFirewall普通模式 220
8.4 小结 221
## 第9章 漏洞保护 222
9.1 CSRF攻击与防御 222
9.1.1 CSRF简介 222
9.1.2 CSRF攻击演示 223
9.1.3 CSRF防御 224
9.1.4 源码分析 231
9.2 HTTP响应头处理 237
9.2.1 缓存控制 239
9.2.2 X-Content-Type-Options 240
9.2.3 Strict-Transport-Security 241
9.2.4 X-Frame-Options 244
9.2.5 X-XSS-Protection 245
9.2.6 Content-Security-Policy 246
9.2.7 Referrer-Policy 248
9.2.8 Feature-Policy 249
9.2.9 Clear-Site-Data 249
9.3 HTTP通信安全 250
9.3.1 使用HTTPS 250
9.3.2 代理服务器配置 253
9.4 小结 254
## 第10章 HTTP认证 255
10.1 HTTP Basic authentication 255
10.1.1 简介 255
10.1.2 具体用法 257
10.1.3 源码分析 257
10.2 HTTP Digest authentication 260
10.2.1 简介 260
10.2.2 具体用法 261
10.2.3 源码分析 263
10.3 小结 268
## 第11章 跨域问题 269
11.1 什么是CORS 269
11.2 Spring处理方案 270
11.2.1 @CrossOrigin 271
11.2.2 addCorsMappings 272
11.2.3 CorsFilter 273
11.3 Spring Security处理方案 274
11.3.1 特殊处理OPTIONS请求 275
11.3.2 继续使用CorsFilter 275
11.3.3 专业解决方案 276
11.4 小结 279
## 第12章 异常处理 280
12.1 Spring Security异常体系 280
12.2 ExceptionTranslationFilter原理分析 281
12.3 自定义异常配置 287
12.4 小结 290
## 第13章 权限管理 291
13.1 什么是权限管理 291
13.2 Spring Security权限管理策略 292
13.3 核心概念 292
13.3.1 角色与权限 292
13.3.2 角色继承 294
13.3.3 两种处理器 295
13.3.4 前置处理器 296
13.3.5 后置处理器 299
13.3.6 权限元数据 300
13.3.7 权限表达式 303
13.4 基于URL地址的权限管理 305
13.4.1 基本用法 306
13.4.2 角色继承 308
13.4.3 自定义表达式 309
13.4.4 原理剖析 310
13.4.5 动态管理权限规则 316
13.5 基于方法的权限管理 325
13.5.1 注解介绍 325
13.5.2 基本用法 326
13.5.3 原理剖析 331
13.6 小结 338
## 第14章 权限模型 339
14.1 常见的权限模型 339
14.2 ACL 340
14.2.1 ACL权限模型介绍 340
14.2.2 ACL核心概念介绍 341
14.2.3 ACL数据库分析 343
14.2.4 实战 345
14.3 RBAC 354
14.3.1 RBAC权限模型介绍 354
14.3.2 RBAC权限模型分类 355
14.3.3 RBAC小结 357
14.4 小结 357
## 第15章 OAuth2 358
15.1 OAuth2简介 358
15.2 OAuth2四种授权模式 359
15.2.1 授权码模式 360
15.2.2 简化模式 361
15.2.3 密码模式 363
15.2.4 客户端模式 363
15.3 Spring Security OAuth2 364
15.4 GitHub授权登录 365
15.4.1 准备工作 365
15.4.2 项目开发 367
15.4.3 测试 368
15.4.4 原理分析 369
15.4.5 自定义配置 375
15.5 授权服务器与资源服务器 379
15.5.1 项目规划 379
15.5.2 项目搭建 380
15.5.3 测试 391
15.5.4 原理分析 393
15.5.5 自定义请求 396
15.6 使用Redis 397
15.7 客户端信息存入数据库 399
15.8 使用JWT 401
15.8.1 JWT 401
15.8.2 JWT数据格式 402
15.8.3 OAuth2中使用JWT 403
15.9 小结 406
