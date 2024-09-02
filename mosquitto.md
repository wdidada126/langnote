# mosquitto

一款实现了消息推送协议 MQTT v3.1 的开源消息代理软件，提供轻量级的，支持可发布/可订阅的的消息推送模式，使设备对设备之间的短消息通信变得简单，比如现在应用广泛的低功耗传感器，手机、嵌入式计算机、微型控制器等移动设备。

https://mosquitto.org/

https://github.com/eclipse/mosquitto

c语言的

## install
https://mosquitto.org/download/
brew install mosquitto

sudo apt install mosquitto -y

which mosquitto
/usr/sbin/mosquitto
mosquitto -h
mosquitto version 2.0.18

mosquitto is an MQTT v5.0/v3.1.1/v3.1 broker.

Usage: mosquitto [-c config_file] [-d] [-h] [-p port]

 -c : specify the broker config file.
 -d : put the broker into the background after starting.
 -h : display this help.
 -p : start the broker listening on the specified port.
      Not recommended in conjunction with the -c option.
 -v : verbose mode - enable all logging types. This overrides
      any logging options given in the config file.

See https://mosquitto.org/ for more information.


在Ubuntu上配置Mosquitto的例子，可以通过修改Mosquitto的配置文件来实现。以下是一个简单的Mosquitto配置文件示例：

### 1. 打开Mosquitto的配置文件

首先，使用文本编辑器（比如nano或vim）打开Mosquitto的配置文件。在Ubuntu上，通常Mosquitto的配置文件位于 `/etc/mosquitto/mosquitto.conf`。

```bash
sudo nano /etc/mosquitto/mosquitto.conf
```

### 2. 编辑Mosquitto配置文件

在打开的配置文件中，您可以添加或修改各种配置项来适应您的需求。以下是一个简单的Mosquitto配置文件示例：

```conf
# 以daemon模式运行
daemon

# 设置监听端口
listener 1883

# 允许匿名访问
allow_anonymous true

# 设置日志文件
log_dest file /var/log/mosquitto/mosquitto.log

# 设置pid文件
pid_file /var/run/mosquitto.pid

# 设置持久化数据库文件
persistence true
persistence_location /var/lib/mosquitto/

# 设置密码文件路径（如果需要认证）
password_file /etc/mosquitto/passwd

# 设置ACL文件路径
acl_file /etc/mosquitto/acl
```

### 3. 保存和退出配置文件

在编辑完配置文件后，按下 `Ctrl + O` 保存文件，然后按下 `Ctrl + X` 退出编辑器。

### 4. 重启Mosquitto服务

在保存配置文件后，您需要重新启动Mosquitto服务以使更改生效。

```bash
sudo systemctl restart mosquitto
```

这样，您就可以通过编辑Mosquitto的配置文件来自定义Mosquitto MQTT代理的设置和行为。请根据您的需求修改配置文件中的参数。


mosquitto -c /etc/mosquitto/mosquitto.conf -v
1725263242: Loading config file /etc/mosquitto/conf.d/mosquitto.conf
1725263242: Error: Unknown configuration variable "daemon".
1725263242: Error found at /etc/mosquitto/conf.d/mosquitto.conf:2.
1725263242: Error found at /etc/mosquitto/mosquitto.conf:11.
