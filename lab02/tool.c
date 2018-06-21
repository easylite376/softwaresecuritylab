#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <string.h>
#include <unistd.h> /* for fork */
#include <sys/types.h> /* for pid_t */
#include <sys/wait.h> /* for wait */
#include "randm.h"
#include <getopt.h>

int main(int argc,char** argv)
{
    struct stat sb;
    if (argc!=3){
        printf("This tool requires 2 arguments \n tool.out PROGRAM OVERFLOW|FORMATSTRING \n");
        exit(1);
    }
    if(! ( strncmp(argv[2],"OVERFLOW",8)  || strncmp(argv[2],"FORMATSTRING",12))){
        printf("This tool requires 2 arguments \n tool.out PROGRAM OVERFLOW|FORMATSTRING \n");
        exit(1);
    }
    if( access( argv[1], F_OK ) < 0 ) {
        printf("This tool requires 2 arguments \n tool.out PROGRAM OVERFLOW|FORMATSTRING \n");
        exit(1);
    }
    int ret = stat(argv[1], &sb);
    if (!(ret == 0 && (sb.st_mode & S_IXUSR))) {
        printf("This tool requires 2 arguments \n tool.out PROGRAM OVERFLOW|FORMATSTRING \n");
        exit(1);
    }

    char arr[16];
    char arr2[16];
    rand_str_dc(arr,16);
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
