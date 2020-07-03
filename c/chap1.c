#include <stdio.h>

chap1main()
{
	countCharNumss();
}

void countCharNumss()
 {
  int lll = 1;
  while (getchar() != EOF)
  {
	  lll++;
  }
  printf("count num is: %d", lll);
 }