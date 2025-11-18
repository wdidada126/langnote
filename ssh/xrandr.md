# xrandr

好的，我们来详细介绍一下 xrandr 这个强大的 Linux 命令行工具。

一、xrandr 是什么？

xrandr 是 X Resize and Rotate 的缩写，它是一个官方的命令行工具，用于配置与 X Window System（大多数 Linux 发行版的图形界面基础）连接的显示器的显示模式。

简单来说，它是一个：
•   屏幕设置神器：你可以用它来设置分辨率、刷新率、旋转屏幕、启用/禁用显示器，以及设置多显示器的排列方式（如扩展、复制等）。

•   RandR（Resize and Rotate）协议 的实现：该协议允许在 X 会话运行时动态改变屏幕的输出特性，而无需重启 X 服务。

二、为什么需要 xrandr？

在图形桌面环境（如 GNOME, KDE, XFCE）中，系统设置里通常都有一个图形化的界面来管理显示器。这个图形界面底层调用的命令就是 xrandr。

当你遇到以下情况时，直接使用 xrandr 会非常有用：
1.  自动化脚本：在开机或连接显示器时自动执行复杂的显示配置。
2.  故障排除：当图形界面设置失效或无法启动时，通过命令行直接调整。
3.  高级配置：进行一些图形界面不支持的精细调整（如设置自定义分辨率模型）。
4.  无桌面环境的系统：在服务器或仅有命令行界面的系统中，如果需要启动图形应用并输出到特定显示器。
5.  解决显示问题：例如，笔记本合盖后外接显示器不工作等。

三、基本用法和常用命令

1. 查询当前屏幕信息（最常用的命令）

直接运行 xrandr 命令，不加任何参数，会列出所有已连接和未连接的显示器及其支持的模式。
xrandr

输出示例：

Screen 0: minimum 320 x 200, current 1920 x 1080, maximum 16384 x 16384
eDP-1 connected primary 1920x1080+0+0 (normal left inverted right x axis y axis) 310mm x 170mm
   1920x1080     60.00*+  40.00
   1680x1050     60.00
   ...
HDMI-1 disconnected (normal left inverted right x axis y axis)
DP-1 connected 1920x1080+1920+0 (normal left inverted right x axis y axis) 530mm x 300mm
   1920x1080     60.00*+  50.00  59.94
   2560x1440     59.95
   ...

解读关键信息：
•   eDP-1, HDMI-1, DP-1：这些是显示器的名称。eDP通常代表笔记本电脑的内置屏幕。HDMI和DP代表对应的视频接口。

•   connected / disconnected：显示连接状态。

•   primary：表示该显示器被设置为主显示器。

•   1920x1080+0+0：当前分辨率是1920x1080，位置在（0, 0）坐标点。

•   下面的列表是该显示器支持的所有分辨率和刷新率，带 * 号的是当前分辨率，带 + 号的是推荐分辨率。

2. 设置分辨率

xrandr --output <显示器名称> --mode <分辨率>

示例：将 HDMI-1 接口的显示器设置为 1920x1080 分辨率。
xrandr --output HDMI-1 --mode 1920x1080


3. 开启/关闭显示器

•   开启显示器（并设置为推荐分辨率）：
    xrandr --output HDMI-1 --auto
    

•   关闭指定显示器：
    xrandr --output HDMI-1 --off
    
    这个命令非常有用，比如当你只想用外接显示器时，可以关闭笔记本的屏幕：
    xrandr --output eDP-1 --off
    

4. 设置多显示器模式

这是 xrandr 最核心的功能之一。

•   扩展模式：将两个屏幕组合成一个大的桌面空间。
    xrandr --output DP-1 --auto --right-of eDP-1
    
    这会将 DP-1 显示器放置在 eDP-1（笔记本内置屏幕）的右侧。你也可以使用 --left-of, --above, --below。

•   复制/镜像模式：两个显示器显示相同的内容。
    xrandr --output DP-1 --auto --same-as eDP-1
    

•   仅外接显示器：
    xrandr --output DP-1 --auto --primary --output eDP-1 --off
    

•   仅内置显示器：
    xrandr --output eDP-1 --auto --primary --output DP-1 --off
    

5. 设置刷新率

有些分辨率支持多个刷新率（如 60Hz, 120Hz）。使用 --rate 参数。
xrandr --output HDMI-1 --mode 1920x1080 --rate 120


6. 旋转屏幕

xrandr --output eDP-1 --rotate left    # 向左旋转90度
xrandr --output eDP-1 --rotate right   # 向右旋转90度
xrandr --output eDP-1 --rotate inverted # 倒转180度
xrandr --output eDP-1 --rotate normal   # 恢复正常


7. 设置主显示器

将某个显示器设置为主显示器（系统任务栏、启动器等通常会出现在主显示器上）。
xrandr --output DP-1 --primary


四、高级用法：添加自定义分辨率模式

如果你的显示器支持高分辨率（如 2560x1080 的带鱼屏）但 xrandr 列表中没有，你可以手动添加。

警告： 设置显示器不支持的分辨率模式可能导致黑屏或无信号。操作需谨慎。

1.  使用 cvt 命令计算模型行：
    cvt 2560 1080 60
    
    输出会给你一行 Modeline 信息。

2.  使用 gtf 命令（另一种选择）：
    gtf 2560 1080 60
    

3.  创建新模式（使用 cvt 或 gtf 输出的 Modeline 后的内容）：
    xrandr --newmode "2560x1080_60.00" 230.00 2560 2720 2992 3424 1080 1083 1093 1120 -hsync +vsync
    

4.  将新模式添加到你的显示器：
    xrandr --addmode HDMI-1 "2560x1080_60.00"
    

5.  现在，你就可以像使用普通分辨率一样使用这个新模式了：
    xrandr --output HDMI-1 --mode "2560x1080_60.00"
    

让自定义分辨率永久生效：你需要将上面的 --newmode 和 --addmode 命令添加到你的 X 启动脚本中（例如 ~/.xprofile 或 /etc/X11/Xsession.d 下的脚本）。

五、重要提示

•   临时生效：xrandr 的配置更改通常是临时性的，重启电脑后就会失效。要永久生效，你需要将命令写入启动脚本。

•   Wayland：xrandr 是 X11 的工具。新一代的显示服务器协议 Wayland 有自己的一套管理工具（如 wlr-randr, gnome-randr），但 xrandr 在 X11 环境和混合环境下依然是最主流和强大的选择。

希望这个详细的介绍能帮助你更好地理解和使用 xrandr！它是 Linux 用户管理显示设备的必备利器。