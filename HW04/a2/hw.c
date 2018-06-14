#include<stdio.h>
#include<stdlib.h>
#include<string.h>
void vuln_copy (char *attack_source)
{
    unsigned long long flag;
    char dest[20];
    char canary='1';
//insecure copy
    strcpy(dest, attack_source);
    if(canary!='1')
        exit(0);
    asm volatile ( "movq %%rbp, %%rax \n"
            "addq $8, %%rax \n"
            "movq (%%rax), %%rax \n "
            "cmpq $0x12345678, (%%rax) \n"
            "je  .LMAX\n "
            "movl    $1, %%edi \n"
            "call    exit@PLT \n"
            ".LMAX: \n"
            "addq $8, 8(%%rbp)"
            :
            :
            :"rax");
}
int main (int argc, char **argv)
{
// call the vulnerable function
    vuln_copy(argv[1]);
    asm volatile ( "; .quad 0x12345678 \n");

}
void hack_me ()
{
    printf("Hacked!\n");
}
