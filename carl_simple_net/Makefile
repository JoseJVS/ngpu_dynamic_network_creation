CC:=g++
INSTALL_PATH:=
CFLAGS:=-std=c++17 -Wall -Wextra -fpic -I$(INSTALL_PATH)/include
LFLAGS:=-lcarlsim -lcarlsim-stopwatch -L$(INSTALL_PATH)/lib -Wl,-rpath=$(INSTALL_PATH)/lib

.PHONY: all
all: run_benchmark.ex

run_benchmark.ex: run_benchmark.cpp
	$(CC) $(CFLAGS) $(LFLAGS) $^ -o $@

clean:
	rm -f run_benchmark.ex
