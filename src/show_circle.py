#! /usr/bin/python3
from src.db.Database import Database
from src.model.Vector import Vector

if __name__ == "__main__":
    print("Hello, World!")

    db = Database('cl-cache', 'localhost', 'root', 'localsql')
    corpus = db.read_corpus('cca', 100)

    oneA = corpus['Fohlen']
    twoA = corpus['Pferd']

    oneB = corpus['Kalb']
    twoB = corpus['Rind']

    diffMaster = Vector.span(oneA, twoA)
    res = oneB.add(diffMaster)

    dist = Vector.span(twoB, res)

    for word, embedding in corpus.items():
        if embedding.in_radius(twoB, dist.norm()):
            print(word)
