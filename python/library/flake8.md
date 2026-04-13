# flake8
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

Flake8 介绍
Flake8 是 Python 生态中最常用的代码静态分析工具，它整合了多个核心工具的功能，能帮你在运行代码前就发现语法错误、代码风格问题、潜在逻辑漏洞，是 Python 开发中保障代码质量的基础工具。
一、核心组成
Flake8 并非从零开发，而是整合了以下 3 个经典工具：
Pyflakes：检查代码中的语法错误、未定义 / 未使用的变量 / 导入、逻辑漏洞（比如 return 后的代码）。
pycodestyle（原 pep8）：检查代码是否符合 PEP 8 规范（Python 官方代码风格指南，比如行长度、缩进、空格使用等）。
McCabe：检测代码的圈复杂度（衡量代码逻辑复杂度，圈复杂度越高，代码越难维护）。
除此之外，Flake8 还支持通过插件扩展功能（比如检查 docstring 规范的 flake8-docstrings）。
二、核心作用
提前发现错误：比如漏写冒号、缩进错误、变量名拼写错误，避免运行时才暴露问题。
统一代码风格：团队协作时，强制遵循 PEP 8，避免每个人风格混乱。
降低维护成本：检测高复杂度代码，提醒你拆分函数 / 重构，让代码更易读、易维护。
三、安装与基础使用
1. 安装
通过 pip 即可快速安装：
bash
运行
# 基础安装
pip install flake8

# 安装常用插件（可选）
pip install flake8-docstrings  # 检查 docstring 规范
pip install flake8-import-order  # 检查导入顺序
2. 基础使用
在终端中执行，支持检查单个文件、整个目录：
bash
运行
# 检查单个文件
flake8 your_script.py

# 检查整个项目（当前目录及子目录）
flake8 .

# 只检查特定错误类型（比如只检查行长度超过88字符的问题）
flake8 --max-line-length=88 your_script.py
3. 输出示例
执行后，Flake8 会输出问题的位置和原因，格式如下：
plaintext
your_script.py:5:10: E225 missing whitespace around operator
your_script.py:12:5: F821 undefined name 'x'
your_script.py:20:1: C901 'calculate' is too complex (10)
前缀说明：
E/W：pycodestyle 的错误 / 警告（比如 E225 是运算符周围缺少空格）。
F：Pyflakes 的错误（比如 F821 是未定义的变量）。
C：McCabe 的圈复杂度警告（比如 C901 是函数复杂度超标）。
四、常用配置
如果不想每次执行都加命令行参数，可以在项目根目录创建配置文件（.flake8 或 setup.cfg），统一配置规则：
ini
[flake8]
# 每行最大长度（默认79，推荐88，适配 black 格式化工具）
max-line-length = 88
# 忽略特定错误（比如忽略行尾空格 W291、空行尾空格 W391）
ignore = W291,W391
# 排除不需要检查的目录/文件
exclude = 
    .git,
    __pycache__,
    venv,
    migrations
# 圈复杂度阈值（默认10）
max-complexity = 10
五、实际开发中的应用
本地开发：写代码后执行 flake8 自查，修复问题再提交。
Git 钩子：配合 pre-commit 工具，提交代码前自动执行 Flake8，拒绝不符合规范的代码提交。
CI/CD 流程：在持续集成（比如 GitHub Actions、GitLab CI）中加入 Flake8 检查，不通过则禁止合并代码。
总结
Flake8 是 Python 静态代码分析工具，整合了 Pyflakes、pycodestyle、McCabe，核心解决语法错误、PEP 8 规范、代码复杂度问题。
安装简单、使用灵活，可通过配置文件定制规则，适配团队开发需求。
是 Python 开发中保障代码质量的基础工具，建议结合 Git 钩子 / CI 流程落地使用。
