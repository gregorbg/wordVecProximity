from src.model.Vector import Vector
import pymysql


class Database:
    def __init__(self, conn_args):
        self.cnx = pymysql.connect(**conn_args)

    def read_word_embedding(self, word: str, corpus: str, dim: int) -> Vector:
        cursor = self.cnx.cursor()
        query = (
            "SELECT id "
            "FROM cl_words_cache "
            "WHERE word = ?"
            "AND corpus = ? "
            "AND dim = ?"
        )

        cursor.execute(query, (word, corpus, dim))
        res = cursor.fetchone()

        word_id = res["word_id"]

        query = (
            "SELECT `value` "
            "FROM cl_word_components "
            "WHERE word_id = ?"
            "ORDER BY dim ASC"
        )

        cursor.execute(query, word_id)

        components = []
        for value in cursor:
            components.append(value)  # FIXME is there a "collect" in Python? Can it work on MySQL cursors?

        return Vector(*components)

    def cache_word_embedding(self, word: str, embedding: Vector, corpus: str):
        cursor = self.cnx.cursor()
        query = (
            "INSERT INTO cl_words_cache "
            "(corpus, dim, word) "
            "VALUES (?, ?, ?)"
        )

        cursor.execute(query, (corpus, embedding.dim(), word))
        insert_id = cursor.lastrowid

        query = (
            "INSERT INTO cl_word_components "
            "(word_id, index, `value`) "
            "VALUES (?, ?, ?)"
        )

        for (index, component) in enumerate(embedding):
            cursor.execute(query, (insert_id, index, component))
