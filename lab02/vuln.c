#include <string.h>
#include <stdio.h>
int main (int argc, char ** argv)
{
    char temp[212];       // string to hold large temp string
    strcpy(temp, argv[1]);   // take argv1 input and jam into temp
    printf(temp);
}
