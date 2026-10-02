# 第 18–20 章 Web 应用（Django 学习笔记 / 用户账户 / 样式与部署）（原书 pp.405–476）

> 用 Django 搭一个「学习笔记」Web 应用：主题+条目 CRUD、用户注册登录、样式与部署。基线：原书 Python 3.11；本目录按 3.12+ 校验。

## 本章地图

| 子主题 | 内容 | 结论 |
|---|---|---|
| 18 起步 | 建项目/应用、模型、迁移、admin | MTV 架构 |
| 19 用户账户 | 注册/登录/注销、权限 | Django 自带 auth |
| 20 样式与部署 | 静态文件、Bootstrap、部署 | 免费层变迁 |

## 核心精讲

教学示意，不参与构建（需 `pip install django`，用虚拟环境）：

```bash
# 现代建项目（用 venv / uv，不用系统 Python）
python -m venv .venv && source .venv/bin/activate
pip install "django>=5"
django-admin startproject learning_log .
python manage.py startapp learning_logs
python manage.py migrate
python manage.py runserver
```

```python
# learning_logs/models.py
from django.db import models

class Topic(models.Model):
    text = models.CharField(max_length=200)
    def __str__(self):
        return self.text
```

## 版本演进

- 原书用 Django 2.x/3.x；今天 Django 5.x（🔧 以官网为准），`path()` 替代旧 `url()`，`asgi.py` 默认存在。
- 部署目标：原书 Heroku 免费层已退场；今天用 Render / Fly.io / Platform.sh / Railway（🔧 以官网为准）。
- 异步视图 Django 已支持（`async def view`），配合 ASGI。

## 经典论文与原始文献

- PEP 3333 — WSGI（2010），https://peps.python.org/pep-3333/ 规范文档，非同行评审论文。
- Django 文档：https://docs.djangoproject.com/ 规范文档。

## 近年研究与工业界开源实践（2015–2026）

- 轻量 API 用 FastAPI/Flask 替代 Django；Django 仍是企业级全栈首选。
- 类型提示进 Django（`django-stubs` + mypy）。
- 容器化部署（Docker）+ CI。

## 常见误区与本书需修正之处

| 原书说法 | 问题 | 2026 正确写法 |
|---|---|---|
| 系统 Python 直接装 django | 污染环境 | 用 venv/`uv` |
| Heroku 免费部署 | 已停 | 换 Render/Fly.io 等 |
| SECRET_KEY 提交仓库 | 严重泄露 | 放环境变量，`.env` 不入库 |
| DEBUG=True 上生产 | 泄露堆栈 | 生产设 False |

## 与其他章 / 其他书的联系

- 模型即类（[08-类.md](08-类.md)）；迁移涉及数据库见本仓库大纲 [../EssentialSQLAlchemy2e.md](../EssentialSQLAlchemy2e.md)。
- Django 深讲见本仓库大纲 [../DjangoForBeginners5e.md](../DjangoForBeginners5e.md)、[../TwoScoopsOfDjango.md](../TwoScoopsOfDjango.md)。
- FastAPI 替代见本仓库大纲 [../BuildingPythonWebAPIsWithFastAPI.md](../BuildingPythonWebAPIsWithFastAPI.md)。
