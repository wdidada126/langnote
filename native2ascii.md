# native2ascii

Java17程序，读取配置文件ares.ent.hljBankName=黑龙江省农村信用社联合社
 application-local.properties文件，spring 代码，      @Value("${ares.ent.hljBankName}")
    private String hljBankName;  debug时显示 é»é¾æ±çåæä¿¡ç¨ç¤¾èåç ¤¾ 是不是文件gbk utf-8之类的原因？

是的，你遇到的问题：

> `é»é¾æ±çåæä¿¡ç¨ç¤¾èåç ¤¾`

完全正确——这确实是由于 `application-local.properties` 文件编码与 Spring 读取时使用的编码不一致 导致的中文乱码问题，典型原因是：文件是 UTF-8 编码，但被错误地以 ISO-8859-1 或平台默认编码（如 GBK）解析了。

## 根本原因分析

### 1. Spring Boot 默认使用 `ISO-8859-1` 读取 `.properties` 文件

这是关键点！

Java 的原生 `Properties` 类在加载 `.properties` 文件时：
- 使用 ISO-8859-1 编码解析（即使你的系统是中文 Windows，默认也是这个）
- 如果文件中包含 UTF-8 中文，就会出现你看到的乱码

> 即使你的 `application-local.properties` 是用 UTF-8 保存的，Spring 也会用 ISO-8859-1 去读，导致中文变成乱码。

### 2. 为什么是 `é»é¾...` 这种形式？

这是典型的“UTF-8 字节流被当成 ISO-8859-1 字符显示”的结果：

- “黑” 的 UTF-8 编码是：`E9 BB 91`
- 当这 3 个字节被当作 ISO-8859-1 解码时，就变成了三个字符：`é»`
- 所以整个字符串就变成一堆 `éã` 开头的拉丁字符，看起来像 `é»é¾æ±...`

## 正确解决方案（Spring Boot 环境）

### 方案一：【推荐】将中文转为 Unicode 转义序列（最兼容）

Spring 官方推荐的做法是：在 `.properties` 文件中使用 Unicode 转义。

#### 修改 `application-local.properties`：
```properties
ares.ent.hljBankName=\u9ED1\u9F99\u6C5F\u7701\u519C\u6751\u4FE1\u7528\u793E\u8054\u5408\u793E
```

> 这是 Java Properties 文件的标准做法，保证在任何环境、任何 JDK 版本下都能正确读取。

#### 验证工具：
你可以用以下命令或在线工具将中文转为 Unicode：
```bash
echo -n "黑龙江省农村信用社联合社" | native2ascii -encoding UTF-8
echo -n "黑龙江农信银行电子回执专用单" | native2ascii -encoding UTF-8
# 输出：\u9ED1\u9F99\u6C5F\u7701\u519C\u6751\u4FE1\u7528\u793E\u8054\u5408\u793E
```
