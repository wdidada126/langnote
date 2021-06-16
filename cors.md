# cors

https://developer.mozilla.org/zh-CN/docs/Web/HTTP/CORS
https://www.cnblogs.com/hustskyking/archive/2013/04/09/CDS_access_contorl_allow_origin.html

为了防止CSRF的攻击，我们建议修改浏览器在发送POST请求的时候加上一个Origin字段，这个Origin字段主要是用来标识出最初请求是从哪里发起的。如果浏览器不能确定源在哪里，那么在发送的请求里面Origin字段的值就为空。

隐私方面：这种Origin字段的方式比Referer更人性化，因为它尊重了用户的隐私。

1、Origin字段里只包含是谁发起的请求，并没有其他信息 (通常情况下是方案，主机和活动文档URL的端口)。跟Referer不一样的是，Origin字段并没有包含涉及到用户隐私的URL路径和请求内容，这个尤其重要。
2、Origin字段只存在于POST请求，而Referer则存在于所有类型的请求。
随便点击一个超链接（比如从搜索列表里或者企业intranet），并不会发送Origin字段，这样可以防止敏感信息的以外泄露。
在应对隐私问题方面，Origin字段的方法可能更能迎合用户的口味。
服务端要做的：用Origin字段的方法来防御CSRF攻击的时候，网站需要做到以下几点：
1、在所有能改变状态的请求里，包括登陆请求，都必须使用POST方法。对于一些特定的能改变状态的GET请求必须要拒绝，这是为了对抗上文中提到过的论坛张贴的那种危害类型。
2、对于那些有Origin字段但是值并不是我们希望的（包括值为空）请求，服务器要一律拒绝。比如，服务器可以拒绝一切Origin字段为外站的请求。
安全性分析：虽然Origin字段的设计非常简单，但是用它来防御CSRF攻击可以起到很好的作用。
1、去掉Origin字段。由于支持这种方法的浏览器在每次POST请求的时候都会带上源header，那么网站就可以通过查看是否存在这种Origin字段来确定请求是否是由支持这种方法的浏览器发起的。这种设计能有效防止攻击者将一个支持这种方法的浏览器改变成不支持这种方法的浏览器，因为即使你改变浏览器去掉了Origin字段，Origin字段还是存在，只不过值变为空了。这跟Referer很不一样，因为Referer 只要是在请求里去掉了，那服务器就探测不到了。
2、DNS重新绑定。在现有的浏览器里面，对于同站的XMLHttpRequests，Origin字段可以被伪造。只依赖网络连接进行身份验证的网站应当使用在第2章里提到的DNS重新绑定的方法，比如验证header里的Host字段。在使用Origin字段来防御CSRF攻击的时候，也需要用到DNS重新绑定的方法，他们是相辅相成的。当然对于在第四章里提到的CSRF防御方法，也需要用到DNS重新绑定的方法。
3、插件。如果网站根据crossdomain.xml准备接受一个跨站HTTP请求的时候，攻击者可以在请求里用Flash Player来设置Origin字段。在处理跨站请求的时候，token验证的方法处理的不好，因为token会暴露。为了应对这些攻击，网站不应当接受不可信来源的跨站请求。
4、应用。Origin字段跟以下四个用来确定请求来源的建议非常类似。Origin字段以下四个建议的基础上统一并改进了，目前已经有几个组织采用了Origin字段的方法建议。
? Cross-Site XMLHttp Request。Cross-Site XMLHttp Request的方法规定了一个Access-Control-Origin 字段，用来确定请求来源。这个字段存在于所有的HTTP方法，但是它只在XMLHttpRequests请求的时候才会带上。我们对Origin字段的设想就是来源于这个建议，而且Cross-Site XMLHttp Request工作组已经接受我们的建议愿意将字段统一命名为Origin。
?XDomainRequest。在Internet Explorer 8 Beta 1里有XDomainRequest的API，它在发送HTTP请求的时候将Referer里的路径和请求内容删掉了。被缩减后的Referer字段可以标识请求的来源。我们的实验结果表明这种删减的Referer字段经常会被拒绝，而我们的Origin字段却不会。微软已经发表声明将会采用我们的建议将XDomainRequest里的删减Referer更改为Origin字段。
? JSONRequest。在JSONRequest这种设计里，包含有一个Domain字段用来标识发起请求的主机名。相比之下，我们的Origin字段方法不仅包含有主机，还包含请求的方案和端口。JSONRequest规范的设计者已经接受我们的建议愿意将Domain字段更改为Origin字段，以用来防止网络攻击。
? Cross-Document Messaging。在HTML5规范里提出了一个建议，就是建立一个新的浏览器API，用来验证客户端在HTML文件之间链接。这种设计里面包含一个不能被覆盖的origin属性，如果不是在客户端的话，在服务端验证这种origin属性的过程与我们验证origin字段的过程其实是一样的。
具体实施：我们在服务器和浏览器端都实现了利用origin字段的方法来防止CSRF攻击。在浏览器端我们的实现origin字段方式是，在WebKit添加一个8行代码的补丁，Safari里有我们的开源组件，Firefox里有一个466行代码的插件。在服务器端我们实现origin字段的方式是，在ModSecurity应用防火墙里我们只用3行代码，在Apache里添加一个应用防火墙语言（见图4）。这些规则在POST请求里能验证Host字段和具有合法值的origin字段。在实现这些规则来防御CSRF攻击的时候，网站并不需要做出什么改变，而且这些规则还能确保GET请求没有任何攻击性(前提是浏览器端已经实现了origin字段方法)。


CORS概念 跨域 同源
CQRS 不同

Http跨域
https://blog.csdn.net/tripleDemo/article/details/105502879

Cqrs
https://blog.csdn.net/hailongcsdn/article/details/107977657


CORS是一个W3C标准，全称是"跨域资源共享"（Cross-origin resource sharing）


什么是跨域
跨域是浏览器的一个特性，就是浏览器从一个“域”向另一个“域”的服务器发出请求，来访问另一个“域”上的资源。但是，由于请求的文件可能会存在恶意攻击，浏览器并不允许直接访问另一个“域”上的资源，只能访问同一个“域”上的资源，这个就是“同源策略”。而所谓的“同源”，指的是“协议、域名、端口号”一致，比如：
https://domain-a.com可以访问https://domain-a.com/data.json的内容，但是不能访问：
http://domain-a.com/data.json（协议不同）https://domain-b.com/data.json（域名不同）https://domain-a.com:8082/data.json（端口号不同）


https://zhuanlan.zhihu.com/p/101037701


@CrossOrigin spring


http://www.ruanyifeng.com/blog/2016/04/cors.html

跨域名不行

Access to XMLHttpRequest at 'http://60.205.225.118:8080/curd/test/comment/2' from origin 'http://localhost:63343' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
VM19:1 Cross-Origin Read Blocking (CORB) blocked cross-origin response http://60.205.225.118:8080/curd/test/comment/2 with MIME type application/json. See https://www.chromestatus.com/feature/5629709824032768 for more details.
(anonymous) @ VM19:1
document.querySelector.onclick @ index.html?_ijt=5g36ilo5uvnhh4q7l0drfehvda:23


跨port也不行
Access to XMLHttpRequest at 'http://localhost:8080/testajax/TestInterface.do?test' from origin 'http://localhost:63343' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.

