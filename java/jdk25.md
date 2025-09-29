# jdk25

2025年9月16日，Java发布了最新的长期支持版本（LTS）JDK 25。

Java 25 新特性与API详解

Java 25作为最新的长期支持版本(LTS)，于2025年9月16日正式发布，带来了许多令人兴奋的新特性和API改进。以下是Java 25的主要新增特性和API，包含详细的代码示例。

1. 语言简化特性

1.1 简化main方法 (JEP 512)

Java 25进一步简化了main方法的写法，使其更接近脚本语言的风格：
// 最简单的main方法形式
void main() {
    IO.println("Hello, Java 25!"); // 自动导入java.lang.IO
}


新版本中，IO类已从java.io包移动到了java.lang包，因此无需显式导入。

1.2 灵活构造函数 (JEP 513)

允许在调用super()或this()之前执行初始化逻辑：
class User {
    private String id;
    
    User(String rawId) {
        if (rawId == null || rawId.isEmpty()) {
            throw new IllegalArgumentException("ID不能为空");
        }
        this.id = normalizeId(rawId); // 校验前置
    }
    
    private String normalizeId(String id) {
        return id.trim().toUpperCase();
    }
}


这一改进使得参数校验和预处理更加直观。

1.3 模块导入声明 (JEP 511，预览)

可以一次性导入整个模块的所有公共类：
import module java.sql; // 导入java.sql模块的所有类

public class DatabaseDemo {
    void main() {
        // 直接使用java.sql中的类，无需单独导入
        var connection = DriverManager.getConnection("jdbc:mysql://localhost/test");
        // ...
    }
}


这大大简化了多模块项目的导入语句。

2. 并发与线程相关特性

2.1 Scoped Values (JEP 506)

替代ThreadLocal的现代化方案，专为虚拟线程设计：
private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();

void processRequest(Request request) {
    var user = authenticate(request);
    ScopedValue.where(CURRENT_USER, user)
               .run(() -> handleRequest(request));
}

void handleRequest(Request request) {
    User user = CURRENT_USER.get(); // 获取当前作用域绑定的用户
    logger.info("Processing request for user: " + user.name());
    // ...
}


相比ThreadLocal，ScopedValue具有自动清理、不可变设计和更好的虚拟线程支持等优势。

2.2 结构化并发 (JEP 505，第五次预览)

Response handle() throws InterruptedException {
    try (var scope = StructuredTaskScope.open()) {
        Subtask<String> user = scope.fork(() -> findUser());
        Subtask<Integer> order = scope.fork(() -> fetchOrder());
        
        scope.join(); // 等待所有子任务完成
        
        return new Response(user.get(), order.get());
    } // 作用域结束时自动取消未完成的任务
}


结构化并发API提供了更清晰的并发任务管理方式。

3. 模式匹配增强

3.1 原始类型模式匹配 (JEP 507，第三次预览)

String evaluate(Object value) {
    return switch(value) {
        case Integer i when i > 100 -> "Large number";
        case int i when i > 100 -> "Large primitive int"; // 直接匹配原始类型
        case double d when d < 0 -> "Negative double";
        case boolean b -> b ? "Yes" : "No";
        default -> "Unknown";
    };
}


现在可以直接在模式匹配中使用原始类型，避免了不必要的装箱拆箱操作。

3.2 带守卫的模式 (Guarded Patterns)

static void test(Object obj) {
    switch (obj) {
        case String s when s.length() == 1 -> 
            System.out.println("Short string: " + s);
        case String s -> 
            System.out.println("Normal string: " + s);
        case Double d when d > 1000 -> 
            System.out.println("Large double: " + d);
        default -> 
            System.out.println("Other type");
    }
}


when子句允许在模式匹配中添加额外的条件判断。

4. 安全相关API

4.1 PEM编码支持 (JEP 470，预览)

// 生成密钥对
KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
KeyPair keyPair = keyGen.generateKeyPair();

// 编码公钥为PEM格式
String publicKeyPEM = PEMEncoder.of().encodeToString(keyPair.getPublic());
System.out.println("Public Key PEM:\n" + publicKeyPEM);

// 编码私钥为加密的PEM格式
String privateKeyPEM = PEMEncoder.of()
    .withEncryption("password".toCharArray())
    .encodeToString(keyPair.getPrivate());

// 解码PEM格式的公钥
PublicKey decodedPubKey = PEMDecoder.of()
    .decode(publicKeyPEM, PublicKey.class);


提供了标准化的API来处理PEM格式的密钥和证书。

4.2 密钥派生函数 (JEP 510)

// 使用PBKDF2算法派生密钥
SecretKey derivedKey = KeyDerivationFunction.of("PBKDF2WithHmacSHA256")
    .withIterations(10000)
    .withSalt(salt)
    .deriveKey("password".toCharArray(), 256);

// 使用Argon2算法(抗量子计算)
SecretKey argon2Key = KeyDerivationFunction.of("Argon2id")
    .withMemoryCost(65536)
    .withParallelism(4)
    .withIterations(3)
    .deriveKey("password".toCharArray(), 256);


新增了标准化的密钥派生API，支持多种算法包括抗量子计算算法。

5. 性能优化相关特性

5.1 紧凑对象头 (JEP 519)

// 启用紧凑对象头(默认已启用，如需关闭可使用-XX:-UseCompactObjectHeaders)
// 无需代码改动，所有对象自动受益

// 测试内存占用
public class SmallObject {
    byte b;
    int i;
}

void testMemory() {
    long before = Runtime.getRuntime().freeMemory();
    SmallObject[] array = new SmallObject[100_000];
    for (int i = 0; i < array.length; i++) {
        array[i] = new SmallObject();
    }
    long used = before - Runtime.getRuntime().freeMemory();
    IO.println("Used memory: " + used + " bytes");
}


对象头从128位压缩至64位，减少小对象内存占用约30%。

5.2 Stable Values (JEP 502，预览)

class Service {
    private final StableValue<ExpensiveResource> resource = StableValue.of();
    
    ExpensiveResource getResource() {
        return resource.orElseSet(() -> initializeResource());
    }
    
    private ExpensiveResource initializeResource() {
        // 昂贵的初始化操作
        return new ExpensiveResource();
    }
}


Stable Values提供了延迟初始化的不可变值支持，比final字段更灵活，比常规字段更安全。

6. 其他实用特性

6.1 字符串模板 (JEP 467)

String name = "Alice";
int score = 98;
LocalDateTime now = LocalDateTime.now();

// STR模板处理器(自动转义)
String message = STR."学生 \{name} 得分 \{score}，时间：\{now}";

// FMT模板处理器(格式化)
String formatted = FMT."成绩：\{score}%，排名：\{%04d, score}";

// 自定义SQL模板处理器(防注入)
String sql = SQL."SELECT * FROM users WHERE name = '\{name}'";


字符串模板提供了更安全、更直观的字符串插值方式。

6.2 向量API (JEP 469，第十次孵化)

static final VectorSpecies<Float> SPECIES = FloatVector.SPECIES_PREFERRED;

void vectorAdd(float[] a, float[] b, float[] c) {
    int i = 0;
    for (; i < SPECIES.loopBound(a.length); i += SPECIES.length()) {
        var va = FloatVector.fromArray(SPECIES, a, i);
        var vb = FloatVector.fromArray(SPECIES, b, i);
        var vc = va.add(vb);
        vc.intoArray(c, i);
    }
    // 处理剩余元素
    for (; i < a.length; i++) {
        c[i] = a[i] + b[i];
    }
}


向量API允许利用CPU的SIMD指令进行高性能计算。

总结

Java 25作为重要的LTS版本，带来了许多实用的新特性和API改进：

1. 语言简化：简化main方法、灵活构造函数、模块导入等
2. 并发增强：Scoped Values、结构化并发等现代化并发工具
3. 模式匹配：原始类型支持、带守卫的模式等增强
4. 安全API：PEM编码、密钥派生函数等安全相关改进
5. 性能优化：紧凑对象头、Stable Values等性能提升特性
6. 其他实用特性：字符串模板、向量API等

这些新特性使Java在保持稳定性的同时，继续提升开发效率和运行时性能，特别是在并发、安全和大数据处理等领域。
