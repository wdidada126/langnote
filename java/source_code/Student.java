package com.xxxx.medium.test.isomerization.proxy.web;

import com.google.gson.Gson;

import java.util.ArrayList;
import java.util.HashMap;

public class Student {
    public int id;
    public String nickName;
    public String email;
    public int age;
    public ArrayList<String> books;
    public HashMap<String, String> booksMap;

    public static void main(String[] args) {
        Gson gson = new Gson();
        student.id = 1;
        student.nickName = "乔晓松";
        student.age = 22;
        student.email = "965266509@qq.com";
        System.out.println("MainActivity:"+gson.toJson(student));
//        Gson gson = new Gson();
//        Student student = new Student();
//        student.id = 1;
//        student.nickName = "乔晓松";
//        student.age = 22;
//        student.email = "965266509@qq.com";
//        ArrayList<String> books = new ArrayList<String>();
//        books.add("数学");
//        books.add("语文");
//        books.add("英语");
//        books.add("物理");
//        books.add("化学");
//        books.add("生物");
//        student.books = books;
//        Log.e("MainActivity", gson.toJson(student));
//
//        Gson gson = new Gson();
//        Student student = new Student();
//        student.id = 1;
//        student.nickName = "乔晓松";
//        student.age = 22;
//        student.email = "965266509@qq.com";
//        ArrayList<String> books = new ArrayList<String>();
//        books.add("数学");
//        books.add("语文");
//        books.add("英语");
//        books.add("物理");
//        books.add("化学");
//        books.add("生物");
//        student.books = books;
//        HashMap<String, String> booksMap = new HashMap<String, String>();
//        booksMap.put("1", "数学");
//        booksMap.put("2", "语文");
//        booksMap.put("3", "英语");
//        booksMap.put("4", "物理");
//        booksMap.put("5", "化学");
//        booksMap.put("6", "生物");
//        student.booksMap = booksMap;
//        Log.e("MainActivity", gson.toJson(student));


    }
}
