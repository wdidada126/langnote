#include <stdio.h>


#include <stdbool.h>

#define Integer int;

#define MAX_NUM 100;

 void chap2main()
{
	
	testDefine();
	
	system("pause");
	return;
}

 void testDefine() 
 {
	 int i = MAX_NUM;
	 int j = i - 12;
	 printf("int num is: %d \n",i);
	 bool isMax = j < MAX_NUM;
	 if (isMax)
	 {
	 	printf("j is less than MAX_NUM \n" );
	 }
	 printf("this is c source\n");
 }

 void getCharFromConsle()
 {
	 char temp;
	 temp = getchar();
	 while (temp != EOF)
	 {
		 putchar(temp);
		 temp = getchar();
	 }
	 return;
 }

  int printfEOF()
  {
	  printf("Hex=%x U=%u D=%d\n", EOF, EOF, EOF);
	  return 0;
  }
