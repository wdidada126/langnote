---
title: linux advance program 3rd chap 8
date: 2017-10-24 08:55:36
categories:
- Diary
tags:
- Linux
- Note
- source code

---

# linux advance program 3rd chap 8

## chap 8

getpid()	获取进程号
getppid()	用来取得目前进程的父进程识别码

守护进程
应用：httpd
守护进程需要输出信息，但是没有与任何终端关联，所以采用日志的方式。
- 1、进程直接与日志进行关联
- 2、使用日志守护进程（syslogd）

查看日志守护进程信息需要的指令
ps -aux | grep syslogd
在进城中，调用openlog（）将与日志守护进程建立联系
syslog（）将产生一条日志信息

<!-- more -->


守护进程示例：

```c

#include <unistd.h> 
#include <signal.h> 
#include <fcntl.h>
#include <sys/syslog.h>
#include <sys/param.h> 
#include <sys/types.h> 
#include <sys/stat.h> 
#include <stdio.h>
#include <stdlib.h>

int init_daemon(const char *pname, int facility)
{ 
        int pid; 
        int i;
	     signal(SIGTTOU,SIG_IGN); 
	     signal(SIGTTIN,SIG_IGN); 
	     signal(SIGTSTP,SIG_IGN); 
	     signal(SIGHUP ,SIG_IGN);
 
        if(pid=fork()) 
            exit(EXIT_SUCCESS); 
        else if(pid< 0) 
	  {
		perror("fork");
		exit(EXIT_FAILURE);
        }
        setsid(); 
        if(pid=fork()) 
                exit(EXIT_SUCCESS); 
        else if(pid< 0) 
	  {
		perror("fork");
		exit(EXIT_FAILURE);
        }  
        for(i=0;i< NOFILE;++i)
                close(i);
         open("/dev/null", O_RDONLY);
          open("/dev/null", O_RDWR);
          open("/dev/null", O_RDWR);

        chdir("/tmp"); 
        umask(0);  
        signal(SIGCHLD,SIG_IGN);
	  openlog(pname, LOG_PID, facility);
	  return; 
} 

int main(int argc,char *argv[]) 
{ 
        FILE *fp; 
        time_t ticks; 
        init_daemon(argv[0],LOG_KERN);
        while(1)
        {
            sleep(1);
			ticks=time(NULL);
            syslog(LOG_INFO,"%s",asctime(localtime(&ticks))); 
        }

} 

```