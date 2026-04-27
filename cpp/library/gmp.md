# GMP
GMP = C 语言库
API = 纯 C API

### GMP 官方开源地址（权威）
GMP（GNU Multiple Precision Arithmetic Library）官方用 Mercurial 管理，非 Git；另有 GitHub 镜像。

#### 1. 官方仓库（Mercurial）
- 主仓库：https://gmplib.org/repo/gmp/
- 开发页：https://gmplib.org/devel/

#### 2. GitHub 镜像（Git，国内访问快）
- 镜像：https://github.com/ncw/gmp

#### 3. 官方下载页（稳定版）
- https://gmplib.org/#DOWNLOAD
- 当前稳定版：6.3.0（2023-07-30）

#### 4. GNU 主站归档
- https://ftp.gnu.org/gnu/gmp/

### 拉取代码示例
Mercurial（官方）
```bash
hg clone https://gmplib.org/repo/gmp/
```

Git（GitHub 镜像）
```bash
git clone https://github.com/ncw/gmp.git
```

需要我补充GMP在macOS的编译安装步骤和C++金额运算示例吗？

# macOS 12.7 (Monterey) + Homebrew 安装 GMP 最简教程
你的系统 macOS 12.7（Monterey） + Homebrew 安装 gmp 超级简单，一条命令搞定！

## 一、安装命令（直接复制运行）
```bash
brew install gmp
```

## 二、验证是否安装成功
```bash
brew info gmp
```
显示版本、路径就说明成功。

## 三、查看安装位置（C/C++ 编译需要）
```bash
ls /usr/local/Cellar/gmp/
```
默认路径：
```
/usr/local/Cellar/gmp/6.2.1_1/
```
- 头文件：`/usr/local/include`
- 库文件：`/usr/local/lib`

## 四、C/C++ 编译时链接 GMP
```bash
gcc test.c -o test -lgmp
```

```bash
g++ test.cpp -o test -lgmp
```

## 如果你之前安装失败 / 找不到包，执行这 3 条修复
```bash
brew update
brew doctor
brew install gmp
```

# 我可以直接给你一段 C++ 金额计算（BigDecimal 等价）GMP 示例代码
你要吗？可以直接编译运行。
