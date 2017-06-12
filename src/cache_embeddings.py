#! /usr/bin/python3
import re
import sys

from src.model.Vector import Vector
from src.db.Database import Database


def read_data(filename: str) -> dict:
    words = {}

    with open(filename, "r") as file:
        for line in file:
            values = line.split()

            if len(values) > 2:
                words[values[0]] = Vector(*map(float, values[1:]))

    return words


def match_threshold(words: dict, a: str, b: str, c: str, d: str) -> float:
    return Vector.distance(words[c].add(Vector.span(words[a], words[b])), words[d])


def matches(words: dict, a: str, b: str, c: str, d: str) -> bool:
    return match_threshold(words, a, b, c, d) <= 0.01


if __name__ == "__main__":
    file = "/home/suushie_maniac/Schreibtisch/German-cca-100-11.txt"

    if re.match('.*-brown-.*', file):
        sys.stderr.write('nope.')
        exit(255)

    data = read_data(file)
    db = Database('cl-cache', 'localhost', 'root', 'localsql')

    db.begin_transaction()

    for word, embedding in data.items():
        print(word)
        db.cache_word_embedding(word, embedding, 'cca', 'de')

    db.commit()