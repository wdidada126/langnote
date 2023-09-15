# java11
https://www.ibm.com/developerworks/cn/java/the-new-features-of-Java-11/index.html

java 11没有sun.misc.BASE64Decoder;
您是正确的，Java 11中已经移除了sun.misc.BASE64Decoder类。在Java 9及之后的版本中，Oracle官方不再推荐使用sun.misc包下的类，因为它们是内部实现，不是公共API，可能会在未来的版本中被删除。

在Java 11中，您可以使用java.util.Base64类来进行Base64编解码操作。该类提供了静态方法来处理Base64数据。下面是一个示例：

```java
import java.util.Base64;

public class Base64Example {
    public static void main(String[] args) {
        String originalString = "Hello, World!";
        
        // 编码为Base64
        String encodedString = Base64.getEncoder().encodeToString(originalString.getBytes());
        System.out.println("Encoded string: " + encodedString);
        
        // 解码Base64
        byte[] decodedBytes = Base64.getDecoder().decode(encodedString);
        String decodedString = new String(decodedBytes);
        System.out.println("Decoded string: " + decodedString);
    }
}
```

在示例中，我们使用`Base64.getEncoder()`获取编码器对象，并调用`encodeToString()`方法将原始字符串编码为Base64字符串。然后，我们使用`Base64.getDecoder()`获取解码器对象，并调用`decode()`方法将Base64字符串解码为字节数组，最后将字节数组转换为字符串。

请注意，Java 11中的`java.util.Base64`类提供了更多的功能，例如支持URL和文件编解码，以及对流的支持。您可以根据实际需求选择适当的方法来进行Base64编解码操作。