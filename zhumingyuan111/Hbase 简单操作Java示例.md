---
title: Hbase 简单操作Java示例
date: 2017-06-24 19:57:52
tags: CSDN迁移
---
  ### Hbase 简单操作Java示例

 继之前完成hbase搭建之后，接下来学习了以下hbase简单的Java操作。在执行代码前需要先开启hadoop和zookeeper.   
 下面给出hbase代码：

 
```
import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.*;
import org.apache.hadoop.hbase.client.*;

import org.apache.hadoop.hbase.util.Bytes;

public class HbaseTest {

    public static Configuration configuration;
    static {
        configuration = HBaseConfiguration.create();
        configuration.set("hbase.zookeeper.property.clientPort", "2181");
        configuration.set("hbase.zookeeper.quorum", "localhost");
    }

    public static void main(String[] args) {
        //createTable("hbase_test1");
        //insertData("hbase_test1");
        getRowData("hbase_test1","rowkey00000001","F3","Q1");
        //scanData("hbase_test1");
        //deleteRow("hbase_test1","rowkey00000001");
    }


    public static void createTable(String tableName) {
        System.out.println("start create table ......");
        try {
            Connection connection = ConnectionFactory.createConnection(configuration);
            Admin admin = connection.getAdmin();
            TableName table = TableName.valueOf(tableName);
            if (admin.tableExists(table)) {// 如果存在要创建的表，那么先删除，再创建
                admin.disableTable(table);
                admin.deleteTable(table);
                System.out.println(tableName + " is exist,detele....");
            }
            HTableDescriptor tableDescriptor = new HTableDescriptor(table);
            tableDescriptor.addFamily(new HColumnDescriptor("F1"));
            tableDescriptor.addFamily(new HColumnDescriptor("F2"));
            tableDescriptor.addFamily(new HColumnDescriptor("F3"));
            admin.createTable(tableDescriptor);
            admin.close();
            connection.close();
        } catch (MasterNotRunningException e) {
            e.printStackTrace();
        } catch (ZooKeeperConnectionException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        System.out.println("end create table ......");
    }


    public static void insertData(String tableName) {
        System.out.println("start insert data ......");
        Put put = new Put("rowkey00000001".getBytes());// 一个PUT代表一行数据，再NEW一个PUT表示第二行数据,每行一个唯一的ROWKEY，此处rowkey为put构造方法中传入的值
        put.addColumn("F1".getBytes(), "Q1".getBytes(), "第一family第一qualifer_update".getBytes());// 本行数据的第一列
        //put.addColumn("F1".getBytes(), "Q2".getBytes(), "第一family第二qualifer".getBytes());
        put.addColumn("F2".getBytes(), "Q1".getBytes(), "第二family第一qualifer".getBytes());
        put.addColumn("F2".getBytes(), "Q2".getBytes(), "第二family第二qualifer".getBytes());
        put.addColumn("F3".getBytes(), "Q1".getBytes(), "第三family第一qualifer".getBytes());
        put.addColumn("F3".getBytes(), "Q2".getBytes(), "第三family第二qualifer".getBytes());
        put.addColumn("F1".getBytes(), null, "第一family,nullqualifer".getBytes());
        put.addColumn("F2".getBytes(), null, "第二family,nullqualifer".getBytes());
        put.addColumn("F3".getBytes(), null, "第三family,nullqualifer".getBytes());
        try {
            Connection connection = ConnectionFactory.createConnection(configuration);
            Table table = connection.getTable(TableName.valueOf(tableName));
            table.put(put);
            table.close();
            connection.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        System.out.println("end insert data ......");
    }


    public static void dropTable(String tableName) {
        try {
            Connection connection = ConnectionFactory.createConnection(configuration);
            Admin admin = connection.getAdmin();
            TableName table = TableName.valueOf(tableName);
            admin.disableTable(table);
            admin.deleteTable(table);
            admin.close();
            connection.close();
        } catch (MasterNotRunningException e) {
            e.printStackTrace();
        } catch (ZooKeeperConnectionException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public static void deleteRow(String tableName, String rowkey)  {
        try {
            Connection connection = ConnectionFactory.createConnection(configuration);
            Table table = connection.getTable(TableName.valueOf(tableName));
            Delete delete = new Delete(Bytes.toBytes(rowkey));
            //删除指定列族
            //delete.addFamily(Bytes.toBytes(colFamily));
            //删除指定列
            //delete.addColumn(Bytes.toBytes(colFamily),Bytes.toBytes(col));
            table.delete(delete);
            table.close();
            connection.close();
            System.out.println("删除行成功!");

        } catch (IOException e) {
            e.printStackTrace();
        }


    }

    public static void getRowData(String tableName,String rowkey,String colFamily,String col){
        try{
            Connection connection = ConnectionFactory.createConnection(configuration);
            Table table = connection.getTable(TableName.valueOf(tableName));
            Get get = new Get(Bytes.toBytes(rowkey));
            //获取指定列族数据
            get.addFamily(Bytes.toBytes(colFamily));
            //获取指定列数据
            get.addColumn(Bytes.toBytes(colFamily),Bytes.toBytes(col));
            Result result = table.get(get);
            showCell(result);
            table.close();
            connection.close();
        }catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void scanData(String tableName) {

        try {
            Connection connection = ConnectionFactory.createConnection(configuration);
            Table table = connection.getTable(TableName.valueOf(tableName));
            Scan scan = new Scan();
            //scan.setStartRow(Bytes.toBytes(startRow));
            //scan.setStopRow(Bytes.toBytes(stopRow));
            ResultScanner resultScanner = table.getScanner(scan);
            for(Result result : resultScanner){
                showCell(result);
            }
            table.close();
            connection.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    private static void showCell(Result result){
        Cell[] cells = result.rawCells();
        for(Cell cell:cells){
            System.out.println("RowName:"+new String(CellUtil.cloneRow(cell))+" ");
            System.out.println("Timetamp:"+cell.getTimestamp()+" ");
            System.out.println("column Family:"+new String(CellUtil.cloneFamily(cell))+" ");
            System.out.println("row Name:"+new String(CellUtil.cloneQualifier(cell))+" ");
            System.out.println("value:"+new String(CellUtil.cloneValue(cell))+" ");
        }
    }
}
```
 
### 注意

 在hbase 1.0版本之后不建议使用HTablePool对象，可使用Admin来跟Hbase交互。

   
  