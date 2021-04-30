# apm



http://www.infoq.com/cn/articles/apm-Pinpoint-practice



全链路追踪技术选型：pinpoint vs skywalking


naver/pinpoint(github上2148个star)

韩国的一个公司开源的，有待评估使用情况，就是整体还不是JDK8，有些还是有点费劲，技术上采用agent的方式，对java友好

大众点评cat(github上1725个star)

看接入的公司还是挺多的，个人感觉是点评名气还可以，但是搭建起来有点费劲，很多东西都写死配置了，不灵活。整体设计的话，由于没有采用agent的方式，采用的是api手工埋点的方式，跟SNG的很像，好处的是跨语言，不好的地方就是对java来说用起来还需要包装一下

sky-walking(github上374个star)

开发团队加入了OneAPM,目前看使用的公司不多，整体技术采用agent方式，对java友好。提供了对dubbo等的支持，属于soa时代的产品
 

