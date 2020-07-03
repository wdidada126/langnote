# grep



grep -H

grep命令执行后的结果 加上文件名：







```
1、或操作

awk '/123|abc/' filename   // awk 的实现方式
```



grep 查询多个关键字 关键字有顺序关系



grep 同时满足多个关键字和满足任意关键字 grep 同时满足多个关键字和满足任意关键字 ① grep -E "word1|word2|word3"   file.txt 满足任意条件（word1、word2和word3之一）将匹配。 ② grep word1 file.txt | grep word2 |grep word3 必须同时满足三个条件（word1、word2和word3）才匹配。











grep在匹配行之前显示文件名
-H 显示匹配的文件名
-n 显示匹配的行号

https://cloud.tencent.com/developer/ask/28017

grep 一次检索多个文件

SYNOPSIS
       grep [OPTIONS] PATTERN [FILE...]
       grep [OPTIONS] [-e PATTERN | -f FILE] [FILE...]



grep 转义
`grep 'ssServiceImpl\]\[access\]PARAMETER' micro-service-auth.log -c`

[grep -A N 显示后几页](https://blog.csdn.net/guizishou00/article/details/64121792)

grep -A 4 wikipedia 密码文件.txt 

-A n 后n行，A记忆为(After)
-B n 前n行，B记忆为(Before)
-C n 前n行，后n行，C记忆为(Center)

简单翻译就是，-A -B -C 后面都跟阿拉伯数字，-A是显示匹配后和它后面的n行。-B是显示匹配行和它前面的n行。-C是匹配行和它前后各n行。总体来说，-C覆盖面最大。用它保险些。哈哈。这3个开关都是关于匹配行的上下文的（context）。
于是，就是搜索密码文件，找到匹配“wikipedia”字串的行，显示该行后后面紧跟的4行。

`grep pattern1 files | grep pattern2`

grep 'data.*token' /ext/myfiles  -nr -c

[linux 文本](https://linuxtools-rst.readthedocs.io/zh_CN/latest/base/03_text_processing.html#cut)

cut  公司生产不支持
cat
wc


`grep -10 ‘123’ test.log//打印匹配行的前后10行`

[grep查找路径下所有文件内容](https://blog.csdn.net/u013485792/article/details/52243479)

-r 递归查找子目录

grep -nr HELLO_HWC_CSND_BLOG* .

例子：

[root@localhost ~]# grep -nr baidu .
./file.txt:8:www.baidu.com
./file.txt:9:tieba.baidu.com
./file.txt:11:www.baidu.com/search/index



[用grep -c来统计匹配的行数](https://blog.csdn.net/xuejiayue1105/article/details/1483940)

[grep 匹配多少行](https://blog.csdn.net/huashao0602/article/details/78018743)

[more — 分页查看文件内容](https://blog.csdn.net/KingBoyWorld/article/details/78279284)

more [-dlfpcsu ] [-num ] [+/ pattern] [+ linenum] [file ... ] 


[cat、tail、head、grep、sed查看文件任意几行的数据](https://blog.csdn.net/ztf312/article/details/78850747)

[linux less命令简介](https://blog.csdn.net/caihaijiang/article/details/6113419)


```java

在 less 中导航命令类似于 vi，如下：
1 搜索
当使用命令 less file-name 打开一个文件后，可以使用下面的方式在文件中搜索。搜索时整个文本中匹配的部分会被高亮显示。
1) 向前搜索
/ ： 使用一个模式进行搜索，并定位到下一个匹配的文本
n ： 向前查找下一个匹配的文本
N ： 向后查找前一个匹配的文本


2) 向后搜索
? ： 使用模式进行搜索，并定位到前一个匹配的文本
n ： 向后查找下一个匹配的文本
N ： 向前查找前一个匹配的文本

2 全屏导航
ctrl + F ：向前移动一屏
ctrl + B ：向后移动一屏
ctrl + D ：向前移动半屏
ctrl + U ：向后移动半屏

3 单行导航
j ： 向下移动一行
k ： 向上移动一行

4 其它导航
G ： 移动到最后一行
g ： 移动到第一行
按空格：向下翻一页
b：向上翻一页
d：向下翻半页
u：向上翻半页
q / ZZ ： 退出 less 命令

5 编辑文件
v ： 进入编辑模式，使用配置的编辑器编辑当前文件

6 标记导航
当使用 less 查看大文件时，可以在任何一个位置作标记，可以通过命令导航到标有特定标记的文本位置。
ma ： 使用 a 标记文本的当前位置
'a ： 导航到标记 a 处

7 浏览多个文件
方式一，传递多个参数给 less，就能浏览多个文件。
less file1 file2


方式二，正在浏览一个文件时，使用 :e 打开另一个文件。
less file1
:e file2


当打开多个文件时，使用如下命令在多个文件之间切换
:n - 浏览下一个文件
:p - 浏览前一个文件


```


less搜索时，不能带有“[”???

‘[’不是转义字符








authcenter-medium-center.2019-09-30.0.log:0
authcenter-medium-center.2019-09-30.1.log:0
authcenter-medium-center.2019-09-30.2.log:0
authcenter-medium-center.2019-09-30.3.log:0


grep ' ExceptionHandler :' authcenter-medium-center.2019-09*log -c | awk -F ':' '{i+=$2} END {print i}'


