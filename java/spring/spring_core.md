# spring_core

org.springframework.core.xlsx



AnnotationAttributes



| AliasRegistry                                           | interface | "void registerAlias(String name, String alias)                    |
|---------------------------------------------------------|-----------|-------------------------------------------------------------------|
| void removeAlias(String alias)"                         |
| AttributeAccessor                                       | interface |                                                                   |
| AttributeAccessorSupport                                | abstract  |                                                                   |
| BridgeMethodResolver                                    |           | final类，一堆static方法                                                 |
| CollectionFactory                                       |           | final类，有两个map属性，工具类，创建map，list的                                   |
| ConfigurableObjectInputStream                           |           |                                                                   |
| Constants                                               |           |                                                                   |
| Constants.ConstantException                             |           |                                                                   |
| Conventions                                             |           |                                                                   |
| CoroutinesUtils                                         |           |                                                                   |
| DecoratingClassLoader                                   | abstract  | "Set<String> excludedPackages                                     |
| Set<String> excludedClasses"                            |
| DecoratingProxy                                         | interface | Class<?> getDecoratedClass()                                      |
| DefaultParameterNameDiscoverer                          |           | extends PrioritizedParameterNameDiscoverer                        |
| ExceptionDepthComparator                                |           |                                                                   |
| GenericTypeResolver                                     |           |                                                                   |
| InfrastructureProxy                                     | interface | Object getWrappedObject()                                         |
| KotlinDetector                                          |           |                                                                   |
| KotlinReflectionParameterNameDiscoverer                 |           |                                                                   |
| LocalVariableTableParameterNameDiscoverer               |           | 工具类，用于获取方法参数的名称。                                                  |
| MethodClassKey                                          |           | final class MethodClassKey implements Comparable<MethodClassKey>  |
| MethodIntrospector                                      |           |                                                                   |
| MethodIntrospector.MetadataLookup<T>                    |           |                                                                   |
| MethodParameter                                         |           | getParameterType()方法                                              |
| NamedInheritableThreadLocal<T>                          |           |                                                                   |
| NamedThreadLocal<T>                                     |           |                                                                   |
| NativeDetector                                          |           |                                                                   |
| NestedCheckedException                                  | exception |                                                                   |
| NestedExceptionUtils                                    |           |                                                                   |
| NestedRuntimeException                                  | exception |                                                                   |
| OrderComparator                                         |           | 工具类，用于对实现了 Ordered 接口的对象进行排序。                                     |
| OrderComparator.OrderSourceProvider                     |           |                                                                   |
| Ordered                                                 | interface | int getOrder()                                                    |
| OverridingClassLoader                                   |           |                                                                   |
| ParameterizedTypeReference<T>                           | interface |                                                                   |
| ParameterNameDiscoverer                                 | interface | "String[] getParameterNames(Method method)                        |
| String[] getParameterNames(Constructor<?> ctor)"        |
| PrioritizedParameterNameDiscoverer                      |           | 实现了ParameterNameDiscoverer                                        |
| PriorityOrdered                                         |           | PriorityOrdered extends Ordered                                   |
| ReactiveAdapter                                         |           | 5.0才有                                                             |
| ReactiveAdapterRegistry                                 |           | 5.0才有                                                             |
| ReactiveAdapterRegistry.SpringCoreBlockHoundIntegration |           |                                                                   |
| ReactiveTypeDescriptor                                  |           | 5.0才有                                                             |
| ResolvableType                                          |           |                                                                   |
| ResolvableTypeProvider                                  | interface |                                                                   |
| SimpleAliasRegistry                                     |           | implements AliasRegistry                                          |
| SmartClassLoader                                        | interface |                                                                   |
| SpringProperties                                        |           |                                                                   |
| SpringVersion                                           |           | getVersion()方法返回 5.2.9.RELEASE                                    |
| StandardReflectionParameterNameDiscoverer               |           |                                                                   |



| org.springframework.asm                |      |      |
| -------------------------------------- | ---- | ---- |
|                                        |      |      |
| Interfaces                             |      |      |
|                                        |      |      |
| Opcodes                                |      |      |
|                                        |      |      |
| Classes                                |      |      |
|                                        |      |      |
| AnnotationVisitor                      |      |      |
| Attribute                              |      |      |
| ByteVector                             |      |      |
| ClassReader                            |      |      |
| ClassVisitor                           |      |      |
| ClassWriter                            |      |      |
| ConstantDynamic                        |      |      |
| FieldVisitor                           |      |      |
| Handle                                 |      |      |
| Label                                  |      |      |
| MethodVisitor                          |      |      |
| ModuleVisitor                          |      |      |
| RecordComponentVisitor                 |      |      |
| SpringAsmInfo                          |      |      |
| Type                                   |      |      |
| TypePath                               |      |      |
| TypeReference                          |      |      |
|                                        |      |      |
| Exceptions                             |      |      |
|                                        |      |      |
| ClassTooLargeException                 |      |      |
| MethodTooLargeException                |      |      |
|                                        |      |      |
|                                        |      |      |
|                                        |      |      |
|                                        |      |      |
|                                        |      |      |
| org.springframework.cglib              |      |      |
|                                        |      |      |
| Classes                                |      |      |
|                                        |      |      |
| SpringCglibInfo                        |      |      |
|                                        |      |      |
| org.springframework.cglib.beans        |      |      |
|                                        |      |      |
| Classes                                |      |      |
|                                        |      |      |
| BeanCopier                             |      |      |
| BeanCopier.Generator                   |      |      |
| BeanGenerator                          |      |      |
| BeanMap                                |      |      |
| BeanMap.Generator                      |      |      |
| BulkBean                               |      |      |
| BulkBean.Generator                     |      |      |
| FixedKeySet                            |      |      |
| ImmutableBean                          |      |      |
| ImmutableBean.Generator                |      |      |
|                                        |      |      |
| Exceptions                             |      |      |
|                                        |      |      |
| BulkBeanException                      |      |      |
|                                        |      |      |
|                                        |      |      |
|                                        |      |      |
| org.springframework.cglib.core         |      |      |
|                                        |      |      |
| Classes                                |      |      |
|                                        |      |      |
| AbstractClassGenerator                 |      |      |
| AbstractClassGenerator.ClassLoaderData |      |      |
| AbstractClassGenerator.Source          |      |      |
| ClassLoaderAwareGeneratorStrategy      |      |      |
| KeyFactory                             |      |      |
| KeyFactory.Generator                   |      |      |
| ReflectUtils                           |      |      |
| SpringNamingPolicy                     |      |      |
|                                        |      |      |
|                                        |      |      |
|                                        |      |      |
| org.springframework.cglib.proxy        |      |      |
|                                        |      |      |
|                                        |      |      |
| Interfaces                             |      |      |
|                                        |      |      |
| Enhancer.EnhancerKey                   |      |      |
|                                        |      |      |
| Classes                                |      |      |
|                                        |      |      |
| Enhancer                               |      |      |
| MethodProxy                            |      |      |
|                                        |      |      |
|                                        |      |      |
|                                        |      |      |
|                                        |      |      |
|                                        |      |      |
| org.springframework.lang               |      |      |
|                                        |      |      |
| Annotation Types                       |      |      |
|                                        |      |      |
| NonNull                                |      |      |
| NonNullApi                             |      |      |
| NonNullFields                          |      |      |
| Nullable                               |      |      |
| UsesJava7                              |      |      |
| UsesJava8                              |      |      |
| UsesSunHttpServer                      |      |      |
| UsesSunMisc                            |      |      |



