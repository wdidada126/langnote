# containerd 

docker 对容器的管理和操作基本都是通过 containerd 完成的

https://www.cnblogs.com/sparkdev/p/9063042.html

Containerd 的技术方向和目标
- 简洁的基于 gRPC 的 API 和 client library
- 完整的 OCI 支持(runtime 和 image spec)
- 同时具备稳定性和高性能的定义良好的容器核心功能
- 一个解耦的系统(让 image、filesystem、runtime 解耦合)，实现插件式的扩展和重用

简单来说：可以，但不完全一样。

- 镜像格式兼容：containerd 和 Docker 都遵循 OCI（Open Container Initiative） 标准。因此，Docker Hub 上的镜像（例如 `nginx:latest`）可以直接被 containerd 拉取和运行，无需转换。
- 命令工具不同：  
  - Docker 使用 `docker pull`  
  - containerd（k3s 使用的）使用 `crictl pull` 或 `ctr image pull`
- 存储位置不同：  
  - Docker 镜像存在 `/var/lib/docker`  
  - k3s 的 containerd 镜像存在 `/var/lib/rancher/k3s/agent/containerd`

所以，你在 Docker Hub 看到的任何镜像，containerd 都可以使用，只是拉取命令和存储路径不一样。例如：
```bash
sudo k3s crictl pull nginx:latest
```
