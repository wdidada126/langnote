# spel


```java
@Test
public void test(){
	ExpressionParser parser =new SpelExpressionParser();
	assertThat(parser.parseExpression("3 between {2,5}").getValue(Boolean.class), is(true));
}

@Test
	public void test(){
		ExpressionParser parser =new SpelExpressionParser();
		assertThat(parser.parseExpression("35 matches '[0-9]+'").getValue(Boolean.class), is(true));
	}


public class TestSpEL {
	@Test
	public void test(){
		ExpressionParser parser =new SpelExpressionParser();
		StandardEvaluationContext context =new StandardEvaluationContext();
		context.setRootObject(new Var());
		Assert.assertTrue(parser.parseExpression("#root").getValue(context) instanceof Var);
	}
}


public class TestSpEL {
	@Test
	public void test(){
		ExpressionParser parser =new SpelExpressionParser();
		StandardEvaluationContext context =new StandardEvaluationContext();
		context.setVariable("message", "Hello World");
		String value =parser.parseExpression("#message").getValue(context, String.class);
		assertThat(value, is("Hello World"));
	}
}

@Test
public void test(){
	ExpressionParser parser =new SpelExpressionParser();
	Expression exp=parser.parseExpression("T(java.lang.Math).abs(-1)");
	Integer value =exp.getValue(Integer.class);
	assertThat(value ,is(1));
}


@Test
public void test(){
	ExpressionParser parser =new SpelExpressionParser();
	Expression exp=parser.parseExpression("new Double(3.1415926)");
	Double value =exp.getValue(Double.class);
	assertThat(value ,is(3.1415926));
}



@Component
public class MyMessage2 {
	
	@Value("#{systemProperties['user.language']}")
	private String message;
 
	public String getMessage() {
		return message;
	}
}




<bean id="MyMessage" class="cn.spy.spel.injection.MyMessage">
        <property name="message" value="#{systemProperties['user.language']}"></property>
</bean>

```


SpEL提供了多种运算符。

类型
运算符
关系
        <，>，<=，>=，==，!=，lt，gt，le，ge，eq，ne
算术
       +，- ，* ，/，%，^
逻辑
       &&，||，!，and，or，not，between，instanceof
条件
       ?: (ternary)，?: (elvis)
正则表达式
       matches
其他类型
       ?.，?[…]，![…]，^[…]，$[…]


https://blog.csdn.net/ya_1249463314/article/details/68484422