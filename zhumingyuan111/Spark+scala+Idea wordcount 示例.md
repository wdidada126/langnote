---
title: Spark+scala+Idea wordcount 示例
date: 2017-06-20 22:23:12
tags: CSDN迁移
---
  上篇文章搭建了spark,并给出了java版本的WordCount示例，但是总感觉spark程序用scala语言编写才更好，因为scala语言会让spark程序很简洁，能在很大程度上提高开发效率，下面给出scala版本的WordCount.

 
### idea项目搭建

 首先用idea搭建一个maven工程。![这里写图片描述](https://img-blog.csdn.net/20170620220815672?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvemh1bWluZ3l1YW4xMTE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)   
 在main文件夹下创建scala文件夹，然后将scala文件夹设置成源码文件夹。 `右键工程名->open model setting ->Modules`    
 选中scala将其设置为Sources   
 此处若不进行设置，在运行程序的时候将找不到我们的主函数，因为idea并没有编译这个文件。   
 ![这里写图片描述](https://img-blog.csdn.net/20170620221227093?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvemh1bWluZ3l1YW4xMTE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

 
### maven文件

 
```
<dependencies>
        <!-- https://mvnrepository.com/artifact/org.scala-lang/scala-library -->
        <dependency>
            <groupId>org.scala-lang</groupId>
            <artifactId>scala-library</artifactId>
            <version>2.11.11</version>
        </dependency>
        <!-- https://mvnrepository.com/artifact/org.apache.spark/spark-core_2.11 -->
        <dependency>
            <groupId>org.apache.spark</groupId>
            <artifactId>spark-core_2.11</artifactId>
            <version>2.1.1</version>
        </dependency>
        <!-- https://mvnrepository.com/artifact/org.apache.spark/spark-mllib_2.11 -->
        <dependency>
            <groupId>org.apache.spark</groupId>
            <artifactId>spark-mllib_2.11</artifactId>
            <version>2.1.0</version>
        </dependency>
        <!-- https://mvnrepository.com/artifact/org.apache.spark/spark-sql_2.11 -->
        <dependency>
            <groupId>org.apache.spark</groupId>
            <artifactId>spark-sql_2.11</artifactId>
            <version>2.1.0</version>
        </dependency>
        <!-- https://mvnrepository.com/artifact/org.apache.spark/spark-hive_2.11 -->
        <dependency>
            <groupId>org.apache.spark</groupId>
            <artifactId>spark-hive_2.11</artifactId>
            <version>2.1.1</version>
        </dependency>
```
 
### scala代码：

 
```
import org.apache.spark.SparkConf
import org.apache.spark.SparkContext

object WordCount {
  def main(args: Array[String]) {

    val conf = new SparkConf()
    conf.setAppName("wordcount")
    //conf.setMaster("local")
    val sc = new SparkContext(conf)
    val line = sc.textFile("/usr/local/hadoop/input")
    line.flatMap(_.split(" ")).map((_, 1)).reduceByKey(_+_).saveAsTextFile("/usr/local/hadoop/output")
    sc.stop()
  }

}
```
 
### 运行代码

 在Edit Configurations设置为本地运行，VM options设置如下：

 
```
-Dspark.master=local
```
 然后直接运行main函数即可。在结果输出的路径可以查看到相关文件。

 
### 总结

 相比java代码，scala代码更是简洁，java30行的代码scala调用几个函数就完成了，由此可见scala在spark工程中的优势！

   
  