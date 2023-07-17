#include<stdio.h>    // importing header files
#include<float.h>
#include<limits.h>
#include<malloc.h>
#include<math.h>
int main()    // main function
{    
  int x=0,y=1,z,i,number=6;  // initializing 1st and 2nd Term and no. of terms     
  printf("\n%d %d",x,y);     // prints 1st and 2nd term
  for(i=2;i<number;++i)      // Loop to calculate Upcoming terms
  {    
    z=x+y;                   // calculating the next variable
    printf(" %d",z);         // Prints the next term
    x=y;                     // Swapping the values
    y=z;    
  }  
  return 0;     // Return Statement
}   