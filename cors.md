# cors


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

