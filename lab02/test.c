#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char ** argv){
    if (strlen(argv[1])>280){
        exit(1);
    }
    printf("%lu: %s \n",strlen(argv[1]),argv[1]);
}
