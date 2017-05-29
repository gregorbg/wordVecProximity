#! /usr/bin/python3
import re

import sys

from src.Vector import Vector


def read_data(filename: str) -> dict:
    words = {}

    with open(filename, "r") as file:
        for line in file:
            values = line.split()

            if len(values) > 2:
                words[values[0]] = Vector(*map(float, values[1:]))

    return words


def read_tests(filename: str) -> list:
    cases = []

    with open(filename, "r") as file:
        for line in file:
            values = re.findall('(.*):(.*) => (.*):(.*)', line)

            if len(values) == 1:
                cases.append(values[0])

    return cases


def analogy(words: dict, a: str, b: str, c: str) -> list:
    check_dist = Vector.distance(words[a], words[b])
    distances = {}
    candidates = []

    for key in words.keys():
        if key != c:
            distances[key] = Vector.distance(words[c], words[key])

    for key in distances.keys():
        if abs(check_dist - distances[key]) <= 0.01:
            candidates.append((key, distances[key]))

    return sorted(candidates, key=lambda x: x[1])


def match_threshold(words: dict, a: str, b: str, c: str, d: str) -> float:
    return Vector.distance(words[c].add(Vector.span(words[a], words[b])), words[d])


def matches(words: dict, a: str, b: str, c: str, d: str) -> bool:
    return match_threshold(words, a, b, c, d) <= 0.01


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write('Please specify a data input file and a test input file!')
        exit(1)

    if re.match('.*-brown-.*', sys.argv[0]):
        sys.stderr.write('nope.')
        exit(255)

    tests = read_tests(sys.argv[0])
    data = read_data(sys.argv[1])

    for test in tests:
        print(match_threshold(data, *test))
