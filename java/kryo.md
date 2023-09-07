# Kryo

java语言，序列化框架

https://gitee.com/mirrors/kryo

4.0.3 - brings bug fixes and performance improvements for chunked encoding.
5.5.0 - brings bug fixes and performance improvements.
5.4.0 - brings bug fixes and performance improvements.
5.3.0 - brings bug fixes and performance improvements.
5.2.1 - brings minor bug fixes and improvements.
5.2.0 - brings bug fixes for RecordSerializer and improvements. Important: If you are currently storing serialized java.util.Record, please see the release notes for upgrade instructions.
5.1.1 - brings bug fixes for CompatibleFieldSerializer and removes dependency from versioned artifact
5.1.0 - brings support for java.util.Record and improved support for older Android versions
5.0.0 - the final Kryo 5 release fixing many issues and making many long awaited improvements over Kryo 4. Note: For libraries (not applications) using Kryo, there's now a completely self-contained, versioned artifact (for details see installation). For migration from Kryo 4.x see also Migration to v5.

<dependency>
   <groupId>com.esotericsoftware</groupId>
   <artifactId>kryo</artifactId>
   <version>5.5.0</version>
</dependency>

例子

```java
import com.esotericsoftware.kryo.Kryo;
import com.esotericsoftware.kryo.io.Input;
import com.esotericsoftware.kryo.io.Output;
import java.io.*;

public class HelloKryo {
   static public void main (String[] args) throws Exception {
      Kryo kryo = new Kryo();
      kryo.register(SomeClass.class);

      SomeClass object = new SomeClass();
      object.value = "Hello Kryo!";

      Output output = new Output(new FileOutputStream("file.bin"));
      kryo.writeObject(output, object);
      output.close();

      Input input = new Input(new FileInputStream("file.bin"));
      SomeClass object2 = kryo.readObject(input, SomeClass.class);
      input.close();   
   }
   static public class SomeClass {
      String value;
   }
}
```

Kryo序列化被很多开源项目使用，社区非常活跃，版本迭代也比较快。以下的重大项目中都在使用Kryo

Apache Hive
Apache Spark
Twitter's Chill
Storm
akka-kryo-serialization

Java 序列化界新贵 kryo 和熟悉的“老大哥”，就是 PowerJob 的序列化方案 
https://www.cnblogs.com/xueweihan/archive/2020/09/10/13640258.html