# thingsboard

https://github.com/thingsboard/thingsboard

linux docker部署thingsborad


```shell
mkdir -p ~/.mytb-data && sudo chown -R 799:799 ~/.mytb-data
mkdir -p ~/.mytb-logs && sudo chown -R 799:799 ~/.mytb-logs
docker run -it -p 9090:9090 -p 7070:7070 -p 1883:1883 -p 5683-5688:5683-5688/udp -v ~/.mytb-data:/data -v ~/.mytb-logs:/var/log/thingsboard --name mytb --restart always thingsboard/tb-postgres
```

http://localhost:8080


用户名 tenant@thingsboard.org
password tenant

git clone -b v3.6.2 https://github.com/thingsboard/thingsboard.git
cd thingsboard
mvn clean package  -DskipTests