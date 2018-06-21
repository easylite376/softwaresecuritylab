#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> /* for fork */
#include <sys/types.h> /* for pid_t */
#include <sys/wait.h> /* for wait */

int main()
{
    /*Spawn a child to run the program.*/
    char arr[4];
    arr[0]='c';
    arr[1]=7;
    arr[2]=8;
    arr[3]=0;
    pid_t pid=fork();
    if (pid==0) { /* child process */
        static char *argv[]={"test.out",NULL,NULL};
        argv[1]=arr;
        execv("./test.out",argv);
        exit(127); /* only if execv fails */
    }
    else { /* pid!=0; parent process */
        sleep(300);
        waitpid(pid,0,0); /* wait for child to exit */
    }
    return 0;
}
