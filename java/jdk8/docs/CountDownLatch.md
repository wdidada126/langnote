# CountDownLatch

countDownLatch.countDown()//通知线程本任务执行完毕
countDownLatch.await();//开始暂停，等待其他线程完毕后继续执行
CountDownLatch通过AQS（AbstractQueuedSynchronizer）里面的共享锁来实现的。
CountDownLatch.Sync实现了AQS接口




