CFLAGS = -I cudd/cudd -I cudd/util -I cudd
LFLAGS = -static -L cudd/cudd/.libs/ -lcudd -lm

default: builder

builder: builder.o
	$(CC) builder.o -o builder $(LFLAGS)

builder.o: builder.c
	$(CC) builder.c -c -o builder.o $(CFLAGS)
