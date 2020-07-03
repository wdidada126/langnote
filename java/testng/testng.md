# Testng

```java

    @Test(expectedExceptions = ArithmeticException.class)
    public void divisionWithException() {
        int i = 1 / 0;
        System.out.println("After division the value of i is :"+ i);
    }

```



TestNG 覆盖 JUnit 功能，适用于更复杂的场景

[《JUnit 4 与 TestNG 对比》](https://blog.csdn.net/hotdust/article/details/53406086)

