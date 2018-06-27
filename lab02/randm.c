#include <stdlib.h>
#include <stdio.h>
#include <time.h>
void rand_str_ndc(char* arr,int size)
{
    int y=0;
    for( int i=0; i < size-1; i++)
    {
        while((y=rand()%255)==0);
        arr[i]=y;
    }
    arr[size-1]=0;
}

void rand_str_dc(char* dest, int length)
{
    char charset[] = "0123456789"
                     "abcdefghijklmnopqrstuvwxyz"
                     "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    while (--length > 0)
    {
        size_t index = (double) rand() / RAND_MAX * (sizeof charset - 1);
        *dest++ = charset[index];
    }
    *dest = '\0';
}
