#include<stdio.h>
#include<stdlib.h>
#include<string.h>
void vuln_copy (char *attack_source)
{
    char dest[20];
    char canary='1';
    printf("%p: %llx \n", (((void*)dest)+40),*(( unsigned long long* )(((void*)dest)+40)));
//insecure copy
    strcpy(dest, attack_source);
    if(canary!='1')
        exit(0);
}
int main (int argc, char **argv)
{
// call the vulnerable function
    vuln_copy(argv[1]);
}
void hack_me ()
{
    printf("Hacked!\n");
}
