#! /usr/bin/python3
from src.db.Database import Database
from src.model.Vector import Vector

if __name__ == "__main__":
    print("Hello, World!")

    db = Database('cl-cache', 'db.suushiemaniac.com', 'cl2', 'wordembeddings')
    print("Database connected")

    corpus = "cca"
    lang = "English"
    dim = 10
    window = 5

    oneA = db.read_word_embedding('man', corpus, lang, dim, window)
    twoA = db.read_word_embedding('woman', corpus, lang, dim, window)

    oneB = db.read_word_embedding('king', corpus, lang, dim, window)
    twoB = db.read_word_embedding('queen', corpus, lang, dim, window)

    print("words cached")

    diffMaster = Vector.span(oneA, twoA)
    res = oneB.add(diffMaster)

    dist = Vector.span(twoB, res)

    print("references calculated")

    for word, embedding in db.yield_corpus(corpus, lang, dim, window):
        if embedding.in_radius(twoB, dist.norm()):
            print(word)
