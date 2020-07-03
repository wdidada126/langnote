---
title: Code interview 删除字符串中连续出现K个'0'
date: 2018-07-19 09:05:19
tags: CSDN迁移
---
  思路很简单，遍历数组遇到连续出现K个‘0’的情况就将其移除，就是用一个变量pos,其左侧是需要保留的字符（包括pos的位置）。   
 注意如果连续出现K+m 个0，m>0,这种情况是不需要移除的。下面给出代码：

 
```
public String removeZero(String str,int k) {

        int len = str.length();
        if(len < k) {
            return str;
        }

        int i = 0;
        int pos = -1;
        char[] chars = str.toCharArray();
        while(i < len) {
            if(chars[i] != '0') {
                chars[++pos] = chars[i++];
            } else {
                int count = 0;
                while(i < len && chars[i] == '0') {
                    count ++;
                    i++;
                }
                if(count != k) {
                    while(count>0) {
                        chars[++pos] = chars[i-count];
                        count--;
                    }
                }
            }
        }

        char[] tmp = new char[pos+1];
        System.arraycopy(chars,0,tmp,0,pos+1);
        return new String(tmp);
    }
```
   
  