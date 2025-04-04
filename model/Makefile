# Compiler
CC = gcc

# Compiler flags
CFLAGS = -Wall -Wextra -Werror -pedantic -std=c99

build: experiments

experiments: bin_dir
	$(CC) $(CFLAGS) -o bin/$@ experiments.c util.c datasets.c model.c -lm 

bin_dir:
	mkdir -p bin

run: build
	cd bin/ && ./experiments

plot: run
	./model_plot.py

clean:
	rm -rf bin/

.PHONY: bin_dir run	plot clean