---
title: Golang goroutine pool 的实现
date: 2019-02-11 16:50:05
tags: CSDN迁移
---
  Golang 语言很好的支持高并发场景，goroutine相比java的thread开销更小。但是大量的goroutine会带来内存开销，如果无限的创建goroutine则会出现内存溢出的灾难，所以萌生出了goroutine pool 的想法，仿照java中的ThreadPoolExecutor实现一个简单的Golang 版本的协程池。代码如下：

 
```
package goroutine_pool

import (
	"fmt"
	"sync"
	"time"
)
/*任务的接口*/
type Task interface {
	Run()
}
//任务的具体结构
type TestTask struct {
	I int
}

//实现接口
func (t TestTask) Run() {
	time.Sleep(300 * time.Millisecond)
	fmt.Printf("No: %d\n",t.I)
}

//协程池结构
type GroutinePool struct {
	lock sync.Mutex  //处理并发的锁
	coreGoroutineSize int32 //核心工作协程数量
	maxGoroutineSize  int32 //最大工作协程数量
	queue chan Task //任务队列
	duration time.Duration //最大等待时间
	status   int32   //线程池状态0:初始化；1:运行；2:shutdown;3:stop
	size     int32   //当前线程池中的工作线程数
	maxQueueSize int32 //工作队列中的最大数量
	reject func ()  //丢弃任务之后回调该方法
}
//原子操作函数，保证方法f对全局变量的操作是原子的
func (pool *GroutinePool) atomicOper(f func() bool) bool {
	pool.lock.Lock()
	defer pool.lock.Unlock()
	return f()
}
//构造一个协程池
func NewGroutinePool(core int32,max int32,queueSize int32,duration time.Duration,rejectHandler func()) *GroutinePool{
	pool := GroutinePool{}
	pool.status = 0
	pool.coreGoroutineSize = core
	pool.maxGoroutineSize = max
	pool.size = 0
	pool.maxQueueSize = queueSize
	pool.queue = make(chan Task,pool.maxQueueSize)
	pool.duration = duration
	pool.lock = sync.Mutex{}
	pool.reject = rejectHandler
	return &pool
}
//启动协程池
func (pool *GroutinePool) Start() {
	if pool.status != 0 {
		panic("GroutinePool has started!")
	}
	pool.status = 1
}

//向协程池放入任务，该逻辑参考java ThreadPoolExecutor
func (pool *GroutinePool)Put(t Task) bool {
     if pool.status != 1 {
		mes := fmt.Sprintf("GroutinePool status: %d\n",pool.status)
		panic(mes)
	}
	return pool.atomicOper(func() bool{
	//如果当前协程数小于核心协程数则创建新协程处理任务
		if pool.size < pool.coreGoroutineSize {
			pool.size++
			go pool.run(t)
			return true
		} else if len(pool.queue) < int(pool.maxQueueSize) {
		//当前协程数大于等于核心协程数并且队列没有满，则将任务放入队列
			pool.queue <- t
			return true
		} else if pool.size < pool.maxGoroutineSize {
		//如果协程数小于最大协程数则创建新协程处理任务
			pool.size++
			go pool.run(t)
			return true
		} else {
		//协程数已经是最大协程数则拒绝该任务
			pool.reject()
			return false
		}
	})
}

//工作协程处理任务，不断从队列中获取任务，直到超时
func (pool *GroutinePool) run(t Task) {
    if t != nil {//正在处理的任务不为nil,则处理任务t
		t.Run()
	}
	loop:
	for pool.status == 1 || pool.status == 2 {
		select {
			case t := <-pool.queue:
				t.Run()
			case <-time.After(pool.duration):
			//如果超时还没有拿到任务，说明该协程已经空闲了一段时间，该协程的生命周期可以结束
				if pool.atomicOper(func() bool {
				//当协程池中的协程数量大于核心数量的时候，将协程结束
					if pool.size > pool.coreGoroutineSize {
						pool.size--
						return true
					} else if pool.status == 2 {
					//如果协程池状态为shutdown,需要查看队列中是否还有任务，如果有任务则保留协程，否则结束协程
						if len(pool.queue) > 0 {
							return false
						} else {
							pool.size--
							return true
						}
					} else {
						return false
					}
				}) {
					break loop
				}
		}
	}
	pool.atomicOper(func() bool {//如果协程池中协程数为0，则关闭协程池
		if pool.status == 2 && pool.size == 0 {
			pool.status = 3
			return true
		} else {
			return false
		}
	})
}

func (pool *GroutinePool) Shutdown() {
	pool.status = 2
}

func (pool *GroutinePool) ShutdownNow() {
	pool.status = 3
}

func (pool *GroutinePool) GetStatus() int32 {
	return pool.status
}

func (pool *GroutinePool) GetQueueSize() int32 {
	return int32(len(pool.queue))
}

func (pool *GroutinePool) GetPoolSize() int32 {
	return pool.size
}

```
 
### []()测试代码

 
```
func main() {
//构造一个协程池
	pool := goroutine_pool.NewGroutinePool(1,2,5,500 * time.Millisecond,func(){
		fmt.Printf("reject task !\n")
	})
	pool.Start()//启动
//放任务
	for i := 0;i < 20;i++ {
		fmt.Printf("i : %d\n",i)
		t := &goroutine_pool.TestTask{}
		t.I = i
		if !pool.Put(t) {
			time.Sleep(100 * time.Millisecond)
		}
	}

	time.Sleep(5 * time.Second)

	fmt.Printf("pool status : %d;\n queue size : %d;\n goroutine size : %d\n",
		pool.GetStatus(),pool.GetQueueSize(),pool.GetPoolSize())
//分别测试shutdown,shutdownNow
	//pool.Shutdown()
	pool.ShutdownNow()

	for pool.GetStatus() != 3 {
		/*fmt.Printf("pool status : %d;\n queue size : %d;\n goroutine size : %d\n",
			pool.GetStatus(),pool.GetQueueSize(),pool.GetPoolSize())
		time.Sleep(time.Millisecond * 10)*/
		fmt.Printf("wait pool shutdown ! \n")
	}

	fmt.Printf("pool status : %d;\n queue size : %d;\n goroutine size : %d\n",
		pool.GetStatus(),pool.GetQueueSize(),pool.GetPoolSize())

}

```
   
  