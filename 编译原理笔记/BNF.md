# BNF

上下文无关语法（Context-Free Grammar, CFG）是描述语言结构的一种形式化表示方法，而BNF是CFG的一种常见表示方法之一。除了BNF之外，还有其他几种表示CFG的标准和变种，包括：
1. 扩展巴克斯-诺尔范式（Extended Backus-Naur Form, EBNF）：EBNF是BNF的扩展形式，引入了一些额外的语法元素和操作符，使得语法规则的表达更加方便和灵活。EBNF的一个常见扩展是使用方括号 `[]` 表示可选项，使用大括号 `{}` 表示重复项，以及使用圆括号 `()` 用于分组。
2. 巴克斯-诺尔范式扩展（Augmented Backus-Naur Form, ABNF）：ABNF是一种用于描述网络协议语法的扩展形式，基于BNF。它引入了额外的元素和语法规则，以满足网络协议的特定需求。ABNF在描述规则时允许使用ASCII字符和范围，以及其他一些特定的操作符和扩展。
3. 巴克斯-诺尔范式形式化语法（Backus-Naur Form Formally Specified, BNF-FS）：BNF-FS是一种形式化描述语言的CFG表示方法。它在BNF的基础上增加了一些标记和操作符，以支持更精确的语义规范和形式化验证。
4. 巴克斯-诺尔范式扩展形式化语法（Backus-Naur Form Extension for Formal Syntax, ISO/IEC 14977）：这是国际标准ISO/IEC 14977定义的一种扩展形式的BNF，用于形式化语法的描述。它支持更丰富的语法元素和操作符，包括可选项、重复项、分组和引用等。
这些形式化语法表示方法在不同的领域和应用中有各自的用途和特点。选择适合特定需求和上下文的表示方法可以更清晰地描述语法规则，并支持进一步的语法分析和解析工作。


EBNF还支持空序列，表示没有符号的序列。

很抱歉，我无法直接提供ISO/IEC 14977:1996(E)文档的网址。ISO/IEC 14977:1996(E)是关于信息技术语法元语言——扩展的BNF（EBNF）的国际标准。为了获取该标准的文档，您通常需要访问国际标准化组织（ISO）或国际电工委员会（IEC）的官方网站，或者通过他们指定的国家标准化机构进行购买或下载。
您可以通过以下步骤尝试找到该标准的文档：

访问ISO或IEC的官方网站，并使用网站的搜索功能来查找ISO/IEC 14977:1996(E)标准。
如果您所在的国家有参与ISO或IEC的国家标准化机构，您也可以访问该机构的网站，他们可能提供该标准的购买或下载服务。
您还可以尝试在专业的标准文献数据库或图书馆中搜索该标准，这些资源可能提供该标准的全文或摘要。
请注意，获取国际标准文档可能需要付费，并且需要遵守相关的版权和使用规定。确保您有权访问和使用该文档，并遵守相关的法律法规。
https://www.iso.org/obp/ui/en/#iso:std:iso-iec:14977:ed-1:v1:en


https://www.zhihu.com/question/27051306/answer/579820547


BNF是John Backus 在20世纪90年代提出的用以简洁描述一种编程语言的语言。
基本结构为：<non-terminal> ::= <replacement>non-terminal意为非终止符，就是说我们还没有定义完的东西，还可以继续由右边的replacement，也就是代替物来进一步解释、定义。举个例子：在中文语法里，一个句子一般由“主语”、“谓语”和“宾语”组成，主语可以是名词或者代词，谓语一般是动词，宾语可以使形容词，名词或者代词。那么“主语”、“谓语”和“宾语”就是非终止符，因为还可以继续由“名词”、“代词”、“动词”、“形容词”等替代。例1. <句子> ::= <主语><谓语><宾语>例2. <主语> ::= <名词>|<代词>例3. <谓语>::=<动词>例4. <宾语>::=<形容词>|<名词>|<代词>例5. <代词>::=<我>例6. <动词>::=<吃>例7. <动词>::=<喜欢>例8. <名词>::=<车>例9. <名词>::=<肉>如上，在::=左边的就是non-terminal非终止符，右边的就是replacement，可以是一系列的非终止符，如例1中的replacement便是后面例234左边的非终止符，也可以是终止符，如例56789的右边，找不到别的符号来进一步代替。因此，终止符永远不会出现在左边。一旦我们看到了终止符，这个描述过程就结束了。

https://www.zhihu.com/question/27051306/answer/35904732



BNF是描述编程语言的文法。自然语言存在不同程度的二义性。这种模糊、不确定的方式无法精确定义一门程序设计语言。必须设计一种准确无误地描述程序设计语言的语法结构，这种严谨、简洁、易读的形式规则描述的语言结构模型称为文法。最著名的文法描述形式是由Backus定义Algol60语言时提出的Backus-Naur范式（Backus-Naur Form, BNF）及其扩展形式EBNF。BNF能以一种简洁、灵活的方式描述语言的语法。具体内容可参考针对编译原理的书。



java bnf



http://bnf-for-java.sourceforge.net/



The "Backus-Naur Form" ([BNF](http://bnf-for-java.sourceforge.net/AboutBNF/AboutBNF.html)) is a simple yet powerful meta-language. It is a *context-free* grammar that defines syntax rules in terms of terminal characters (the content of the source text) and non-terminal elements (the syntax of the source language). BNF supports alternative definitions and recursion.

[Extended BNF](http://bnf-for-java.sourceforge.net/AboutBNF/AboutExtendedBNF.html) conforms to the International Standard [ISO-14977](http://www.iso.org/iso/en/CatalogueDetailPage.CatalogueDetail?CSNUMBER=26153&ICS1=35&ICS2=60&ICS3=). The improved language is expressive and easy to use.

[BNF for Java](http://bnf-for-java.sourceforge.net/) implements Extended BNF as a working compiler and parser, providing command-line tools, as well as the complete Java API. BNF for Java implements context, and allows you to add your own powerful *extensions*, such as custom code generation, or database lookup during parsing.

The [BNF for Java Project](http://sourceforge.net/projects/bnf-for-java/), hosted on [SourceForge](http://sourceforge.net/), is an open-source, community-based team project. The goal is to deliver this useful technology to the world's community of programmers.



左递归”（left-recursion



　　解释：LL(1)的意思是，第一个L,指的是从左往右处理输入，第二个L,指的是它为输入生成一个最左推导。1指的是向前展望1个符号。



https://www.cnblogs.com/icmzn/p/5979008.html



recursion 递归 英语