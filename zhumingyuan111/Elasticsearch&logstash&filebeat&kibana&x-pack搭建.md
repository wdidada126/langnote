---
title: Elasticsearch&logstash&filebeat&kibana&x-pack搭建
date: 2017-09-09 10:17:35
tags: CSDN迁移
---
  ### filebeat安装

  
  2. 下载filebeat安装包，filebeat-5.5.2-linux-x86_64.tar.gz 
  4. 解压 tar-zxvf filebeat-5.5.2-linux-x86_64.tar.gz 
  6. 修改filebeat.yml配置文件如下：
     
      
     ```
     filebeat.prospectors:
input_type: log
paths:
- /path/fail.log
document_type: type1

input_type: log
paths:
- /path/full.log
document_type: type2

fields:
tail_files: "true"
output.logstash:
hosts: ["ip1:5043","ip2:5043"]
loadbalance: "true"
     ```
      
  8. 启动filebeat 
     
      
     ```
     如果非第一次启动则删除%FILEBEAT_HOME%/data/registry 文件
rm data/registry
启动脚本
./filebeat -e -c filebeat.yml -d "publish"
或者后台启动
nohup ./filebeat -e -c filebeat.yml -d "publish" >output 2>&1 &
     ```
       
### 安装logstash

  
  2. 下载logstash安装包：logstash-5.5.2.tar.gz 
  4. 解压： `tar -zxvf logstash-5.5.2.tar.gz`  
  6. 修改logstash.conf 配置文件如下：  
```
input {
    beats{
            port=>"5043"
        }
}

output {

    if [type] == "type1"{
    elasticsearch {
            hosts => ["ip1:9200","ip2:9200"]
            index => "logstash-type1-%{+YYYY.MM.dd}"
            document_type => "type1"
        }
    }

    if [type] == "type2"{
    elasticsearch {
            hosts => ["ip1:9200","ip2:9200"]
            index => "logstash-type2-%{+YYYY.MM.dd}"
            document_type => "type2"
        }
    }

}
```
  
  2. 启动logstash   
```
启动脚本
bin/logstash -f logstash.conf --config.reload.automatic
或者后台启动脚本
nohup bin/logstash -f logstash.conf --config.reload.automatic >nohup.out 2>&1 &
```
 
### 安装elasticsearch

  
  2. 下载安装包： elasticsearch-5.5.2.tar.gz 
  4. 解压： tar -zxvf elasticsearch-5.5.2.tar.gz 
  6. 修改elasticsearch.yml 配置如下  
```
cluster.name: cluster1
node.name: c1-node-1
http.cors.enabled: true
http.cors.allow-origin: "*"
path.data: /es-path/data
path.logs: /es-path/logs
bootstrap.memory_lock: false
network.host: ip //如果是远程机器访问该es应用，则需要配置ip而不是localhost
http.port: 9200
discovery.zen.ping.unicast.hosts: ["ip1","ip2"]
discovery.zen.minimum_master_nodes: 5
action.auto_create_index: +*
xpack.security.enabled: false
```
  
  2. 启动脚本  
```
$ ./bin/elasticsearch -p ./e-pid -d
```
 
### 安装kibana

  
  2. 下载安装包 ： kibana-5.5.2-linux-x86_64.tar.gz 
  4. 解压 tar -zxvf kibana-5.5.2-linux-x86_64.tar.gz 
  6. 修改kibana.yml配置如下：  
```
server.port: 8601
server.host: "ip"
elasticsearch.url: "http://ip:9200" //elsaticsearch 服务ip和端口
xpack.security.enabled: false
```
  
  2. 启动kibana  
```
nohup ./bin/kibana >nohup.out 2>&1 &
```
 
### 安装x-pack [该软件是收费的]

  
  2. 下载：x-pack-5.5.2.zip 
  4. 切换到elasticsearch下： `%ES_HOME/%` 下面。   
      执行如下命令：  `bin/elasticsearch-plugin install file:///path/to/file/x-pack-5.5.2.zip` 即可。 
  6. 切换到kibana下： `KI_HOME` 下面。   
      4.执行同样的命令： `bin/elasticsearch-plugin install file:///path/to/file/x-pack-5.5.2.zip` 即可。  
## 注意：

  
  2. 如果有远程机器相互访问，以上ip部分最好设置为机器的ip地址，避免使用localhost或者127.0.0.1 
  4. 如果使用x-pack，默认是开启security功能，所以你需要在logstash部分设置用户名和密码才能让logstash和elasticsearch连接上。因为本人是在测试环境内部使用所以就省去了安全功能。如上所示，分别在elasticsearch.yml和kibana.yml中添加如下语句：   
       `xpack.security.enabled: false`  
  6. 使用x-pack会自动建立index，所以我们需要修改elasticsearch.yml文件如下： `action.auto_create_index: +*`    
      这里我的设置几乎没有限制，任何名字的索引都可以建立。    
  