org.springframework.beans.factory
BeanFactory
 
bean的配置

<bean  name="user" class="top.edidada.springday01.bean.User" ></bean>


一、id 不可以重复
二、name 可以重复，实际项目中没有意义 可以含有特殊字符

创建bean的三种方式
1、普通
2、静态工厂
3、实例工厂


#{}

spel

基于注解的bean IoC方式
@Component
@Controller
@Respository

@Resource