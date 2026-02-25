# patroni

https://patroni.readthedocs.io/en/latest/

pg数据库高可用方案
A template for PostgreSQL High Availability with Etcd, Consul, ZooKeeper, or Kubernetes

https://github.com/zalando/patroni

## 版本
https://patroni.readthedocs.io/en/latest/releases.html

v4.1.0
v4.0.7 Sep 23, 2025
v4.0.0 Aug 29, 2024
v3.2.0 Oct 25, 2023
v3.0.0 Jan 30, 2023
## 编程语言
Python

## 编译脚本
which pip
which python
pip install setuptools wheel
git clone https://github.com/patroni/patroni.git
cd patroni
git checkout v4.0.0
ls -la setup.py
pip install -r requirements.txt
pip install -r requirements.dev.txt
python setup.py bdist_wheel
ls -la dist/

# 安装 build 工具
pip install build
# 执行打包
python -m build --wheel