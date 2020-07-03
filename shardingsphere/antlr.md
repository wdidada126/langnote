# antlr

[antlr](https://www.antlr.org/)

[开源语法分析器--ANTLR](https://www.cnblogs.com/blfshiye/p/4359390.html)

词法分析是计算机科学中将字符序列转换为标记（token）序列的过程。从输入字符流中生成标记的过程叫作标记化（tokenization），在这个过程中，词法分析器还会对标记进行分类。

antlr可以对接多种语言
runtime






#### antlr的概述


antlr是一个包含了`词法分析`,`语法分析`两大模块的工具，并且提供了大量主流语言的现成的语法描述`grammar`文件

使用antlr你可以将某种语言的代码文件，以纯文本字符串的方式输入，被antlr整理分析成一个语法树，一个可以清晰地从树状结构里，看到代码真正的逻辑的结构化数据。

通俗易懂的说，antlr的作用就是将计算机不明白，无法读取，无法执行的字符串代码，一个字一个字`读`，一行一行的`分析`，最后把`字符串`读明白了，分析明白了，转化成了计算机程序能`弄懂`(也就是能遍历，能执行，能运行的)的结构化数据`语法树`

听起来是不是很神秘？没错，这里面其实是编译原理里面的概念，我们所写的C++,OC,JAVA各种知名语言，我们其实写的都是一行一行字符串，这一行行的字符是怎么编译成可以运行的app的，这都是要经过这样的一个步骤，但这也只是编译原理中的一环，经过了`词法,语法解析`，后面还有很多重要的环节

- 有了`词法,语法解析`，我们甚至还可以独创我们自己的语言
- 有了`词法,语法解析`，再引入编译原理中的其他概念，我们甚至还可以自己写我们独创语言的编译器

看起来是不是很神秘很牛逼~我们今天深入讨论一下


#### antlr的基本使用


antlr包含以下几个部分

- antlr 主工程
- antlr 语法描述 grammer
- antlr 运行时 runtime



目标语言的语法描述grammer文件，在antlr官网可以下载,https://github.com/antlr/grammars-v4，从里面可以看到，我们可以找到几乎所有主流语言的语法描述，换句话说，如果我们要分析的语言有现成的grammar文件，那我们可以直接拿来输入给antlr就能搞起词法语法分析。

antlr主工程虽然是Java，但是antlr运行可以在Java，JavaScript，Python，C#等语言里，原因就是官网开放了这四种语言的antlr运行时，[www.antlr.org/download](http://www.antlr.org/download.html)。

举个通俗点的例子，如果我打算用JavaScript语言，用来分析Oc语法，那么

- 我需要先去官网下载`ObjectiveC.g4`grammer语法描述文件
- 我需要用antlr的Java主程序，输入OC的grammer，选择JavaScript语言输出，生成`ObjectiveCParser.js`这个用js代码写出来的，OC解析器
- 我需要开始搭建我的JS程序，将一整个antlr的JavaScript运行时都import进来，并且import进来刚刚生成的`ObjectiveCParser.js`，在JS代码里开始编写JSPatchConvertor的代码逻辑


antlr书籍

测试用例推荐熟悉的json sql

不要看cvs