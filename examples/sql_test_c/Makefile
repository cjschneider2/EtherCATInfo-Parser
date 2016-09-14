all: sql_test.c sqlite3.c
	clang sql_test.c sqlite3.c -lpthread -ldl -g -o sql_test

run: all
	./sql_test

clean:
	rm *.o
