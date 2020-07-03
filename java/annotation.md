# annotation



https://blog.csdn.net/heyrian/article/details/80764783





注解处理器类库
Java通过反射机制获取类、方法、属性上的注解，因此java.lang.reflect提供AnnotationElement支持注解，主要方法如下：

boolean is AnnotationPresent(Class<?extends Annotation> annotationClass)：判断该元素是否被annotationClass注解修饰
<T extends Annotation> T getAnnotation(Class<T> annotationClass)：获取 该元素上annotationClass类型的注解，如果没有返回null
Annotation[] getAnnotations()：返回该元素上所有的注解
<T extends Annotation> T[] getAnnotationsByType(Class<T> annotationClass)：返回该元素上指定类型所有的注解
Annotation[] getDeclaredAnnotations()：返回直接修饰该元素的所有注解
<T extends Annotation> T[] getDeclaredAnnotationsByType(Class<T> annotationClass)：返回直接修饰该元素的所有注解
————————————————
版权声明：本文为CSDN博主「heyrian」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/heyrian/article/details/80764783



@interface



元注解

@Target

@Documented

@Retention

@Inherent







Java目前内置了三种注解@Override、@Deprecated、@SuppressWarnnings



 注解中的参数类型

注解中的参数只支持如下类型：



- 所有的基本类型：byte、short、char、int、long、float、double （boolean不支持
- String类型
- Class类型
- enum类型
- Annotation类型
- 以上类型的数组





java.lang.Class



Class上的注解

class.getAnnotation();



java.lang.reflect.Method





