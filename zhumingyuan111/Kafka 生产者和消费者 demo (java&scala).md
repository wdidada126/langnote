---
title: Kafka 生产者和消费者 demo (java&scala)
date: 2017-06-30 22:39:10
tags: CSDN迁移
---
  前几天完成了kafka ubuntu单机的搭建，后来就尝试写写kafka的简单代码，网上也有很多例子，但是如果自己编写运行还是有一些坑在里面，我也简单记录以下自己遇到的问题。如何在idea下建立java&scala工程请参考我以前的博客：[http://blog.csdn.net/zhumingyuan111/article/details/73521974](http://blog.csdn.net/zhumingyuan111/article/details/73521974)

 下面直接给出代码：   
 Maven依赖

 
```
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>kafkaDemo</groupId>
    <artifactId>com.kafka.demo</artifactId>
    <version>1.0-SNAPSHOT</version>

    <dependencies>
        <dependency>
            <groupId>log4j</groupId>
            <artifactId>log4j</artifactId>
            <version>1.2.14</version>
        </dependency>
        <dependency>
            <groupId>org.apache.kafka</groupId>
            <artifactId>kafka_2.11</artifactId>
            <version>0.10.2.0</version>
            <exclusions>
                <exclusion>
                    <groupId>log4j</groupId>
                    <artifactId>log4j</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
        <dependency>
            <groupId>org.apache.kafka</groupId>
            <artifactId>kafka-clients</artifactId>
            <version>0.10.2.0</version>
        </dependency>
        <dependency>
            <groupId>org.scala-lang</groupId>
            <artifactId>scala-library</artifactId>
            <version>2.11.11</version>
        </dependency>
        <dependency>
            <groupId>com.yammer.metrics</groupId>
            <artifactId>metrics-core</artifactId>
            <version>2.2.0</version>
        </dependency>
        <dependency>
            <groupId>com.101tec</groupId>
            <artifactId>zkclient</artifactId>
            <version>0.10</version>
        </dependency>
    </dependencies>
</project>
```
 生产者JAVA版

 
```
import org.apache.kafka.clients.producer.ProducerConfig;
import java.util.Properties;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;

/**
 * Created by hadoop on 17-6-30.
 */
public class KafkaJavaProducer {
    public final static String TOPIC = "kafka_test";
    public final static String BROKER_LIST = "localhost:9092";

    public static void main(String[]args){
        Properties props = new Properties();
        props.put("metadata.broker.list", BROKER_LIST);
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, BROKER_LIST);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,
                "org.apache.kafka.common.serialization.StringSerializer");
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,
                "org.apache.kafka.common.serialization.StringSerializer");

        System.out.println("开始生产消息...");
        KafkaProducer<String,String> producer = new KafkaProducer(props);
        while(true){
            for(int i=1;i<=10;i++) {
                producer.send(new ProducerRecord<String, String>(TOPIC, "key-"+i,"message-"+i));
            }
            try{
                Thread.sleep(3000);
            }catch (Exception e){
                e.printStackTrace();
            }
        }
    }
}

```
 生产者Scala版本

 
```
package com.kafka.demo

import java.util.Properties


import org.apache.kafka.clients.producer.{KafkaProducer, ProducerConfig, ProducerRecord, RecordMetadata}
import org.apache.kafka.common.serialization.StringSerializer

/**
  * Created by hadoop on 17-6-30.
  */
object  KafkaScalaProducer {

  def BROKER_LIST = "localhost:9092"
  def TOPIC = "kafka_test_4"

  def main(args: Array[String]): Unit = {
    println("开始产生消息！")
    val props = new Properties()
    props.put("metadata.broker.list", BROKER_LIST)
    props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, BROKER_LIST)
    props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, classOf[StringSerializer].getName)
    props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, classOf[StringSerializer].getName)

    val producer = new KafkaProducer[String, String](props)

    while(true){
      for (i <- 0 to 10) {
        producer.send(new ProducerRecord(TOPIC, "key-" + i, "msg-" + i))
      }
      Thread.sleep(3000)
    }
    producer.close
  }
}
```
 消费者Java版本

 
```
package com.java.kafka.demo;

import kafka.consumer.ConsumerConfig;
import kafka.consumer.ConsumerIterator;
import kafka.consumer.KafkaStream;
import kafka.javaapi.consumer.ConsumerConnector;
import kafka.message.MessageAndMetadata;

import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


/**
 * Created by hadoop on 17-6-30.
 */
public class KafkaJavaConsumer {
    private ConsumerConnector consumer;
    private org.apache.kafka.clients.consumer.KafkaConsumer<String, String> kafkaConsumer;
    private String topic="kafka_test_4";
    public KafkaJavaConsumer() {
        consumer = kafka.consumer.Consumer.createJavaConsumerConnector(createConsumerConfig());
    }
    private static ConsumerConfig createConsumerConfig() {
        Properties props = new Properties();
        props.put("zookeeper.connect", "localhost:2181");
        props.put("group.id", "test-consumer-group106");
        props.put("zookeeper.session.timeout.ms", "5000");
        props.put("auto.commit.interval.ms", "1000");
        props.put("rebalance.backoff.ms","3000");
        props.put("rebalance.max.retries","50");
        props.put("auto.offset.reset", "smallest");
        return new ConsumerConfig(props);
    }

    public void startConsume() {
        System.out.println("start consume......");
        Map<String, Integer> topicMap = new HashMap<String, Integer>();
        ExecutorService threadPool =  Executors.newFixedThreadPool(3);
        //设置3个线程去消费主题
        topicMap.put(topic, new Integer(3));
        Map<String, List<KafkaStream<byte[], byte[]>>> consumerStreamsMap = consumer.createMessageStreams(topicMap);
        List<KafkaStream<byte[], byte[]>> streamList = consumerStreamsMap.get(topic);
        System.out.println("streamList size is : "+streamList.size());
            int counter = 1;
            for (final KafkaStream<byte[], byte[]> stream : streamList) {
                try{
                    threadPool.submit(new Task("consumer_"+counter++,stream));
                }catch (Exception e){
                    e.printStackTrace();
                }
            }

    }

    static class Task implements Runnable{

        private String taskName;
        private KafkaStream<byte[],byte[]> stream;
        public Task(String taskName,KafkaStream<byte[], byte[]> stream){
            this.taskName = taskName;
            this.stream = stream;
        }

        @Override
        public void run() {
            System.out.println("task "+taskName+" is doing...");
            ConsumerIterator<byte[], byte[]> it = stream.iterator();
            while (it.hasNext()){
                MessageAndMetadata<byte[],byte[]> mes = it.next();
                System.out.println("task is : "+this.taskName+" ; Topic : "+mes.topic()+"; partition : "+mes.partition()+" ;  message : "+ new String(mes.message()));
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
        }
    }
    public static void main(String[] args) {

        KafkaJavaConsumer consumer = new KafkaJavaConsumer();
        consumer.startConsume();
    }
}
```
 消费者Scala版本

 
```
package com.kafka.demo

import java.util.Properties
import java.util.concurrent.{ExecutorService, Executors}

import kafka.consumer.{Consumer, ConsumerConfig, ConsumerIterator, KafkaStream}
import kafka.message.MessageAndMetadata

import scala.collection.Map
import scala.collection.mutable.HashMap

/**
  * Created by hadoop on 17-6-30.
  */
object KafkaScalaConsumer {

  def ZK_CONN     = "localhost:2181"
  def GROUP_ID    = "test-consumer-group108"
  def TOPIC       = "kafka_test_4"


  def main(args: Array[String]): Unit = {
    //println(" 开始了 ")

    val connector = Consumer.create(createConfig())

    val topicCountMap = new HashMap[String, Int]()
    topicCountMap.put(TOPIC, 3) // TOPIC在创建时就指定了它有3个partition

    val msgStreams: Map[String, List[KafkaStream[Array[Byte], Array[Byte]]]] = connector.createMessageStreams(topicCountMap)

    println("# of streams is " + msgStreams.get(TOPIC).get.size)

    val threadPool:ExecutorService=Executors.newFixedThreadPool(3)

    var index = 0;
    for (stream <- msgStreams.get(TOPIC).get) {
      threadPool.execute(new ThreadDemo("consumer_"+index,stream))
      index+=1;
    }
  }

  class ThreadDemo(threadName:String,stream:KafkaStream[Array[Byte], Array[Byte]]) extends Runnable{
    override def run(): Unit = {

      val it: ConsumerIterator[Array[Byte], Array[Byte]] = stream.iterator();

      while(it.hasNext()){
        val data : MessageAndMetadata[Array[Byte], Array[Byte]] = it.next()
        print("消费者名称："+threadName+" ");
        println("key ->["+new String(data.key)+"], message->["+new String(data.message)+"], " +
          "partition->["+data.partition+"], offset->["+data.offset+"]")
      }
    }
  }

  def createConfig(): ConsumerConfig = {
    val props = new Properties()
    props.put("zookeeper.connect", ZK_CONN)
    props.put("bootstrap.servers","localhost:9092")
    props.put("group.id", GROUP_ID)
    props.put("zookeeper.session.timeout.ms", "5000")
    props.put("zookeeper.connection.timeout.ms","10000")
    props.put("auto.offset.reset", "smallest")
    props.put("auto.commit.interval.ms", "300")
    props.put("rebalance.backoff.ms","2000")
    props.put("rebalance.max.retries","10")
    props.put("auto.offset.reset", "smallest")
    new ConsumerConfig(props)
  }
}
```
  
  * props.put(“auto.offset.reset”, “smallest”) ,该参数表示当此groupId下的消费者,在ZK中没有offset值时(比如新的groupId,或者是zk数据被清空),consumer应该从哪个offset开始消费.largest表示接受接收最大的offset(即最新消息),smallest表示最小offset,即从topic的开始位置消费所有消息. 
  * topicMap.put(topic, new Integer(3)); 这里与topic的partition个数相等。   
     在运行消费者的时候，遇到这样一个异常：  
```
kafka.common.ConsumerRebalanceFailedException: XXXXXXXXXXXXXXXXXXXXXXXXXXXXX can't rebalance after 5 retries
        at kafka.consumer.ZookeeperConsumerConnector$ZKRebalancerListener.syncedRebalance(ZookeeperConsumerConnector.scala:660)
        at kafka.consumer.ZookeeperConsumerConnector.kafka$consumer$ZookeeperConsumerConnector$$reinitializeConsumer(ZookeeperConsumerConnector.scala:967)
        at kafka.consumer.ZookeeperConsumerConnector.consume(ZookeeperConsumerConnector.scala:254)
        at kafka.javaapi.consumer.ZookeeperConsumerConnector.createMessageStreams(ZookeeperConsumerConnector.scala:84)

```
 网上搜索了一阵，基本给出的方案是：   
 rebalance.backoff.ms乘以rebalance.max.retries的值大于zookeeper.session.timeout.ms的值;   
 但是该方案对我来说并没有解决解决问题，后来又纠结了好久，网上说zookeeper 和zkClient的版本不一致导致，后来我修改了以下版本问题解决了。我按装zookeeper版本是：3.4.9 , maven 依赖为

 
```
<dependency>
            <groupId>com.101tec</groupId>
            <artifactId>zkclient</artifactId>
            <version>0.10</version>
        </dependency>
```
 之后问题解决了，希望能带大家带来帮助～～

   
  