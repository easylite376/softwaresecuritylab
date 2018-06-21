#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> /* for fork */
#include <sys/types.h> /* for pid_t */
#include <sys/wait.h> /* for wait */
#include "randm.h"

int main()
{
    char arr[16];
    char arr2[16];
    rand_str_dc(arr,15);
    rand_str_ndc(arr2,16);

    printf("%s \n",arr);
    printf("%s \n",arr2);
    pid_t pid=fork();
    if (pid==0)   /* child process */
    {
        static char *argv[]= {"test.out",NULL,NULL};
        argv[1]=arr;
        execv("./test.out",argv);
        exit(127); /* only if execv fails */
    }
    else   /* pid!=0; parent process */
    {
        waitpid(pid,0,0); /* wait for child to exit */
    }
    return 0;
}
