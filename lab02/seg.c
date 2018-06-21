#include <stdio.h>
#include <unistd.h>

int main(int argc, char ** argv){
    int *ptr =0;
    *ptr=5;
    printf("%s",argv[1]);
    sleep(300);
}
