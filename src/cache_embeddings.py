#! /usr/bin/python3
import lzma
import re
import requests

from io import BytesIO
from .model.Vector import Vector
from .db.Database import Database


def read_file_data(filename: str) -> dict:
    words = {}

    with open(filename, "r") as fs_file:
        for f_line in fs_file:
            values = f_line.split()

            if len(values) > 2:
                words[values[0]] = Vector(*map(float, values[1:]))

    return words


def read_lzma_data(lzma_file: lzma.LZMAFile) -> dict:
    words = {}

    for lzma_line in lzma_file:
        values = lzma_line.split()

        if len(values) > 2:
            words[values[0]] = Vector(*map(float, values[1:]))

    return words


def match_threshold(words: dict, a: str, b: str, c: str, d: str) -> float:
    return Vector.distance(words[c].add(Vector.span(words[a], words[b])), words[d])


def matches(words: dict, a: str, b: str, c: str, d: str) -> bool:
    return match_threshold(words, a, b, c, d) <= 0.01


if __name__ == "__main__":
    db = Database('cl-cache', 'localhost', 'root', 'localsql')

    url = "http://arne.chark.eu/emnlp2015/"
    source = requests.get(url).text

    for line in re.finditer(r"<li><a href=\"(http://chark\.synology\.me/arne/emnlp2015/(([A-Z][a-z]+?)-(.+?)-(\d+)-("
                            r"\d+)\.txt\.xz))\">\2</a></li>", source):
        link = line.group(1)
        file = line.group(2)

        lang = line.group(3)
        corpus = line.group(4)
        dim = line.group(5)
        window = line.group(6)

        if lang in ["German", "English", "French"] and corpus != "brown" and dim == "10":
            xz = requests.get(link, stream=True)

            with lzma.LZMAFile(BytesIO(xz.content)) as f:
                data = read_lzma_data(f)

                db.begin_transaction()

                for word, embedding in data.items():
                    print(word)
                    db.cache_word_embedding(word, embedding, corpus, lang, window)

                db.commit()
