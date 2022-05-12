# BNF



https://www.zhihu.com/question/27051306/answer/579820547


BNF是John Backus 在20世纪90年代提出的用以简洁描述一种编程语言的语言。
基本结构为：<non-terminal> ::= <replacement>non-terminal意为非终止符，就是说我们还没有定义完的东西，还可以继续由右边的replacement，也就是代替物来进一步解释、定义。举个例子：在中文语法里，一个句子一般由“主语”、“谓语”和“宾语”组成，主语可以是名词或者代词，谓语一般是动词，宾语可以使形容词，名词或者代词。那么“主语”、“谓语”和“宾语”就是非终止符，因为还可以继续由“名词”、“代词”、“动词”、“形容词”等替代。例1. <句子> ::= <主语><谓语><宾语>例2. <主语> ::= <名词>|<代词>例3. <谓语>::=<动词>例4. <宾语>::=<形容词>|<名词>|<代词>例5. <代词>::=<我>例6. <动词>::=<吃>例7. <动词>::=<喜欢>例8. <名词>::=<车>例9. <名词>::=<肉>如上，在::=左边的就是non-terminal非终止符，右边的就是replacement，可以是一系列的非终止符，如例1中的replacement便是后面例234左边的非终止符，也可以是终止符，如例56789的右边，找不到别的符号来进一步代替。因此，终止符永远不会出现在左边。一旦我们看到了终止符，这个描述过程就结束了。

https://www.zhihu.com/question/27051306/answer/35904732



BNF是描述编程语言的文法。自然语言存在不同程度的二义性。这种模糊、不确定的方式无法精确定义一门程序设计语言。必须设计一种准确无误地描述程序设计语言的语法结构，这种严谨、简洁、易读的形式规则描述的语言结构模型称为文法。最著名的文法描述形式是由Backus定义Algol60语言时提出的Backus-Naur范式（Backus-Naur Form, BNF）及其扩展形式EBNF。BNF能以一种简洁、灵活的方式描述语言的语法。具体内容可参考针对编译原理的书。



java bnf



http://bnf-for-java.sourceforge.net/



The "Backus-Naur Form" (**[BNF](http://bnf-for-java.sourceforge.net/AboutBNF/AboutBNF.html)**) is a simple yet powerful meta-language. It is a *context-free* grammar that defines syntax rules in terms of terminal characters (the content of the source text) and non-terminal elements (the syntax of the source language). BNF supports alternative definitions and recursion.

**[Extended BNF](http://bnf-for-java.sourceforge.net/AboutBNF/AboutExtendedBNF.html)** conforms to the International Standard [ISO-14977](http://www.iso.org/iso/en/CatalogueDetailPage.CatalogueDetail?CSNUMBER=26153&ICS1=35&ICS2=60&ICS3=). The improved language is expressive and easy to use.

**[BNF for Java](http://bnf-for-java.sourceforge.net/)** implements Extended BNF as a working compiler and parser, providing command-line tools, as well as the complete Java API. BNF for Java implements context, and allows you to add your own powerful *extensions*, such as custom code generation, or database lookup during parsing.

The **[BNF for Java Project](http://sourceforge.net/projects/bnf-for-java/)**, hosted on [SourceForge](http://sourceforge.net/), is an open-source, community-based team project. The goal is to deliver this useful technology to the world's community of programmers.



左递归”（left-recursion



　　**解释：LL(1)的意思是，第一个L,指的是从左往右处理输入，第二个L,指的是它为输入生成一个最左推导**。**1指的是向前展望1个符号**。



https://www.cnblogs.com/icmzn/p/5979008.html



recursion 递归 英语