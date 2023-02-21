CC = g++
CFLAGS = -Wall -g -O0
OBJS = main.o comp.o
TARGET = lr1

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(TARGET)

main.o: main.cpp comp.h
	$(CC) $(CFLAGS) -c main.cpp

comp.o: comp.cpp comp.h
	$(CC) $(CFLAGS) -c comp.cpp

clean:
	rm -f $(OBJS) $(TARGET)