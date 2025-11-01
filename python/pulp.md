# pulp

PuLP是用于线性规划（LP）、整数线性规划（ILP）和混合整数线性规划（MILP）的Python库，支持通过MPS或LP文件调用多种求解器（如GLPK、COIN CLP/CBC、CPLEX、GUROBI等）。 

## 官网
http://coin-or.github.io/pulp/

## 开源协议
Copyright (c) 2002-2005, Jean-Sebastien Roy
Modifications Copyright (c) 2007- Stuart Anthony Mitchell

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## 源代码
https://github.com/coin-or/pulp

## 版本version

3.3.0 2025.09.18
3.2.2 2025 8 6
2.8.0 Jan 17, 2024
2.7.0 Nov 3, 2022
2.6.0 Dec 5, 2021

## 邮件讨论组

## 例子
https://github.com/edidada/OrToolsProject/

git clone https://github.com/coin-or/pulp.git
cd pulp
git checkout 3.3.0
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install --group=dev --editable .
