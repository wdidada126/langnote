---
title: Leetcode  51. N-Queens
date: 2017-02-19 11:30:21
tags: CSDN迁移
---
  ## Leetcode

 
#### 51. N-Queens

 The n-queens puzzle is the problem of placing n queens on an n×n chessboard such that no two queens attack each other.

 Given an integer n, return all distinct solutions to the n-queens puzzle.

 Each solution contains a distinct board configuration of the n-queens’ placement, where ‘Q’ and ‘.’ both indicate a queen and an empty space respectively.

 For example,   
 There exist two distinct solutions to the 4-queens puzzle:

 [   
 [“.Q..”, // Solution 1   
 “…Q”,   
 “Q…”,   
 “..Q.”],

 [“..Q.”, // Solution 2   
 “Q…”,   
 “…Q”,   
 “.Q..”]   
 ]   
 原题可以查看   
 [https://leetcode.com/problems/n-queens/?tab=Description](https://leetcode.com/problems/n-queens/?tab=Description)

 解题思路：   
 深度优先搜索，进行遍历，若当前位置可以放“皇后”，则对下一行的位置进行遍历。下面给出代码：

 
```
public class Solution {
    public List<List<String>> solveNQueens(int n) {
        List<List<String>> result = new ArrayList<>();
        int[] recorder = new int[n+1];
        dfs(1,n,recorder,result);
        return result;
    }

//通过recorder 的记录给出其中一个可能的棋盘摆放结果
    private List<String> generateBlock(int []recorder,int n){

        List<String> block = new ArrayList<String>();
        for(int i=1;i<=n;i++){
            StringBuilder strBuilder = new StringBuilder();
            for(int j=1;j<=n;j++){
                if(recorder[i]==j){
                    strBuilder.append("Q");
                }else{
                    strBuilder.append(".");
                }
            }
            block.add(strBuilder.toString());
        }
        return block;
    }
//检查第x行，第y列能否放“皇后”
    private boolean put(int x,int y,int[]recorder){
        for(int i=1;i<x;i++){
            int dx = Math.abs(x-i);
            int dy = Math.abs(y-recorder[i]);
            if(dx==dy||dy==0)
                return false;
        }
        return true;
    }
//深度搜索
    private void dfs(int row,int n,int[]recorder,List<List<String>> result){
        if(row>n){
            result.add(generateBlock(recorder,n));
            return;
        }
        for(int i=1;i<=n;i++){
            if(put(row,i,recorder)){
                recorder[row]=i;
                dfs(row+1,n,recorder,result);
            }
        }
    }
}
```
 ![这里写图片描述](https://img-blog.csdn.net/20170219112541007?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvemh1bWluZ3l1YW4xMTE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

 欢迎大家提出宝贵意见。

   
  