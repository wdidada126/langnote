---
title: 算法：KMP算法实现
date: 2018-02-25 13:55:24
tags: CSDN迁移
---
  ### KMP算法

 KMP的主要思想是当文本串与模式串发生不匹配的时候，可以减少移动模式串的次数，或者是更加准确的移动模式串减少比较的次数。   
 所以需要对模式串进行预处理。next数组则找出模式串的最大相同的前最和后缀，-1表示没有。0表示1个，1表示2个，依次类推。   
 例如模式串：   
 ababcab   
 则生成的next数组为：（-1，-1，0，1，-1，0，1）   
 next[0]=-1 ,表示模式串a没有最大前、后缀;   
 next[1]=-1,表示模式串ab没有最大前、后缀;   
 next[2]=0,表示模式串aba有1个最大前、后缀，其为a;   
 next[3]=1,表示模式串abab有2个最大前、后缀，其为ab;   
 next[4]=-1,表示模式串ababc没有最大前、后缀   
 next[5]=0,表示模式串ababca有1个最大前、后缀，其为a;   
 next[6]=1,表示模式串ababcab有2个最大前、后缀，其为ab;

 下面给出KMP的算法。

 
```
//生成next数组
private void next(char[] ptr,int []next) {

        int len = ptr.length;
        next[0] = -1;
        int k;
        for(int i=1;i<len;i++){

            k = next[i-1];
            while(k>-1 && ptr[i]!=ptr[k+1]){
                k = next[k];
            }
            if(ptr[i]==ptr[k+1]) {
                k ++;
            }
            next[i] = k;
        }
    }
  //字符匹配
  public int kmp(String str,String ptr){
        int [] next = new int[ptr.length()];
        next(ptr.toCharArray(),next);
        int k = -1;
        for(int i=0;i<str.length();i++){
            while(k>-1 && ptr.charAt(k+1)!=str.charAt(i)){
                k = next[k];
            }
            if(ptr.charAt(k+1) == str.charAt(i)){
                k++;
            }
            if(k==ptr.length()-1){
                return i-ptr.length()+1;
            }
        }
        return -1;
    }
```
   
  