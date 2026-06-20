# freemaker

并用来输出文本(HTML网页、电子邮件、配置文件、源代码等) 

用freemaker模板引擎生成简单crud代码
https://zhuanlan.zhihu.com/p/365803535
https://github.com/JavaBest1/code-generator

.ftl文件

在FreeMarker中，模板文件也可以被视为一种源代码，因此在渲染模板时，FreeMarker会将模板文件转换成AST，然后根据AST和提供的数据生成最终的输出。这个过程类似于编译器将源代码转换成目标代码的过程，只是目标代码变成了文本输出。

FreeMarker AST可视化可以帮助开发人员更好地理解模板文件的抽象语法结构。以下是一些常用的FreeMarker AST可视化工具：

1. FreeMarker AST Viewer：这是一个在线工具，可以将FreeMarker模板文件转换成AST，并以可视化方式呈现。它还提供了一些调试工具，例如变量查看器和调试信息。
2. 没找到 IntelliJ IDEA插件：IntelliJ IDEA是一款流行的Java IDE，它提供了一个FreeMarker插件，可以将模板文件转换成AST，并在IDE中以可视化方式呈现。
3. VisualVM：这是一个Java性能分析工具，它可以分析Java应用程序的内存使用情况和线程活动。VisualVM还提供了一个FreeMarker插件，可以将模板文件转换成AST，并在VisualVM中以可视化方式呈现。
4. FreeMarker AST Parser：这是一个Java库，可以将FreeMarker模板文件转换成AST，并以程序化方式访问AST。它还提供了一些工具类，可以将AST转换成其他格式，例如JSON和XML。

这些工具可以帮助开发人员更好地理解FreeMarker模板文件的抽象语法结构，并在调试和优化模板文件时提供有用的信息。


https://freemarker-online.kenshoo.com/ast-viewer



public class Main {
    public static void main(String[] args) throws Exception {
        Configuration cfg = new Configuration(Configuration.VERSION_2_3_28);
        cfg.setClassForTemplateLoading(Main.class, "/");
        Template template = cfg.getTemplate("service.ftl");
        template.dump(new OutputStreamWriter(System.out));
    }
}
