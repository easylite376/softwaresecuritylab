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
    asm volatile ( "movq %%rbp, %%rax \n" //Get the stack base pointer into general purpose register
            "addq $8, %%rax \n"  //increase registe to return address
            "movq (%%rax), %%rax \n " // dereference return address
            "cmpq $0x12345678, (%%rax) \n" //compare label at the return address with static saved label to ensure Programm flow
            "je .LMAX\n " // Jump in success to Label MAX
            "movl $1, %%edi \n" // Set exit value to one in case of manipulation
            "movq $60, %%rax \n" //Set the syscall number for exit 
            "syscall\n" // invoce the kernel trap
            ".LMAX: \n" // Label MAX
            "addq $8, 8(%%rbp)" //Add 8 to the return address to bypass label and execute next instruction in main.
            :
            :
            :"rax"); //cobbler register (Register used in the assembly code)
}
int main (int argc, char **argv)
{
// call the vulnerable function
    vuln_copy(argv[1]);
    asm volatile ( "; .quad 0x12345678 \n"); // The label used for the check

}
void hack_me ()
{
    printf("Hacked!\n");
}
