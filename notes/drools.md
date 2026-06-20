# drools

#### 基础语法



黑马博学谷2020年最新Java项目Drools业务规则管理系统（BRMS）


https://github.com/HappySnailSunshine/JavaInterview/blob/master/docs/Drools.md



https://www.drools.org/



GitHub testdrools repo





Try the examples now

1. Download the zip and unzip it
2. On Linux/Mac, run `examples/runExamples.sh`
   On Windows, run `examples/runExamples.bat`






jboss
drtools

复杂企业级项目的开发以及其中随外部条件不断变化的业务规则(business logic),迫切需要分离商业决策者的商业决策逻辑和应用开发者的技术决策，并把这些商业决策放在中心数据库或其他统一的地方，让它们能在运行时（即商务时间）可以动态地管理和修改从而提供软件系统的柔性和适应性。规则正是应用于上述动态环境中的一种解决方法。
https://cloud.tencent.com/developer/article/1031839
规则引擎-BRMS在企业开发中的应用	

规则引擎实现了将业务决策从应用程序代码中分离出来，并使用预定义的语义模块编写业务决策。
规则引擎具体执行可以分为接受数据输入，解释业务规则，根据业务规则做出业务决策几个过程，使用规则引擎可以把复杂、
冗余的业务规则同整个支撑系统分离开，做到架构的可复用移植。
https://www.cnblogs.com/binyue/p/6774903.html

目前版本是5.0.1，Drools从5.0后分为四个模块：

Drools Guvnor (BRMS/BPMS)
Drools Expert (rule engine)
Drools Flow (process/workflow)
Drools Fusion (cep/temporal reasoning)

https://github.com/kiegroup/drools

轻量级规则引擎Easy Rules
Easy Rules官方主页：http://www.easyrules.org/
Easy Rules提供以下功能：
轻量级框架和易于学习的API
基于POJO的开发
通过高效的抽象来定


规则引擎由推理引擎发展而来，是一种嵌入在应用程序中的组件，实现了将业务决策从应用程序代码中分离出来，并使用预定义的语义模块编写业务决策。接受数据输入，解释业务规则，并根据业务规则做出业务决策，一个好的规则引擎能大大提高系统的灵活性，扩展性。
https://zhuanlan.zhihu.com/p/267785532
https://blog.csdn.net/ityouknow/article/details/76803412
https://blog.csdn.net/ityouknow/article/details/76803412


https://blog.csdn.net/huxiangen/article/details/81772107

如何学习一个新的java库/框架

有没有官方文档 readme
跑turial examples
依赖哪些三方框架
mail list 开发者 用户
git issues

技术层面 分析 Java标准库提供的 class jvm扩展
使用场景 
竞品分析
互联网大厂有没有在qcon
gt 大会分享

```shell script
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/edidada/testdrools.git
git push -u origin main
```

## jar包
drools-compiler
drools-core

### idea插件
.drl

语法类似java
package
rule

### 规则引擎
使用场景

https://zhuanlan.zhihu.com/p/140916822
金融风控





支付系统账务系统 《支付系统架构》

https://blog.csdn.net/zghmnb/article/details/62892835



一个简单的使用demo，这里我们主要用到Drools Expert 部分。

业务场景：模拟清算对账
输入数据源：零花钱流水对账数据、快钱渠道对账数据，执行业务规则，输出平账数据、对账差异数据

零花钱流水对账数据实体类

precheck.drl

```drl
package rules;
dialect  "java"
import com.shinyleo.drools.mode.AccountOrder;
import com.shinyleo.drools.mode.BIll99Order;

global java.util.List successCheckList;


//元数据定义
declare SuccessData
   orderId :Long
   checkresult:String
   checkStatus:int
    amount:Long
    status:int
end



rule "precheck"
    salience 100
    when
       $accountOrder : AccountOrder(checkStatus == 0 ,$transAmount:transAmount,$orderId:orderId,$status:orderStatus)
       $bill99Order : BIll99Order(checkStatus == 0,outerOrderId == $orderId,amount == $transAmount,orderStatus == $status)
    then
      System.out.println("-----start rules-----" + $accountOrder.getOrderId());
      $accountOrder.setCheckStatus(1); //标记为对平
      $bill99Order.setCheckStatus(1);
      update($accountOrder);
      update($bill99Order);
      //获取平账数据
      SuccessData successData = new SuccessData();
      successData.setAmount($transAmount);
      successData.setCheckresult("平账");
      successData.setOrderId($orderId);
      //insertLogical(successData);
      insert(successData);
      //返回
      successCheckList.add(successData);
end

rule "successData"
  when
      SuccessData(checkStatus == 1);
  then
     System.out.println("success increase 1 ..." );
end

query "successList"
   // 找出对平的数据
   successData:AccountOrder(checkStatus == 1)
end

query "errorList"
   // 找出还未对平的数据
   errorData:AccountOrder(checkStatus == 0)

end

query "queryOrder" (int $status,Long $orderId)
   // 找出还未对平的数据
   queryOrder:AccountOrder(checkStatus == $status,orderId == $orderId)
end
```





https://gitee.com/dream21th/drools-study/tree/master/drools-springboot