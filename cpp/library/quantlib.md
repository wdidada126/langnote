# quantlib

## 功能
量化的
能计算投资标的的内部收益率吗？

## example
testquantlib

## doc
https://www.cnblogs.com/xuruilong100/p/8711520.html
《QuantLib 金融计算》系列
QuantLib 入门
基本组件之 Date 类
基本组件之 Calendar 类
基本组件之 DayCounter 类
基本组件之 DateGeneration 类
基本组件之 Schedule 类
基本组件之天数计算规则详解
基本组件之 Index 类
基本组件之 InterestRate 类
基本组件之 Currency 类
基本组件之 Money 类
基本组件之 ExchangeRate 类
基本组件之 ExchangeRateManager 类
数学工具之数值积分
数学工具之求解器
数学工具之插值
数学工具之优化器
数学工具之随机数发生器
随机过程之概述
随机过程之一般 Black Scholes 过程
随机过程之 Heston 过程
修复 BatesProcess 中的两个 Bug
高级话题之模拟跳扩散过程
案例之普通欧式期权分析
收益率曲线之构建曲线（1）
收益率曲线之构建曲线（2）
收益率曲线之构建曲线（3）
收益率曲线之构建曲线（4）
收益率曲线之构建曲线（5）
自己动手封装 Python 接口（1）
自己动手封装 Python 接口（2）
自己动手封装 Python 接口（3）
案例之普通利率互换分析（1）
案例之普通利率互换分析（2）
案例之普通利率互换分析（3）
C++ 代码改写成 Python 程序的一些经验
案例之固息债的价格、久期、凸性和 BPS
案例之固息债的关键利率久期（KRD）
案例之浮息债（挂钩 LPR）的价格、久期和凸性
一个使用 ActualActual 时需要注意的陷阱
案例之 KRD、Fisher-Weil 久期及久期的解释能力
案例之主成分久期（PCD）
原理之 Bootstrap
原理之利率互换的分析
原理之蒙特卡洛（Monte Carlo）
一个线程安全隐患
原理之有限差分法（FDM）

### QuantLib 库介绍

QuantLib 是一个免费开源的 C++ 库，专为量化金融（quantitative finance）设计，用于金融工具定价、风险管理、建模和交易模拟。它支持多种资产类别（如利率衍生品、期权、债券、股票等），并提供Python、Excel 等绑定接口。库的核心优势在于其模块化设计、跨平台兼容性和社区驱动开发，已被银行、研究机构和软件公司广泛使用。项目始于2000年，由Ferdinando Ametrano、Luigi Ballabio 等量化分析师发起，目前由Luigi Ballabio领导维护。QuantLib的最新版本（截至 2025 年）为1.40，支持现代C++标准和多曲线引导等高级功能。

QuantLib 的文档、书籍和论文资源丰富，涵盖从入门教程到高级实现。以下按类别分类介绍主要资源（基于官方站点和学术出版物）。这些资源可帮助开发者、分析师和研究者快速上手或深入扩展库。

#### 1. 官方文档（Documentation）
QuantLib 的文档以参考手册和教程为主，免费在线可用。核心入口是官方网站的文档页面。

| 资源名称 | 描述 | 链接/格式 | 适用人群 |
|----------|------|-----------|----------|
|  QuantLib 官方文档  | 全面参考手册，包括类层次、API 描述、安装指南和示例。涵盖日期处理、利率曲线、期权定价等模块。 | [https://www.quantlib.org/docs.shtml](https://www.quantlib.org/docs.shtml)<br>HTML/PDF | 开发者与用户 |
|  QuantLib Python 绑定文档  | 专注于 Python 接口的对象构建和使用指南，包括数组、现金流、利率等基础概念。 | [https://quantlib-python-docs.readthedocs.io/](https://quantlib-python-docs.readthedocs.io/)<br>ReadTheDocs | Python 用户 |
|  QuantLib 用户指南与参考  | GitHub 仓库中的设计文档、变更历史和贡献指南。 | [https://github.com/lballabio/QuantLib](https://github.com/lballabio/QuantLib)<br>Markdown/HTML | 贡献者 |
|  QuantLib Notebooks  | Luigi Ballabio 的 Jupyter Notebook 系列视频和示例，演示库功能（如多曲线引导）。 | [QuantLib 官网 Screencasts](https://www.quantlib.org/docs.shtml)<br>Jupyter/Video | 初学者 |
|  Introduction to QuantLib  | Felix Lee 的安装与基础使用视频系列。 | [YouTube 系列](https://www.quantlib.org/docs.shtml)<br>Video | 新手 |

这些文档强调实际应用，如 Black-Scholes 模型实现和蒙特卡洛模拟。

#### 2. 书籍（Books）
QuantLib 的书籍多由核心开发者 Luigi Ballabio 撰写，聚焦实际编码和架构。多数通过 Leanpub 提供电子版，支持免费更新。

| 书籍名称 | 作者/编者 | 描述 | 格式/获取 | 适用人群 |
|----------|----------|------|-----------|----------|
|  A QuantLib Guide  | Luigi Ballabio | 教程式指南，填补库使用文档空白。覆盖基础到高级主题，如仪器定价和扩展库。包含博客/Wilmott 杂志更新内容。 | [Leanpub 电子书](https://leanpub.com/quantlibguide)<br>[免费 HTML](https://www.quantlibguide.com/)<br>PDF/Kindle | 用户与初学者 |
|  Implementing QuantLib  | Luigi Ballabio | 深入库架构设计，针对扩展库（如自定义仪器/模型）的开发者。讨论类层次、框架和最佳实践。 | [Leanpub 电子书](https://leanpub.com/implementingquantlib)<br>[Amazon 平装](https://www.amazon.com/Implementing-QuantLib-Quantitative-finance-architecture/dp/B08KHSZK86)<br>PDF/Paperback | 高级开发者 |
|  QuantLib Python Cookbook  | Luigi Ballabio 等 | Jupyter Notebook 示例合集，展示库功能（如期权定价、多利率曲线）。包含 Ametrano-Bianchetti 论文结果重现。 | [Leanpub 电子书](https://leanpub.com/quantlibpythoncookbook)<br>PDF/iPad/Kindle | Python 量化分析师 |
|  C++ Design Patterns and Derivatives Pricing  | Mark Joshi | 虽非专论 QuantLib，但使用库示例解释设计模式在衍生品定价中的应用。 | 商业出版<br>PDF/Print | 架构爱好者 |

这些书籍强调“动手编码”，如用 QuantLib 实现 LMM（Libor Market Model）校准。

#### 3. 论文（Papers）
QuantLib 常用于学术研究，许多论文直接引用库实现复杂模型。以下是关键论文列表（选自官方文档），聚焦库应用在利率曲线、多曲线引导和校准等主题。

| 论文标题 | 作者 | 出版信息 | 摘要/焦点 | 获取 |
|----------|------|----------|-----------|------|
|  Bootstrapping the Illiquidity: Multiple Yield Curves Construction for Market Coherent Forward Rates Estimation  | Ferdinando Ametrano, Marco Bianchetti | *Modelling Interest Rates*, ed. Fabio Mercurio, Risk Books, 2009 | 使用 QuantLib 构建多收益率曲线，实现市场一致的前向利率估计。 | [SSRN 摘要](https://ssrn.com/abstract=1371311) |
|  Smooth Simultaneous Calibration of the LMM to Caplets and Coterminal Swaptions  | Ferdinando Ametrano, Mark S. Joshi | *Quantitative Finance*, vol. 11(4), pp. 547-558, 2011 | QuantLib 在 LMM（Libor Market Model）平滑校准中的应用，针对 caplets 和 swaptions。 | [SSRN 下载](https://ssrn.com/abstract=1092665) |
|  Farmer's CMS Spread Option Formula for Negative Rates  | Peter Caspers | SSRN, 2015 | 扩展 QuantLib 处理负利率下的 CMS Spread 期权定价。 | [SSRN 下载](https://ssrn.com/abstract=2686998) |
|  Derivatives Pricing using QuantLib: An Introduction  | Daniel J. Duffy | Wilmott Magazine, 2018 | QuantLib 在衍生品定价的入门应用，包括 C++11 互操作性。 | [Wilmott 摘要](https://doi.org/10.1002/wilm.10692) |
|  Software Interoperability in Computational Finance, Part I: Foundations for Applications Using C++11 and C# in the .NET Framework  | Daniel J. Duffy, Mikael Katajamäki | Wilmott Magazine, July 2018 | QuantLib 与 .NET 框架的集成，用于计算金融。 | [DOI 下载](https://doi.org/10.1002/wilm.10692) |
|  A Parallel Package to Evaluate Financial Options  | Francesca Mariani 等 | HPCwire, September 2009 | QuantLib 的并行实现，用于高性能期权评估。 | [HTML 全文](https://www.quantlib.org/docs.shtml) |

这些论文多发表于 *Quantitative Finance* 和 *Wilmott Magazine*，证明 QuantLib 在学术界的实用性。更多论文可在 SSRN 或 Google Scholar 搜索 "QuantLib"。

#### 总结与建议
QuantLib 的资源生态以 Luigi Ballabio 的作品为核心，结合官方文档和社区论文，形成完整学习路径：
-  入门 ：从 *A QuantLib Guide* 和官方文档开始。
-  实践 ：用 *QuantLib Python Cookbook* 的 Notebook 示例。
-  高级 ：阅读 *Implementing QuantLib* 和相关论文扩展模型。

社区支持包括 GitHub issue、quantlib-users 邮件列表（[订阅](https://www.quantlib.org/mailinglists.shtml)）。如果需要特定主题（如利率衍生品）的深入资源，或代码示例，欢迎提供更多细节！

## 功能
https://www.quantlib.org/reference/index.html

## 官网
https://www.quantlib.org/
## 源代码
https://github.com/lballabio/QuantLib

## 源代码版本
v1.40 2025.10
v1.32 Oct 19, 2023
QuantLib-v1.25 Jan 17, 2022
## 源代码编译

# 1. 安装编译依赖
sudo apt update
sudo apt install -y build-essential libboost-all-dev

# 2. 下载 QuantLib 源码
wget https://github.com/lballabio/QuantLib/releases/download/QuantLib-v1.31/QuantLib-1.31.tar.gz

# 3. 解压并编译
tar -xzf QuantLib-1.31.tar.gz
cd QuantLib-1.31

# 4. 配置编译选项
./configure --prefix=/usr/local

# 5. 编译并安装
make -j$(nproc)
sudo make install

# 6. 更新动态链接库缓存
sudo ldconfig

# 7. 验证安装
pkg-config --modversion QuantLib

以下是用于贷后管理、房贷每月还款金额计算的开源库，涵盖C、C++、Java语言：

## 一、Java 开源库

### 1.  Apache Commons Math 
 最推荐 的Java数学计算库，包含完整的金融计算功能。

```xml
<!-- Maven 依赖 -->
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-math3</artifactId>
    <version>3.6.1</version>
</dependency>
```

 代码示例： 
```java
import org.apache.commons.math3.analysis.function.*;
import java.math.BigDecimal;
import java.math.RoundingMode;

public class MortgageCalculator {
    
    / 
     * 计算等额本息每月还款额
     * @param principal 贷款本金
     * @param annualRate 年利率（如0.05表示5%）
     * @param years 贷款年限
     * @return 每月还款额
     */
    public static BigDecimal calculateEqualPrincipalAndInterest(double principal, 
                                                               double annualRate, 
                                                               int years) {
        double monthlyRate = annualRate / 12; // 月利率
        int totalMonths = years * 12; // 总月数
        
        // 等额本息公式：每月还款额 = [本金×月利率×(1+月利率)^还款月数] ÷ [(1+月利率)^还款月数-1]
        double temp = Math.pow(1 + monthlyRate, totalMonths);
        double monthlyPayment = principal * monthlyRate * temp / (temp - 1);
        
        return BigDecimal.valueOf(monthlyPayment).setScale(2, RoundingMode.HALF_UP);
    }
    
    / 
     * 计算等额本金每月还款额
     * @param principal 贷款本金
     * @param annualRate 年利率
     * @param years 贷款年限
     * @return 每月还款明细列表
     */
    public static void calculateEqualPrincipal(double principal, double annualRate, int years) {
        double monthlyRate = annualRate / 12;
        int totalMonths = years * 12;
        double monthlyPrincipal = principal / totalMonths; // 每月归还本金
        
        System.out.println("等额本金还款计划:");
        System.out.println("期次\t月还本金\t月还利息\t月还款额\t剩余本金");
        
        double remainingPrincipal = principal;
        for (int i = 1; i <= totalMonths; i++) {
            double monthlyInterest = remainingPrincipal * monthlyRate;
            double totalMonthly = monthlyPrincipal + monthlyInterest;
            remainingPrincipal -= monthlyPrincipal;
            
            System.out.printf("%d\t%.2f\t%.2f\t%.2f\t%.2f\n", 
                i, monthlyPrincipal, monthlyInterest, totalMonthly, 
                Math.max(0, remainingPrincipal));
        }
    }
    
    / 
     * 使用Apache Commons Math进行精确计算
     */
    public static BigDecimal calculateWithApacheMath(double principal, double annualRate, int years) {
        double monthlyRate = annualRate / 12;
        int totalMonths = years * 12;
        
        // 使用精确的幂计算
        double temp = new Pow().value(1 + monthlyRate, totalMonths);
        double monthlyPayment = principal * monthlyRate * temp / (temp - 1);
        
        return BigDecimal.valueOf(monthlyPayment).setScale(2, RoundingMode.HALF_UP);
    }
    
    public static void main(String[] args) {
        double principal = 1000000; // 100万贷款
        double annualRate = 0.05;   // 5%年利率
        int years = 30;              // 30年
        
        BigDecimal monthlyPayment = calculateEqualPrincipalAndInterest(principal, annualRate, years);
        System.out.println("等额本息月供: " + monthlyPayment + "元");
        
        calculateEqualPrincipal(principal, annualRate, years);
    }
}
```

### 2.  JFin （专门金融计算库）
专门为金融计算设计的Java库。

```java
// 需要自行下载或实现核心算法
public class JFinMortgageCalculator {
    
    public static class LoanTerms {
        private double principal;
        private double annualRate;
        private int years;
        
        // 构造函数、getter、setter
    }
    
    public static class PaymentSchedule {
        private int period;
        private double principalPayment;
        private double interestPayment;
        private double remainingBalance;
        
        // getter、setter
    }
    
    public static List<PaymentSchedule> generateSchedule(LoanTerms terms) {
        List<PaymentSchedule> schedule = new ArrayList<>();
        // 实现还款计划生成逻辑
        return schedule;
    }
}
```

## 二、C++ 开源库

### 1.  QuantLib （推荐）
 金融计算的标准库 ，功能非常强大。

```cpp
#include <ql/quantlib.hpp>
#include <iostream>
#include <iomanip>

using namespace QuantLib;

void calculateMortgage() {
    // 贷款参数
    Real principal = 1000000.0;    // 贷款金额
    Rate annualRate = 0.05;        // 年利率
    Integer years = 30;           // 贷款年限
    Integer months = years * 12;   // 总期数
    
    // 设置计算日期
    Date settlementDate(15, January, 2024);
    Settings::instance().evaluationDate() = settlementDate;
    
    // 创建利率对象
    InterestRate rate(annualRate, Actual360(), Compounded, Monthly);
    
    // 计算等额本息月供
    Real monthlyPayment = principal * rate.discountFactor(months) / 
                         (1.0 - std::pow(1.0 + annualRate/12, -months));
    
    std::cout << "贷款金额: " << principal << "元" << std::endl;
    std::cout << "年利率: " << annualRate * 100 << "%" << std::endl;
    std::cout << "贷款期限: " << years << "年" << std::endl;
    std::cout << "月供: " << std::fixed << std::setprecision(2) 
              << monthlyPayment << "元" << std::endl;
    
    // 生成还款计划表
    std::cout << "\n还款计划表:" << std::endl;
    std::cout << "期次\t月供\t本金\t利息\t剩余本金" << std::endl;
    
    Real remainingPrincipal = principal;
    for (int i = 1; i <= months; ++i) {
        Real interest = remainingPrincipal * annualRate / 12;
        Real principalPayment = monthlyPayment - interest;
        remainingPrincipal -= principalPayment;
        
        if (remainingPrincipal < 0) remainingPrincipal = 0;
        
        std::cout << i << "\t" << monthlyPayment << "\t" 
                  << principalPayment << "\t" << interest << "\t" 
                  << remainingPrincipal << std::endl;
    }
}

int main() {
    calculateMortgage();
    return 0;
}
```

 编译命令： 
```bash
g++ -std=c++11 mortgage.cpp -lQuantLib -o mortgage
```

### 2.  Boost.Math  工具包
```cpp
#include <boost/math/special_functions.hpp>
#include <iostream>

class MortgageCalculator {
public:
    static double calculateMonthlyPayment(double principal, double annualRate, int years) {
        double monthlyRate = annualRate / 12;
        int totalMonths = years * 12;
        
        double temp = boost::math::pow<long double>(1 + monthlyRate, totalMonths);
        return principal * monthlyRate * temp / (temp - 1);
    }
    
    static double calculateTotalInterest(double principal, double annualRate, int years) {
        double monthlyPayment = calculateMonthlyPayment(principal, annualRate, years);
        return monthlyPayment * years * 12 - principal;
    }
};

int main() {
    double principal = 1000000.0;
    double rate = 0.05;
    int years = 30;
    
    double monthly = MortgageCalculator::calculateMonthlyPayment(principal, rate, years);
    double totalInterest = MortgageCalculator::calculateTotalInterest(principal, rate, years);
    
    std::cout << "月供: " << monthly << std::endl;
    std::cout << "总利息: " << totalInterest << std::endl;
    
    return 0;
}
```

## 三、C 语言实现

### 1.  纯C数学计算 
```c
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

typedef struct {
    double principal;      // 贷款本金
    double annual_rate;    // 年利率
    int years;            // 贷款年限
    int payment_type;     // 还款方式：0-等额本息，1-等额本金
} LoanParams;

typedef struct {
    int period;           // 期数
    double principal_pay; // 本金
    double interest_pay;  // 利息
    double total_pay;     // 总额
    double remaining;     // 剩余本金
} PaymentRecord;

// 等额本息计算
double calculate_equal_installment(LoanParams params) {
    double monthly_rate = params.annual_rate / 12;
    int total_months = params.years * 12;
    
    double temp = pow(1 + monthly_rate, total_months);
    return params.principal * monthly_rate * temp / (temp - 1);
}

// 等额本金计算
void calculate_equal_principal(LoanParams params) {
    double monthly_rate = params.annual_rate / 12;
    int total_months = params.years * 12;
    double monthly_principal = params.principal / total_months;
    double remaining = params.principal;
    
    printf("期次\t月还本金\t月还利息\t月还款额\t剩余本金\n");
    
    for (int i = 1; i <= total_months; i++) {
        double interest = remaining * monthly_rate;
        double total = monthly_principal + interest;
        remaining -= monthly_principal;
        
        printf("%d\t%.2f\t\t%.2f\t\t%.2f\t\t%.2f\n", 
               i, monthly_principal, interest, total, remaining);
    }
}

// 生成完整还款计划
PaymentRecord* generate_payment_schedule(LoanParams params, int* total_records) {
    *total_records = params.years * 12;
    PaymentRecord* schedule = malloc(*total_records * sizeof(PaymentRecord));
    
    if (params.payment_type == 0) { // 等额本息
        double monthly_payment = calculate_equal_installment(params);
        double monthly_rate = params.annual_rate / 12;
        double remaining = params.principal;
        
        for (int i = 0; i < *total_records; i++) {
            double interest = remaining * monthly_rate;
            double principal_pay = monthly_payment - interest;
            
            schedule[i].period = i + 1;
            schedule[i].principal_pay = principal_pay;
            schedule[i].interest_pay = interest;
            schedule[i].total_pay = monthly_payment;
            schedule[i].remaining = remaining - principal_pay;
            
            remaining -= principal_pay;
        }
    } else { // 等额本金
        double monthly_principal = params.principal / (*total_records);
        double remaining = params.principal;
        
        for (int i = 0; i < *total_records; i++) {
            double interest = remaining * params.annual_rate / 12;
            double total = monthly_principal + interest;
            
            schedule[i].period = i + 1;
            schedule[i].principal_pay = monthly_principal;
            schedule[i].interest_pay = interest;
            schedule[i].total_pay = total;
            schedule[i].remaining = remaining - monthly_principal;
            
            remaining -= monthly_principal;
        }
    }
    
    return schedule;
}

int main() {
    LoanParams params = {
        .principal = 1000000.0,
        .annual_rate = 0.05,
        .years = 30,
        .payment_type = 0
    };
    
    int total;
    PaymentRecord* schedule = generate_payment_schedule(params, &total);
    
    printf("贷款计算报告\n");
    printf("贷款金额: %.2f元\n", params.principal);
    printf("年利率: %.2f%%\n", params.annual_rate * 100);
    printf("期限: %d年\n", params.years);
    printf("还款方式: %s\n", params.payment_type == 0 ? "等额本息" : "等额本金");
    printf("月供: %.2f元\n", schedule[0].total_pay);
    
    // 输出前12期还款计划
    printf("\n前12期还款计划:\n");
    printf("期次\t本金\t利息\t总额\t剩余本金\n");
    for (int i = 0; i < 12 && i < total; i++) {
        printf("%d\t%.2f\t%.2f\t%.2f\t%.2f\n",
               schedule[i].period, schedule[i].principal_pay,
               schedule[i].interest_pay, schedule[i].total_pay,
               schedule[i].remaining);
    }
    
    free(schedule);
    return 0;
}
```

 编译命令： 
```bash
gcc mortgage.c -lm -o mortgage
```

## 四、专门的开源金融计算库

### 1.  金融数学公式库对比 

| 库名称 | 语言 | 特点 | 适用场景 |
|--------|------|------|----------|
|  Apache Commons Math  | Java | 功能全面，文档完善 | 企业级应用，需要丰富数学函数 |
|  QuantLib  | C++/Python | 专业金融计算，行业标准 | 金融机构，复杂金融产品定价 |
|  Boost.Math  | C++ | 高性能，精度高 | 高性能计算，科学计算 |
|  NumPy/NumFinancial  | Python | 易用性好，生态丰富 | 数据分析，科学研究 |
|  自实现算法  | 任何语言 | 轻量，可控性强 | 简单应用，学习理解 |

### 2.  推荐选择建议 

-  企业级应用 ：选择  Apache Commons Math  (Java) 或  QuantLib  (C++)
-  学习研究 ：自实现算法，理解数学原理
-  高性能需求 ： QuantLib  或  Boost.Math 
-  快速开发 ：Python的  numpy-financial  包

这些库都提供了完整的房贷计算功能，可以根据项目需求和技术栈选择合适的解决方案。
