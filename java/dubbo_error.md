# dubbo

```

"D:\Program Files\Java\jdk1.8.0_161\bin\java.exe" -DSTOP.PORT=0 -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=1100 -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -DOPTIONS=jmx "-javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\lib\idea_rt.jar=8562:C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\bin" -Dfile.encoding=GBK -classpath "E:\jetty-distribution-8.1.13.v20130916-1\start.jar;D:\Program Files\Java\jdk1.8.0_161\lib\tools.jar" org.eclipse.jetty.start.Main C:\Users\edidada\AppData\Local\Temp\context7761config\contexts-config.xml
[2019-08-16 10:46:41,232] Artifact isomerization-proxy-web-1.7.0.war: Waiting for server connection to start artifact deployment...
Detected server http port: 8111
WARNING: System properties and/or JVM args set.  Consider using --dry-run or --exec
2019-08-16 10:46:44.396:WARN:oejd.ContextDeployer:ContextDeployer is deprecated. Use ContextProvider
STOP.PORT=8585
STOP.KEY=gf6edv19yry8
2019-08-16 10:46:44.404:INFO:oejs.Server:jetty-8.1.13.v20130916
2019-08-16 10:46:44.443:INFO:oejdp.ScanningAppProvider:Deployment monitor E:\jetty-distribution-8.1.13.v20130916-1\webapps at interval 1
2019-08-16 10:46:44.451:INFO:oejd.DeploymentManager:Deployable added: E:\jetty-distribution-8.1.13.v20130916-1\webapps\spdy.war
2019-08-16 10:46:44.658:INFO:oejw.WebInfConfiguration:Extract jar:file:/E:/jetty-distribution-8.1.13.v20130916-1/webapps/spdy.war!/ to C:\Users\edidada\AppData\Local\Temp\jetty-0.0.0.0-8111-spdy.war-_spdy-any-\webapp
2019-08-16 10:46:45.593:INFO:oejdp.ScanningAppProvider:Deployment monitor E:\jetty-distribution-8.1.13.v20130916-1\contexts at interval 1
2019-08-16 10:46:45.600:INFO:oejd.DeploymentManager:Deployable added: E:\jetty-distribution-8.1.13.v20130916-1\contexts\javadoc.xml
2019-08-16 10:46:45.673:INFO:oejd.DeploymentManager:Deployable added: E:\jetty-distribution-8.1.13.v20130916-1\contexts\test.xml
2019-08-16 10:46:46.020:INFO:oejw.WebInfConfiguration:Extract jar:file:/E:/jetty-distribution-8.1.13.v20130916-1/webapps/test.war!/ to C:\Users\edidada\AppData\Local\Temp\jetty-0.0.0.0-8111-test.war-_-any-\webapp
2019-08-16 10:46:49.537:INFO:oejs.TransparentProxy:TransparentProxy @ /javadoc-proxy to http://download.eclipse.org/jetty/stable-8/apidocs
2019-08-16 10:46:49.553:INFO:oejs.AbstractConnector:Started SelectChannelConnector@0.0.0.0:8111
ShutdownMonitorThread already started2019-08-16 10:46:49.554:INFO:oejs.Server:jetty-8.1.13.v20130916
Connected to server
[2019-08-16 10:46:49,579] Artifact isomerization-proxy-web-1.7.0.war: Artifact is being deployed, please wait...
2019-08-16 10:46:51.590:INFO:oejd.ContextDeployer:Deploy C:\Users\edidada\AppData\Local\Temp\context922deploy\isomerization-proxy-web-1.7.0.xml -> o.e.j.w.WebAppContext{/isomerization-proxy-web-1.7.0,null},D:\mavenrepository\201904\com\xxxx\media\platform\isomerization-proxy-web\1.7.0\isomerization-proxy-web-1.7.0.war
2019-08-16 10:46:51.855:INFO:oejw.WebInfConfiguration:Extract jar:file:/D:/mavenrepository/201904/com/xxxx/media/platform/isomerization-proxy-web/1.7.0/isomerization-proxy-web-1.7.0.war!/ to C:\Users\edidada\AppData\Local\Temp\jetty-0.0.0.0-8111-isomerization-proxy-web-1.7.0.war-_isomerization-proxy-web-1.7.0-any-\webapp
2019-08-16 10:46:55.528:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/SingleConsumerQueue.class
java.lang.ArrayIndexOutOfBoundsException: 49291
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:898)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.531:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/Async$AsyncRemovalListener.class
java.lang.ArrayIndexOutOfBoundsException: 14080
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.536:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/BoundedLocalCache$BoundedLocalAsyncCache.class
java.lang.ArrayIndexOutOfBoundsException: 41728
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.537:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/BoundedLocalCache$BoundedLocalAsyncLoadingCache.class
java.lang.ArrayIndexOutOfBoundsException: 41216
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.541:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/BoundedLocalCache$BoundedLocalLoadingCache.class
java.lang.ArrayIndexOutOfBoundsException: 52264
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.543:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/BoundedLocalCache$BoundedPolicy$BoundedRefreshAfterWrite.class
java.lang.ArrayIndexOutOfBoundsException: 2925
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.547:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/BoundedLocalCache$EntrySpliterator.class
java.lang.ArrayIndexOutOfBoundsException: 4096
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.549:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/BoundedLocalCache$KeySpliterator.class
java.lang.ArrayIndexOutOfBoundsException: 2664
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.569:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/BoundedLocalCache$ValueSpliterator.class
java.lang.ArrayIndexOutOfBoundsException: 2925
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.571:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/BoundedLocalCache.class
java.lang.ArrayIndexOutOfBoundsException: 131311
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:898)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.573:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/CacheLoader.class
java.lang.ArrayIndexOutOfBoundsException: 51966
	at org.objectweb.asm.ClassReader.readUTF8(Unknown Source)
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.577:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/Caffeine.class
java.lang.ArrayIndexOutOfBoundsException: 58817
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:898)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.595:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/LocalAsyncCache$AbstractCacheView.class
java.lang.ArrayIndexOutOfBoundsException: 37632
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.597:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/LocalAsyncCache$AsMapView.class
java.lang.ArrayIndexOutOfBoundsException: 13478
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:898)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.609:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/LocalAsyncCache$AsyncAsMapView.class
java.lang.ArrayIndexOutOfBoundsException: 22272
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.610:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/LocalAsyncCache.class
java.lang.ArrayIndexOutOfBoundsException: 51966
	at org.objectweb.asm.ClassReader.readUTF8(Unknown Source)
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.616:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/LocalAsyncLoadingCache$AsyncBulkCompleter.class
java.lang.ArrayIndexOutOfBoundsException: 2925
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.617:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/LocalAsyncLoadingCache$LoadingCacheView.class
java.lang.ArrayIndexOutOfBoundsException: 17571
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:898)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.619:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/LocalAsyncLoadingCache.class
java.lang.ArrayIndexOutOfBoundsException: 14042
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:898)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.619:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/LocalCache.class
java.lang.ArrayIndexOutOfBoundsException: 2674
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.622:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/LocalLoadingCache.class
java.lang.ArrayIndexOutOfBoundsException: 18600
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.objectweb.asm.ClassReader.<init>(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:898)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.668:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/UnboundedLocalCache$EntrySpliterator.class
java.lang.ArrayIndexOutOfBoundsException: 4970
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.670:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/UnboundedLocalCache$UnboundedLocalLoadingCache.class
java.lang.ArrayIndexOutOfBoundsException: 52264
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:55.675:WARN:oeja.AnnotationParser:Problem processing jar entry com/github/benmanes/caffeine/cache/UnboundedLocalCache.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:57.742:WARN:oeja.AnnotationParser:Problem processing jar entry com/zaxxer/hikari/metrics/micrometer/MicrometerMetricsTracker.class
java.lang.ArrayIndexOutOfBoundsException: 10024
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:57.743:WARN:oeja.AnnotationParser:Problem processing jar entry com/zaxxer/hikari/metrics/prometheus/HikariCPCollector.class
java.lang.ArrayIndexOutOfBoundsException: 26152
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:57.745:WARN:oeja.AnnotationParser:Problem processing jar entry com/zaxxer/hikari/pool/HikariPool.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:57.751:WARN:oeja.AnnotationParser:Problem processing jar entry com/zaxxer/hikari/pool/ProxyConnection$ClosedConnection.class
java.lang.ArrayIndexOutOfBoundsException: 1108
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:57.764:WARN:oeja.AnnotationParser:Problem processing jar entry com/zaxxer/hikari/util/ConcurrentBag.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:57.767:WARN:oeja.AnnotationParser:Problem processing jar entry com/zaxxer/hikari/util/PropertyElf.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:58.237:WARN:oeja.AnnotationParser:Problem processing jar entry com/xxxx/media/platform/isomerization/proxy/common/factory/ValidationResultFactory.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:58.259:WARN:oeja.AnnotationParser:Problem processing jar entry com/xxxx/media/platform/isomerization/proxy/service/accessor/HttpGetAccessor.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:58.259:WARN:oeja.AnnotationParser:Problem processing jar entry com/xxxx/media/platform/isomerization/proxy/service/accessor/HttpPostFormAccessor.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:58.261:WARN:oeja.AnnotationParser:Problem processing jar entry com/xxxx/media/platform/isomerization/proxy/service/impl/IsomerizationAccessServiceImpl.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:58.261:WARN:oeja.AnnotationParser:Problem processing jar entry com/xxxx/media/platform/isomerization/proxy/service/impl/IsomerizationGroupManagementServiceImpl.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:58.262:WARN:oeja.AnnotationParser:Problem processing jar entry com/xxxx/media/platform/isomerization/proxy/service/impl/IsomerizationManagementServiceImpl.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:58.262:WARN:oeja.AnnotationParser:Problem processing jar entry com/xxxx/media/platform/isomerization/proxy/service/impl/IsomerizationResourceCacheServiceImpl.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:58.262:WARN:oeja.AnnotationParser:Problem processing jar entry com/xxxx/media/platform/isomerization/proxy/service/impl/IsomerizationResourceGroupCacheServiceImpl.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:58.897:WARN:oeja.AnnotationParser:Problem processing jar entry META-INF/versions/9/org/apache/logging/log4j/util/StackLocator.class
java.lang.ArrayIndexOutOfBoundsException: 7266
	at org.objectweb.asm.ClassReader.readInt(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:59.707:WARN:oeja.AnnotationParser:Problem processing jar entry okhttp3/EventListener.class
java.lang.ArrayIndexOutOfBoundsException: 28160
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:59.711:WARN:oeja.AnnotationParser:Problem processing jar entry okhttp3/internal/Util.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.717:WARN:oeja.AnnotationParser:Problem processing jar entry okhttp3/Authenticator.class
java.lang.ArrayIndexOutOfBoundsException: 3584
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:59.721:WARN:oeja.AnnotationParser:Problem processing jar entry okhttp3/internal/ws/RealWebSocket.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.721:WARN:oeja.AnnotationParser:Problem processing jar entry okhttp3/CipherSuite.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.734:WARN:oeja.AnnotationParser:Problem processing jar entry okhttp3/Dns.class
java.lang.ArrayIndexOutOfBoundsException: 3175
	at org.objectweb.asm.ClassReader.readClass(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.objectweb.asm.ClassReader.accept(Unknown Source)
	at org.eclipse.jetty.annotations.AnnotationParser.scanClass(AnnotationParser.java:899)
	at org.eclipse.jetty.annotations.AnnotationParser$2.processEntry(AnnotationParser.java:857)
	at org.eclipse.jetty.webapp.JarScanner.matched(JarScanner.java:161)
	at org.eclipse.jetty.util.PatternMatcher.matchPatterns(PatternMatcher.java:100)
	at org.eclipse.jetty.util.PatternMatcher.match(PatternMatcher.java:82)
	at org.eclipse.jetty.webapp.JarScanner.scan(JarScanner.java:84)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:869)
	at org.eclipse.jetty.annotations.AnnotationParser.parse(AnnotationParser.java:884)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.parseWebInfLib(AnnotationConfiguration.java:422)
	at org.eclipse.jetty.annotations.AnnotationConfiguration.configure(AnnotationConfiguration.java:120)
	at org.eclipse.jetty.webapp.WebAppContext.configure(WebAppContext.java:468)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1237)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:46:59.737:WARN:oeja.AnnotationParser:Problem processing jar entry okhttp3/internal/connection/RealConnectionPool.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.752:WARN:oeja.AnnotationParser:Problem processing jar entry org/jboss/resteasy/plugins/providers/sse/client/SseEventSourceImpl.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.754:WARN:oeja.AnnotationParser:Problem processing jar entry org/jboss/resteasy/client/jaxrs/internal/CompletionStageRxInvokerImpl.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.764:WARN:oeja.AnnotationParser:Problem processing jar entry org/jboss/resteasy/plugins/providers/sse/client/SseEventSourceImpl$EventHandler.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.780:WARN:oeja.AnnotationParser:Problem processing jar entry org/jboss/resteasy/core/AsyncResponseConsumer$AsyncGeneralStreamingSseResponseConsumer.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.780:WARN:oeja.AnnotationParser:Problem processing jar entry org/jboss/resteasy/core/SynchronousDispatcher.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.782:WARN:oeja.AnnotationParser:Problem processing jar entry org/jboss/resteasy/core/AsyncResponseConsumer$AsyncRawStreamingResponseConsumer.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.783:WARN:oeja.AnnotationParser:Problem processing jar entry org/jboss/resteasy/core/AbstractAsynchronousResponse.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.784:WARN:oeja.AnnotationParser:Problem processing jar entry org/jboss/resteasy/core/AsyncResponseConsumer$AsyncStreamCollectorResponseConsumer.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.785:WARN:oeja.AnnotationParser:Problem processing jar entry org/jboss/resteasy/core/ResourceMethodInvoker.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.787:WARN:oeja.AnnotationParser:Problem processing jar entry org/jboss/resteasy/core/interception/ContainerResponseContextImpl.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.798:WARN:oeja.AnnotationParser:Problem processing jar entry org/jboss/resteasy/core/SynchronousExecutionContext$SynchronousAsynchronousResponse.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.806:WARN:oeja.AnnotationParser:Problem processing jar entry org/jboss/resteasy/core/AsyncResponseConsumer$AsyncStreamResponseConsumer.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.809:WARN:oeja.AnnotationParser:Problem processing jar entry org/jboss/resteasy/core/AsyncResponseConsumer$CompletionStageResponseConsumer.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.822:WARN:oeja.AnnotationParser:Problem processing jar entry org/jboss/resteasy/core/AsyncResponseConsumer.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.824:WARN:oeja.AnnotationParser:Problem processing jar entry org/jboss/resteasy/core/ServerResponseWriter.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.919:WARN:oeja.AnnotationParser:Problem processing jar entry org/jboss/resteasy/plugins/server/servlet/Servlet3AsyncHttpRequest$Servlet3ExecutionContext$Servle3AsychronousResponse.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.932:WARN:oeja.AnnotationParser:Problem processing jar entry org/jboss/resteasy/plugins/providers/sse/SseBroadcasterImpl.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:46:59.933:WARN:oeja.AnnotationParser:Problem processing jar entry org/jboss/resteasy/plugins/providers/sse/SseEventOutputImpl.class
java.lang.ArrayIndexOutOfBoundsException
2019-08-16 10:47:01.457:INFO:/7.0:No Spring WebApplicationInitializer types detected on classpath
2019-08-16 10:47:02,638 Scanner-2 ERROR MarkerPatternSelector contains an invalid element or attribute "charset"
2019-08-16 10:47:03.001:INFO:/7.0:Initializing Spring FrameworkServlet 'springMvc'
[2019-08-16 10:47:03,003][INFO][org.springframework.web.servlet.DispatcherServlet 489][55]traceLogid:[]dstTraceId:[]FrameworkServlet 'springMvc': initialization started
[2019-08-16 10:47:03,069][INFO][org.springframework.web.context.support.XmlWebApplicationContext 583][55]traceLogid:[]dstTraceId:[]Refreshing WebApplicationContext for namespace 'springMvc-servlet': startup date [Fri Aug 16 10:47:03 CST 2019]; root of context hierarchy
[2019-08-16 10:47:03,143][INFO][org.springframework.beans.factory.xml.XmlBeanDefinitionReader 317][55]traceLogid:[]dstTraceId:[]Loading XML bean definitions from class path resource [spring/spring.xml]
[2019-08-16 10:47:03,733][INFO][org.springframework.beans.factory.xml.XmlBeanDefinitionReader 317][55]traceLogid:[]dstTraceId:[]Loading XML bean definitions from file [C:\Users\edidada\AppData\Local\Temp\jetty-0.0.0.0-8111-isomerization-proxy-web-1.7.0.war-_isomerization-proxy-web-1.7.0-any-\webapp\WEB-INF\classes\spring\spring-archaius.xml]
[2019-08-16 10:47:03,753][INFO][org.springframework.beans.factory.xml.XmlBeanDefinitionReader 317][55]traceLogid:[]dstTraceId:[]Loading XML bean definitions from file [C:\Users\edidada\AppData\Local\Temp\jetty-0.0.0.0-8111-isomerization-proxy-web-1.7.0.war-_isomerization-proxy-web-1.7.0-any-\webapp\WEB-INF\classes\spring\spring-beans.xml]
[2019-08-16 10:47:03,781][INFO][org.springframework.beans.factory.xml.XmlBeanDefinitionReader 317][55]traceLogid:[]dstTraceId:[]Loading XML bean definitions from URL [jar:file:/C:/Users/edidada/AppData/Local/Temp/jetty-0.0.0.0-8111-isomerization-proxy-web-1.7.0.war-_isomerization-proxy-web-1.7.0-any-/webapp/WEB-INF/lib/micro-service-auth-provider-api-1.3.0.jar!/micro-service-auth-provider.xml]
[2019-08-16 10:47:03,845][INFO][com.alibaba.dubbo.common.logger.LoggerFactory ][55]traceLogid:[]dstTraceId:[]using logger: com.alibaba.dubbo.common.logger.log4j.Log4jLoggerAdapter
[2019-08-16 10:47:03,885][INFO][org.springframework.beans.factory.xml.XmlBeanDefinitionReader 317][55]traceLogid:[]dstTraceId:[]Loading XML bean definitions from file [C:\Users\edidada\AppData\Local\Temp\jetty-0.0.0.0-8111-isomerization-proxy-web-1.7.0.war-_isomerization-proxy-web-1.7.0-any-\webapp\WEB-INF\classes\spring\spring-dubbo-consumer.xml]
[2019-08-16 10:47:03,932][INFO][org.springframework.beans.factory.xml.XmlBeanDefinitionReader 317][55]traceLogid:[]dstTraceId:[]Loading XML bean definitions from file [C:\Users\edidada\AppData\Local\Temp\jetty-0.0.0.0-8111-isomerization-proxy-web-1.7.0.war-_isomerization-proxy-web-1.7.0-any-\webapp\WEB-INF\classes\spring\spring-dubbo-provider.xml]
[2019-08-16 10:47:03,998][INFO][org.springframework.beans.factory.xml.XmlBeanDefinitionReader 317][55]traceLogid:[]dstTraceId:[]Loading XML bean definitions from file [C:\Users\edidada\AppData\Local\Temp\jetty-0.0.0.0-8111-isomerization-proxy-web-1.7.0.war-_isomerization-proxy-web-1.7.0-any-\webapp\WEB-INF\classes\spring\spring-hikari.xml]
[2019-08-16 10:47:04,065][INFO][org.springframework.beans.factory.xml.XmlBeanDefinitionReader 317][55]traceLogid:[]dstTraceId:[]Loading XML bean definitions from file [C:\Users\edidada\AppData\Local\Temp\jetty-0.0.0.0-8111-isomerization-proxy-web-1.7.0.war-_isomerization-proxy-web-1.7.0-any-\webapp\WEB-INF\classes\spring\spring-hystrix.xml]
[2019-08-16 10:47:04,082][INFO][org.springframework.beans.factory.xml.XmlBeanDefinitionReader 317][55]traceLogid:[]dstTraceId:[]Loading XML bean definitions from file [C:\Users\edidada\AppData\Local\Temp\jetty-0.0.0.0-8111-isomerization-proxy-web-1.7.0.war-_isomerization-proxy-web-1.7.0-any-\webapp\WEB-INF\classes\spring\spring-mvc.xml]
[2019-08-16 10:47:04,202][INFO][org.springframework.beans.factory.xml.XmlBeanDefinitionReader 317][55]traceLogid:[]dstTraceId:[]Loading XML bean definitions from file [C:\Users\edidada\AppData\Local\Temp\jetty-0.0.0.0-8111-isomerization-proxy-web-1.7.0.war-_isomerization-proxy-web-1.7.0-any-\webapp\WEB-INF\classes\spring\spring-mybatis.xml]
[2019-08-16 10:47:04,261][INFO][org.springframework.beans.factory.xml.XmlBeanDefinitionReader 317][55]traceLogid:[]dstTraceId:[]Loading XML bean definitions from file [C:\Users\edidada\AppData\Local\Temp\jetty-0.0.0.0-8111-isomerization-proxy-web-1.7.0.war-_isomerization-proxy-web-1.7.0-any-\webapp\WEB-INF\classes\spring\spring-redis.xml]
[2019-08-16 10:47:06,358][INFO][com.zaxxer.hikari.HikariDataSource 80][55]traceLogid:[]dstTraceId:[]springHikariCP - Starting...
[2019-08-16 10:47:06,741][INFO][com.zaxxer.hikari.HikariDataSource 82][55]traceLogid:[]dstTraceId:[]springHikariCP - Start completed.
八月 16, 2019 10:47:08 上午 redis.clients.jedis.JedisSentinelPool initSentinels
信息: Trying to find master from available Sentinels...
八月 16, 2019 10:47:08 上午 redis.clients.jedis.JedisSentinelPool initSentinels
信息: Redis master running at 172.17.46.11:26380, starting Sentinel listeners...
八月 16, 2019 10:47:08 上午 redis.clients.jedis.JedisSentinelPool initPool
信息: Created JedisPool to master at 172.17.46.11:26380
[2019-08-16 10:47:09,623][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 203][55]traceLogid:[]dstTraceId:[] [DUBBO] Load registry store file C:\Users\edidada\.dubbo\dubbo-registry-isomerization-proxy-127.0.0.1:2181.cache, data: {com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService=empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=configurators&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=23020&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565873105347 empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=23020&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565873105347 empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=23020&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565873105347, com.xxxx.media.platform.isomerization.proxy.api.IsomerizationGroupManagementService=empty://10.0.75.1:20800/com.xxxx.media.platform.isomerization.proxy.api.IsomerizationGroupManagementService?anyhost=true&application=isomerization-proxy&category=configurators&check=false&dispatcher=message&dubbo=2.5.8&generic=false&interface=com.xxxx.media.platform.isomerization.proxy.api.IsomerizationGroupManagementService&methods=add,get,update,remove&pid=23020&revision=1.7.0&side=provider&threads=500&timestamp=1565873113613, com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService=empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=configurators&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=23020&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565873104711 empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=23020&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565873104711 empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=23020&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565873104711, com.xxxx.media.platform.isomerization.proxy.api.IsomerizationManagementService=empty://10.0.75.1:20800/com.xxxx.media.platform.isomerization.proxy.api.IsomerizationManagementService?anyhost=true&application=isomerization-proxy&category=configurators&check=false&dispatcher=message&dubbo=2.5.8&generic=false&interface=com.xxxx.media.platform.isomerization.proxy.api.IsomerizationManagementService&methods=add,protocolList,get,update,remove&pid=23020&revision=1.7.0&side=provider&threads=500&timestamp=1565873113554, com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService=empty://10.0.75.1:20800/com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService?anyhost=true&application=isomerization-proxy&category=configurators&check=false&dispatcher=message&dubbo=2.5.8&generic=false&interface=com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService&methods=access,accessHttp&pid=23020&revision=1.7.0&side=provider&threads=500&timestamp=1565873113259}, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:09,633][INFO][com.alibaba.dubbo.common.concurrent.ExecutionList 76][55]traceLogid:[]dstTraceId:[] [DUBBO] Executor for listenablefuture is null, will use default executor!, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:09,646][INFO][org.I0Itec.zkclient.ZkEventThread 64][117]traceLogid:[]dstTraceId:[]Starting ZkClient event thread.
[2019-08-16 10:47:09,659][INFO][org.apache.zookeeper.ZooKeeper 100][116]traceLogid:[]dstTraceId:[]Client environment:zookeeper.version=3.4.6-1569965, built on 02/20/2014 09:09 GMT
[2019-08-16 10:47:09,659][INFO][org.apache.zookeeper.ZooKeeper 100][116]traceLogid:[]dstTraceId:[]Client environment:host.name=windows10.microdone.cn
[2019-08-16 10:47:09,659][INFO][org.apache.zookeeper.ZooKeeper 100][116]traceLogid:[]dstTraceId:[]Client environment:java.version=1.8.0_161
[2019-08-16 10:47:09,659][INFO][org.apache.zookeeper.ZooKeeper 100][116]traceLogid:[]dstTraceId:[]Client environment:java.vendor=Oracle Corporation
[2019-08-16 10:47:09,659][INFO][org.apache.zookeeper.ZooKeeper 100][116]traceLogid:[]dstTraceId:[]Client environment:java.home=D:\Program Files\Java\jdk1.8.0_161\jre
[2019-08-16 10:47:09,659][INFO][org.apache.zookeeper.ZooKeeper 100][116]traceLogid:[]dstTraceId:[]Client environment:java.class.path=E:\jetty-distribution-8.1.13.v20130916-1\lib\jetty-xml-8.1.13.v20130916.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\servlet-api-3.0.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jetty-http-8.1.13.v20130916.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jetty-continuation-8.1.13.v20130916.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jetty-server-8.1.13.v20130916.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jetty-security-8.1.13.v20130916.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jetty-servlet-8.1.13.v20130916.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jetty-webapp-8.1.13.v20130916.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jetty-deploy-8.1.13.v20130916.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jetty-servlets-8.1.13.v20130916.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jetty-annotations-8.1.13.v20130916.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\annotations\javax.annotation-1.1.0.v201108011116.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\annotations\org.objectweb.asm-3.1.0.v200803061910.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jetty-jmx-8.1.13.v20130916.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jsp\com.sun.el-2.2.0.v201108011116.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jsp\javax.el-2.2.0.v201108011116.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jsp\javax.servlet.jsp.jstl-1.2.0.v201105211821.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jsp\javax.servlet.jsp-2.2.0.v201112011158.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jsp\org.apache.jasper.glassfish-2.2.2.v201112011158.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jsp\org.apache.taglibs.standard.glassfish-1.2.0.v201112081803.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jsp\org.eclipse.jdt.core-3.7.1.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jetty-jndi-8.1.13.v20130916.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jetty-plus-8.1.13.v20130916.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jndi\javax.activation-1.1.0.v201105071233.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jndi\javax.mail.glassfish-1.4.1.v201005082020.jar;E:\jetty-distribution-8.1.13.v20130916-1\resources;E:\jetty-distribution-8.1.13.v20130916-1\lib\jetty-websocket-8.1.13.v20130916.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jetty-util-8.1.13.v20130916.jar;E:\jetty-distribution-8.1.13.v20130916-1\lib\jetty-io-8.1.13.v20130916.jar
[2019-08-16 10:47:09,659][INFO][org.apache.zookeeper.ZooKeeper 100][116]traceLogid:[]dstTraceId:[]Client environment:java.library.path=D:\Program Files\Java\jdk1.8.0_161\bin;C:\WINDOWS\Sun\Java\bin;C:\WINDOWS\system32;C:\WINDOWS;C:\Python27\;C:\Python27\Scripts;C:\Users\edidada\.cargo\bin;E:\etcd-v3.3.12-windows-amd64;D:\Program Files\Java\jdk1.8.0_161\bin;G:\apache-jmeter-4.0\bin;C:\Program Files (x86)\Common Files\Oracle\Java\javapath;D:\kubernetes;C:\Program Files\Docker Toolbox\netcat-1.11;C:\Program Files\Docker Toolbox;D:\zookeeper-3.4.10\bin;G:\cmake-3.12.0-win64-x64\bin;E:\gradle-3.5.1\bin;C:\Program Files\qemu;E:\apache-maven-3.6.1\bin;C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\bin;C:\ProgramData\Chocolatey\lib\chocolatey;D:\android-ndk-r10b;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;D:\android-sdk-windows\platform-tools;D:\android-sdk-windows\tools;D:\MinGW\bin;D:\Program Files\ffmpeg-win64-static\bin;C:\Program Files\PuTTY\;D:\mysql-5.7.17-winx64\bin;D:\opencv\build\x64\vc14\bin;C:\Program Files (x86)\WinSCP\;C:\Program Files\Microsoft SQL Server\130\Tools\Binn\;C:\Program Files (x86)\Windows Kits\10\Windows Performance Toolkit\;D:\springbotcli\spring-1.3.0.RELEASE\bin;C:\Program Files\Git\cmd;D:\apktool;C:\WINDOWS\System32\OpenSSH\;G:\node-v8.11.3-win-x64;C:\Program Files\erl9.0\bi;E:\apache-ant-1.10.5\bin;E:\tiancheng\20190311\jna\test\com\sun\jna\win32-x86-64;D:\Program Files\Java\jdk1.8.0_161\jre\bin;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\WINDOWS\System32\OpenSSH\;C:\Go\bin;D:\antlr;C:\Program Files\Sublime Text 3;D:\vert.x-3.7.1-full\vertx\bin;D:\groovy-2.5.7\bin;C:\Users\edidada\.cargo\bin;d:\Ruby24-x64\bin;C:\Users\edidada\AppData\Local\Microsoft\WindowsApps;;C:\Users\edidada\AppData\Local\Microsoft\WindowsApps;C:\Program Files\JetBrains\CLion 2019.1.2\bin;;C:\Users\edidada\go\bin;C:\Program Files\JetBrains\GoLand 2019.1.1\bin;;C:\Program Files\JetBrains\DataGrip 2019.1.2\bin;;.
[2019-08-16 10:47:09,659][INFO][org.apache.zookeeper.ZooKeeper 100][116]traceLogid:[]dstTraceId:[]Client environment:java.io.tmpdir=C:\Users\edidada\AppData\Local\Temp\
[2019-08-16 10:47:09,659][INFO][org.apache.zookeeper.ZooKeeper 100][116]traceLogid:[]dstTraceId:[]Client environment:java.compiler=<NA>
[2019-08-16 10:47:09,659][INFO][org.apache.zookeeper.ZooKeeper 100][116]traceLogid:[]dstTraceId:[]Client environment:os.name=Windows 10
[2019-08-16 10:47:09,659][INFO][org.apache.zookeeper.ZooKeeper 100][116]traceLogid:[]dstTraceId:[]Client environment:os.arch=amd64
[2019-08-16 10:47:09,660][INFO][org.apache.zookeeper.ZooKeeper 100][116]traceLogid:[]dstTraceId:[]Client environment:os.version=10.0
[2019-08-16 10:47:09,660][INFO][org.apache.zookeeper.ZooKeeper 100][116]traceLogid:[]dstTraceId:[]Client environment:user.name=edidada
[2019-08-16 10:47:09,660][INFO][org.apache.zookeeper.ZooKeeper 100][116]traceLogid:[]dstTraceId:[]Client environment:user.home=C:\Users\edidada
[2019-08-16 10:47:09,661][INFO][org.apache.zookeeper.ZooKeeper 100][116]traceLogid:[]dstTraceId:[]Client environment:user.dir=E:\jetty-distribution-8.1.13.v20130916-1
[2019-08-16 10:47:09,662][INFO][org.apache.zookeeper.ZooKeeper 438][116]traceLogid:[]dstTraceId:[]Initiating client connection, connectString=127.0.0.1:2181 sessionTimeout=30000 watcher=org.I0Itec.zkclient.ZkClient@5078a5bb
[2019-08-16 10:47:09,694][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:10,697][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:11,800][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:12,814][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:13,916][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:14,918][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:16,019][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:17,022][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:18,123][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:19,125][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:20,226][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:21,229][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:22,330][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:23,332][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:24,434][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:25,437][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:26,537][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:27,538][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:28,639][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:29,641][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:30,743][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:31,745][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:32,846][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:33,849][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:34,949][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:35,951][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:37,052][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:38,057][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:39,157][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:39,636][ERROR][com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper 53][55]traceLogid:[]dstTraceId:[] [DUBBO] Timeout! zookeeper server can not be connected in : 30000ms!, dubbo version: 2.5.8, current host: 10.0.75.1
java.util.concurrent.TimeoutException: null
	at java.util.concurrent.FutureTask.get(FutureTask.java:205) ~[?:1.8.0_161]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.start(ZkClientWrapper.java:51) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.<init>(ZkclientZookeeperClient.java:39) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperTransporter.connect(ZkclientZookeeperTransporter.java:10) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.ZookeeperTransporter$Adaptive.connect(ZookeeperTransporter$Adaptive.java) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.<init>(ZookeeperRegistry.java:69) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistryFactory.createRegistry(ZookeeperRegistryFactory.java:37) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.AbstractRegistryFactory.getRegistry(AbstractRegistryFactory.java:95) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.RegistryFactory$Adaptive.getRegistry(RegistryFactory$Adaptive.java) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.refer(RegistryProtocol.java:282) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.rpc.protocol.ProtocolListenerWrapper.refer(ProtocolListenerWrapper.java:76) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.rpc.protocol.ProtocolFilterWrapper.refer(ProtocolFilterWrapper.java:99) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.rpc.Protocol$Adaptive.refer(Protocol$Adaptive.java) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.ReferenceConfig.createProxy(ReferenceConfig.java:395) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.ReferenceConfig.init(ReferenceConfig.java:334) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.ReferenceConfig.get(ReferenceConfig.java:163) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.spring.ReferenceBean.getObject(ReferenceBean.java:59) ~[dubbo-2.5.8.jar:2.5.8]
	at org.springframework.beans.factory.support.FactoryBeanRegistrySupport.doGetObjectFromFactoryBean(FactoryBeanRegistrySupport.java:168) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.FactoryBeanRegistrySupport.getObjectFromFactoryBean(FactoryBeanRegistrySupport.java:103) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getObjectForBeanInstance(AbstractBeanFactory.java:1634) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:254) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:202) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:208) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.addCandidateEntry(DefaultListableBeanFactory.java:1316) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.findAutowireCandidates(DefaultListableBeanFactory.java:1282) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1101) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1066) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:585) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:88) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessPropertyValues(AutowiredAnnotationBeanPostProcessor.java:366) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1264) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:553) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:483) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:306) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:230) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:302) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:197) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:761) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:867) ~[spring-context-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:543) ~[spring-context-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:668) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:634) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:682) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:553) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:494) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:171) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at javax.servlet.GenericServlet.init(GenericServlet.java:244) ~[servlet-api-3.0.jar:?]
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:534) ~[?:?]
	at org.eclipse.jetty.servlet.ServletHolder.doStart(ServletHolder.java:346) ~[?:?]
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64) ~[?:?]
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:786) ~[?:?]
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:265) ~[?:?]
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1242) ~[?:?]
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717) ~[?:?]
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494) ~[?:?]
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64) ~[?:?]
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359) ~[?:?]
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82) ~[?:?]
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107) ~[?:?]
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615) ~[?:?]
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540) ~[?:?]
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403) ~[?:?]
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353) ~[?:?]
	at java.util.TimerThread.mainLoop(Timer.java:555) ~[?:1.8.0_161]
	at java.util.TimerThread.run(Timer.java:505) ~[?:1.8.0_161]
[2019-08-16 10:47:39,714][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 273][55]traceLogid:[]dstTraceId:[] [DUBBO] Register: consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:39,716][ERROR][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 151][55]traceLogid:[]dstTraceId:[] [DUBBO] Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541, waiting for retry, cause: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:112) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.register(FailbackRegistry.java:136) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.doRefer(RegistryProtocol.java:312) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.refer(RegistryProtocol.java:296) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.rpc.protocol.ProtocolListenerWrapper.refer(ProtocolListenerWrapper.java:76) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.rpc.protocol.ProtocolFilterWrapper.refer(ProtocolFilterWrapper.java:99) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.rpc.Protocol$Adaptive.refer(Protocol$Adaptive.java) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.ReferenceConfig.createProxy(ReferenceConfig.java:395) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.ReferenceConfig.init(ReferenceConfig.java:334) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.ReferenceConfig.get(ReferenceConfig.java:163) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.spring.ReferenceBean.getObject(ReferenceBean.java:59) ~[dubbo-2.5.8.jar:2.5.8]
	at org.springframework.beans.factory.support.FactoryBeanRegistrySupport.doGetObjectFromFactoryBean(FactoryBeanRegistrySupport.java:168) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.FactoryBeanRegistrySupport.getObjectFromFactoryBean(FactoryBeanRegistrySupport.java:103) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getObjectForBeanInstance(AbstractBeanFactory.java:1634) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:254) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:202) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:208) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.addCandidateEntry(DefaultListableBeanFactory.java:1316) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.findAutowireCandidates(DefaultListableBeanFactory.java:1282) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1101) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1066) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:585) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:88) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessPropertyValues(AutowiredAnnotationBeanPostProcessor.java:366) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1264) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:553) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:483) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:306) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:230) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:302) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:197) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:761) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:867) ~[spring-context-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:543) ~[spring-context-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:668) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:634) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:682) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:553) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:494) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:171) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at javax.servlet.GenericServlet.init(GenericServlet.java:244) ~[servlet-api-3.0.jar:?]
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:534) ~[?:?]
	at org.eclipse.jetty.servlet.ServletHolder.doStart(ServletHolder.java:346) ~[?:?]
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64) ~[?:?]
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:786) ~[?:?]
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:265) ~[?:?]
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1242) ~[?:?]
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717) ~[?:?]
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494) ~[?:?]
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64) ~[?:?]
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359) ~[?:?]
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82) ~[?:?]
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107) ~[?:?]
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615) ~[?:?]
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540) ~[?:?]
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403) ~[?:?]
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353) ~[?:?]
	at java.util.TimerThread.mainLoop(Timer.java:555) ~[?:1.8.0_161]
	at java.util.TimerThread.run(Timer.java:505) ~[?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:110) ~[dubbo-2.5.8.jar:2.5.8]
	... 58 more
[2019-08-16 10:47:39,716][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 296][55]traceLogid:[]dstTraceId:[] [DUBBO] Subscribe: consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:39,719][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 384][55]traceLogid:[]dstTraceId:[] [DUBBO] Notify urls for subscribe url consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541, urls: [empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=configurators&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=23020&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565873104711, empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=23020&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565873104711, empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=23020&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565873104711], dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:39,721][ERROR][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 208][55]traceLogid:[]dstTraceId:[] [DUBBO] Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541, Using cached list: [empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=configurators&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=23020&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565873104711, empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=23020&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565873104711, empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=23020&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565873104711] from cache file: C:\Users\edidada/dubbo-registry-10.0.75.1.cache, cause: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:185) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.subscribe(FailbackRegistry.java:201) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.integration.RegistryDirectory.subscribe(RegistryDirectory.java:159) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.doRefer(RegistryProtocol.java:315) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.refer(RegistryProtocol.java:296) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.rpc.protocol.ProtocolListenerWrapper.refer(ProtocolListenerWrapper.java:76) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.rpc.protocol.ProtocolFilterWrapper.refer(ProtocolFilterWrapper.java:99) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.rpc.Protocol$Adaptive.refer(Protocol$Adaptive.java) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.ReferenceConfig.createProxy(ReferenceConfig.java:395) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.ReferenceConfig.init(ReferenceConfig.java:334) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.ReferenceConfig.get(ReferenceConfig.java:163) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.spring.ReferenceBean.getObject(ReferenceBean.java:59) ~[dubbo-2.5.8.jar:2.5.8]
	at org.springframework.beans.factory.support.FactoryBeanRegistrySupport.doGetObjectFromFactoryBean(FactoryBeanRegistrySupport.java:168) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.FactoryBeanRegistrySupport.getObjectFromFactoryBean(FactoryBeanRegistrySupport.java:103) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getObjectForBeanInstance(AbstractBeanFactory.java:1634) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:254) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:202) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:208) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.addCandidateEntry(DefaultListableBeanFactory.java:1316) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.findAutowireCandidates(DefaultListableBeanFactory.java:1282) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1101) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1066) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:585) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:88) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessPropertyValues(AutowiredAnnotationBeanPostProcessor.java:366) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1264) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:553) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:483) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:306) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:230) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:302) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:197) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:761) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:867) ~[spring-context-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:543) ~[spring-context-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:668) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:634) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:682) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:553) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:494) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:171) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at javax.servlet.GenericServlet.init(GenericServlet.java:244) ~[servlet-api-3.0.jar:?]
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:534) ~[?:?]
	at org.eclipse.jetty.servlet.ServletHolder.doStart(ServletHolder.java:346) ~[?:?]
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64) ~[?:?]
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:786) ~[?:?]
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:265) ~[?:?]
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1242) ~[?:?]
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717) ~[?:?]
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494) ~[?:?]
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64) ~[?:?]
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359) ~[?:?]
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82) ~[?:?]
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107) ~[?:?]
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615) ~[?:?]
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540) ~[?:?]
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403) ~[?:?]
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353) ~[?:?]
	at java.util.TimerThread.mainLoop(Timer.java:555) ~[?:1.8.0_161]
	at java.util.TimerThread.run(Timer.java:505) ~[?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:176) ~[dubbo-2.5.8.jar:2.5.8]
	... 59 more
[2019-08-16 10:47:39,728][INFO][com.alibaba.dubbo.config.AbstractConfig 426][55]traceLogid:[]dstTraceId:[] [DUBBO] Refer dubbo service com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService from url zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&register.ip=10.0.75.1&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:40,126][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 273][55]traceLogid:[]dstTraceId:[] [DUBBO] Register: consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:40,127][ERROR][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 151][55]traceLogid:[]dstTraceId:[] [DUBBO] Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, waiting for retry, cause: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:112) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.register(FailbackRegistry.java:136) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.doRefer(RegistryProtocol.java:312) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.refer(RegistryProtocol.java:296) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.rpc.protocol.ProtocolListenerWrapper.refer(ProtocolListenerWrapper.java:76) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.rpc.protocol.ProtocolFilterWrapper.refer(ProtocolFilterWrapper.java:99) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.rpc.Protocol$Adaptive.refer(Protocol$Adaptive.java) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.ReferenceConfig.createProxy(ReferenceConfig.java:395) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.ReferenceConfig.init(ReferenceConfig.java:334) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.ReferenceConfig.get(ReferenceConfig.java:163) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.spring.ReferenceBean.getObject(ReferenceBean.java:59) ~[dubbo-2.5.8.jar:2.5.8]
	at org.springframework.beans.factory.support.FactoryBeanRegistrySupport.doGetObjectFromFactoryBean(FactoryBeanRegistrySupport.java:168) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.FactoryBeanRegistrySupport.getObjectFromFactoryBean(FactoryBeanRegistrySupport.java:103) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getObjectForBeanInstance(AbstractBeanFactory.java:1634) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:254) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:197) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.BeanDefinitionValueResolver.resolveReference(BeanDefinitionValueResolver.java:351) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.BeanDefinitionValueResolver.resolveValueIfNecessary(BeanDefinitionValueResolver.java:108) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.resolveConstructorArguments(ConstructorResolver.java:648) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.autowireConstructor(ConstructorResolver.java:145) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireConstructor(AbstractAutowireCapableBeanFactory.java:1193) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1095) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:513) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:483) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:306) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:230) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:302) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:197) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:761) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:867) ~[spring-context-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:543) ~[spring-context-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:668) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:634) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:682) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:553) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:494) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:171) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at javax.servlet.GenericServlet.init(GenericServlet.java:244) ~[servlet-api-3.0.jar:?]
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:534) ~[?:?]
	at org.eclipse.jetty.servlet.ServletHolder.doStart(ServletHolder.java:346) ~[?:?]
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64) ~[?:?]
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:786) ~[?:?]
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:265) ~[?:?]
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1242) ~[?:?]
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717) ~[?:?]
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494) ~[?:?]
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64) ~[?:?]
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359) ~[?:?]
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82) ~[?:?]
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107) ~[?:?]
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615) ~[?:?]
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540) ~[?:?]
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403) ~[?:?]
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353) ~[?:?]
	at java.util.TimerThread.mainLoop(Timer.java:555) ~[?:1.8.0_161]
	at java.util.TimerThread.run(Timer.java:505) ~[?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:110) ~[dubbo-2.5.8.jar:2.5.8]
	... 55 more
[2019-08-16 10:47:40,137][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 296][55]traceLogid:[]dstTraceId:[] [DUBBO] Subscribe: consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:40,139][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 384][55]traceLogid:[]dstTraceId:[] [DUBBO] Notify urls for subscribe url consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, urls: [empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=configurators&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=23020&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565873105347, empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=23020&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565873105347, empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=23020&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565873105347], dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:40,140][ERROR][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 208][55]traceLogid:[]dstTraceId:[] [DUBBO] Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, Using cached list: [empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=configurators&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=23020&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565873105347, empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=23020&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565873105347, empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=23020&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565873105347] from cache file: C:\Users\edidada/dubbo-registry-10.0.75.1.cache, cause: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:185) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.subscribe(FailbackRegistry.java:201) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.integration.RegistryDirectory.subscribe(RegistryDirectory.java:159) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.doRefer(RegistryProtocol.java:315) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.refer(RegistryProtocol.java:296) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.rpc.protocol.ProtocolListenerWrapper.refer(ProtocolListenerWrapper.java:76) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.rpc.protocol.ProtocolFilterWrapper.refer(ProtocolFilterWrapper.java:99) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.rpc.Protocol$Adaptive.refer(Protocol$Adaptive.java) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.ReferenceConfig.createProxy(ReferenceConfig.java:395) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.ReferenceConfig.init(ReferenceConfig.java:334) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.ReferenceConfig.get(ReferenceConfig.java:163) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.spring.ReferenceBean.getObject(ReferenceBean.java:59) ~[dubbo-2.5.8.jar:2.5.8]
	at org.springframework.beans.factory.support.FactoryBeanRegistrySupport.doGetObjectFromFactoryBean(FactoryBeanRegistrySupport.java:168) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.FactoryBeanRegistrySupport.getObjectFromFactoryBean(FactoryBeanRegistrySupport.java:103) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getObjectForBeanInstance(AbstractBeanFactory.java:1634) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:254) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:197) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.BeanDefinitionValueResolver.resolveReference(BeanDefinitionValueResolver.java:351) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.BeanDefinitionValueResolver.resolveValueIfNecessary(BeanDefinitionValueResolver.java:108) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.resolveConstructorArguments(ConstructorResolver.java:648) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.autowireConstructor(ConstructorResolver.java:145) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireConstructor(AbstractAutowireCapableBeanFactory.java:1193) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1095) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:513) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:483) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:306) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:230) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:302) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:197) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:761) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:867) ~[spring-context-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:543) ~[spring-context-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:668) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:634) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:682) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:553) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:494) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:171) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at javax.servlet.GenericServlet.init(GenericServlet.java:244) ~[servlet-api-3.0.jar:?]
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:534) ~[?:?]
	at org.eclipse.jetty.servlet.ServletHolder.doStart(ServletHolder.java:346) ~[?:?]
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64) ~[?:?]
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:786) ~[?:?]
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:265) ~[?:?]
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1242) ~[?:?]
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717) ~[?:?]
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494) ~[?:?]
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64) ~[?:?]
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359) ~[?:?]
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82) ~[?:?]
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107) ~[?:?]
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615) ~[?:?]
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540) ~[?:?]
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403) ~[?:?]
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353) ~[?:?]
	at java.util.TimerThread.mainLoop(Timer.java:555) ~[?:1.8.0_161]
	at java.util.TimerThread.run(Timer.java:505) ~[?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:176) ~[dubbo-2.5.8.jar:2.5.8]
	... 56 more
[2019-08-16 10:47:40,140][INFO][com.alibaba.dubbo.config.AbstractConfig 426][55]traceLogid:[]dstTraceId:[] [DUBBO] Refer dubbo service com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService from url zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&register.ip=10.0.75.1&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:40,159][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:41,267][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:41,436][INFO][org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping 543][55]traceLogid:[]dstTraceId:[]Mapped "{[/healthcheck.html]}" onto public java.lang.Object com.xxxx.media.platform.isomerization.proxy.web.controller.HealthCheckController.healthCheck()
[2019-08-16 10:47:41,437][INFO][org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping 543][55]traceLogid:[]dstTraceId:[]Mapped "{[/checkmerchantbillinfo.html]}" onto public java.lang.Object com.xxxx.media.platform.isomerization.proxy.web.controller.TestOcrCheckMerchantBillInfoController.checkMerchantBillInfo()
[2019-08-16 10:47:41,438][INFO][org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping 543][55]traceLogid:[]dstTraceId:[]Mapped "{[/checkpersonbillinfo2.html]}" onto public java.lang.Object com.xxxx.media.platform.isomerization.proxy.web.controller.TestOcrCheckMerchantBillInfoController.checkPersonBillInfo2()
[2019-08-16 10:47:41,438][INFO][org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping 543][55]traceLogid:[]dstTraceId:[]Mapped "{[/checkmerchantbillinfo2.html]}" onto public java.lang.Object com.xxxx.media.platform.isomerization.proxy.web.controller.TestOcrCheckMerchantBillInfoController.checkMerchantBillInfo2()
[2019-08-16 10:47:41,438][INFO][org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping 543][55]traceLogid:[]dstTraceId:[]Mapped "{[/pingmerchantbillinfo.html]}" onto public java.lang.Object com.xxxx.media.platform.isomerization.proxy.web.controller.TestOcrCheckMerchantBillInfoController.ping()
[2019-08-16 10:47:41,786][INFO][org.hibernate.validator.internal.util.Version 30][55]traceLogid:[]dstTraceId:[]HV000001: Hibernate Validator 5.4.2.Final
[2019-08-16 10:47:42,273][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:43,374][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:44,378][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:44,635][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 324][115]traceLogid:[]dstTraceId:[] [DUBBO] Retry register [consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541], dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:44,636][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 332][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry register [consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541], waiting for again, cause: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:112) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:329) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:110) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:47:44,639][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 332][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry register [consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541], waiting for again, cause: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:112) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:329) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:110) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:47:44,639][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 369][115]traceLogid:[]dstTraceId:[] [DUBBO] Retry subscribe {consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541=[com.alibaba.dubbo.registry.integration.RegistryDirectory@4223b03e], consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110=[com.alibaba.dubbo.registry.integration.RegistryDirectory@13837e72]}, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:44,639][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 380][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry subscribe {consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541=[com.alibaba.dubbo.registry.integration.RegistryDirectory@4223b03e], consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110=[com.alibaba.dubbo.registry.integration.RegistryDirectory@13837e72]}, waiting for again, cause: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:185) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:377) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:176) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:47:44,641][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 380][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry subscribe {consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541=[com.alibaba.dubbo.registry.integration.RegistryDirectory@4223b03e], consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110=[com.alibaba.dubbo.registry.integration.RegistryDirectory@13837e72]}, waiting for again, cause: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:185) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:377) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:176) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:47:44,679][INFO][org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter 534][55]traceLogid:[]dstTraceId:[]Looking for @ControllerAdvice: WebApplicationContext for namespace 'springMvc-servlet': startup date [Fri Aug 16 10:47:03 CST 2019]; root of context hierarchy
[2019-08-16 10:47:45,323][INFO][org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter 534][55]traceLogid:[]dstTraceId:[]Looking for @ControllerAdvice: WebApplicationContext for namespace 'springMvc-servlet': startup date [Fri Aug 16 10:47:03 CST 2019]; root of context hierarchy
[2019-08-16 10:47:45,479][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
2019-08-16 10:47:47.742:WARN:/7.0:unavailable
java.lang.IllegalStateException: Failed to register dubbo://10.0.75.1:20800/com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService?anyhost=true&application=isomerization-proxy&dispatcher=message&dubbo=2.5.8&generic=false&interface=com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService&methods=access,accessHttp&pid=15340&revision=1.7.0&side=provider&threads=500&timestamp=1565923667102 to registry 127.0.0.1:2181, cause: Failed to register dubbo://10.0.75.1:20800/com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService?anyhost=true&application=isomerization-proxy&dispatcher=message&dubbo=2.5.8&generic=false&interface=com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService&methods=access,accessHttp&pid=15340&revision=1.7.0&side=provider&threads=500&timestamp=1565923667102 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.support.FailbackRegistry.register(FailbackRegistry.java:149)
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.register(RegistryProtocol.java:117)
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.export(RegistryProtocol.java:136)
	at com.alibaba.dubbo.rpc.protocol.ProtocolListenerWrapper.export(ProtocolListenerWrapper.java:67)
	at com.alibaba.dubbo.rpc.protocol.ProtocolFilterWrapper.export(ProtocolFilterWrapper.java:92)
	at com.alibaba.dubbo.rpc.Protocol$Adaptive.export(Protocol$Adaptive.java)
	at com.alibaba.dubbo.config.ServiceConfig.doExportUrlsFor1Protocol(ServiceConfig.java:504)
	at com.alibaba.dubbo.config.ServiceConfig.doExportUrls(ServiceConfig.java:356)
	at com.alibaba.dubbo.config.ServiceConfig.doExport(ServiceConfig.java:315)
	at com.alibaba.dubbo.config.ServiceConfig.export(ServiceConfig.java:214)
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:113)
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:42)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.doInvokeListener(SimpleApplicationEventMulticaster.java:172)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.invokeListener(SimpleApplicationEventMulticaster.java:165)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.multicastEvent(SimpleApplicationEventMulticaster.java:139)
	at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:393)
	at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:347)
	at org.springframework.context.support.AbstractApplicationContext.finishRefresh(AbstractApplicationContext.java:883)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:546)
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:668)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:634)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:682)
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:553)
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:494)
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:171)
	at javax.servlet.GenericServlet.init(GenericServlet.java:244)
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:534)
	at org.eclipse.jetty.servlet.ServletHolder.doStart(ServletHolder.java:346)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:786)
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:265)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1242)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
Caused by: 
com.alibaba.dubbo.rpc.RpcException: Failed to register dubbo://10.0.75.1:20800/com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService?anyhost=true&application=isomerization-proxy&dispatcher=message&dubbo=2.5.8&generic=false&interface=com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService&methods=access,accessHttp&pid=15340&revision=1.7.0&side=provider&threads=500&timestamp=1565923667102 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:112)
	at com.alibaba.dubbo.registry.support.FailbackRegistry.register(FailbackRegistry.java:136)
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.register(RegistryProtocol.java:117)
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.export(RegistryProtocol.java:136)
	at com.alibaba.dubbo.rpc.protocol.ProtocolListenerWrapper.export(ProtocolListenerWrapper.java:67)
	at com.alibaba.dubbo.rpc.protocol.ProtocolFilterWrapper.export(ProtocolFilterWrapper.java:92)
	at com.alibaba.dubbo.rpc.Protocol$Adaptive.export(Protocol$Adaptive.java)
	at com.alibaba.dubbo.config.ServiceConfig.doExportUrlsFor1Protocol(ServiceConfig.java:504)
	at com.alibaba.dubbo.config.ServiceConfig.doExportUrls(ServiceConfig.java:356)
	at com.alibaba.dubbo.config.ServiceConfig.doExport(ServiceConfig.java:315)
	at com.alibaba.dubbo.config.ServiceConfig.export(ServiceConfig.java:214)
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:113)
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:42)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.doInvokeListener(SimpleApplicationEventMulticaster.java:172)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.invokeListener(SimpleApplicationEventMulticaster.java:165)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.multicastEvent(SimpleApplicationEventMulticaster.java:139)
	at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:393)
	at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:347)
	at org.springframework.context.support.AbstractApplicationContext.finishRefresh(AbstractApplicationContext.java:883)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:546)
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:668)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:634)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:682)
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:553)
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:494)
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:171)
	at javax.servlet.GenericServlet.init(GenericServlet.java:244)
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:534)
	at org.eclipse.jetty.servlet.ServletHolder.doStart(ServletHolder.java:346)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:786)
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:265)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1242)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
Caused by: 
java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82)
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45)
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47)
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41)
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41)
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41)
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:110)
	at com.alibaba.dubbo.registry.support.FailbackRegistry.register(FailbackRegistry.java:136)
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.register(RegistryProtocol.java:117)
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.export(RegistryProtocol.java:136)
	at com.alibaba.dubbo.rpc.protocol.ProtocolListenerWrapper.export(ProtocolListenerWrapper.java:67)
	at com.alibaba.dubbo.rpc.protocol.ProtocolFilterWrapper.export(ProtocolFilterWrapper.java:92)
	at com.alibaba.dubbo.rpc.Protocol$Adaptive.export(Protocol$Adaptive.java)
	at com.alibaba.dubbo.config.ServiceConfig.doExportUrlsFor1Protocol(ServiceConfig.java:504)
	at com.alibaba.dubbo.config.ServiceConfig.doExportUrls(ServiceConfig.java:356)
	at com.alibaba.dubbo.config.ServiceConfig.doExport(ServiceConfig.java:315)
	at com.alibaba.dubbo.config.ServiceConfig.export(ServiceConfig.java:214)
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:113)
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:42)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.doInvokeListener(SimpleApplicationEventMulticaster.java:172)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.invokeListener(SimpleApplicationEventMulticaster.java:165)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.multicastEvent(SimpleApplicationEventMulticaster.java:139)
	at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:393)
	at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:347)
	at org.springframework.context.support.AbstractApplicationContext.finishRefresh(AbstractApplicationContext.java:883)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:546)
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:668)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:634)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:682)
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:553)
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:494)
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:171)
	at javax.servlet.GenericServlet.init(GenericServlet.java:244)
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:534)
	at org.eclipse.jetty.servlet.ServletHolder.doStart(ServletHolder.java:346)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:786)
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:265)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1242)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:47:48.254:WARN:oejuc.AbstractLifeCycle:FAILED springMvc: javax.servlet.ServletException: springMvc
javax.servlet.ServletException: springMvc
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:555)
	at org.eclipse.jetty.servlet.ServletHolder.doStart(ServletHolder.java:346)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:786)
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:265)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1242)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
Caused by: 
java.lang.IllegalStateException: Failed to register dubbo://10.0.75.1:20800/com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService?anyhost=true&application=isomerization-proxy&dispatcher=message&dubbo=2.5.8&generic=false&interface=com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService&methods=access,accessHttp&pid=15340&revision=1.7.0&side=provider&threads=500&timestamp=1565923667102 to registry 127.0.0.1:2181, cause: Failed to register dubbo://10.0.75.1:20800/com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService?anyhost=true&application=isomerization-proxy&dispatcher=message&dubbo=2.5.8&generic=false&interface=com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService&methods=access,accessHttp&pid=15340&revision=1.7.0&side=provider&threads=500&timestamp=1565923667102 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.support.FailbackRegistry.register(FailbackRegistry.java:149)
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.register(RegistryProtocol.java:117)
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.export(RegistryProtocol.java:136)
	at com.alibaba.dubbo.rpc.protocol.ProtocolListenerWrapper.export(ProtocolListenerWrapper.java:67)
	at com.alibaba.dubbo.rpc.protocol.ProtocolFilterWrapper.export(ProtocolFilterWrapper.java:92)
	at com.alibaba.dubbo.rpc.Protocol$Adaptive.export(Protocol$Adaptive.java)
	at com.alibaba.dubbo.config.ServiceConfig.doExportUrlsFor1Protocol(ServiceConfig.java:504)
	at com.alibaba.dubbo.config.ServiceConfig.doExportUrls(ServiceConfig.java:356)
	at com.alibaba.dubbo.config.ServiceConfig.doExport(ServiceConfig.java:315)
	at com.alibaba.dubbo.config.ServiceConfig.export(ServiceConfig.java:214)
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:113)
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:42)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.doInvokeListener(SimpleApplicationEventMulticaster.java:172)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.invokeListener(SimpleApplicationEventMulticaster.java:165)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.multicastEvent(SimpleApplicationEventMulticaster.java:139)
	at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:393)
	at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:347)
	at org.springframework.context.support.AbstractApplicationContext.finishRefresh(AbstractApplicationContext.java:883)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:546)
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:668)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:634)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:682)
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:553)
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:494)
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:171)
	at javax.servlet.GenericServlet.init(GenericServlet.java:244)
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:534)
	at org.eclipse.jetty.servlet.ServletHolder.doStart(ServletHolder.java:346)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:786)
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:265)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1242)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
Caused by: 
com.alibaba.dubbo.rpc.RpcException: Failed to register dubbo://10.0.75.1:20800/com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService?anyhost=true&application=isomerization-proxy&dispatcher=message&dubbo=2.5.8&generic=false&interface=com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService&methods=access,accessHttp&pid=15340&revision=1.7.0&side=provider&threads=500&timestamp=1565923667102 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:112)
	at com.alibaba.dubbo.registry.support.FailbackRegistry.register(FailbackRegistry.java:136)
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.register(RegistryProtocol.java:117)
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.export(RegistryProtocol.java:136)
	at com.alibaba.dubbo.rpc.protocol.ProtocolListenerWrapper.export(ProtocolListenerWrapper.java:67)
	at com.alibaba.dubbo.rpc.protocol.ProtocolFilterWrapper.export(ProtocolFilterWrapper.java:92)
	at com.alibaba.dubbo.rpc.Protocol$Adaptive.export(Protocol$Adaptive.java)
	at com.alibaba.dubbo.config.ServiceConfig.doExportUrlsFor1Protocol(ServiceConfig.java:504)
	at com.alibaba.dubbo.config.ServiceConfig.doExportUrls(ServiceConfig.java:356)
	at com.alibaba.dubbo.config.ServiceConfig.doExport(ServiceConfig.java:315)
	at com.alibaba.dubbo.config.ServiceConfig.export(ServiceConfig.java:214)
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:113)
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:42)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.doInvokeListener(SimpleApplicationEventMulticaster.java:172)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.invokeListener(SimpleApplicationEventMulticaster.java:165)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.multicastEvent(SimpleApplicationEventMulticaster.java:139)
	at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:393)
	at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:347)
	at org.springframework.context.support.AbstractApplicationContext.finishRefresh(AbstractApplicationContext.java:883)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:546)
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:668)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:634)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:682)
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:553)
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:494)
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:171)
	at javax.servlet.GenericServlet.init(GenericServlet.java:244)
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:534)
	at org.eclipse.jetty.servlet.ServletHolder.doStart(ServletHolder.java:346)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:786)
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:265)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1242)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
Caused by: 
java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82)
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45)
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47)
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41)
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41)
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41)
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:110)
	at com.alibaba.dubbo.registry.support.FailbackRegistry.register(FailbackRegistry.java:136)
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.register(RegistryProtocol.java:117)
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.export(RegistryProtocol.java:136)
	at com.alibaba.dubbo.rpc.protocol.ProtocolListenerWrapper.export(ProtocolListenerWrapper.java:67)
	at com.alibaba.dubbo.rpc.protocol.ProtocolFilterWrapper.export(ProtocolFilterWrapper.java:92)
	at com.alibaba.dubbo.rpc.Protocol$Adaptive.export(Protocol$Adaptive.java)
	at com.alibaba.dubbo.config.ServiceConfig.doExportUrlsFor1Protocol(ServiceConfig.java:504)
	at com.alibaba.dubbo.config.ServiceConfig.doExportUrls(ServiceConfig.java:356)
	at com.alibaba.dubbo.config.ServiceConfig.doExport(ServiceConfig.java:315)
	at com.alibaba.dubbo.config.ServiceConfig.export(ServiceConfig.java:214)
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:113)
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:42)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.doInvokeListener(SimpleApplicationEventMulticaster.java:172)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.invokeListener(SimpleApplicationEventMulticaster.java:165)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.multicastEvent(SimpleApplicationEventMulticaster.java:139)
	at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:393)
	at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:347)
	at org.springframework.context.support.AbstractApplicationContext.finishRefresh(AbstractApplicationContext.java:883)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:546)
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:668)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:634)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:682)
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:553)
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:494)
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:171)
	at javax.servlet.GenericServlet.init(GenericServlet.java:244)
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:534)
	at org.eclipse.jetty.servlet.ServletHolder.doStart(ServletHolder.java:346)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:786)
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:265)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1242)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
2019-08-16 10:47:48.288:WARN:oejw.WebAppContext:Failed startup of context o.e.j.w.WebAppContext{/isomerization-proxy-web-1.7.0,file:/C:/Users/edidada/AppData/Local/Temp/jetty-0.0.0.0-8111-isomerization-proxy-web-1.7.0.war-_isomerization-proxy-web-1.7.0-any-/webapp/},D:\mavenrepository\201904\com\xxxx\media\platform\isomerization-proxy-web\1.7.0\isomerization-proxy-web-1.7.0.war
javax.servlet.ServletException: springMvc
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:555)
	at org.eclipse.jetty.servlet.ServletHolder.doStart(ServletHolder.java:346)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:786)
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:265)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1242)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
Caused by: 
java.lang.IllegalStateException: Failed to register dubbo://10.0.75.1:20800/com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService?anyhost=true&application=isomerization-proxy&dispatcher=message&dubbo=2.5.8&generic=false&interface=com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService&methods=access,accessHttp&pid=15340&revision=1.7.0&side=provider&threads=500&timestamp=1565923667102 to registry 127.0.0.1:2181, cause: Failed to register dubbo://10.0.75.1:20800/com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService?anyhost=true&application=isomerization-proxy&dispatcher=message&dubbo=2.5.8&generic=false&interface=com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService&methods=access,accessHttp&pid=15340&revision=1.7.0&side=provider&threads=500&timestamp=1565923667102 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.support.FailbackRegistry.register(FailbackRegistry.java:149)
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.register(RegistryProtocol.java:117)
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.export(RegistryProtocol.java:136)
	at com.alibaba.dubbo.rpc.protocol.ProtocolListenerWrapper.export(ProtocolListenerWrapper.java:67)
	at com.alibaba.dubbo.rpc.protocol.ProtocolFilterWrapper.export(ProtocolFilterWrapper.java:92)
	at com.alibaba.dubbo.rpc.Protocol$Adaptive.export(Protocol$Adaptive.java)
	at com.alibaba.dubbo.config.ServiceConfig.doExportUrlsFor1Protocol(ServiceConfig.java:504)
	at com.alibaba.dubbo.config.ServiceConfig.doExportUrls(ServiceConfig.java:356)
	at com.alibaba.dubbo.config.ServiceConfig.doExport(ServiceConfig.java:315)
	at com.alibaba.dubbo.config.ServiceConfig.export(ServiceConfig.java:214)
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:113)
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:42)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.doInvokeListener(SimpleApplicationEventMulticaster.java:172)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.invokeListener(SimpleApplicationEventMulticaster.java:165)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.multicastEvent(SimpleApplicationEventMulticaster.java:139)
	at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:393)
	at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:347)
	at org.springframework.context.support.AbstractApplicationContext.finishRefresh(AbstractApplicationContext.java:883)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:546)
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:668)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:634)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:682)
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:553)
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:494)
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:171)
	at javax.servlet.GenericServlet.init(GenericServlet.java:244)
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:534)
	at org.eclipse.jetty.servlet.ServletHolder.doStart(ServletHolder.java:346)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:786)
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:265)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1242)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
Caused by: 
com.alibaba.dubbo.rpc.RpcException: Failed to register dubbo://10.0.75.1:20800/com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService?anyhost=true&application=isomerization-proxy&dispatcher=message&dubbo=2.5.8&generic=false&interface=com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService&methods=access,accessHttp&pid=15340&revision=1.7.0&side=provider&threads=500&timestamp=1565923667102 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:112)
	at com.alibaba.dubbo.registry.support.FailbackRegistry.register(FailbackRegistry.java:136)
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.register(RegistryProtocol.java:117)
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.export(RegistryProtocol.java:136)
	at com.alibaba.dubbo.rpc.protocol.ProtocolListenerWrapper.export(ProtocolListenerWrapper.java:67)
	at com.alibaba.dubbo.rpc.protocol.ProtocolFilterWrapper.export(ProtocolFilterWrapper.java:92)
	at com.alibaba.dubbo.rpc.Protocol$Adaptive.export(Protocol$Adaptive.java)
	at com.alibaba.dubbo.config.ServiceConfig.doExportUrlsFor1Protocol(ServiceConfig.java:504)
	at com.alibaba.dubbo.config.ServiceConfig.doExportUrls(ServiceConfig.java:356)
	at com.alibaba.dubbo.config.ServiceConfig.doExport(ServiceConfig.java:315)
	at com.alibaba.dubbo.config.ServiceConfig.export(ServiceConfig.java:214)
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:113)
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:42)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.doInvokeListener(SimpleApplicationEventMulticaster.java:172)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.invokeListener(SimpleApplicationEventMulticaster.java:165)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.multicastEvent(SimpleApplicationEventMulticaster.java:139)
	at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:393)
	at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:347)
	at org.springframework.context.support.AbstractApplicationContext.finishRefresh(AbstractApplicationContext.java:883)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:546)
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:668)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:634)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:682)
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:553)
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:494)
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:171)
	at javax.servlet.GenericServlet.init(GenericServlet.java:244)
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:534)
	at org.eclipse.jetty.servlet.ServletHolder.doStart(ServletHolder.java:346)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:786)
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:265)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1242)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
Caused by: 
java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82)
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45)
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47)
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41)
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41)
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41)
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:110)
	at com.alibaba.dubbo.registry.support.FailbackRegistry.register(FailbackRegistry.java:136)
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.register(RegistryProtocol.java:117)
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.export(RegistryProtocol.java:136)
	at com.alibaba.dubbo.rpc.protocol.ProtocolListenerWrapper.export(ProtocolListenerWrapper.java:67)
	at com.alibaba.dubbo.rpc.protocol.ProtocolFilterWrapper.export(ProtocolFilterWrapper.java:92)
	at com.alibaba.dubbo.rpc.Protocol$Adaptive.export(Protocol$Adaptive.java)
	at com.alibaba.dubbo.config.ServiceConfig.doExportUrlsFor1Protocol(ServiceConfig.java:504)
	at com.alibaba.dubbo.config.ServiceConfig.doExportUrls(ServiceConfig.java:356)
	at com.alibaba.dubbo.config.ServiceConfig.doExport(ServiceConfig.java:315)
	at com.alibaba.dubbo.config.ServiceConfig.export(ServiceConfig.java:214)
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:113)
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:42)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.doInvokeListener(SimpleApplicationEventMulticaster.java:172)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.invokeListener(SimpleApplicationEventMulticaster.java:165)
	at org.springframework.context.event.SimpleApplicationEventMulticaster.multicastEvent(SimpleApplicationEventMulticaster.java:139)
	at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:393)
	at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:347)
	at org.springframework.context.support.AbstractApplicationContext.finishRefresh(AbstractApplicationContext.java:883)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:546)
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:668)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:634)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:682)
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:553)
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:494)
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:171)
	at javax.servlet.GenericServlet.init(GenericServlet.java:244)
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:534)
	at org.eclipse.jetty.servlet.ServletHolder.doStart(ServletHolder.java:346)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:786)
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:265)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1242)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)
[2019-08-16 10:47:46,493][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:47,094][INFO][com.alibaba.dubbo.config.AbstractConfig 111][55]traceLogid:[]dstTraceId:[] [DUBBO] The service ready on spring started. service: com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:47,463][INFO][com.alibaba.dubbo.config.AbstractConfig 529][55]traceLogid:[]dstTraceId:[] [DUBBO] Export dubbo service com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService to local registry, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:47,463][INFO][com.alibaba.dubbo.config.AbstractConfig 489][55]traceLogid:[]dstTraceId:[] [DUBBO] Export dubbo service com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService to url dubbo://10.0.75.1:20800/com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService?anyhost=true&application=isomerization-proxy&bind.ip=10.0.75.1&bind.port=20800&dispatcher=message&dubbo=2.5.8&generic=false&interface=com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService&methods=access,accessHttp&pid=15340&revision=1.7.0&side=provider&threads=500&timestamp=1565923667102, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:47,464][INFO][com.alibaba.dubbo.config.AbstractConfig 499][55]traceLogid:[]dstTraceId:[] [DUBBO] Register dubbo service com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService url dubbo://10.0.75.1:20800/com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService?anyhost=true&application=isomerization-proxy&bind.ip=10.0.75.1&bind.port=20800&dispatcher=message&dubbo=2.5.8&generic=false&interface=com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService&methods=access,accessHttp&pid=15340&revision=1.7.0&side=provider&threads=500&timestamp=1565923667102 to registry registry://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&pid=15340&registry=zookeeper&timestamp=1565923667101, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:47,646][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:47,736][INFO][com.alibaba.dubbo.remoting.transport.AbstractServer 67][55]traceLogid:[]dstTraceId:[] [DUBBO] Start NettyServer bind /0.0.0.0:20800, export /10.0.75.1:20800, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:47,740][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 273][55]traceLogid:[]dstTraceId:[] [DUBBO] Register: dubbo://10.0.75.1:20800/com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService?anyhost=true&application=isomerization-proxy&dispatcher=message&dubbo=2.5.8&generic=false&interface=com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService&methods=access,accessHttp&pid=15340&revision=1.7.0&side=provider&threads=500&timestamp=1565923667102, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:47,742][ERROR][org.springframework.web.servlet.DispatcherServlet 502][55]traceLogid:[]dstTraceId:[]Context initialization failed
java.lang.IllegalStateException: Failed to register dubbo://10.0.75.1:20800/com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService?anyhost=true&application=isomerization-proxy&dispatcher=message&dubbo=2.5.8&generic=false&interface=com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService&methods=access,accessHttp&pid=15340&revision=1.7.0&side=provider&threads=500&timestamp=1565923667102 to registry 127.0.0.1:2181, cause: Failed to register dubbo://10.0.75.1:20800/com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService?anyhost=true&application=isomerization-proxy&dispatcher=message&dubbo=2.5.8&generic=false&interface=com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService&methods=access,accessHttp&pid=15340&revision=1.7.0&side=provider&threads=500&timestamp=1565923667102 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.support.FailbackRegistry.register(FailbackRegistry.java:149) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.register(RegistryProtocol.java:117) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.integration.RegistryProtocol.export(RegistryProtocol.java:136) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.rpc.protocol.ProtocolListenerWrapper.export(ProtocolListenerWrapper.java:67) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.rpc.protocol.ProtocolFilterWrapper.export(ProtocolFilterWrapper.java:92) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.rpc.Protocol$Adaptive.export(Protocol$Adaptive.java) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.ServiceConfig.doExportUrlsFor1Protocol(ServiceConfig.java:504) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.ServiceConfig.doExportUrls(ServiceConfig.java:356) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.ServiceConfig.doExport(ServiceConfig.java:315) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.ServiceConfig.export(ServiceConfig.java:214) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:113) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:42) ~[dubbo-2.5.8.jar:2.5.8]
	at org.springframework.context.event.SimpleApplicationEventMulticaster.doInvokeListener(SimpleApplicationEventMulticaster.java:172) ~[spring-context-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.context.event.SimpleApplicationEventMulticaster.invokeListener(SimpleApplicationEventMulticaster.java:165) ~[spring-context-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.context.event.SimpleApplicationEventMulticaster.multicastEvent(SimpleApplicationEventMulticaster.java:139) ~[spring-context-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:393) ~[spring-context-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.publishEvent(AbstractApplicationContext.java:347) ~[spring-context-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.finishRefresh(AbstractApplicationContext.java:883) ~[spring-context-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:546) ~[spring-context-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:668) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:634) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:682) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:553) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:494) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:171) ~[spring-webmvc-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at javax.servlet.GenericServlet.init(GenericServlet.java:244) ~[servlet-api-3.0.jar:?]
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:534) ~[?:?]
	at org.eclipse.jetty.servlet.ServletHolder.doStart(ServletHolder.java:346) ~[?:?]
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64) ~[?:?]
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:786) ~[?:?]
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:265) ~[?:?]
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1242) ~[?:?]
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717) ~[?:?]
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494) ~[?:?]
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64) ~[?:?]
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359) ~[?:?]
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82) ~[?:?]
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107) ~[?:?]
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615) ~[?:?]
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540) ~[?:?]
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403) ~[?:?]
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353) ~[?:?]
	at java.util.TimerThread.mainLoop(Timer.java:555) ~[?:1.8.0_161]
	at java.util.TimerThread.run(Timer.java:505) ~[?:1.8.0_161]
Caused by: com.alibaba.dubbo.rpc.RpcException: Failed to register dubbo://10.0.75.1:20800/com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService?anyhost=true&application=isomerization-proxy&dispatcher=message&dubbo=2.5.8&generic=false&interface=com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService&methods=access,accessHttp&pid=15340&revision=1.7.0&side=provider&threads=500&timestamp=1565923667102 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:112) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.register(FailbackRegistry.java:136) ~[dubbo-2.5.8.jar:2.5.8]
	... 43 more
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:110) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.register(FailbackRegistry.java:136) ~[dubbo-2.5.8.jar:2.5.8]
	... 43 more
[2019-08-16 10:47:48,428] Artifact isomerization-proxy-web-1.7.0.war: Artifact is deployed successfully
[2019-08-16 10:47:48,435] Artifact isomerization-proxy-web-1.7.0.war: Deploy took 58,856 milliseconds
[2019-08-16 10:47:48,760][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:49,644][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 324][115]traceLogid:[]dstTraceId:[] [DUBBO] Retry register [consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541], dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:49,647][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 332][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry register [consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541], waiting for again, cause: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:112) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:329) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:110) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:47:49,649][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 332][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry register [consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541], waiting for again, cause: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:112) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:329) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:110) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:47:49,649][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 369][115]traceLogid:[]dstTraceId:[] [DUBBO] Retry subscribe {consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541=[com.alibaba.dubbo.registry.integration.RegistryDirectory@4223b03e], consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110=[com.alibaba.dubbo.registry.integration.RegistryDirectory@13837e72]}, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:49,649][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 380][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry subscribe {consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541=[com.alibaba.dubbo.registry.integration.RegistryDirectory@4223b03e], consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110=[com.alibaba.dubbo.registry.integration.RegistryDirectory@13837e72]}, waiting for again, cause: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:185) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:377) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:176) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:47:49,649][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 380][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry subscribe {consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541=[com.alibaba.dubbo.registry.integration.RegistryDirectory@4223b03e], consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110=[com.alibaba.dubbo.registry.integration.RegistryDirectory@13837e72]}, waiting for again, cause: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:185) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:377) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:176) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:47:49,863][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:50,937][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:52,038][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:53,046][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:54,148][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:54,650][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 324][115]traceLogid:[]dstTraceId:[] [DUBBO] Retry register [consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541], dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:54,651][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 332][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry register [consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541], waiting for again, cause: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:112) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:329) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:110) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:47:54,653][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 332][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry register [consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541], waiting for again, cause: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:112) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:329) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:110) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:47:54,653][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 369][115]traceLogid:[]dstTraceId:[] [DUBBO] Retry subscribe {consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541=[com.alibaba.dubbo.registry.integration.RegistryDirectory@4223b03e], consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110=[com.alibaba.dubbo.registry.integration.RegistryDirectory@13837e72]}, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:54,654][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 380][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry subscribe {consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541=[com.alibaba.dubbo.registry.integration.RegistryDirectory@4223b03e], consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110=[com.alibaba.dubbo.registry.integration.RegistryDirectory@13837e72]}, waiting for again, cause: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:185) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:377) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:176) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:47:54,655][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 380][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry subscribe {consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541=[com.alibaba.dubbo.registry.integration.RegistryDirectory@4223b03e], consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110=[com.alibaba.dubbo.registry.integration.RegistryDirectory@13837e72]}, waiting for again, cause: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:185) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:377) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:176) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:47:55,150][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:56,251][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:57,253][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:58,355][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:47:59,357][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:47:59,657][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 324][115]traceLogid:[]dstTraceId:[] [DUBBO] Retry register [consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541], dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:59,657][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 332][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry register [consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541], waiting for again, cause: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:112) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:329) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:110) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:47:59,658][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 332][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry register [consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541], waiting for again, cause: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:112) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:329) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:110) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:47:59,658][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 369][115]traceLogid:[]dstTraceId:[] [DUBBO] Retry subscribe {consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541=[com.alibaba.dubbo.registry.integration.RegistryDirectory@4223b03e], consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110=[com.alibaba.dubbo.registry.integration.RegistryDirectory@13837e72]}, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:47:59,658][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 380][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry subscribe {consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541=[com.alibaba.dubbo.registry.integration.RegistryDirectory@4223b03e], consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110=[com.alibaba.dubbo.registry.integration.RegistryDirectory@13837e72]}, waiting for again, cause: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:185) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:377) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:176) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:47:59,658][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 380][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry subscribe {consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541=[com.alibaba.dubbo.registry.integration.RegistryDirectory@4223b03e], consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110=[com.alibaba.dubbo.registry.integration.RegistryDirectory@13837e72]}, waiting for again, cause: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:185) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:377) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:176) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:48:00,458][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:48:01,461][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:48:02,576][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:48:03,578][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:48:04,659][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 324][115]traceLogid:[]dstTraceId:[] [DUBBO] Retry register [consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541], dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:48:04,660][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 332][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry register [consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541], waiting for again, cause: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:112) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:329) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:110) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:48:04,661][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 332][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry register [consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541], waiting for again, cause: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:112) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:329) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:110) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:48:04,662][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 369][115]traceLogid:[]dstTraceId:[] [DUBBO] Retry subscribe {consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541=[com.alibaba.dubbo.registry.integration.RegistryDirectory@4223b03e], consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110=[com.alibaba.dubbo.registry.integration.RegistryDirectory@13837e72]}, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:48:04,662][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 380][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry subscribe {consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541=[com.alibaba.dubbo.registry.integration.RegistryDirectory@4223b03e], consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110=[com.alibaba.dubbo.registry.integration.RegistryDirectory@13837e72]}, waiting for again, cause: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:185) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:377) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:176) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:48:04,663][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 380][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry subscribe {consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541=[com.alibaba.dubbo.registry.integration.RegistryDirectory@4223b03e], consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110=[com.alibaba.dubbo.registry.integration.RegistryDirectory@13837e72]}, waiting for again, cause: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:185) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:377) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:176) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:48:04,680][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:48:05,682][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:48:06,783][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:48:07,784][WARN][org.apache.zookeeper.ClientCnxn 1102][118]traceLogid:[]dstTraceId:[]Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect
java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[?:1.8.0_161]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[?:1.8.0_161]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
[2019-08-16 10:48:08,885][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:48:09,664][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 324][115]traceLogid:[]dstTraceId:[] [DUBBO] Retry register [consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541], dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:48:09,664][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 332][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry register [consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541], waiting for again, cause: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:112) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:329) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:110) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:48:09,665][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 332][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry register [consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541], waiting for again, cause: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to register consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:112) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:329) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doRegister(ZookeeperRegistry.java:110) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:48:09,665][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 369][115]traceLogid:[]dstTraceId:[] [DUBBO] Retry subscribe {consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541=[com.alibaba.dubbo.registry.integration.RegistryDirectory@4223b03e], consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110=[com.alibaba.dubbo.registry.integration.RegistryDirectory@13837e72]}, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:48:09,665][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 380][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry subscribe {consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541=[com.alibaba.dubbo.registry.integration.RegistryDirectory@4223b03e], consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110=[com.alibaba.dubbo.registry.integration.RegistryDirectory@13837e72]}, waiting for again, cause: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:185) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:377) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:176) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:48:09,665][WARN][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 380][115]traceLogid:[]dstTraceId:[] [DUBBO] Failed to retry subscribe {consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541=[com.alibaba.dubbo.registry.integration.RegistryDirectory@4223b03e], consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110=[com.alibaba.dubbo.registry.integration.RegistryDirectory@13837e72]}, waiting for again, cause: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!, dubbo version: 2.5.8, current host: 10.0.75.1
com.alibaba.dubbo.rpc.RpcException: Failed to subscribe consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110 to zookeeper zookeeper://127.0.0.1:2181/com.alibaba.dubbo.registry.RegistryService?application=isomerization-proxy&dubbo=2.5.8&interface=com.alibaba.dubbo.registry.RegistryService&pid=15340&timestamp=1565923629577, cause: Zookeeper is not connected yet!
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:185) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry.retry(FailbackRegistry.java:377) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.support.FailbackRegistry$1.run(FailbackRegistry.java:70) ~[dubbo-2.5.8.jar:2.5.8]
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511) ~[?:1.8.0_161]
	at java.util.concurrent.FutureTask.runAndReset(FutureTask.java:308) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.access$301(ScheduledThreadPoolExecutor.java:180) ~[?:1.8.0_161]
	at java.util.concurrent.ScheduledThreadPoolExecutor$ScheduledFutureTask.run(ScheduledThreadPoolExecutor.java:294) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) ~[?:1.8.0_161]
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) ~[?:1.8.0_161]
	at java.lang.Thread.run(Thread.java:748) [?:1.8.0_161]
Caused by: java.lang.IllegalStateException: Zookeeper is not connected yet!
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkClientWrapper.createPersistent(ZkClientWrapper.java:82) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.zkclient.ZkclientZookeeperClient.createPersistent(ZkclientZookeeperClient.java:45) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:47) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.remoting.zookeeper.support.AbstractZookeeperClient.create(AbstractZookeeperClient.java:41) ~[dubbo-2.5.8.jar:2.5.8]
	at com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry.doSubscribe(ZookeeperRegistry.java:176) ~[dubbo-2.5.8.jar:2.5.8]
	... 9 more
[2019-08-16 10:48:09,890][INFO][org.apache.zookeeper.ClientCnxn 852][118]traceLogid:[]dstTraceId:[]Socket connection established to 127.0.0.1/127.0.0.1:2181, initiating session
[2019-08-16 10:48:09,944][INFO][org.apache.zookeeper.ClientCnxn 1098][118]traceLogid:[]dstTraceId:[]Unable to read additional data from server sessionid 0x0, likely server has closed socket, closing socket connection and attempting reconnect
[2019-08-16 10:48:11,795][INFO][org.apache.zookeeper.ClientCnxn 975][118]traceLogid:[]dstTraceId:[]Opening socket connection to server 127.0.0.1/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
[2019-08-16 10:48:11,796][INFO][org.apache.zookeeper.ClientCnxn 852][118]traceLogid:[]dstTraceId:[]Socket connection established to 127.0.0.1/127.0.0.1:2181, initiating session
[2019-08-16 10:48:11,813][INFO][org.apache.zookeeper.ClientCnxn 1235][118]traceLogid:[]dstTraceId:[]Session establishment complete on server 127.0.0.1/127.0.0.1:2181, sessionid = 0x16c985345de0000, negotiated timeout = 30000
[2019-08-16 10:48:11,814][INFO][org.I0Itec.zkclient.ZkClient 449][119]traceLogid:[]dstTraceId:[]zookeeper state changed (SyncConnected)
[2019-08-16 10:48:14,667][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 324][115]traceLogid:[]dstTraceId:[] [DUBBO] Retry register [consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=consumers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541], dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:48:14,797][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 369][115]traceLogid:[]dstTraceId:[] [DUBBO] Retry subscribe {consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541=[com.alibaba.dubbo.registry.integration.RegistryDirectory@4223b03e], consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110=[com.alibaba.dubbo.registry.integration.RegistryDirectory@13837e72]}, dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:48:14,881][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 384][115]traceLogid:[]dstTraceId:[] [DUBBO] Notify urls for subscribe url consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541, urls: [empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=providers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541, empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=configurators&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541, empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService?application=isomerization-proxy&category=routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthTokenService&methods=getToken&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923629541], dubbo version: 2.5.8, current host: 10.0.75.1
[2019-08-16 10:48:14,953][INFO][com.alibaba.dubbo.registry.zookeeper.ZookeeperRegistry 384][115]traceLogid:[]dstTraceId:[] [DUBBO] Notify urls for subscribe url consumer://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers,configurators,routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, urls: [empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=providers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=configurators&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110, empty://10.0.75.1/com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService?application=isomerization-proxy&category=routers&check=false&dubbo=2.5.8&interface=com.xxxx.media.platform.auth.api.MicroServiceAuthAccessService&methods=access&pid=15340&retries=0&revision=1.3.0&side=consumer&timeout=3000&timestamp=1565923660110], dubbo version: 2.5.8, current host: 10.0.75.1

```
