/*
 * Exercise 5-2 from The C Programming Language, 2nd edition, by Kernighan
 * and Ritchie.
 *
 * "Write getfloat, the floating-point analog of getint. What type does
 * getfloat return as its function value?"
 */
 
/*
 * Here's the getint function, from section 5.2:
 */
 
#include <ctype.h>
#include <stdio.h>
 
int getch(void);
void ungetch(int);
 
/* getint:  get next integer from input into *pn */
int getint(int *pn)
{
        int c, sign;
        
        while (isspace(c = getch()))   /* skip white space */
                ;
        
        if (!isdigit(c) && c != EOF && c != '+' && c != '-') {
                ungetch(c);  /* it is not a number */
                return 0;
        }
        sign = (c == '-') ? -1 : 1;
        if (c == '+' || c == '-')
                c = getch();
        for (*pn = 0; isdigit(c); c = getch())
                *pn = 10 * *pn + (c - '0');
        *pn *= sign;
        if (c != EOF)
                ungetch(c);
        return c;
}
