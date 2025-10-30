# quantlib

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

### 1. **Apache Commons Math**
**最推荐**的Java数学计算库，包含完整的金融计算功能。

```xml
<!-- Maven 依赖 -->
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-math3</artifactId>
    <version>3.6.1</version>
</dependency>
```

**代码示例：**
```java
import org.apache.commons.math3.analysis.function.*;
import java.math.BigDecimal;
import java.math.RoundingMode;

public class MortgageCalculator {
    
    /**
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
    
    /**
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
    
    /**
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

### 2. **JFin**（专门金融计算库）
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

### 1. **QuantLib**（推荐）
**金融计算的标准库**，功能非常强大。

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

**编译命令：**
```bash
g++ -std=c++11 mortgage.cpp -lQuantLib -o mortgage
```

### 2. **Boost.Math** 工具包
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

### 1. **纯C数学计算**
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

**编译命令：**
```bash
gcc mortgage.c -lm -o mortgage
```

## 四、专门的开源金融计算库

### 1. **金融数学公式库对比**

| 库名称 | 语言 | 特点 | 适用场景 |
|--------|------|------|----------|
| **Apache Commons Math** | Java | 功能全面，文档完善 | 企业级应用，需要丰富数学函数 |
| **QuantLib** | C++/Python | 专业金融计算，行业标准 | 金融机构，复杂金融产品定价 |
| **Boost.Math** | C++ | 高性能，精度高 | 高性能计算，科学计算 |
| **NumPy/NumFinancial** | Python | 易用性好，生态丰富 | 数据分析，科学研究 |
| **自实现算法** | 任何语言 | 轻量，可控性强 | 简单应用，学习理解 |

### 2. **推荐选择建议**

- **企业级应用**：选择 **Apache Commons Math** (Java) 或 **QuantLib** (C++)
- **学习研究**：自实现算法，理解数学原理
- **高性能需求**：**QuantLib** 或 **Boost.Math**
- **快速开发**：Python的 **numpy-financial** 包

这些库都提供了完整的房贷计算功能，可以根据项目需求和技术栈选择合适的解决方案。
