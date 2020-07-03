#include <stdio.h>
#include <stdlib.h>

#define MAXOP 100
#define NUMBER '0'

int getop(char []);
void push(double);
double pull(void);

void main()
{
	int type;
	double op2;
	char s[MAXOP];
	
	while((type = getop(s)) != EOF)
	{
		switch(type){
			case NUMBER :
			push(atof(s));
			break;
			case '+':
				push(pull() + pull());
			break;
			case '-':
			push(pull() - pull());
			break;
			case '*':
			push(pull() * pull());
			break;
			case '/':
			op2 = pull();
			if(op2 != 0.0)
				push(pull() / op2);
			else
                printf("\nError: Division by zero!");
			break;
			case '%':
			op2 = pop();
			if(op2)
				push(fmod(pop(), op2));
			else
				printf("\nError: Division by zero!");
			break;			
			default:

			break;
		}
	}
	return 0;
}