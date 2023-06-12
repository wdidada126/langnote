# cas client

sso

CAS protocol

https://apereo.github.io/cas/6.5.x/protocol/CAS-Protocol.html

注意这个网页上流程图

shiro cas

https://github.com/bujiio/buji-pac4j

Apereo CAS Server
CAS Protocol 3.0 Specification.


URI	Description
/login	credential requestor / acceptor
/logout	destroy CAS session (logout)
/validate	service ticket validation
/serviceValidate	service ticket validation [CAS 2.0]
/proxyValidate	service/proxy ticket validation [CAS 2.0]
/proxy	proxy ticket service [CAS 2.0]
/p3/serviceValidate	service ticket validation [CAS 3.0]
/p3/proxyValidate	service/proxy ticket validation [CAS 3.0]


Apereo CAS（Central Authentication Service）是一个开源的单点登录（SSO）服务器，它提供了安全的身份验证和授权解决方案。Apereo CAS旨在简化和统一应用程序的身份验证流程，并支持多个应用程序之间的单点登录。

Apereo CAS具有以下主要功能：

1. 单点登录（SSO）：用户只需登录一次，即可访问多个应用程序而无需重复认证。
2. 身份验证和授权：Apereo CAS提供了一套灵活的身份验证和授权机制，可根据需求进行配置和扩展。
3. 客户端支持：Apereo CAS支持各种客户端应用程序，包括Java、.NET、PHP等，并提供相应的客户端库和API。
4. 多因素认证：Apereo CAS支持多种身份验证方式，包括用户名/密码、双因素认证（例如短信验证码、指纹等）等。
5. 安全性：Apereo CAS提供了一系列安全性功能，包括加密通信、防止重放攻击、会话管理等。
6. 扩展性：Apereo CAS可根据需要进行定制和扩展，支持插件和扩展点。

您提到的"apereo cas server"是指Apereo CAS服务器，它是一个完整的身份验证和授权解决方案，可用于构建安全的单点登录系统。您可以在Apereo CAS的官方网站（https://www.apereo.org/projects/cas）上找到更多关于该项目的信息，包括文档、示例和社区支持。


https://github.com/apereo/cas



Apereo CAS是一个非常受欢迎的开源单点登录（SSO）解决方案，但市场上也有其他竞品可以考虑。以下是一些与Apereo CAS竞争或提供类似功能的SSO解决方案：
1. Keycloak: Keycloak是一个开源的身份和访问管理解决方案，提供了单点登录、身份验证、授权、用户管理等功能。
2. Shibboleth: Shibboleth是一个基于SAML（Security Assertion Markup Language）协议的开源身份提供者，可用于实现跨组织的单点登录和身份验证。
3. Gluu: Gluu是一个基于OpenID Connect和OAuth 2.0的身份和访问管理平台，提供了单点登录、身份验证、授权等功能。
4. OneLogin: OneLogin是一个云身份和访问管理平台，提供了企业级的单点登录、身份验证、授权等功能，支持多种身份提供者和标准。
这些竞品解决方案都提供了类似的功能，但具体选择取决于您的需求、技术栈和预算等因素。建议您根据具体情况进行比较和评估，选择最适合您的解决方案。


