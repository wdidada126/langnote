# 

布隆过滤器可以用于检索一个元素是否在一个集合中。它的优点是空间效率和查询时间都远远超过一般的算法，缺点是有一定的误识别率和删除困难。


个人电脑上搭建OpenStack的实验室
https://blog.csdn.net/karamos/article/details/80121744
Mirantis

https://www.cnblogs.com/Leo_wl/p/8526552.html
https://blog.csdn.net/huanghuibai/article/details/47184733


https://blog.csdn.net/hchuchuan/article/details/52225660

https://www.cnblogs.com/shoufengwei/p/6901173.html

WINSERVER2016  ESXI6.7  PVE 常用这3种
VMware ESXi 
http://blog.51cto.com/xuhaili100love/536186
现在openstack社区，也有很多可用的部署工具，有mirantis的fuel，redhat的RDO，还有开源社区的devstack

http://demo.fuel-infra.org:8000/

fuel

https://blog.csdn.net/enweitech/article/details/50477377

https://my.oschina.net/u/2285247/blog/955318

https://www.cnblogs.com/dongdongwq/p/5627532.html

https://www.mirantis.com/software/openstack/releases/#supported

https://www.bookstack.cn/read/deployopenstackwithpuppet/howto.md


不想搭建环境，官方提供测试Fuel9.0的demo环境 http://demo.fuel-infra.org:8000（只要你电脑能上外网）默认用户名、密码admin


linux党还是kvm 虽然比较折腾。。。
https://www.osboxes.org/virtualbox-images/ 桌面我通常直接拉。

https://www.osboxes.org/screenshots/


块存储：
 
LVM使用默认的存储
 
Ceph使用 Ceph 作为 Cinder 卷存储的后端
对象存储：
 
Ceph使用 Ceph 作为 Swift 对象存储的后端
镜像存储：
 
Ceph使用 Ceph 作为 Glance 镜像存储的后端
临时存储：
 
Ceph使用 Ceph 作为 Nova 的后端


https://www.kubernetes.org.cn/2704.html

http://docs.kubernetes.org.cn/

Kubernetes 学习笔记之 MiniKube 安装

https://ehlxr.me/2018/01/12/kubernetes-minikube-installation/

https://blog.csdn.net/fishinhouse/article/details/80589683

https://kubernetes.io/docs/setup/minikube/#minikube-features

https://blog.csdn.net/shurenyun/article/details/78066126

https://blog.csdn.net/zhaohuabing/article/details/78954820

kubeadm
kubelet
kubectl

https://zhaohuabing.com/

https://jimmysong.io/

https://www.cnblogs.com/Mrhuangrui/p/7249253.html

https://kubernetes.io/docs/tasks/run-application/run-stateless-application-deployment/

Create a Deployment based on the YAML file:

kubectl apply -f https://k8s.io/examples/application/deployment.yaml
Display information about the Deployment:

kubectl describe deployment nginx-deployment

