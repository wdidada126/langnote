# curl log

curl -x http://172.18.176.1:20800 https://www.google.com
curl -x http://172.18.176.1:20800 https://www.google.com

curl是支持这种Cookie机制的。当服务器在HTTP响应中返回`Set-Cookie`头时，curl可以处理并在后续请求中自动带上相应的Cookie，前提是Cookie没有过期。以下是curl处理Cookie的一些方式和相关参数：

### 自动处理Cookie
curl默认会根据服务器返回的`Set-Cookie`头来自动管理Cookie。它会在内存中维护一个Cookie列表，在后续对同一服务器的请求中自动带上未过期的Cookie。例如，当你使用curl发送一个请求，服务器返回包含`Set-Cookie`头的响应后，下次再向同一服务器发送请求时，curl会自动将之前收到的未过期Cookie添加到请求头中。

### 使用-c和-b参数
- -c参数：用于指定将服务器返回的Cookie保存到文件中。例如`curl -c cookies.txt https://example.com`，这会将服务器返回的Cookie保存到`cookies.txt`文件中。
- -b参数：用于指定在请求时从文件中读取Cookie并添加到请求头中。例如`curl -b cookies.txt https://example.com`，这会使curl从`cookies.txt`文件中读取Cookie，并在请求`https://example.com`时带上这些Cookie。你可以结合`-c`和`-b`参数，先使用`-c`保存Cookie，然后在后续请求中使用`-b`读取并发送Cookie。

### 其他相关参数
- --cookie-jar：与`-c`类似，用于指定保存Cookie的文件。例如`curl --cookie-jar cookies.jar https://example.com`。
- --cookie：可以直接在命令行中指定要发送的Cookie内容，而不是从文件中读取。例如`curl --cookie "name=value; another=value" https://example.com`。


curl-8.9.0_1-win64-mingw.zip

在 Ubuntu 22.04 上安装 curl 的头文件和库文件的步骤如下:
1. 更新系统软件包:
```
sudo apt-get update
```
2. 安装 curl 开发包:
```
sudo apt-get install libcurl4-openssl-dev -y
```
这个包包含了 curl 的头文件和库文件,您可以在开发过程中使用它们。
3. 确认安装成功:
您可以通过以下命令检查是否成功安装:
```
pkg-config --cflags --libs libcurl
```
如果输出了一些 include 和 lib 的路径,说明安装成功了。
现在您可以在您的代码中引用 curl 的头文件和链接 curl 的库文件了。比如在 C/C++ 代码中使用 `#include <curl/curl.h>` 来引用头文件。



```
curl -v --form user=user --form password=password http://localhost:8080/login
```

curl -o xxx.file o是小写
wget -O O是大写

[curl blog](http://www.ruanyifeng.com/blog/2019/09/curl-reference.html)

--output？？？

curl 文件传参

url encoded传参

```shell
-d ""
-d @filename
man curl
```

form-data传参
curl -X POST -F "file=@1.jpg;orient=UP" http://127.0.0.1/OCR/ocr/general
不是-d --data

curl post二进制数据
命令示例：
curl --data-binary @demo.dat http://localhost/demo.do

注：
--data-binary代表传送的是二进制数据；
@demo.dat代表当前传送的二进制文件路径，即当前目录下的demo.dat文件；
http://localhost/demo.do代表服务器接口地址；


http://www.ruanyifeng.com/blog/2019/09/curl-reference.html

```shell
curl -I http://ocr.edidada.cn/v1/ocr/predictions/contracts
curl -I http://ocr-contractRecognition.XX.cn/v1/ocr/predictions/contracts

HTTP/1.1 302 Moved Temporarily
Server: nginx
Date: Wed, 03 Apr 2019 00:33:04 GMT
Content-Type: text/html
Content-Length: 154
Connection: keep-alive
Location: https://ocr-contractrecognition.XXX.cn/v1/ocr/predictions/contracts

curl -l http://ocr.edidada.cn/v1/ocr/predictions/contracts
curl -l http://ocr-contractRecognition.XXX.cn/v1/ocr/predictions/contracts

<html>
<head><title>302 Found</title></head>
<body bgcolor="white">
<center><h1>302 Found</h1></center>
<hr><center>nginx</center>
</body>
</html>

```

```shell
curl argument list too long
```



curl

http method默认是POST

-X POST



post默认是form-data



curl -F file=@yingyezzhizhao_demo.jpg http://172.17.165.243:8232/ocr/businessLicense



https://stackoverflow.com/questions/19116016/what-is-the-right-way-to-post-multipart-form-data-using-curl



https://stackoverflow.com/questions/54090784/curl-argument-list-too-long



[curl add argument](https://stackoverflow.com/questions/19116016/what-is-the-right-way-to-post-multipart-form-data-using-curl)

## source code源代码

https://github.com/curl/curl

autoconf is already the newest version (2.69-11.1).
automake is already the newest version (1:1.16.1-4ubuntu6).
libtool is already the newest version (2.4.6-14).
m4 is already the newest version (1.4.18-4).


## 编译
https://everything.curl.dev/build/cmake

git clone https://github.com/curl/curl.git
cd curl
git checkout curl-8_5_0
autoreconf -fi
chmod +x configure
./configure --with-openssl
make
sudo make install

## doc manul
man curl
https://everything.curl.dev/project
