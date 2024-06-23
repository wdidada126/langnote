# mac

无法打开“EasyLPAC”，因为无法验证开发者。

使用右键打开：在应用程序上按住Control键，然后点击应用程序图标，选择“打开”。在弹出的警告对话框中，再次点击“打开”。

当遇到“无法打开‘EasyLPAC’，因为无法验证开发者”的问题时，这通常表示macOS系统的安全机制（Gatekeeper）阻止了未经验证的应用程序的运行。以下是一些建议的解决步骤：

一次性方法
打开系统偏好设置：点击屏幕左上角的苹果图标，选择“系统偏好设置”。
进入安全性与隐私：在系统偏好设置窗口中，点击“安全性与隐私”。
选择“通用”选项卡：在安全性与隐私窗口中，点击左侧的“通用”选项卡。
允许未验证的应用：在窗口底部，你可能会看到“已阻止使用‘EasyLPAC’，因为来自身份不明的开发者”的提示。点击其后的“仍要打开”按钮。
确认打开：在弹出的确认弹窗中，点击“打开”按钮。
永久解决方法
如果你经常需要安装未经验证的应用，并且确定这些应用是安全的，你可以考虑永久禁用Gatekeeper。但请注意，这样做可能会增加系统风险。

检查Gatekeeper状态：打开终端（Terminal），输入spctl --status。如果返回“assessments enabled”，则Gatekeeper当前是启用的。
禁用Gatekeeper：在终端中输入sudo spctl --master-disable，然后输入管理员密码以禁用Gatekeeper。
其他建议
更新应用程序：如果可能，尝试从官方来源下载最新版本的“EasyLPAC”，因为旧版本可能不兼容或存在已知的安全问题。
使用右键打开：在应用程序上按住Control键，然后点击应用程序图标，选择“打开”。在弹出的警告对话框中，再次点击“打开”。
更改安全性设置：在“安全性与隐私”的“通用”选项卡中，尝试更改“允许从以下位置下载的应用程序”的设置，选择“任何来源”。如果“任何来源”选项没有显示，你可能需要先点击左下角的锁图标以进行更改。
重新启用Gatekeeper：如果你之前禁用了Gatekeeper并希望重新启用它，可以在终端中输入sudo spctl --master-enable。
请注意，在更改系统设置或安装未经验证的应用程序时，请务必谨慎行事，并确保你信任该应用程序的来源。


港区Apple ID注册流程
以下注册流程较繁琐，你也可以到第三方平台如：https://taohao.me/product/、https://fk.appledi.com/product/ 购买Apple ID。



[WebStorm快捷键（Mac版）](https://www.cnblogs.com/xjchenhao/p/4430544.html)

# ⌘——Command
# ⌃ ——Control
# ⌥——alt
# ⇧——Shift
# ⇪——Caps Lock
# fn——功能键就是fn

# Mac必备软件
Shuttle

Shadowsockt-NG
Telegram
Xcode
Texmaker
Typora
ezip
Clash
xmind
jprofile

mac连接外部显示器 竖屏
https://blog.csdn.net/KingJin_CSDN_/article/details/106497347

dell主机第一个有线数据线的接口
mac地址
ec:f4:bb:eb:fe:48
EC:F4:BB:EB:FE:48

招聘
奇瑞控股集团有限公司

[Sublime Mac快捷键](https://segmentfault.com/q/1010000002397241)

https://segmentfault.com/q/1010000002397241

Ctrl+A：到行首（达到Home键的效果）
Ctrl+E：到行尾（达到End键的效果）
Ctrl+N：到下一行
Ctrl+P：到上一行
Ctrl+K：从光标处开始删除，直到行尾
fn键+左方向键是HOME
fn键+右方向键是END
fn+上方向键是page up
fn+下方向键是page down

使用电脑有记录



nvme转接卡苹果

回复 @超级喜欢成宝拉 :需要m.2转苹果的转接卡

同样的配置，同样的年份，昨天换了m.2的1T固态，读可以跑到2700，写可以跑到2600，同样的测试软件。限制你速度的不是主板，应该是那个转接卡，我的是PCIe3.0的转接卡，你的可能是PCIe2.0的
提示下，2015,15'的是PCIE3.0速率，13'是PCIE2.0速率。

看了up的视频，动手换了金士顿 kc3000 1TB 固态硬盘！，读写跑分超过2800MB/s了，比预想的要好！
回复 @阿小新阿 :在某宝买的 阿卡西斯 转接卡 19.9米 用着挺好的 一切正常

京东普遍贵上百分之二三十

2024-05-08 苹果发布了新款 iPad Pro
mac app store 取消下载
Command option

mbp 切换icloud账户
设置 系统偏好设置
apple id
概览
退出登录


Windows的逻辑是，复制(ctrl+c)——粘贴(ctrl+v)，剪切(ctrl+x)——粘贴(ctrl+v)。macOS的逻辑是：拷贝(CMD+C)——粘贴(CMD+V)，拷贝(CMD+C)——剪切(CMD+OPTION+V)

https://www.zhihu.com/question/37544123/answer/3426479727


https://www.bilibili.com/video/BV1Ps4y1R7Lo/?spm_id_from=333.337.search-card.all.click&vd_source=71b9c2a5f966942c83677c2110efde22

https://support.apple.com/zh-cn/guide/mac-pro/apdc6980d3be/2022/mac/12.2

mac 无法打开“xxx”,因为无法验证开发者。

当您在Mac上尝试打开第三方软件时，可能会遇到“无法验证开发者”的提示。这种情况通常出现在新安装的非AppStore软件上。这个警告并不意味着该应用有问题，可能是因为开发者未向Apple注册其ID。为了解决这个问题，您可以按照以下步骤操作：

1. 在应用程序的右侧菜单栏中找到提示“无法验证开发者”的应用。
2. 右键点击该应用，选择“打开”。
3. 第一次打开时，可能会出现额外的提示信息，但继续点击“打开”即可完成设置。

Pagers mac软件

sudo spctl --master-disable

Ctrl+A：到行首（达到Home键的效果）
Ctrl+E：到行尾（达到End键的效果）
Ctrl+N：到下一行
Ctrl+P：到上一行
Ctrl+K：从光标处开始删除，直到行尾

fn键+左方向键是HOME
fn键+右方向键是END
fn+上方向键是page up
fn+下方向键是page down

alfred、coderunner、dash
Mac工具

## mac产品

XCode是连其他开发工具一起装的
mac可以下载安装包安装软件，iPhone还没有开放安装软件安装

## mac book pro
mbp 2015 
