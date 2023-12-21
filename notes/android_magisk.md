# Magisk

Nexus 5X 8.1工厂镜像在安装Magisk的时候，需要安装三方recovery，比如twrp。
实际操作时，twrp第一次安装时生效，开机重启后，手机会进不去系统，第二次就可以进去。但是手机的recovery会被换成官网的。

## 安装三方recovery
进入fastboot模式，输入指令

```shell
fastboot boot twrpXXX.img
```

注意，如下指令对Nexus 5X，安卓8.1的系统没有效果
```shell
fastboot flash recovery twrtXXX.img
```
Nexus 5X，安卓8.1的系统，重启之后会恢复官方recovery

## 安装
在安装三方recovery之后，可以刷入Magisk的压缩包。
注意，从16.2开始，Magisk的安装包不再包含32位的文件，在Nexus 5X 安卓8.1系统的时候，termux会报错，找不到32位的su文件。因此建议刷16.0版本的。

## 体验
安装好进入系统之后，会安装一个应用：MagiskManager
可以安装module，可以管理root授权

## 卸载
Magiskuninstaller


