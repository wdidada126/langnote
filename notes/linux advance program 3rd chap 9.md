---
title: linux advance program 3rd chap 9
date: 2017-10-24 08:56:36
categories:
- Diary
tags:
- Linux
- Note

---
# linux advance program 3rd chap 9

## chap 9
无名管道pipe用来在具有亲缘关系的进程间传递数据
示例：

```shell

ps -aux |grep syslogd

```

无名管道在两个进程退出时消失

mkfifo（）用来创建有名管道

<!-- more -->

## chap 10

消息队列

msqid_ds
双端链表
struct ipc_perm
struct msg *msg_first;
struct msg *msg_last;

- 1、创建消息队列
msgget()
- 2、消息队列属性控制
msgctl()
- 3、发送消息队列
msgsend()
- 4、从消息队列消息队列接受信息
msgrcv()


```c

#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<sys/types.h>
#include<sys/ipc.h>
#include<string.h>
#include<sys/msg.h>
#define BUFSIZE 128
struct msg_buf
{
	long type;
	char msg[BUFSIZE];
};

int main(int argc,char *argv[])
{
	key_t key;
	int msgid;
	struct msg_buf msg_snd,msg_rcv;
	struct msginfo buf;
	char *ptr="helloworld";

	memset(&msg_snd,'\0',sizeof(struct msg_buf));
	memset(&msg_rcv,'\0',sizeof(struct msg_buf));

	msg_rcv.type=1;

	msg_snd.type=1;
	memcpy(msg_snd.msg,ptr,strlen(ptr));
	if((key=ftok(".",'A'))==-1)
	{
		perror("ftok");
		exit(EXIT_FAILURE);
	}

	if((msgid=msgget(key,0600|IPC_CREAT))==-1)
	{
		perror("msgget");
		exit(EXIT_FAILURE);
	}
	printf("msgsnd_return=%d\n",msgsnd(msgid,(void *)&msg_snd,strlen(msg_snd.msg),0));
	
	msgctl(msgid,MSG_INFO,&buf);
	printf("buf.msgmax=%d\n",buf.msgmax);
	printf("buf.msgmnb=%d\n",buf.msgmnb);
	printf("buf.msgpool=%d\n",buf.msgpool);
	printf("buf.semmap=%d\n",buf.msgmap);
	printf("buf.msgmni=%d\n",buf.msgmni);
	printf("buf.msgssz=%d\n",buf.msgssz);
	printf("buf.msgtql=%d\n",buf.msgtql);
	printf("buf.msgseg=%u\n",buf.msgseg);
	
	printf("msgrcv_return=%d\n",msgrcv(msgid,(void *)&msg_rcv,BUFSIZE,msg_rcv.type,0));
	printf("rev msg:%s\n",msg_rcv.msg);
	printf("msgctl_return=%d\n",msgctl(msgid,IPC_RMID,0));
}

```


## chap 11
在实际应用中，两个进程间通信可能会使用多个信号量，因此，Linux在管理时以信号量集合的概念来管理。
整个信号量集合由一下部分组成：
- 信号量集合数据结构：在此数据结构中定义了整个信号量集合的基本属性，如访问权限。
- 信号量：信号量集合使用指针指向一个由数组组成的信号量单元，在此信号量单元中存储了各信号量的值。

信号量集合数据结构定义在：
struct semid_ds

每一个信号量数据结构：
struct sem

linux信号量管理操作

- 1、创建
semget()
- 2、设置属性
semctl()
- 3、操作
semop()

共享内存
数据结构
shmid_ds


