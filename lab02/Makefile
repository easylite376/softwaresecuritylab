all: tool.out test.out vuln.out 

tool.out: tool.c randm.o
	gcc -g -o tool.out tool.c randm.o

randm.o: randm.c
	gcc -g -c randm.c

test.out: test.c
	gcc -o test.out test.c

vuln.out: vuln.c
	gcc -o vuln.out vuln.c

clean:
	rm *.out
	rm *.o
