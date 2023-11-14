# jackson

com.fasterxml.jackson.databind.ObjectMapper
ObjectMapper

readValue()
writeValueAsString()               com.fasterxml.jackson.databind.ObjectMapper#writeValueAsString

报错：
```shell
com.fasterxml.jackson.databind.exc.InvalidFormatException: Cannot deserialize value of type `java.util.Date` from String "2023-05-18": not a valid representation (error: Failed to parse Date value '2023-05-18': Unparseable date: "2023-05-18")
```

在该字段上加上
```java
    @JsonFormat(shape = JsonFormat.Shape.STRING,pattern = 
```
### 支持多种格式

当使用Jackson库解析JSON数据时，如果JSON中包含了Java对象中未定义的属性，Jackson会抛出UnrecognizedPropertyException异常，提示存在未识别的属性。为了避免这个问题，可以使用ObjectMapper类的configure()方法来设置忽略未知属性的选项。

以下是一个示例：

```java
ObjectMapper objectMapper = new ObjectMapper();
objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
MyData myData = objectMapper.readValue(jsonString, MyData.class);
```

在上述代码中，我们首先创建了一个ObjectMapper对象，并使用configure()方法将FAIL_ON_UNKNOWN_PROPERTIES选项设置为false。这个选项表示在反序列化时，如果遇到未知属性，Jackson不会抛出异常，而是忽略这些属性。然后，我们使用readValue()方法将JSON字符串转换为MyData对象。在转换过程中，Jackson会忽略JSON中存在但Java对象中未定义的属性。

需要注意的是，禁用FAIL_ON_UNKNOWN_PROPERTIES选项可能会使反序列化结果不完整，因为未知属性被忽略了。因此，我们应该根据实际情况来决定是否需要禁用这个选项。如果JSON中包含了大量未知属性，而我们只关心其中的一部分，可以考虑使用Mix-in机制来为Java对象添加需要的属性，而忽略不需要的属性。


```java
package cn.wdidada.springmvccurl.vo;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;

public enum Fruit {
    APPLE,
    BANANA,
    ORANGE;

    @JsonCreator
    public static Fruit fromString(String value) {
        return valueOf(value.toUpperCase());
    }

    @JsonValue
    public String toValue() {
        return name().toLowerCase();
    }
}
```

当HTTP请求中传递0或1时，如果您的服务器端代码中使用了Java枚举类型来表示状态，您可以使用Jackson库的`@JsonCreator`注解来自定义反序列化逻辑，将0和1分别映射到枚举类型的不同值。

下面是一个示例，演示了如何在服务器端接收HTTP请求中的状态值，并将其映射到枚举类型的不同值：

```java
public enum Status {
    SUCCESS, FAILURE;

    @JsonCreator
    public static Status fromInt(int value) {
        return value == 0 ? SUCCESS : FAILURE;
    }
}
```

在上述示例中，`Status`是一个简单的枚举类型，包含了两个状态值：`SUCCESS`和`FAILURE`。`@JsonCreator`注解被用于静态的`fromInt()`方法上，表示在反序列化时将使用该方法来创建枚举类型。在`fromInt()`方法中，我们根据传入的整数值（0或1）来选择相应的枚举类型。

在处理HTTP请求时，您可以将状态值作为HTTP参数传递，并使用`@RequestParam`注解来接收该参数。例如：

```java
@RestController
public class MyController {

    @PostMapping("/myendpoint")
    public MyResponse handleRequest(@RequestParam("status") Status status) {
        // 处理请求，并返回一个MyResponse对象
        MyResponse response = new MyResponse();
        response.setStatus(status);
        return response;
    }
}
```

在上述示例中，`@RequestParam("status")`注解表示将HTTP参数中名为`status`的值映射到`Status`类型的`status`参数上。当HTTP请求中传递0时，`status`参数将被映射到`SUCCESS`枚举值；当传递1时，`status`参数将被映射到`FAILURE`枚举值。

需要注意的是，如果HTTP参数中传递的值不是0或1，那么`fromInt()`方法将会抛出`IllegalArgumentException`异常。因此，您需要在代码中进行相应的异常处理。


支持json和xml
springmvc默认的json序列化 反序列化工具

## 测试代码 demo

https://gitee.com/edidada/testjackson
http接口入参 出参 json格式的，用这个
日期参数，加上@JsonFormat @DateTimeFormat
注解@DateTimeFormat:主要是控制后台到前台的时间格式
注解@JsonFormat:主要是限制前台到后台的时间格式



json规范，需要读一下

如何处理java Enum String的空格字符串，空字符串，没有赋值的字符串

[Jackson实现序列化和反序列化](https://blog.csdn.net/wus_shang/article/details/79286544)

Spring用
Jackson是一个 Java 的用来处理 JSON 格式数据的类库，性能非常好。


https://github.com/FasterXML/jackson-core/
http://wiki.fasterxml.com/JacksonDownload

### jar包
- jackson-annotations
- jackson-core
- jackson-databind

- jackson-dataformat-xml xml格式化的

```xml
<!--Jackson包-->
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-core</artifactId>
      <version>2.9.0</version>
    </dependency>
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-databind</artifactId>
      <version>2.9.0</version>
    </dependency>
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-annotations</artifactId>
      <version>2.9.0</version>
    </dependency>
```

版本

com.fasterxml.jackson.databind.ObjectMapper
ObjectMapper

readValue()
String writeValueAsString()               com.fasterxml.jackson.databind.ObjectMapper#writeValueAsString


ObjectMapper中的writeVaule和writeValueAsString方法之间的关系
https://blog.csdn.net/qq_43872529/article/details/104176433


springmvccurl jackson



List
https://blog.csdn.net/qq_35872456/article/details/96295943

```java
    ObjectMapper mapper = new ObjectMapper();

    List<User> users = null;
    try {
        users = mapper.readValue(json, new TypeReference<List<User>>(){});
        mapper.writeValueAsString(users);
    }catch (IOException e){
        throw new RuntimeException(e);
    }
```


com.fasterxml.jackson.core.type.TypeReference
new TypeReference<List<User>>(){};

匿名内部类

例子
https://www.baeldung.com/jackson-object-mapper-tutorial
例子对应的源码
https://github.com/eugenp/tutorials/tree/master/jackson-simple

@JsonPropertyOrder
@JsonRawValue
@JsonRootName(value = "user")
@JsonRootName(value = "user", namespace="users") xml的
@JacksonInject
@JsonRootName
@JacksonInject

@JacksonInject
@JsonRootName
@JsonSetter
@JsonDeserialize
@JsonAlias({ "fName", "f_name" })


@JsonIgnoreProperties({ "id" })
@JsonIgnore
@JsonIgnoreType
@JsonInclude(Include.NON_NULL)
@JsonIncludeProperties({ "name" })
@JsonAutoDetect(fieldVisibility = Visibility.ANY)


@JsonProperty("name") 方法上
@JsonUnwrapped
    @JsonView(Views.Public.class)
    @JsonManagedReference


@JsonIdentityInfo(
  generator = ObjectIdGenerators.PropertyGenerator.class,
  property = "id")
public class ItemWithIdentity {
    public int id;
    public String itemName;
    public UserWithIdentity owner;
}




@JsonAnySetter是Jackson库中的一个注解，用于在反序列化JSON数据时，解析不确定或动态的JSON属性。
当我们在反序列化JSON数据时，如果JSON数据包含一些我们未知的属性，或者属性名在运行时才能确定，我们就可以使用@JsonAnySetter注解来处理这些属性。
@JsonAnySetter可以用于一个方法上。这个方法需要带有两个参数：一个String类型的参数表示属性名，一个Object类型的参数表示属性值。
当Jackson反序列化JSON数据时，如果遇到未知的属性，它会调用被@JsonAnySetter注解的方法，并将未知属性的名字和值传递给该方法。然后我们可以在这个方法中根据属性名和属性值做一些处理，比如将它们存储在一个Map中，或者将它们设置为对象的某个属性。
@JsonAnyGetter反过来
例子：
com.baeldung.jackson.test.JacksonAnnotationUnitTest#whenSerializingUsingJsonAnyGetter_thenCorrect

public @ResponseBody String  fileUpload(@RequestParam("file") CommonsMultipartFile file) throws IOException



org.springframework.web.multipart.commons.CommonsMultipartFile


### spring是如何使用jackson

<bean class="org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter">
    <property name="messageConverters">
        <list>
            <bean class="org.springframework.http.converter.json.MappingJackson2HttpMessageConverter">
                <property name="objectMapper" ref="jacksonObjectMapper"/>
            </bean>
        </list>
    </property>
</bean>

<bean id="jacksonObjectMapper" class="com.fasterxml.jackson.databind.ObjectMapper"/>



### com.fasterxml.jackson.databind.ObjectMapper配置项

ObjectMapper是Jackson库中的一个核心类，它负责将Java对象序列化为JSON格式的数据，或将JSON格式的数据反序列化为Java对象。 ObjectMapper提供了许多配置项，可以帮助你自定义序列化和反序列化的行为。下面是一些常用的ObjectMapper配置项：

1、SerializationFeature
SerializationFeature是用于控制序列化行为的枚举类，它包含了许多序列化相关的配置项。例如，SerializationFeature.INDENT_OUTPUT可以让ObjectMapper在序列化时输出美观的格式化JSON数据，SerializationFeature.WRITE_DATES_AS_TIMESTAMPS可以让ObjectMapper将Date类型的数据序列化为timestamp格式的数据等等。

2、DeserializationFeature
DeserializationFeature是用于控制反序列化行为的枚举类，它包含了许多反序列化相关的配置项。例如，DeserializationFeature.ACCEPT_EMPTY_STRING_AS_NULL_OBJECT可以让ObjectMapper在反序列化时将空字符串转换为null对象，DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES可以让ObjectMapper在反序列化时忽略未知的JSON属性等等。

3、ObjectMapper.registerModule(Module)
ObjectMapper.registerModule(Module)方法可以注册一个自定义的Module，它可以帮助你自定义序列化和反序列化的行为。例如，你可以通过创建一个自定义的SimpleModule来自定义Date类型的序列化和反序列化行为。例如：
```java
SimpleModule module = new SimpleModule();
module.addSerializer(Date.class, new JsonSerializer<Date>() {
    @Override
    public void serialize(Date value, JsonGenerator gen, SerializerProvider serializers) throws IOException {
        gen.writeString(new SimpleDateFormat("yyyy-MM-dd").format(value));
    }
});

module.addDeserializer(Date.class, new JsonDeserializer<Date>() {
    @Override
    public Date deserialize(JsonParser p, DeserializationContext ctxt) throws IOException, JsonProcessingException {
        String dateString = p.getText();
        try {
            return new SimpleDateFormat("yyyy-MM-dd").parse(dateString);
        } catch (ParseException e) {
            throw new RuntimeException(e);
        }
    }
});

ObjectMapper objectMapper = new ObjectMapper();
objectMapper.registerModule(module);
```

上面的代码中，我们创建了一个SimpleModule，然后添加了一个Date类型的序列化器和反序列化器。在序列化时，我们使用SimpleDateFormat将Date类型的数据格式化为"yyyy-MM-dd"的格式，然后将其输出为字符串；在反序列化时，我们使用SimpleDateFormat将字符串解析为Date类型的数据。最后，我们将这个自定义的Module注册到ObjectMapper中。

4、ObjectMapper.setDateFormat(DateFormat)
ObjectMapper.setDateFormat(DateFormat)方法可以设置一个默认的日期格式化器，它可以帮助你在序列化和反序列化Date类型的数据时使用指定的日期格式。例如：

```java
ObjectMapper objectMapper = new ObjectMapper();
DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
objectMapper.setDateFormat(dateFormat);
```

上面的代码中，我们创建了一个SimpleDateFormat，然后使用ObjectMapper.setDateFormat()方法将其设置为ObjectMapper的默认日期格式化器。

5、ObjectMapper.configure(JsonParser.Feature, boolean)
ObjectMapper.configure(JsonParser.Feature, boolean)方法可以用于配置JsonParser的行为。例如，我们可以使用JsonParser.Feature.ALLOW_SINGLE_QUOTES来启用JSON单引号的支持：

```java
ObjectMapper objectMapper = new ObjectMapper();
objectMapper.configure(JsonParser.Feature.ALLOW_SINGLE_QUOTES, true);
```

上面的代码中，我们启用了JSON单引号的支持，这意味着ObjectMapper可以解析包含单引号的JSON数据。

这些是ObjectMapper中的一些常用配置项，它们可以帮助你自定义JSON序列化和反序列化的行为。当然，ObjectMapper还提供了许多其他的配置项，你可以根据自己的需求进行选择和配置。

JsonParser.Feature

JsonParser_Feature.png

- AUTO_CLOSE_SOURCE
- ALLOW_COMMENTS
- ALLOW_YAML_COMMENTS
- ALLOW_UNQUOTED_FIELD_NAMES
- ALLOW_SINGLE_QUOTES
- ALLOW_UNQUOTED_CONTROL_CHARS
- ALLOW_BACKSLASH_ESCAPING_ANY_CHARACTER
- ALLOW_NUMERIC_LEADING_ZEROS
- ALLOW_NON_NUMERIC_NUMBERS
- ALLOW_MISSING_VALUES
- ALLOW_TRAILING_COMMA
- STRICT_DUPLICATE_DETECTION
- IGNORE_UNDEFINED
- INCLUDE_SOURCE_IN_LOCATION


这些配置项是Jackson库中JsonParser的一些特定配置项，它们可以帮助你控制JSON解析的行为。下面是这些配置项的详细解释：

AUTO_CLOSE_SOURCE
AUTO_CLOSE_SOURCE是一个布尔值，如果设置为true，JsonParser在完成解析后将自动关闭输入流。这可以帮助你自动释放资源，但也有可能导致一些问题，比如在处理大型JSON文件时可能会耗尽文件句柄。

ALLOW_COMMENTS
ALLOW_COMMENTS是一个布尔值，如果设置为true，JsonParser可以解析JSON中的注释。这可以帮助你在JSON数据中添加注释，但也可能会导致一些问题，比如可能会使JSON解析变慢。

ALLOW_YAML_COMMENTS
ALLOW_YAML_COMMENTS是一个布尔值，如果设置为true，JsonParser可以解析YAML风格的注释。YAML注释可以跨越多行，并且可以使用#或//作为注释符号。

ALLOW_UNQUOTED_FIELD_NAMES
ALLOW_UNQUOTED_FIELD_NAMES是一个布尔值，如果设置为true，JsonParser可以解析没有引号的JSON属性名。这可以帮助你在JSON数据中使用更简洁的语法，但也可能会导致一些问题，比如可能会使JSON解析变慢，或者可能会使解析器错误地将属性值解析为属性名。

ALLOW_SINGLE_QUOTES
ALLOW_SINGLE_QUOTES是一个布尔值，如果设置为true，JsonParser可以解析单引号括起来的字符串。这可以帮助你在JSON数据中使用更灵活的语法，但也可能会导致一些问题，比如可能会使JSON解析变慢，或者可能会使解析器错误地将属性值解析为属性名。

ALLOW_UNQUOTED_CONTROL_CHARS
ALLOW_UNQUOTED_CONTROL_CHARS是一个布尔值，如果设置为true，JsonParser可以解析未使用引号括起来的控制字符。这可以帮助你在JSON数据中使用更灵活的语法，但也可能会导致一些安全问题，比如可能会使解析器错误地解析恶意JSON数据。

ALLOW_BACKSLASH_ESCAPING_ANY_CHARACTER
ALLOW_BACKSLASH_ESCAPING_ANY_CHARACTER是一个布尔值，如果设置为true，JsonParser可以解析任何被反斜杠转义的字符。这可以帮助你在JSON数据中使用更灵活的语法，但也可能会导致一些安全问题，比如可能会使解析器错误地解析恶意JSON数据。

ALLOW_NUMERIC_LEADING_ZEROS
ALLOW_NUMERIC_LEADING_ZEROS是一个布尔值，如果设置为true，JsonParser可以解析以0开头的数字。这可以帮助你在JSON数据中使用更灵活的语法，但也可能会导致一些问题，比如可能会使JSON解析变慢，或者可能会使解析器错误地解析数字。

ALLOW_NON_NUMERIC_NUMBERS
ALLOW_NON_NUMERIC_NUMBERS是一个布尔值，如果设置为true，JsonParser可以解析非数字的JSON数据，比如NaN和Infinity。这可以帮助你在JSON数据中使用更灵活的语法，但也可能会导致一些问题，比如可能会使JSON解析变慢，或者可能会使解析器错误地解析JSON数据。

ALLOW_MISSING_VALUES
ALLOW_MISSING_VALUES是一个布尔值，如果设置为true，JsonParser可以解析缺少属性值的JSON数据。这可以帮助你在JSON数据中使用更灵活的语法，但也可能会导致一些问题，比如可能会使解析器错误地解析JSON数据。

ALLOW_TRAILING_COMMA
ALLOW_TRAILING_COMMA是一个布尔值，如果设置为true，JsonParser可以解析在JSON数组和对象中的末尾添加逗号。这可以帮助你在JSON数据中使用更灵活的语法，但也可能会导致一些问题，比如可能会使JSON解析变慢，或者可能会使解析器错误地解析JSON数据。

STRICT_DUPLICATE_DETECTION
STRICT_DUPLICATE_DETECTION是一个布尔值，如果设置为true，JsonParser会在解析JSON对象时检测重复的属性名。这可以帮助你在JSON数据中避免重复的属性名，但也可能会使JSON解析变慢。

IGNORE_UNDEFINED
IGNORE_UNDEFINED是一个布尔值，如果设置为true，JsonParser会忽略JSON数据中的未定义属性。这可以帮助你在JSON数据中忽略一些不需要的属性，但也可能会导致一些问题，比如可能会使解析器错误地解析JSON数据。

INCLUDE_SOURCE_IN_LOCATION
INCLUDE_SOURCE_IN_LOCATION是一个布尔值，如果设置为true，JsonParser会在解析JSON时包含源文件的位置信息。这可以帮助你在处理JSON数据时进行调试，但也可能会使JSON解析变慢

#### 代码分包详解

https://fasterxml.github.io/jackson-databind/javadoc/2.11/

jackson_2_11_apidoc.xlsx
