---
title: Leetcode 2SUM-3SUM-4SUM
date: 2016-11-13 23:21:47
tags: CSDN迁移
---
  之前刷过Leetcode 一些题，现在有时间整理一下！

 
## 2Sum

 
> 题意大概如下：   
>  Given an array of integers, return indices of the two numbers such that they add up to a specific target.You may assume that each input would have exactly one solution.   
>  Example:   
>  Given nums = [2, 7, 11, 15], target = 9,Because nums[0] + nums[1] = 2 + 7 = 9,return [0, 1].
> 
>  
 
#### 思路：本题采用双指针，先对给定的数组进行排序，然后一个指针Head在数组开头，另一个Rear指针指向数组最后一个一个元素，如果两个指针所指的元素之和等于目标值，则已找到答案返回，如果大于目标值，则Rear向前指一个;如果小于目标值，则Head向后移动一个元素。注意Head小于Rear的位置。

 
#### 代码如下：

 
```
public class Solution {

    static class Node implements Comparable<Node>{
        int index;
        int val;

        Node(int index,int val){
            this.index = index;
            this.val = val;
        }

        public int compareTo(Node node){
            return this.val - node.val;
        }

    }
    public int[] twoSum(int[] nums, int target) {
        int []result = new int[2];
        int len  = nums.length;
        int head = 0;
        int rear = len-1;
        int tmp;
        Node []nodes = new Node[len];
        for(int i=0;i<len;i++){
            nodes[i] = new Node(i,nums[i]);
        }
        Arrays.sort(nodes);
        while(head<rear){
            tmp = nodes[head].val+nodes[rear].val;
            if(tmp==target){
                result[0] = nodes[head].index;
                result[1] = nodes[rear].index;
                return result;
            }else if(tmp>target){
                rear--;
            }else{
                head++;
            }
        }
        return result;
    }
}
```
 
#### 运行结果：

 ![这里写图片描述](https://img-blog.csdn.net/20161113232245866)   
 ![这里写图片描述](https://img-blog.csdn.net/20161113232304195)   
 能用类似的方法完成3SUM和4SUM，因为在3SUM和4SUM中不需要记录数字的位置，只是返回数值的集合，所以这里还要对2SUM作出一点修改！先把3SUM和4SUM两个问题贴上来！

 
> Given an array S of n integers, are there elements a, b, c in S such that a + b + c = 0? Find all unique triplets in the array which gives the sum of zero.   
>  Note: The solution set must not contain duplicate triplets.
> 
>  
 
```
For example, given array S = [-1, 0, 1, 2, -1, -4],

A solution set is:
[
  [-1, 0, 1],
  [-1, -1, 2]
]
```
 3sum 问题就是在数组中找一个数，然后在剩下的数字中完成2SUM的操作;4SUM 问题就是在数组中找一个数，然后在剩余数字中完成3SUM的操作！   
 下面先把2SUM的代码修改一下！

 
```
public void sum2Helper(int[]a,int target,int start,int end,int cur,List<List<Integer>>result){
        int head = start;
        int rear = end;
        int tmp;
        while(head<rear) {
            tmp = a[head] + a[rear];
            if (tmp == target) {
                List<Integer> row = new ArrayList<Integer>();
                row.add(a[head]);
                row.add(a[rear]);
                row.add(a[cur]);
                result.add(row);
                head++;
                rear--;
                while (head<=rear&&a[head] == a[head - 1]) {
                    head++;
                }
                while (rear>=0&&a[rear] == a[rear + 1]) {
                    rear--;
                }
            } else if (tmp < target) {
                head++;
            } else {
                rear--;
            }
        }
    }
```
 下面给出3SUM完整代码！

 
```
public class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);
        return sum3(nums,0);
    }

    public List<List<Integer>> sum3(int[]a,int target){
        int len = a.length;
        List<List<Integer>> result = new ArrayList<List<Integer>>();
        for(int i=0;i<len-2;i++){
            if(i>0&&a[i]==a[i-1]){
                continue;
            }
            sum2Helper(a,target-a[i],i+1,len-1,i,result);
        }
        return result;
    }


    public void sum2Helper(int[]a,int target,int start,int end,int cur,List<List<Integer>>result){
        int head = start;
        int rear = end;
        int tmp;
        while(head<rear) {
            tmp = a[head] + a[rear];
            if (tmp == target) {
                List<Integer> row = new ArrayList<Integer>();
                row.add(a[head]);
                row.add(a[rear]);
                row.add(a[cur]);
                result.add(row);
                head++;
                rear--;
                while (head<=rear&&a[head] == a[head - 1]) {
                    head++;
                }
                while (rear>=0&&a[rear] == a[rear + 1]) {
                    rear--;
                }
            } else if (tmp < target) {
                head++;
            } else {
                rear--;
            }
        }
    }
}
```
 在3SUM上进行改进，支持4SUM！

 
```
public class Solution {
    public List<List<Integer>> fourSum(int[] nums, int target) {
        Arrays.sort(nums);
        return sum4(nums,target);
    }

    public List<List<Integer>> sum4(int[]a,int target){
        int len = a.length;
        List<List<Integer>> result = new ArrayList<List<Integer>>();
        for(int i=0;i<len-3;i++){
            if(i>0&&a[i]==a[i-1]){
                continue;
            }
            sum3Helper(a,target-a[i],i+1,len-1,i,result);
        }
        return result;
    }

    public void sum3Helper(int[]a,int target,int start,int end,int cur,List<List<Integer>>result){
        for(int i=start;i<=end;i++){
            if(i>start&&a[i-1]==a[i]){
                continue;
            }
            sum2Helper(a,target-a[i],i+1,end,i,cur,result);
        }
    }
    public void sum2Helper(int[]a,int target,int start,int end,int cur3,int cur4,List<List<Integer>>result){
        int head = start;
        int rear = end;
        int tmp;
        while(head<rear) {
            tmp = a[head] + a[rear];
            if (tmp == target) {
                List<Integer> row = new ArrayList<Integer>();
                row.add(a[head]);
                row.add(a[rear]);
                row.add(a[cur3]);
                if(cur4>=0)
                    row.add(a[cur4]);
                result.add(row);
                head++;
                rear--;
                while (head<=rear&&a[head] == a[head - 1]) {
                    head++;
                }
                while (rear>=0&&a[rear] == a[rear + 1]) {
                    rear--;
                }
            } else if (tmp < target) {
                head++;
            } else {
                rear--;
            }
        }
    }
}
```
 最后给出4SUM 的运行结果！时间是O(n3)   
 ![这里写图片描述](https://img-blog.csdn.net/20161113234138179)

   
  