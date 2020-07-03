---
title: Leetcode 289. Game of Life
date: 2019-01-06 11:52:14
tags: CSDN迁移
---
  ### []()题目描述

  
  2. Game of Life  
      Medium  647

 131

 Favorite

 Share  
 According to the Wikipedia’s article: “The Game of Life, also known simply as Life, is a cellular automaton devised by the British mathematician John Horton Conway in 1970.”

 Given a board with m by n cells, each cell has an initial state live (1) or dead (0). Each cell interacts with its eight neighbors (horizontal, vertical, diagonal) using the following four rules (taken from the above Wikipedia article):

 Any live cell with fewer than two live neighbors dies, as if caused by under-population.  
 Any live cell with two or three live neighbors lives on to the next generation.  
 Any live cell with more than three live neighbors dies, as if by over-population…  
 Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.  
 Write a function to compute the next state (after one update) of the board given its current state. The next state is created by applying the above rules simultaneously to every cell in the current state, where births and deaths occur simultaneously.

 
### []()解题思路

 本题解题比较简单，就是遍历每一个cell,然后计算出neightbor的live数量，然后改变状态，之所以有难度就是因为后面的cell需要依赖前面的cell（cell[i,j] 需要依赖cell[i-1,j-1],但是cell[i-1,j-1]的状态已经变化了），但是前面的cell状态已经改变了，所以我们需要保存最初的状态。参考他人discuss，采取一个小技巧就是使用二进制.比如:十进制 1 的二进制01, 表示由1 变为0;十进制3 的二进制11 表示由1变为1.  
 转换规则如下：

  
  2. 邻居live数量小于2， 1 -> 0; 
  4. 邻居live数量等于2或者等于3, 1->1; 
  6. 邻居live数量大于等于4, 1->0; 
  8. 邻居live数量等于3, 0->1.  
      根据上面的情况其实case 1,3我们不需要处理，1 和 01的数值是一样的。下面给出代码。  
### []()代码

 
```
//向量用于遍历邻居
int []dimx = new int[]{-1,1,0,0,-1,-1,1,1};
    int []dimy = new int[]{0,0,-1,1,-1,1,-1,1};

    public void gameOfLife(int[][] board) {
        int n = board.length;
        int m = board[0].length;
        if (n==0||m==0) return;
        for (int i = 0;i<n;i++) {
            for(int j=0;j<m;j++) {
                int live = liveNeighbor(board,i,j,n,m);
                if(board[i][j] == 1 && (live==2 || live ==3)) {
                    board[i][j] = 3;
                } else if(board[i][j] == 0 && live == 3) {
                    board[i][j] = 2;
                }
            }
        }
//恢复数据
        for (int i=0;i<n;i++){
            for(int j=0;j<m;j++) {
                board[i][j] >>= 1;
            }
        }
    }
//计算live邻居的数量
    int liveNeighbor(int[][] board,int i,int j,int n,int m) {
        int live = 0;
        for (int k=0;k<8;k++){
            int tmpi = i + dimx[k];
            int tmpj = j + dimy[k];
            if(tmpi>=0 && tmpi<n && tmpj >=0 && tmpj<m) {
                live += board[tmpi][tmpj] & 1;
            }
        }
        return live;
    }

```
   
  