# volley

http请求抽象成任务，设计了一个队列，多线程通信

回调

volley设计的时候nio不流行


retrofit与picasso一样都是在okhttp基础之上做的封装，项目中可以直接用了。

volley是一个简单的异步http库，仅此而已。缺点是不支持同步，这点会限制开发模式；不能post大数据，所以不适合用来上传文件。android-async-http。与volley一样是异步网络库，但volley是封装的httpUrlConnection，它是封装的httpClient，而android平台不推荐用HttpClient了，所以这个库已经不适合android平台了。

java.net.HttpURLConnection




![HttpURLConnection](..\imgs\HttpURLConnection.png)