# hibernate

jboss

java ee 5开始的

http://hibernate.org/validator/


hibernate Oracle自动建表 项目 github


https://gitee.com/edidada/hibernate-tutorials5.1.7



https://github.com/hibernate/hibernate-orm/blob/5.1/documentation/src/test/java/org/hibernate/userguide/naming/AcmeCorpPhysicalNamingStrategy.java

`AcmeCorpPhysicalNamingStrategy`是Hibernate官方文档中提供的一个示例`PhysicalNamingStrategy`实现，用于将Java实体类中的属性名转换为下划线命名法的数据库列名，并添加"acme_"前缀。你可以在Hibernate官方文档中找到该示例的详细介绍和代码实现。

你可以从Hibernate的GitHub仓库中下载最新版本的Hibernate官方文档，或者访问Hibernate官方网站上的文档页面。以下是从GitHub仓库中下载Hibernate 5.5版本的命名策略文档及示例代码的步骤：

1. 访问Hibernate的GitHub仓库：https://github.com/hibernate/hibernate-orm
2. 点击“Releases”标签页，找到最新版本的Hibernate发行版，并点击其名称进入发行版页面。
3. 在页面底部的“Assets”部分中，找到名为“hibernate-orm-x.y.z.docs.zip”的文档压缩包，其中“x.y.z”是当前发行版的版本号。点击该文件名即可下载文档压缩包。
4. 解压文档压缩包，找到“documentation/userguide/html_single/naming/index.html”文件，用浏览器打开该文件即可阅读Hibernate命名策略文档的HTML版本。
5. 在该文档中，找到“AcmeCorpPhysicalNamingStrategy”一节，即可查看该示例实现的代码。

如果你只需要获取`AcmeCorpPhysicalNamingStrategy`的代码实现，可以通过访问Hibernate的GitHub仓库，找到该类对应的Java源码文件，然后下载或复制该文件即可。以下是获取`AcmeCorpPhysicalNamingStrategy`类代码的具体步骤：

1. 访问Hibernate的GitHub仓库：https://github.com/hibernate/hibernate-orm
2. 在仓库主页的搜索框中输入“AcmeCorpPhysicalNamingStrategy”，然后点击搜索按钮。
3. 在搜索结果中找到名为“AcmeCorpPhysicalNamingStrategy.java”的Java源码文件，点击该文件名即可进入该文件的页面。
4. 在该页面中，可以查看该类的代码实现，并复制或下载该文件以便在你的项目中使用。



`@Basic`是Java Persistence API (JPA)中的注解之一，用于标注实体类中的属性或字段，表示这个属性或字段是一个基本类型，需要进行持久化存储。它是JPA规范中最基础的注解之一，用于定义实体类属性的基本特征。
`@Basic`注解可以被用于实体类中的任何属性或字段，包括基本类型（如String、Integer、Boolean等）和复杂类型（如集合、数组等）。当一个实体类中的属性或字段被标注了`@Basic`注解后，JPA会将其映射为数据库表中的一个列，用于存储该属性或字段的值。
`@Basic`注解可以指定两个可选属性：

- `optional`：指定该属性是否可为null。默认为true，即可为null。
- `fetch`：指定该属性的加载方式。默认为`FetchType.EAGER`，即立即加载。

以下是`@Basic`注解的一个示例：

```
@Entity
public class Person {
 
    @Id
    private Long id;
 
    @Basic(optional = false)
    private String name;
 
    @Basic(fetch = FetchType.LAZY)
    private int age;
 
    // 省略其他属性和方法
}
```

在这个示例中，`Person`实体类中的`name`和`age`属性都被标注了`@Basic`注解。其中，`name`属性指定了`optional`属性为false，表示该属性不可为null；而`age`属性指定了`fetch`属性为`FetchType.LAZY`，表示该属性应该在需要时才进行加载。
总之，`@Basic`注解是JPA中最基础的注解之一，用于标注实体类中需要进行持久化存储的属性或字段，并可以指定一些可选属性来控制该属性或字段的行为。


`BasicTypeRegistry`是Hibernate中的一个类，它是Hibernate的类型注册表，用于管理Hibernate的基本数据类型。该类的主要作用是将Java的基本数据类型和Java Persistence（JPA）的类型映射到Hibernate的基本数据类型，并注册到Hibernate的类型系统中以供使用。
Hibernate中的基本数据类型包括：`String`、`Integer`、`Long`、`Boolean`、`Byte`、`Character`、`Short`、`Float`、`Double`、`BigInteger`、`BigDecimal`等。在Hibernate中，这些基本数据类型被称为“基本类型”，并对应了Hibernate中的基本类型名称，例如：`string`、`integer`、`long`、`boolean`、`byte`、`char`、`short`、`float`、`double`、`big_integer`、`big_decimal`等。
当Hibernate需要将Java对象映射到数据库中时，它需要确定每个Java属性对应的数据类型，以便正确地将属性值转换为数据库中的数据类型。`BasicTypeRegistry`就是用于实现这一功能的，它维护了Hibernate中的基本数据类型与Java的基本数据类型之间的映射关系，并提供了一些方法来获取、注册、查找和创建这些类型。
以下是一个示例，展示如何使用`BasicTypeRegistry`来注册和查找Hibernate的基本数据类型：

```
BasicTypeRegistry registry = new BasicTypeRegistry();

// 注册基本类型
registry.register(StringType.INSTANCE);
registry.register(IntegerType.INSTANCE);
registry.register(LongType.INSTANCE);
registry.register(BooleanType.INSTANCE);

// 查找基本类型
Type stringType = registry.getRegisteredType("string");
Type integerType = registry.getRegisteredType("integer");
Type longType = registry.getRegisteredType("long");
Type booleanType = registry.getRegisteredType("boolean");
```

在这个示例中，我们首先创建了一个`BasicTypeRegistry`对象，并使用`register`方法注册了四个Hibernate的基本数据类型：`StringType`、`IntegerType`、`LongType`和`BooleanType`。然后，我们使用`getRegisteredType`方法根据名称查找这些基本类型，并将它们分别赋值给了`stringType`、`integerType`、`longType`和`booleanType`变量。
总之，`BasicTypeRegistry`是Hibernate中的一个类型注册表，用于管理Hibernate的基本数据类型，并提供了一些方法来获取、注册、查找和创建这些类型。它是Hibernate类型系统的核心组件之一，为Hibernate对象映射提供了基础支持。




`javax.persistence.EnumType`是Java Persistence API (JPA)中的一个枚举类型，用于指定枚举类型属性的映射策略。在JPA中，当一个实体类中的属性是枚举类型时，需要使用`@Enumerated`注解来标注该属性，并指定一个枚举类型映射策略。`EnumType`枚举类型中定义了两个枚举值：

- `ORDINAL`：将枚举类型属性映射为Java中的`int`类型，即使用枚举值的序号来进行映射。在数据库中，该属性通常被映射为整数类型的列，并存储枚举值的序号。
- `STRING`：将枚举类型属性映射为Java中的`String`类型，即使用枚举值的名称来进行映射。在数据库中，该属性通常被映射为字符串类型的列，并存储枚举值的名称。

以下是一个示例，展示了如何使用`EnumType`枚举类型来指定枚举类型属性的映射策略：

```
public enum Gender {
    MALE,
    FEMALE
}

@Entity
public class Person {
 
    @Id
    private Long id;
 
    @Enumerated(EnumType.STRING)
    private Gender gender;
 
    // 省略其他属性和方法
}
```

在这个示例中，`Person`实体类中的`gender`属性是一个枚举类型，它被标注了`@Enumerated`注解，并指定了`EnumType.STRING`枚举值，表示使用枚举值的名称来进行映射。在数据库中，该属性通常被映射为字符串类型的列，并存储枚举值的名称。

总之，`javax.persistence.EnumType`是JPA中的一个枚举类型，用于指定枚举类型属性的映射策略。通过指定`EnumType`枚举值，可以将枚举类型属性映射为Java中的`int`类型或`String`类型，并对应地在数据库中存储。



