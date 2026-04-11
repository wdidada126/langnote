# poetry
poetry config repositories.default https://mirrors.aliyun.com/pypi/simple/
poetry config pypi-token.mirrors.aliyun.com ""


poetry config repositories.default https://pypi.org/simple/


python 工业级依赖管理工具

ibqo@ibqodeMBP test_python_toad % poetry install
Updating dependencies
Resolving dependencies... (6.6s)

Package operations: 23 installs, 0 updates, 0 removals

  - Installing numpy (1.25.2)
  - Installing contourpy (1.3.2)
  - Installing cycler (0.12.1)
  - Installing fonttools (4.62.1)
  - Installing kiwisolver (1.5.0)
  - Installing packaging (26.0)
  - Installing pillow (12.2.0)
  - Installing pyparsing (3.3.2)
  - Installing python-dateutil (2.9.0.post0)
  - Installing pytz (2026.1.post1)
  - Installing tzdata (2026.1)
  - Installing joblib (1.5.3)
  - Installing matplotlib (3.8.4)
  - Installing pandas (2.0.3)
  - Installing scipy (1.15.3)
  - Installing threadpoolctl (3.6.0)
  - Installing cython (3.2.4)
  - Installing et-xmlfile (2.0.0)
  - Installing scikit-learn (1.3.2)
  - Installing seaborn (0.13.2)
  - Installing setuptools (82.0.1)
  - Installing openpyxl (3.1.5)
  - Installing toad (0.1.5)

Writing lock file

Installing the current project: test-python-toad (0.1.0)

poetry.lock
.venv

我给你整理 Poetry 配置文件 `pyproject.toml` 中 `[tool.poetry]` 下面所有标准子节点、作用、用法、是否必填，纯清晰清单，一看就懂，适合你给 AI IDE 自动生成配置。

# `[tool.poetry]` 完整子节点列表 + 作用
所有节点均为 Poetry 专用标准配置。

## 一、基础信息节点（必填）
### 1. name
- 作用：项目名称（包名 / 项目名）
- 示例：`name = "test-python-sqlalchemy"`

### 2. version
- 作用：项目版本号
- 示例：`version = "0.1.0"`

### 3. description
- 作用：项目描述
- 示例：`description = "SQLAlchemy multi-datasource demo"`

### 4. authors
- 作用：作者列表
- 示例：
```
authors = [
    "张三 <zhangsan@example.com>",
    "李四 <lisi@example.com>"
]
```

## 二、包结构节点（重要）
### 5. packages
- 作用：指定哪些目录作为源码包导入
- 你的项目：`src/xxx` 结构必须用它
- 示例：
```
packages = [{ include = "test_python_sqlalchemy", from = "src" }]
```

### 6. include / exclude
- 作用：打包时包含/排除文件
- 示例：
```
include = ["src/*.py"]
exclude = ["tests/", "logs/"]
```

## 三、依赖管理（重要）
### 7. dependencies
- 作用：项目运行依赖
- 示例：
```
[tool.poetry.dependencies]
python = ">=3.11,<4.0"
sqlalchemy = "^2.0"
```

### 8. group.dev.dependencies
- 作用：开发环境依赖（pytest、black 等）
- 示例：
```
[tool.poetry.group.dev.dependencies]
pytest = "^7.0"
```

---

## 四、脚本命令（你正在用）
### 9. scripts
- 作用：定义快捷命令
- 你用的：
```
[tool.poetry.scripts]
single-table-demo = "test_python_sqlalchemy.single_table_demo:main"
```

## 五、仓库、证书、README
### 10. readme
- 作用：指定 README 文件
- 示例：`readme = "README.md"`

### 11. repository
- 作用：代码仓库地址
- 示例：`repository = "https://github.com/xxx/yyy"`

### 12. homepage
- 作用：项目主页

### 13. keywords
- 作用：搜索关键词
- 示例：`keywords = ["sqlalchemy", "mysql", "poetry"]`

### 14. license
- 作用：开源协议
- 示例：`license = "MIT"`

### 15. classifiers
- 作用：PyPI 分类标签

## 六、插件、构建、高级
### 16. plugins
- 作用：Poetry 插件配置

### 17. extras
- 作用：可选依赖组

# 最精简、最常用、你必须记住的 9 个节点
```
name
version
description
authors
packages
readme
dependencies
scripts
keywords
```


# 你当前项目最标准的 `[tool.poetry]` 完整版
```toml
[tool.poetry]
name = "test-python-sqlalchemy"
version = "0.1.0"
description = "SQLAlchemy multi-datasource demo with Poetry"
authors = ["Your Name <your@email.com>"]
readme = "README.md"
packages = [{ include = "test_python_sqlalchemy", from = "src" }]
keywords = ["sqlalchemy", "mysql", "poetry", "multi-datasource"]

[tool.poetry.dependencies]
python = ">=3.11,<4.0"
sqlalchemy = ">=2.0.40,<3.0.0"
pymysql = ">=1.1.1,<2.0.0"

[tool.poetry.scripts]
single-table-demo = "test_python_sqlalchemy.single_table_demo:main"
multi-table-query = "test_python_sqlalchemy.multi_table_query:main"
```


## 一句话总结
`[tool.poetry]` 是 Poetry 项目的核心配置区，管理项目信息、源码目录、依赖、脚本、打包规则。
你用 src 目录结构必须写 packages，脚本必须写 scripts。


需要我给你 Poetry 所有配置节点的完整官方清单（中文版） 吗？
