# BNF



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