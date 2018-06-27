all: tool.out test.out

tool.out: tool.c randm.o
	gcc -o tool.out tool.c randm.o

randm.o: randm.c
	gcc -c randm.c

test.out: test.c
	gcc -o test.out test.c
