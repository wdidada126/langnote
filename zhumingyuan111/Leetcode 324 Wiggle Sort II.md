---
title: Leetcode 324 Wiggle Sort II
date: 2018-12-30 16:58:17
tags: CSDN迁移
---
  ### []()题目描述

 Given an unsorted array nums, reorder it such that nums[0] < nums[1] > nums[2] < nums[3]…

 Example 1:

 Input: nums = [1, 5, 1, 1, 6, 4]  
 Output: One possible answer is [1, 4, 1, 5, 1, 6].  
 Example 2:

 Input: nums = [1, 3, 2, 2, 3, 1]  
 Output: One possible answer is [2, 3, 1, 3, 1, 2].  
 Note:  
 You may assume all input has valid answer.

 Follow Up:  
 Can you do it in O(n) time and/or in-place with O(1) extra space?

 
### []()解题思路

 此题是多路排序的变种，在多路排序中，我们会分为大于key,等于key和小于key三部分，这题我们也仿照此思路。首先我们求出中位数后面简称mid ，因为输入的数据保证有结果，所以输入数组必满足：  
 数组中大于mid的数量为n/2,比如：n=5,那么有2个元素大于mid;如果n=6，那么有3个元素大于mid。所以我们设计算法的时候保证位置1,3,5,7…的位置大于mid，同时2,4,6,8…的位置小于等于mid即可。在算法实现上很像快排的partition操作。下面给出代码：

 
```
public class WiggleSort {

    public void wiggleSort(int[] nums) {
        if (nums==null || nums.length==0) {
            return;
        }
        int n = nums.length;
        int i=0,j=0,k=n-1;
        int mid = getMid(nums,(n+1)/2,0,n-1);
        print(nums);
        //System.out.println("start to compute!");
        while (i<=k) {
            if (nums[index(i,n)] > mid) {
                swap(nums,index(i,n),index(j,n));
                i++;
                j++;
            } else if(nums[index(i,n)] < mid) {
                swap(nums,index(i,n),index(k,n));
                k--;
            } else {
                i++;
            }
            //print(nums);
        }
        System.out.println("final result : ");
        print(nums);
    }

    void print(int[] nums) {
        for(int n : nums) {
            System.out.print(n+",");
        }
        System.out.println();
    }

    int getMid(int[]a,int mid,int start,int end) {
        int key = a[start];
        int j = start-1;
        for(int i=start;i<=end;i++) {
            if(a[i] <= key) {
                swap(a,i,++j);
            }
        }
        swap(a,start,j);
        int count = j-start + 1;
        if (count==mid) {
            return key;
        } else if (count > mid) {
            return getMid(a,mid,start,j-1);
        } else {
            return getMid(a,mid - count,j+1,end);
        }
    }

    int index(int i,int n) {
        return (i*2+1) % (n|1);
    }

    void swap(int[]nums,int i,int j) {
        int tmp = nums[i];
        nums[i] = nums[j];
        nums[j] = tmp;
    }

    public static void main(String[]args) {
        WiggleSort wiggleSort = new WiggleSort();
        int [] nums = new int[]{1};
        int mid = wiggleSort.getMid(nums,(nums.length + 1)/2,0,nums.length-1);
        System.out.println("mid : " + mid);
        wiggleSort.wiggleSort(nums);
    }
}


```
   
  