# glide

glide是Golang的包管理工具，是为了解决Golang依赖问题的。 为什么需要glide？ 原因很简单，Go 语言原生包管理的缺陷。罗列一下golang的 get 子命令管理依赖有很多大缺陷：

https://glidedocs.readthedocs.io/zh/latest/

Glide 提供了以下功能：

在 glide.yaml 文件中记录依赖信息。包括了名称、版本或版本范围、私有仓库或者类型不能识别时的版本控制信息等等
通过glide.lock文件来追踪每个包的具体修改，这使得能够重用依赖树。
适用于语义版本和语义版本范围。
支持 Git、Bzr、HG 和 SVN。和 go get 支持的版本控制系统一致。
利用 vendor/目录使得不同项目可以拥有相同依赖的不同版本。
允许使用包别名，这对 forks 非常有用。
支持从 Godep、GPM、Gom 和 GB 导入配置
