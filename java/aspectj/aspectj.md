# aspectj

[maven-weave-aspectj](https://github.com/edidada/maven-weave-aspectj)



1.8.9



1.9.3



Java5+ 之后 AspectJ 可以写成 Java 类加注解的方式，*.aj 文件一般都没太大必要了



只要用 `@Aspect` 标识出它是一个 Aspect, 或者也可以完全用 AspectJ 语法，创建 *.aj 文件，里面写 `public aspect MethodStartAspect` 这样的的定义




http://www.eclipse.org/aspectj/



https://www.eclipse.org/aspectj/doc/released/progguide/examples-howto.html



有可执行文件，生成.class文件？

asm字节码技术



<<<<<<< HEAD
[使用插件 aspectj-maven-plugin 织入 AspectJ AOP](https://blog.csdn.net/weixin_34417814/article/details/92531310)
=======
使用插件 aspectj-maven-plugin 织入 AspectJ AOP

https://blog.csdn.net/weixin_34417814/article/details/92531310
>>>>>>> afe522da082020e5ece0b75c43067644b2edb768


aspectj-maven-plugin




<<<<<<< HEAD
[aspectjweaver和aspectjrt的作用 作用、说明、案例 ](https://www.cnblogs.com/Peter-Yu/p/11604969.html)
=======
[aspectjweaver和aspectjrt的作用？（作用、说明、案例）](https://www.cnblogs.com/Peter-Yu/p/11604969.html)
>>>>>>> afe522da082020e5ece0b75c43067644b2edb768





aspectjweaver

aj.org.objectweb.asm.CurrentFrame



aspectjweaver包含aspectjrt



例子

AspectJ是一个面向切面的AOP框架，AOP的织入方式分为编译期织入、装载期织入、运行期织入。



https://blog.csdn.net/u012477420/article/details/71981950



aspectj vs Spring AOP

[比较Spring AOP与AspectJ](https://juejin.im/post/5a695b3cf265da3e47449471)

[Aspectj中call与execution区别，织入代码位置不同](https://blog.csdn.net/Dax1n/article/details/81944975)

[AspectJ切入点@Pointcut语法详解](https://www.mekau.com/4880.html)

分类pointcuts 遵循特定的语法用于捕获每一个种类的可使用连接点。 主要的种类：
方法执行：execution(MethodSignature)
方法调用：call(MethodSignature)
构造器执行：execution(ConstructorSignature)
构造器调用：call(ConstructorSignature)
类初始化：staticinitialization(TypeSignature)
属性读操作：get(FieldSignature)
属性写操作：set(FieldSignature)
例外处理执行：handler(TypeSignature)
对象初始化：initialization(ConstructorSignature)
对象预先初始化：preinitialization(ConstructorSignature)



<<<<<<< HEAD
=======


>>>>>>> afe522da082020e5ece0b75c43067644b2edb768
.aj文件

aspectj自用编译器



下一步，查看其他编程语言是如何实现aop的



aop的实现原理



修改字节码

ajc编译器



<<<<<<< HEAD
https://www.jianshu.com/p/f9acae180f81




=======


https://www.jianshu.com/p/f9acae180f81
>>>>>>> afe522da082020e5ece0b75c43067644b2edb768

https://www.eclipse.org/aspectj/doc/released/progguide/examples-howto.html


<<<<<<< HEAD


=======
>>>>>>> afe522da082020e5ece0b75c43067644b2edb768
AspectJ在Spring中的使用

https://www.jianshu.com/p/958af6a90477

