---
title: ListenableFuture demo
date: 2017-09-09 10:15:07
tags: CSDN迁移
---
  ```
import com.google.common.util.concurrent.*;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

/**
 * Created by author on 2017/7/27.
 */
public class GuavaUtils {

    private static ListeningExecutorService pool = MoreExecutors.listeningDecorator(
            Executors.newFixedThreadPool(30));

    public static ListenableFuture<List<String>> getFutureList(){
        List<ListenableFuture<String>> list = new ArrayList<>(10);
        for(int i=0;i<10;i++){
            final ListenableFuture<String> future =  pool.submit(new Callable<String>() {
                @Override
                public String call() throws Exception {
                    Thread.sleep(1000*10);
                    return "Task done !";
                }
            });

            Futures.addCallback(future, new FutureCallback<String>() {
                @Override
                public void onSuccess(String result) {
                    System.out.println(result);
                }

                @Override
                public void onFailure(Throwable t) {
                    System.out.println(t.getMessage());
                }
            });
            list.add(future);
        }
        return Futures.successfulAsList(list);
    }


    public static void main(String args[]){
       ListenableFuture<List<String>> result = getFutureList();
        try{
            List<String> list = result.get();
            int counter = 1;
            for(String s : list){
                System.out.println(counter+++ s);
            }
        }catch (Exception e){
            e.printStackTrace();
        }

    }

}
```
   
  