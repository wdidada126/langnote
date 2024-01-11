# curl log

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
