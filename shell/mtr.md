# mtr

       mtr     [-BfhvrctglxspQemniuTP46]     [--help]     [--version]     [--report]    [--report-wide]
       [--report-cycles COUNT] [--curses] [--split] [--raw] [ --xml] [--mpls]  [--no-dns]  [--show-ips]
       [--gtk]  [--address IP.ADD.RE.SS] [--interval SECONDS] [--max-ttl NUM] [--first-ttl NUM] [--bit‐
       pattern NUM] [--tos NUM] [--psize BYTES |  -s  BYTES]  [--tcp]  [--udp]  [--port PORT]  [--time‐
       out SECONDS] HOSTNAME [PACKETSIZE]


​	  
mtr -n -i 1 -c 100 www.edidada.cn



先说一种解决方案吧: chmod +s /usr/sbin/mtr 即可，解释如下(比较啰嗦)

Linux的权限模型：
  - 对于某个文件而言, Linux对其3类对象各自分别定义了3种不同的权限
  - 这3类对象：  属主u、属组g、其他o
  - 这3种权限：  读r、写w、执行x  
    注意：每个对象都拥有3种权限， 所以我们通过ls -l filename 看到的 -rwxr-xr-x 即该文件属主拥有读写执行、属组拥有读执行、其他用于拥有读执行权限。

进程的安全上下文：
  - 每个进程也有属主、属组，进程需要访问的文件也有属主、属组
  - 默认情况下进程的属主是进程发起者这个用户，比如你用 zhangsan 这个用户 执行mtr 那么mtr进程的属主就是 zhangsan 
  - 进程的属组是这个用户的基本组

  而raw socket套接字需要root用户才能够使用，因此一个 zhangsan 普通用户执行mtr时当需要用到 raw socket时 进程的属主 zhangsan 并没有权限！因而报错。

至于为什么 chmod +s /usr/sbin/mtr 可以解决， 这是用到了SUID机制(类似还有SGID、STICKY)

SUID机制 可以让进程的属主不再是发起者(zhangsan用户) 而是该可执行程序文件的本身的属主(root用户)，由于root用户可以获取raw socket因此可以顺利执行。
可自行CU查找这方面的知识，最典型的就是 passwd这个命令了。

普通用户用mtr的时候总提示我mtr: unable to get raw sockets
http://bbs.chinaunix.net/thread-1922239-1-1.html

