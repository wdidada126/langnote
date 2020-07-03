# corba


https://www.corba.org/

jacorb java开源实现



[java core corba](https://www.oracle.com/java/technologies/core-corba-rmi-iiop.html)



https://docs.oracle.com/javase/8/docs/technotes/guides/idl/



https://www.omg.org/

https://www.jacorb.org/

https://github.com/JacORB/JacORB

分布式方案

```
org.omg.CORBA.ORB
```



(COMM_FAILURE) Connection failure: socketType: IIOP_CLEAR_TEXT; hostname: 127.0.0.1; port: 81"
该问题在网上查了是因为服务在linux上而应用在windows上造成的。
但实际是因为修改了应用端口，而org应用端口与其不一致造成的，修改org目录下的如D:\aictms\aicorg\applications\WEB-INF\classes的entity-j2ee.xml文件，将端口修改为与应用一致，该目录下其他文件修改正确的路径值则解决。


<<<<<<< HEAD
https://www.iteye.com/blog/kanexiao-1259105







Corba



在华为的时候看过，真的是要人命的东西，超级复杂 ！ 有的朋友会问超级复杂为何就被抛弃呢？ 简单来说：任何东西一切正常的时候比的是功能是否强大，但出问题的时候比的是能否快速处理（定位 + 恢复），CORBA过于复杂，太难掌控，大家都不敢用。还是UNIX的哲学好：KISS，Keep it simple and stupid





CORBA这玩艺只在史书上看到过，据说很精密很完善，是终极方案。



没有分布式系统设计经验时候的一个幻想



终极方案为什么舍弃掉了被 外行不懂求说说



“终极方案”的意思就是想太多，类似要你命那样。



webservice很不幸，也步其后尘，载入史册。



Java有开源实现



=======
https://www.iteye.com/blog/kanexiao-1259105
>>>>>>> a37e32040eec40d601569c731c313a398efb2dec
