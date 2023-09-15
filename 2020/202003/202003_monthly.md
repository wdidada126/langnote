# 202003 month

在家工作
汇编语言
os的相关知识，不应该涉及

java类加载机制 jvm spec

load  link 初始化   Initializing

https://blog.csdn.net/m0_38075425/article/details/81627349

### 1.Loading

```
	类加载器通过双亲委派机制将类的class文件载入内存
```

### 2.Linking

```
	1）Verification:检验载入的class文件是否符合jvm的规范格式
	2）Preparation: 为类的静态变量申请内存并赋默认值（注：默认值不是初始值，并且此时对象的内存还未申请）
	3）Resolution:解析阶段。将二进制文件中的类、方法、属性等符号引用解析为直接引用（成员属性的变量名或空引用等，如int i;Object o；），将常量池中的各种符号引用解析为指针、偏移量等内存地址的直接引用。
```

### 3.Initializing

```
	1）初始化静态成员变量
	2）执行静态代码块
```

mysql index page block

平安面试 必须要离职的，俗称捡漏