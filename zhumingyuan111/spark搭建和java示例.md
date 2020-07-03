---
title: spark搭建和java示例
date: 2017-06-14 22:57:40
tags: CSDN迁移
---
  ### 1. scala 安装

 下载scala: [http://www.scala-lang.org/download/](http://www.scala-lang.org/download/)   
 最开始下载scala2.12,后来运行spark出现版本不一致的错误，后来安装了 scala-2.11.11 .tgz   
 解压

 
```
tar -zxvf scala-2.11.11.tgz -C /usr/local/
mv scala-2.11 scala
```
 配置scala环境变量

 
```
export SCALA_HOME=/usr/local/scala
export PATH=${SCALA_HOME}/bin:$PATH
```
 运行  `scala -version` 查看是否安装成功

 
### 安装spark

 我下载的版本是： `spark-2.1.0-bin-hadoop2.7.tgz` 

 
```
重命名 mv spark-2.1.0-bin spark
```
 spark 环境变量配置

 
```
export SPARK_HOME=/usr/local-extend/spark
export PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH
```
 测试spark是否安装成功

 
```
/usr/local-extend/spark/bin$ ./spark-shell
```
 出现下图则安装成功   
 ![这里写图片描述](https://img-blog.csdn.net/20170615084731745?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvemh1bWluZ3l1YW4xMTE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

 
### 修改spark配置

 在%SPARK_HOME%/conf下

 
```
cp spark-env.sh.template spark-env.sh
添加如下内容
export SPARK_DIST_CLASSPATH=$(/usr/local/hadoop/bin/hadoop classpath)
export JAVA_HOME=/usr/lib/jvm/jdk1.8.0_111
HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop

```
 
### 运行spark例子

 %SPARK_HOME%/bin下执行：

 
```
run-example SparkPi 2>&1 | grep "Pi is roughly"
```
 输出结果：   
 ![这里写图片描述](https://img-blog.csdn.net/20170615085843276?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvemh1bWluZ3l1YW4xMTE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)   
 以上spark基本完成安装，下面通过在idea上建立WordCount demo并运行，采用maven工程。

 
### 工程代码

 代码：

 
```
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.function.FlatMapFunction;
import org.apache.spark.api.java.function.Function2;
import org.apache.spark.api.java.function.PairFunction;
import scala.Tuple2;

import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.regex.Pattern;

/**
 * Created by hadoop on 17-6-11.
 */
public class WordCount {
    private static final Pattern SPACE = Pattern.compile(" ");

    public static void main(String[] args)throws Exception {
        SparkConf sparkConf = new SparkConf().setAppName("SparkWordCount");
        String srcPath = "/usr/tmp/input/";
        String desPath = "/usr/tmp/output/";
        if(args.length == 2) {
            srcPath = args[0];
            desPath = args[1];
        }
        JavaSparkContext jsc = new JavaSparkContext(sparkConf);
        JavaRDD<String> lines = jsc.textFile(srcPath, 1);

        System.out.println("file text split!");
        JavaRDD<String> words = lines.flatMap(new FlatMapFunction<String, String>() {
            @Override
            public Iterator<String> call(String s) throws Exception {
                return Arrays.asList(s.split(" ")).iterator();
            }
            /*@Override
            public Iterable<String> call(String s) throws Exception {
                return Arrays.asList(SPACE.split(" "));
            }*/
        });

        System.out.println("word map!");
        JavaPairRDD<String, Integer> ones = words.mapToPair(new PairFunction<String, String, Integer>() {
            @Override
            public Tuple2<String, Integer> call(String s) throws Exception {
                return new Tuple2<String, Integer>(s, 1);
            }
        });

        System.out.println("word reduce!");
        JavaPairRDD<String, Integer> counts = ones.reduceByKey(new Function2<Integer, Integer, Integer>() {
            @Override
            public Integer call(Integer i1, Integer i2) throws Exception {
                return i1 + i2;
            }
        });

        System.out.println("word count save!");
        counts.saveAsTextFile(desPath);
        jsc.stop();
    }
}
```
 maven 文件

 
```
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>SparkDemo</groupId>
    <artifactId>com.jd.demo.spark</artifactId>
    <version>1.0-SNAPSHOT</version>

    <dependencies>
        <dependency>
            <groupId>org.apache.spark</groupId>
            <artifactId>spark-core_2.11</artifactId>
            <version>2.1.1</version>
        </dependency>
    </dependencies>

</project>
```
 
### idea中运行spark程序

 在 edit Configuration中的VM option添加参数 -Dspark.master=local

 然后运行java程序即可。注意输入和输出路径为本地路径。   
 最后在本地的输出文件夹中出现part-0000和_SUCCESS文件。part_0000内容如下：   
 ![这里写图片描述](https://img-blog.csdn.net/20170615092341357?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvemh1bWluZ3l1YW4xMTE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

 
### 在本地运行上spark程序

 在idea Terminal下运行

 
```
/usr/local-extend/spark/bin/spark-submit --class "com.spark.demo.WordCount" --master local[4] target/com.jd.demo.spark-1.0-SNAPSHOT.jar
```
 注意此时使用hdfs输入和输出路径。如果运行成功同样会出现output文件夹，以及part_0000和_SUCCESS文件。

 
### 在YARN集群运行spark程序

 在idea Terminal下运行

 
```
/usr/local-extend/spark/bin/spark-submit --class "com.jd.spark.demo.WordCount" --master yarn --deploy-mode cluster  target/com.demo.spark-1.0-SNAPSHOT.jar
```
 我们可以在hadoop管理界面查看任务

 
```
地址： http://localhost:8088/cluster/apps/RUNNING
```
 ![这里写图片描述](https://img-blog.csdn.net/20170615225323614?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvemh1bWluZ3l1YW4xMTE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)   
 因为我在pc机上运行程序，花费时间比较长，还有几次死机了。。。。运行成功之后状态会变成SUCCESSED。

 
### 总结

 到此spark环境搭建和示例运行就完成啦，注意在运行代码的过程中可能出现错误 `ERROR Executor: Exception in task 0.0 in stage 0.0 (TID 0) 
java.lang.AbstractMethodError: lekko.spark.SparkDemo$1.call(Ljava/lang/Object;)Ljava/util/Iterator;`    
 这是由于scala和spark版本不兼容的原因，最开始我安装的是scala-2.12,后来在spark官网发现如下内容：

 
```
Note: Starting version 2.0, Spark is built with Scala 2.11 by default. Scala 2.10 users should download the Spark source package and build with Scala 2.10 support.
```
 也就是说我的spark是用scala-2.11构建的，所以把scala版本改为2.11，然后对代码进行调整，上面代码示例中有一段注释的部分

 
```
@Override
            public Iterable<String> call(String s) throws Exception {
                return Arrays.asList(SPACE.split(" "));
            }
```
 这里返回的类型是Iterable,这是scala-2.12版本的返回类型，对于scala-2.11我们的返回类型是Iterator，所以调整代码如下：

 
```
@Override
            public Iterator<String> call(String s) throws Exception {
                return Arrays.asList(s.split(" ")).iterator();
```
 至此所有问题解决啦，希望对其他掉进坑里的同学有所帮助！   
 个人认为使用spark还是需要使用scala编程语言进行开发，这样可以非常简化代码，同是也可能避免这种版本问题，这个后续待研究！

   
  