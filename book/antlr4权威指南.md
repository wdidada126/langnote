# antlr4权威指南

参考文档
https://github.com/edidada/hand_in_hand_with_antlr

### 图形工具

TestRig这个java程序
-tokens 打印词法分析的程序

在线调试工具
http://lab.antlr.org/
如何调试多个.g .g4文件

antlrworks2 基于netbeans的ide
https://tunnelvisionlabs.com/downloads/antlr/2013-07-21-antlrworks-2.1.zip
https://github.com/antlr/antlrworks

https://blog.csdn.net/u014454538/article/details/86351781

vsc插件
vs插件

问题：
github上的lexiual.rule
parser.rule是干啥的？

-- skip？


https://book.douban.com/subject/27082372/       中文版
win 11电脑
ANTLR4权威指南.pdf

https://book.douban.com/subject/17912658/        英文版

Twitter搜索使用ANTLR进行语法分析，每天处理超过20亿次查询；Hadoop生态系统中的Hive、Pig、数据仓库和分析系统所使用的语言都用到了ANTLR；Lex Machina将ANTLR用于分析法律文本；Oracle公司在SQL开发者IDE和迁移工具中使用了ANTLR；NetBeans公司的IDE使用ANTLR来解析C++；Hibernate对象-关系映射框架（ORM）使用ANTLR来处理HQL语言。

antlr4 vs antlr3

antlr4 访问者模式 flex、bison需要在.i .y中嵌入c c++代码
antlr4不用

antlr4 java版本的lex和yacc

g4文件四大部分
ANTLR 的 `.g4` 文件主要用于定义语言的语法规则，它通常由四个主要部分组成：选项（options）、词法规则（lexer rules）、语法规则（parser rules） 和 代码块（code blocks）。下面详细介绍这四大部分：

### 1. 选项（Options）

选项部分用于配置 ANTLR 解析器和词法分析器的行为。这些选项可以影响诸如输出的语言类型、是否生成监听器或访问者等。

```antlr
grammar MyGrammar; // 定义语法名称

options {
    language = Java; // 输出的编程语言，默认为Java
    tokenVocab = MyLexer; // 如果将解析器和词法分析器分开定义，这里引用词法分析器的名字
}
```

常见的选项包括：
- `language`: 指定目标语言（如 Java, C#, Python3 等）。
- `tokenVocab`: 当你将词法分析器和解析器分离到不同的文件时使用，指定要使用的词法分析器的名字。
- `superClass`: 指定生成的解析器类继承自哪个基类。

### 2. 导入（Imports）

虽然这不是每个 `.g4` 文件都必须的部分，但有时候你需要从另一个语法文件中导入规则，这时就需要用到 `import` 关键字。

```antlr
import MyOtherGrammar; // 导入其他语法文件中的规则
```

### 3. 词法规则（Lexer Rules）

词法规则是用来定义如何将输入字符流分割成有意义的标记（tokens）。每个词法规则定义了一个特定类型的标记，并且以大写字母开头。

```antlr
ID  : [a-zA-Z]+ ;      // 匹配标识符
INT : [0-9]+ ;         // 匹配整数
WS  : [ \t\r\n]+ -> skip ; // 跳过空白字符
```

词法规则通常位于解析规则之前，并且是互斥的，即一旦匹配了某个规则，就不会再尝试匹配后续规则。

### 4. 语法规则（Parser Rules）

语法规则是用来定义如何根据标记构建抽象语法树（AST）。每个语法规则定义了一种合法的语言结构，并且以小写字母开头。

```antlr
prog:   stat+ ;

stat:   expr NEWLINE                # PrintExpr
    |   ID '=' expr NEWLINE         # Assign
    |   NEWLINE                     # BlankLine
    ;

expr:   expr ('*'|'/') expr         # MulDiv
    |   expr ('+'|'-') expr         # AddSub
    |   INT                         # Int
    |   ID                          # Id
    |   '(' expr ')'                # Parens
    ;
```

在上面的例子中，`# LabelName` 是标签，它们决定了生成的具体上下文类名，从而可以在访问者或监听器中实现具体的处理逻辑。

### 5. 代码块（Code Blocks）

在 `.g4` 文件中，你还可以嵌入目标语言的代码块来执行一些操作，比如初始化变量、修改解析过程中的行为等。

#### 动作代码（Action Code）

动作代码可以直接插入到产生式中，在特定的解析阶段执行。

```antlr
expr:   expr '*' expr {System.out.println("multiply");}  // Java code block
    |   ...
    ;
```

#### 初始化代码（Init Code）

你也可以在文件顶部添加初始化代码，这些代码会在生成的解析器类中作为成员变量或方法存在。

```antlr
@members {
    int count = 0;
}
```

### 总结

一个典型的 `.g4` 文件可能包含以下四大部分：
1. 选项（Options）：配置解析器和词法分析器的行为。
2. 导入（Imports）：可选，用于导入其他语法文件中的规则。
3. 词法规则（Lexer Rules）：定义如何将输入字符流分割成标记。
4. 语法规则（Parser Rules）：定义如何根据标记构建抽象语法树。
5. 代码块（Code Blocks）：可选，用于嵌入目标语言的代码，执行特定的操作或逻辑。

请注意，尽管“导入”不是每个 `.g4` 文件必需的部分，但在需要复用规则或模块化设计时非常有用。希望这个解释能帮助你更好地理解 `.g4` 文件的结构！如果有任何进一步的问题，请随时提问。
antlr3的
http://blog.chinaunix.net/uid-20606073-id-1916338.html

ANTLR 4进阶
https://www.liangshuang.name/2017/08/20/antlr/

https://blog.csdn.net/yangguosb/article/details/86007195

四类

一个文件
有四个部分

ANTLR是一款强大的语法分析器生成工具，可用于读取、处理、执行和翻译结构化的文本或二进制文件。它被广泛应用于学术领域和工业生产实践，是众多语言、工具和框架的基石。Twitter搜索使用ANTLR进行语法分析，每天处理超过20亿次查询；Hadoop生态系统中的Hive、Pig、数据仓库和分析系统所使用的语言都用到了ANTLR；Lex Machina将ANTLR用于分析法律文本；Oracle公司在SQL开发者IDE和迁移工具中使用了ANTLR；NetBeans公司的IDE使用ANTLR来解析C++；Hibernate对象-关系映射框架（ORM）使用ANTLR来处理HQL语言。


.g4规范？

:开始 ;结尾

BNF范式（巴科斯范式）

BNF范式是一种用递归的思想来表述计算机语言符号集的定义规范法则：::=表示定义；“  ”双引号里的内容表示字符；<>尖括号里的内容表示必选内容；| 竖线两边的是可选内容，相当于or；示例定义java中的switch语句：
<switch statement> ::= switch ( <expression> ) <switch block><switch block> ::= { <switch block statement groups><switch labels> }<switch block statement groups> ::= <switch block statement group> | <switch block statement groups> <switch block statement group><switch block statement group> ::= <switch labels><block statements><switch labels> ::= <switch label> | <switch labels> <switch label><switch label> ::= case <constant expression> :<……> | default :< ……>
现在在网络上大多数能搜出来的都是extended BNF ，允许使用循环，但正真的BNF只需要递归就够了。

这个是java的BNF定义
http://cs.au.dk/~amoeller/RegAut/JavaBNF.html

“巴克斯-诺尔形式”（BNF）是一种简单而强大的元语言。它是一种上下文无关的语法，根据终端字符（源文本的内容）和非终端元素（源语言的语法）定义语法规则。BNF支持替代定义和递归。

是的，BNF（巴科斯-诺尔范式）是CFG（上下文无关文法）的一种表示方法。它主要用于描述编程语言的语法规则，具有递归性质，可以精确地描述语言的语法结构。CFG则是一种形式化的方法，用于描述语言的语法规则，但不涉及语言的语义。

BNF起源于20世纪50年代，由美国计算机科学家巴科斯和诺尔共同提出。BNF具有特定的形式，如“symbol ::= expression”，其中symbol是非终结符，expression是一个包含symbol的表达式，可以由“|”连接。只有在BNF的右边出现的symbol是终结符。BNF在编程语言设计、数据交换格式和文本处理等领域具有广泛的应用。

ANTLR4 的 .g4 文件使用的语法并不是严格的 BNF（巴科斯-诺尔范式），而是更接近于 EBNF（扩展巴科斯-诺尔范式）。EBNF 是 BNF 的一个扩展，它提供了更多的元语法构造，使得描述语法时更为简洁和灵活。
在 ANTLR4 的 .g4 文件中，你可以使用各种 EBNF 特性，比如：
* 表示前面的元素可以出现零次或多次。
+ 表示前面的元素必须至少出现一次。
? 表示前面的元素是可选的，可以出现零次或一次。
() 用于分组元素。
| 表示选择，即可以匹配其中任意一个元素。
=> 用于语义谓词。
以及其他一些 ANTLR 特有的构造和语法。
这些特性使得 .g4 文件能够更简洁地描述复杂的语法结构，同时也为 ANTLR 工具链提供了更多的灵活性来生成高效的解析器。

虽然 ANTLR4 的 .g4 文件不是严格的 BNF，但它们确实基于相同的元语法思想，即使用递归规则来描述语言的语法结构。因此，如果你熟悉 BNF，那么理解 ANTLR4 的 .g4 文件应该不会太困难。不过，由于 EBNF 提供了更多的特性和灵活性，所以在实际使用中可能会遇到一些 BNF 中没有的概念和构造。


.g4格式的文件

无论是用antr自带的工具antlrworks2还是idea的插件 .g4 -->> *.java

解析json

编程语言实现模式.pdf

Terence Parr是美国旧金山大学的计算机教授、研究生导师，他一直致力于从事ANTLR项目（antlr.org）和模板引擎（stringtemplate.org）的设计和开发工作。Terence曾担任IBM、洛克希德马丁、NeXT、雷诺汽车等公司的技术顾问，另著有《ANTLR权威指南》。

stringtemplate
What is StringTemplate?
StringTemplate is a java template engine (with ports for C#, Objective-C, JavaScript, Scala) for generating source code, web pages, emails, or any other formatted text output. StringTemplate is particularly good at code generators, multiple site skins, and internationalization / localization.

https://github.com/antlr/stringtemplate4
https://www.stringtemplate.org/

ANTLR4与StringTemplate4之间的关系主要体现在它们可以协同工作以生成目标代码或其他文本输出。ANTLR4是一个解析器生成器，用于读取、处理、执行或翻译结构化文本或二进制文件。它根据输入的语法规则生成词法分析器和语法分析器，用于解析符合这些规则的文本。
而StringTemplate4是一个轻量级的模板引擎，主要用于生成各种文本输出，如代码、配置文件、HTML页面等。它使用模板文件和数据填充来生成最终的文本输出，并拥有灵活的模板语法，支持循环、条件语句等功能。
在ANTLR4项目中，开发者可以利用ANTLR4生成的解析器从输入文本中提取所需的数据，然后将这些数据传递给StringTemplate4。StringTemplate4使用这些数据填充预定义的模板，最终生成所需的输出，如Java代码。这种协同工作的方式使得ANTLR4和StringTemplate4能够高效地结合使用，实现文本生成和代码生成的任务。
综上所述，ANTLR4和StringTemplate4之间的关系是协同工作关系，它们可以结合在一起使用，利用ANTLR4的解析能力和StringTemplate4的模板生成能力，实现复杂文本和代码生成的需求。

Antlr如何解析json g4文件格式

json分为array object

json rfc

生成Java代码
PHP代码

yacc/flex

hplsql

https://github.com/apache/hive/tree/master/hplsql/src/main/antlr4/org/apache/hive/hplsql 

token  有.tokens文件

parser

org.antlr.v4.runtime.TokenStream

org.antlr.v4.runtime.ParserRuleContext 实际上是ast

第一部分　ANTLR和计算机语言简介
第1章 初识ANTLR
1.1 安装ANTLR
1.2 运行ANTLR并测试识别程序
第2章 纵观全局
2.1 从ANTLR元语言开始
2.2 实现一个语法分析器
2.3 你再也不能往核反应堆多加水了
2.4 使用语法分析树来构建语言类应用程序
2.5 语法分析树监听器和访问器
第3章 入门的ANTLR项目
3.1 ANTLR工具、运行库以及自动生成的代码
3.2 测试生成的语法分析器
3.3 将生成的语法分析器与Java程序集成
3.4 构建一个语言类应用程序
第4章 快速指南
4.1 匹配算术表达式的语言
4.2 利用访问器构建一个计算器
4.3 利用监听器构建一个翻译程序
4.4 定制语法分析过程
4.5 神奇的词法分析特性

### 第二部分　使用ANTLR语法开发语言类应用程序

#### Chap. 5 设计语法

运算符优先级

传统 无法指定

Bison  通过额外的标记

Antlr 通过优先选择靠前的备选分支

right recursive
右递归

计算机语言中的常见模式
使用Antlr编辑来表达这些模式

语法规则
词法符号

语法模式
词法结构

Antlr核心标记 

？

|



+ ​          + 一次或多次

RE里面或者 出现一次或多次

零次或多次

通配符

a-z

P.67
start/Test.java


```shell
D:\Java\jdk1.8.0_231\bin\java.exe "-javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\lib\idea_rt.jar=11179:C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\bin" -Dfile.encoding=UTF-8 -classpath D:\Java\jdk1.8.0_231\jre\lib\charsets.jar;D:\Java\jdk1.8.0_231\jre\lib\deploy.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\access-bridge-64.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\cldrdata.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\dnsns.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\jaccess.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\jfxrt.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\localedata.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\nashorn.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\sunec.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\sunjce_provider.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\sunmscapi.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\sunpkcs11.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\zipfs.jar;D:\Java\jdk1.8.0_231\jre\lib\javaws.jar;D:\Java\jdk1.8.0_231\jre\lib\jce.jar;D:\Java\jdk1.8.0_231\jre\lib\jfr.jar;D:\Java\jdk1.8.0_231\jre\lib\jfxswt.jar;D:\Java\jdk1.8.0_231\jre\lib\jsse.jar;D:\Java\jdk1.8.0_231\jre\lib\management-agent.jar;D:\Java\jdk1.8.0_231\jre\lib\plugin.jar;D:\Java\jdk1.8.0_231\jre\lib\resources.jar;D:\Java\jdk1.8.0_231\jre\lib\rt.jar;D:\git\github\testantlr\target\classes;D:\mavenrepository\201904\org\antlr\antlr4-runtime\4.7.2\antlr4-runtime-4.7.2.jar starter.Test
{1，{2，3}，4}
^D
line 1:1 token recognition error at: '，'
line 1:4 token recognition error at: '，'
line 1:5 extraneous input '3' expecting {',', '}'}
line 1:7 token recognition error at: '，'
line 1:8 extraneous input '4' expecting {',', '}'}
(init { (value (init { (value 2) 3 })) 4 })

Process finished with exit code 0


```

#### Chap. 6 第6章 探索真实的语法世界
csv
json
dot
cymbol
R


#### Chap. 7 第7章 将语法和程序的逻辑代码解耦
XXXVistor.java


#### Chap. 8 第8章 构建真实的语言类应用程序
生成xml


### 第三部分　高级特性
#### Chap. 9 第9章 错误报告与恢复

9.1 错误处理入门
9.2 修改和转发ANTLR的错误消息
9.3 自动错误恢复机制
9.4 勘误备选分支
9.5 修改ANTLR的错误处理策略
#### 第10章 属性和动作
10.1 使用带动作的语法编写一个计算器
10.2 访问词法符号和规则的属性
10.3 识别关键字不固定的语言
#### 第11章 使用语义判定修改语法分析过程
11.1 识别编程语言的多种方言
11.2 关闭词法符号
11.3 识别歧义性文本
#### 第12章 掌握词法分析的“黑魔法”
12.1 将词法符号送入不同通道
12.2 上下文相关的词法问题
12.3 字符流中的孤岛
12.4 对XML进行语法分析和词法分析
### 第四部分　ANTLR参考文档
#### 第13章 探究运行时API
13.1 包结构概览
13.2 识别器
13.3 输入字符流和词法符号流
13.4 词法符号和词法符号工厂
13.5 语法分析树
13.6 错误监听器和监听策略
13.7 提高语法分析器的速度
13.8 无缓冲的字符流和词法符号流
13.9 修改ANTLR的代码生成机制
#### 第14章 移除直接左递归
14.1 直接左递归备选分支模式
14.2 左递归规则转换
#### 第15章 语法参考
15.1 语法词汇表
15.2 语法结构
15.3 文法规则
15.4 动作和属性
15.5 词法规则
15.6 通配符与非贪婪子规则
15.7 语义判定
15.8 选项
15.9 ANTLR命令行参数
参考文献



Chap 15
antlr注释

关键词


避免使用if
避免使用特定语言中的关键字


词法分析 大写

语法分析 小写


