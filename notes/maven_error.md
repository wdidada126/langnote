# maven error

Plugin org.apache.maven.plugins:maven-clean-plugin:2.5 or one of its dependencies could not be resolved: 
Failure to find org.apache.maven.plugins:maven-clean-plugin:jar:2.5 in 
http://mvnrepository.com/ was cached in the local repository,
resolution will not be reattempted until the update interval of nexus has elapsed or updates are forced -


Downloading from nexus: http://mvnrepository.com/org/apache/maven/plugins/maven-clean-plugin/2.5/maven-clean-plugin-2.5.pom
[WARNING] The POM for org.apache.maven.plugins:maven-clean-plugin:jar:2.5 is missing, no dependency information available
Downloading from nexus: http://mvnrepository.com/
org/apache/maven/plugins/maven-clean-plugin/2.5/maven-clean-plugin-2.5.jar

--settings 

`mvn verify -Poschina -U`

`mvn clean install -Dmaven.test.skip=true -U -Poschina --settings D:\apache-maven-3.5.3\setting.xml`

-javaagent:/opt/tprofiler/tprofiler.jar
-Dprofile.properties=/opt/tprofiler/profile.properties

4538 Bootstrap -Djava.util.logging.config.file=/usr/tomcat/apache-tomcat-7.0.88/conf/logging.properties -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Dcom.sun.management.jmxremote= -Dcom.sun.management.jmxremote.port=1099 -Dcom.sun.management.jmxremote.rmi.port=1099 -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.authenticate=false -Djava.rmi.server.hostname=193.112.34.55 -Djdk.tls.ephemeralDHKeySize=2048 -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=1099 -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.authenticate=false -Djava.rmi.server.hostname=193.112.34.55 -Dignore.endorsed.dirs= -Dcatalina.base=/usr/tomcat/apache-tomcat-7.0.88 -Dcatalina.home=/usr/tomcat/apache-tomcat-7.0.88 -Djava.io.tmpdir=/usr/tomcat/apache-tomcat-7.0.88/temp

14680 jar
18489 Main -XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=75 -XX:+UseCMSInitiatingOccupancyOnly -XX:+DisableExplicitGC -Djava.awt.headless=true -Dfile.encoding=UTF-8 -XX:+HeapDumpOnOutOfMemoryError -Xmx1g -Xms256m -Xss2048k -Djffi.boot.library.path=/root/logstash-5.0.2/vendor/jruby/lib/jni -Xbootclasspath/a:/root/logstash-5.0.2/vendor/jruby/lib/jruby.jar -Djruby.home=/root/logstash-5.0.2/vendor/jruby -Djruby.lib=/root/logstash-5.0.2/vendor/jruby/lib -Djruby.script=jruby -Djruby.shell=/bin/sh
6138 jar -Xms512m -Xmx512m -XX:NewRatio=3 -XX:SurvivorRatio=4 -XX:TargetSurvivorRatio=90 -XX:MaxTenuringThreshold=8 -XX:+UseConcMarkSweepGC -XX:+UseParNewGC -XX:ConcGCThreads=4 -XX:ParallelGCThreads=4 -XX:+CMSScavengeBeforeRemark -XX:PretenureSizeThreshold=64m -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=50 -XX:CMSMaxAbortablePrecleanTime=6000 -XX:+CMSParallelRemarkEnabled -XX:+ParallelRefProcEnabled -XX:-OmitStackTraceInFastThrow -verbose:gc -XX:+PrintHeapAtGC -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintGCTimeStamps -XX:+PrintTenuringDistribution -XX:+PrintGCApplicationStoppedTime -Xloggc:/root/solr-6.6.0/server/logs/solr_gc.log -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=9 -XX:GCLogFileSize=20M -Dsolr.log.dir=/root/solr-6.6.0/server/logs -Djetty.port=8983 -DSTOP.PORT=7983 -DSTOP.KEY=solrrocks -Duser.timezone=UTC -Djetty.home=/root/solr-6.6.0/server -Dsolr.solr.home=/root/solr-6.6.0/server/solr -Dsolr.install.dir=/root/solr-6.6.0 -Xss256k -Dsolr.log.muteconsole -XX:OnOutOfMemory
21166 Jps -Denv.class.path=.:/usr/jdk1.8.0_172/jre/lib/rt.jar:/usr/jdk1.8.0_172/lib/dt.jar:/usr/jdk1.8.0_172/lib/tools.jar -Dapplication.home=/usr/jdk1.8.0_172 -Xms8m
