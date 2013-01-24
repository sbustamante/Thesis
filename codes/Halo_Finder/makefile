CC=gcc
CFLAGS=-g -I. -c

#Principal Program
Pair_finder:inout.o finder.o halo_pairs.o
	gcc -lm inout.o finder.o halo_pairs.o -o Pair_finder.out
	rm -r *.o

edit:
	kate *.c *.h &

clean:
	rm -r *.o *.out *.png *.tmp script.gpl