# eigen

https://www.zhihu.com/question/663853003/answer/3589211608

[C++]kalman filter 卡尔曼滤波器原理与基于Eigen库的实现


卡尔曼滤波器（Kalman Filter）原理
卡尔曼滤波器是一种高效的递归滤波器（自回归滤波器），它能够从一系列的包含统计噪声的测量中，估计动态系统的状态。它广泛应用于信号处理、控制理论、机器人技术、航空航天等领域。

基本原理
卡尔曼滤波器主要分为两个步骤：预测（Predict）和更新（Update）。

预测：使用前一时刻的估计值和已知的模型动态（如控制输入）来预测当前时刻的状态和协方差。
x
^
  
k∣k−1
 
P 
k∣k−1
 
  
=A 
x
^
  
k−1∣k−1
​
 +Bu 
k−1
​
 
=AP 
k−1∣k−1
 A 
T
 +Q
 
其中， 
x
^
  
k∣k−1
  是 k 时刻的预测状态，A 是状态转移矩阵，B 是控制输入矩阵，u 
k−1
​
  是控制输入，P 
k∣k−1
​
  是预测的协方差，Q 是过程噪声的协方差。

更新：结合预测值和新的测量值来更新状态估计和协方差。
K 
k
​
 
x
^
  
k∣k
​
 
P 
k∣k
​
 
​
  
=P 
k∣k−1
​
 H 
T
 (HP 
k∣k−1
​
 H 
T
 +R) 
−1
 
= 
x
^
  
k∣k−1
​
 +K 
k
​
 (z 
k
​
 −H 
x
^
  
k∣k−1
​
 )
=(I−K 
k
​
 H)P 
k∣k−1
​
 
​
 
其中，K 
k
​
  是卡尔曼增益，H 是观测矩阵，z 
k
​
  是 k 时刻的测量值，R 是测量噪声的协方差， 
x
^
  
k∣k
​
  是更新后的状态估计，P 
k∣k
​
  是更新后的协方差。

基于Eigen库的实现
Eigen 是一个高级的 C++ 库，用于线性代数、矩阵和向量运算，非常适合用于实现卡尔曼滤波器。

示例代码
以下是一个基于 Eigen 的简单卡尔曼滤波器实现框架：

```cpp
#include <eigen3/Eigen/Dense>
#include <iostream>

using namespace Eigen;
using namespace std;

class KalmanFilter {
public:
    MatrixXd A, B, H, Q, R, P;
    VectorXd x_hat, u;

    KalmanFilter(int state_size, int meas_size, int control_size)
            : A(MatrixXd::Identity(state_size, state_size)),
              B(MatrixXd::Zero(state_size, control_size)),
              H(MatrixXd::Zero(meas_size, state_size)),
              Q(MatrixXd::Identity(state_size, state_size) * 0.1),
              R(MatrixXd::Identity(meas_size, meas_size) * 1.0),
              P(MatrixXd::Identity(state_size, state_size) * 1.0),
              x_hat(VectorXd::Zero(state_size)),
              u(VectorXd::Zero(control_size)) {}

    void predict(const VectorXd &control) {
        u = control;
        x_hat = A * x_hat + B * u;
        P = A * P * A.transpose() + Q;
    }

    void update(const VectorXd &measurement) {
        VectorXd y = measurement - H * x_hat;
        MatrixXd S = H * P * H.transpose() + R;
        MatrixXd K = P * H.transpose() * S.inverse();

        x_hat = x_hat + K * y;
        P = (MatrixXd::Identity(P.rows(), P.cols()) - K * H) * P;
    }
};

int main() {
    KalmanFilter kf(2, 1, 1); // 假设有2个状态变量，1个测量变量，1个控制变量  

    // 初始化 Kalman 滤波器的矩阵
    kf.A << 1, 1, 0, 1;  // 状态转移矩阵
    kf.B << 0.5, 1.0;    // 控制矩阵
    kf.H << 1, 0;        // 测量矩阵

    // 假设的初始条件和控制输入  
    VectorXd z(1);
    z << 1.0;  // 假设的测量值

    VectorXd u(1);
    u << 0.1;  // 假设的控制输入

    // 进行预测和更新
    kf.predict(u);   // 预测步骤
    kf.update(z);    // 更新步骤

    // 打印结果
    cout << "Updated state: \n" << kf.x_hat << endl;
    cout << "Updated covariance: \n" << kf.P << endl;

    return 0;
}
```
