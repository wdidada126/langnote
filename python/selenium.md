# selenium

[python 包之 selenium 自动化使用教程](https://xie.infoq.cn/article/b2c5d786fded71894e1f69ce8)

tbody selenium

https://blog.csdn.net/weixin_34378815/article/details/113494339

iframe



测试源码：
testselenium

thoughtworks公司

打开浏览器
输入
关闭弹窗
点击
右键


驱动 浏览器 os版本

Python 、Java C# Ruby JS

https://www.selenium.dev/zh-cn/

https://github.com/seleniumhq/selenium

https://www.selenium.dev/selenium/docs/api/py/index.html



`pip install selenium`

```shell
pip install selenium
Collecting selenium
  Using cached selenium-3.141.0-py2.py3-none-any.whl (904 kB)
Collecting urllib3
  Downloading urllib3-1.26.7-py2.py3-none-any.whl (138 kB)
     |████████████████████████████████| 138 kB 1.3 MB/s
Installing collected packages: urllib3, selenium
Successfully installed selenium-3.141.0 urllib3-1.26.7
```

[selenium驱动下载](https://blog.csdn.net/weixin_42170439/article/details/90611962)


iframe
iframeset

button
imput

div

hr
br

img

select

### python api
多个标签切换

     要定位页面中的单个元素方式：

find_element_by_id
find_element_by_name
find_element_by_xpath
find_element_by_link_text
find_element_by_partial_link_text
find_element_by_tag_name
find_element_by_class_name
find_element_by_css_selector
   要定位多个元素（这些方法将返回一个列表）：

find_elements_by_name
find_elements_by_xpath
find_elements_by_link_text
find_elements_by_partial_link_text
find_elements_by_tag_name
find_elements_by_class_name
find_elements_by_css_selector
   selenium对页面对象的定位器的方法：find_element和find_elements。（有上面两私有方法）。



chromedriver -h
Usage: chromedriver [OPTIONS]

Options
  --port=PORT                     port to listen on
  --adb-port=PORT                 adb server port
  --log-path=FILE                 write server log to file instead of stderr, increases log level to INFO
  --log-level=LEVEL               set log level: ALL, DEBUG, INFO, WARNING, SEVERE, OFF
  --verbose                       log verbosely (equivalent to --log-level=ALL)
  --silent                        log nothing (equivalent to --log-level=OFF)
  --append-log                    append log file instead of rewriting
  --replayable                    (experimental) log verbosely and don't truncate long strings so that the log can be replayed.
  --version                       print the version number and exit
  --url-base                      base URL path prefix for commands, e.g. wd/url
  --readable-timestamp            add readable timestamps to log
  --enable-chrome-logs            show logs from the browser (overrides other logging options)
  --allowed-ips=LIST              comma-separated allowlist of remote IP addresses which are allowed to connect to ChromeDriver
  --allowed-origins=LIST          comma-separated allowlist of request origins which are allowed to connect to ChromeDriver. Using `*` to allow an
y host origin is dangerous!


图片另存为
pip install pyautogui

https://gitee.com/edidada/mytestpro-master


- selenium2自动化测试指南
