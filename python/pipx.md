# pipx

简单说：
pipx = 专门用来安装「全局命令行工具」的 pip，而且自带独立虚拟环境，不污染系统 Python。

## 1. pipx 是干嘛的？
你平时用 `pip install xxx`：
- 装到系统或当前环境里
- 装多了容易版本冲突
- 很多库只是命令行工具，不是项目依赖

`pipx` 就是解决这个的：
- 专门安装命令行工具：`poetry`、`httpie`、`yt-dlp`、`ruff`、`jupyter` 等
- 每个工具自动创建独立虚拟环境，互不干扰
- 工具命令直接全局可用，不用切环境

## 2. 举个最典型的例子：安装 poetry
以前你可能：
```bash
pip install poetry
```
容易和系统库冲突。

用 pipx：
```bash
pipx install poetry
```
- 自动建虚拟环境
- `poetry` 命令全局能用
- 不污染任何项目环境

## 3. 和 pip、poetry 的区别
- pip：给当前项目/环境装库
- poetry：管理项目依赖 + 虚拟环境
- pipx：安装全局 CLI 工具，每个工具独立环境


## 4. 常用命令（记住这4个就够）
```bash
# 安装工具
pipx install 工具名

# 查看已装
pipx list

# 升级
pipx upgrade 工具名

# 卸载
pipx uninstall 工具名
```

### 一句话总结
你要在终端全局用的 Python 工具，就用 pipx 装；项目里用的库，用 poetry 装。