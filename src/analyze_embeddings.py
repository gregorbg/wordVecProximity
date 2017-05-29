#! /usr/bin/python3

import math
import sys

def read_data(filename):
	words = {}
	with open(filename, "r") as file:
		for line in file:
			values = line.split()
			if len(values) > 2:
				words[values[0]] = tuple(map(float, values[1:]))
	return words

def get_distance(p, q):
	sq_sum = 0 
	for x,y in zip(p, q):
		sq_sum += (x - y) ** 2
	return math.sqrt(sq_sum)

def analogy(words, a, b, c):
	dist = get_distance(words[a], words[b])
	distances = {}
	candidates = []
	for key in words.keys():
		if key != c:
			distances[key] = get_distance(words[c], words[key])
	for key in distances.keys():
		if abs(dist - distances[key]) <= 0.01:
			candidates.append((key, distances[key]))
	return sorted(candidates, key = lambda x: x[1])


if __name__ == "__main__":
	files = sys.argv[1:]
	assert len(files) == 2, "Kann nur zwei Dateien entgegennehmen!"
	data0 = read_data(files[0])
	data1 = read_data(files[1])
	print(analogy(data1, "Fohlen", "Pferd", "Kalb"))
