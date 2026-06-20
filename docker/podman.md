# podman

红帽搞得，开源吗？
https://github.com/containers/podman-desktop
ts写的

## 代码仓库
https://github.com/containers/podman
Go写的

Documents: https://docs.podman.io

http://podman.io/

https://podman-desktop.io/downloads

Podman
定位：Podman是一个基于libpod库的容器引擎，用于管理容器和容器镜像。
功能：Podman提供了类似 Docker 的容器化解决方案，允许用户创建、运行和管理容器。
优势：与Docker类似的命令行接口、无需守护进程、Rootless模式支持、可与Kubernetes集成等。
应用场景：适用于需要容器化的应用程序部署和管理，特别是在无需 Root 权限的场景下使用。

winget install -e --id RedHat.Podman-Desktop
brew install podman-desktop
flatpak install flathub io.podman_desktop.PodmanDesktop

## docker比优势
docker必须root权限，

## 版本

v5.8.0

## 编译脚本
git clone https://github.com/containers/podman.git
cd podman
git checkout v5.8.0
go mod tidy
go build -v -o bin/podman ./cmd/podman
ls -la bin/podman

## 安装
### win