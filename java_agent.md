# java agent7

/tools/java/bin/java -Dapp.id=authmedia -Dapollo.env=FUC -Dapollo.meta=http://172.17.46.16:20880 -server -XX:+UseCompressedOops -Xms3g -Xmx3g -XX:PermSize=256M -XX:MaxPermSize=1024m -XX:NewSize=2048m -XX:MaxNewSize=2048m -XX:SurvivorRatio=10 -Xloggc:/data/dataLogs/gc/gc.log -verbose:gc -XX:+PrintGCDateStamps -XX:+PrintGCDetails -XX:+UseConcMarkSweepGC -XX:+UseCMSCompactAtFullCollection -XX:+CMSClassUnloadingEnabled -XX:+DisableExplicitGC -XX:CMSInitiatingOccupancyFraction=80 -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/data/dataLogs/dump -Dcom.sun.management.jmxremote -Dcom.sun.maagement.jmxremote.ssl=false -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.managment.jmxremote.port=8866 -Djava.rmi.server.hostname=172.17.47.74 -Djetty.state=/tools/jetty/jetty.state -Djetty.port=8030 -Djetty.home=/tools/jetty -Djava.io.tmpdir=/tmp -jar /tools/jetty/start.jar etc/jetty-logging.xml etc/jetty-started.xml


