#include <stdio.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <time.h>
#include <sys/stat.h>
#include <sys/param.h>
#include <sys/types.h>
#include <limits.h>
#include <string.h>
#include <unistd.h> /* for fork */
#include <sys/types.h> /* for pid_t */
#include <sys/wait.h> /* for wait */
#include "randm.h"
#include <getopt.h>
# define RETRYS 3
int fd;
int get_arg_max()
{
#ifdef ARG_MAX
    return ARG_MAX;
#else
    int value = sysconf (_SC_ARG_MAX);
    if (value < 0)
    {
        fprintf(stderr,"Couldn't get ARG_MAX from sysconf! Not a POSIX System?\n");
        exit(2);
    }
    return value;
#endif
}

int check_status(int status,char** args,char* argument)
{
    if (WIFSIGNALED(status))
    {
        if (WTERMSIG(status) == SIGSEGV || WTERMSIG(status) == SIGILL )
        {
            fprintf(stderr,"Overflow detected of %s, with the input: \n %s \n",args[0],
                    argument);
        }
        else if (WTERMSIG(status) == SIGABRT )
        {
            fprintf(stderr,
                    "Signal Abort detected of %s, with the input: \n %s \nThis is probably send by glibc Stackprotector \n",
                    args[0],argument);
        }
        else
        {
            fprintf(stderr,
                    "Signal: %d  got cought on execution of %s, with the input: \n %s \n",
                    WTERMSIG(status), args[0],
                    argument);
        }
        exit(0);
    }
    if(WIFEXITED(status))
    {
        if(WEXITSTATUS(status)!=0)
        {
            return 1;
        }
    }
    return 0;
}

void build_format_string(char *argument, int count )
{
    if (sizeof (void*)==8)
    {
        rand_str_ndc(argument,9);
        for ( int i=0; i<count; i++)
        {
            strcat(argument, " %016lx");
            /* Pattern for 64 bit Machines "AAAAAAAA %016lx %016lx %016lx %016lx %016lx %016lx %016lx %s" */
        }
        strcat(argument, " %s");
    }
    else if ( sizeof(void*)==4)
    {
        rand_str_ndc(argument,5);
        for ( int i=0; i<count; i++)
        {
            strcat(argument, " %08x");
            /* Pattern for 32 bit Machines "AAAAAAAA %08x %08x %08x %08x %08x %08x %08x %s" */
        }
        strcat(argument, " %s");
    }
    else
    {
        fprintf(stderr,
                "This tool can only fuzz format strings on 32bit and 64bit machines!");
        exit(1);
    }
}

void format_detection(char **argv, char* argument)
{
    static char *args[]= {NULL,NULL,NULL};
    args[0]=argv[1];
    int status=0;
    for(int i=0; i<960; i++)
    {
        build_format_string(argument,(i%15)+5 );
        pid_t pid=fork();
        if (pid==0)   /* child process */
        {
            dup2(fd, 1);
            dup2(fd, 2);
            args[1]=argument;
            execv(argv[1],args);
            exit(127); /* only if execv fails */
        }
        else   /* pid!=0; parent process */
        {
            waitpid(pid,&status,0); /* wait for child to exit */
            if(check_status(status,args,argument))
                continue;
        }
    }
}
void overflow_detection(char **argv,char* argument)
{
    static char *args[]= {NULL,NULL,NULL};
    args[0]=argv[1];
    int i=1,count=0,status=0,error=0,last=1;
    while(i<=get_arg_max())
    {
        rand_str_dc(argument,i);
        pid_t pid=fork();
        if (pid==0)   /* child process */
        {
            dup2(fd, 1);
            dup2(fd, 2);
            args[1]=argument;
            execv(argv[1],args);
            exit(127); /* only if execv fails */
        }
        else   /* pid!=0; parent process */
        {
            waitpid(pid,&status,0); /* wait for child to exit */
            if((error=check_status(status,args,argument)))
                break;
            if (count < RETRYS )
                count++;
            else
            {
                last=i;
                i*=2;
                count=0;
            }
        }
    }
    count=0;
    if (error ==1)
    {
        while(last<i)
        {
            rand_str_dc(argument,last);
            pid_t pid=fork();
            if (pid==0)   /* child process */
            {
                dup2(fd, 1);
                dup2(fd, 2);
                args[1]=argument;
                execv(argv[1],args);
                exit(127); /* only if execv fails */
            }
            else   /* pid!=0; parent process */
            {
                check_status(status,args,argument);
                if (count < RETRYS )
                    count++;
                else
                {
                    last++;
                    count=0;
                }
            }
        }
    }
}
int main(int argc,char** argv)
{
    struct stat sb;
    if (argc!=3)
    {
        printf("This tool requires 2 arguments \n tool.out PROGRAM OVERFLOW|FORMATSTRING \n");
        exit(1);
    }
    if( !(strncmp(argv[2],"OVERFLOW",8)==0  || strncmp(argv[2],"FORMATSTRING",12) ==0 ))
    {
        printf("This tool requires 2 arguments \n tool.out PROGRAM OVERFLOW|FORMATSTRING \n");
        exit(1);
    }
    if( access( argv[1], F_OK ) < 0 )
    {
        printf("This tool requires 2 arguments \n tool.out PROGRAM OVERFLOW|FORMATSTRING \n");
        exit(1);
    }
    int ret = stat(argv[1], &sb);
    if (!(ret == 0 && (sb.st_mode & S_IXUSR)))
    {
        printf("This tool requires 2 arguments \n tool.out PROGRAM OVERFLOW|FORMATSTRING \n");
        exit(1);
    }
    char* argument = (char *) calloc(get_arg_max(),1);
    fd = open("/dev/null",O_WRONLY | O_CREAT, 0666);   // open the file /dev/null
    srand(time(NULL));
    //rand_str_ndc(arr2,16);
    if(!(strncmp(argv[2],"OVERFLOW",8)))
    {
        overflow_detection( argv,argument);
    }
    else
    {
        format_detection(argv,argument);
    }
    close(fd);
    printf("Nothing found :(\n");
    return 0;
}
