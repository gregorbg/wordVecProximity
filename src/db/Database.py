from typing import Dict
from src.model.Vector import Vector

import pymysql


class Database:
    def __init__(self, db: str, host: str, user: str, passwd: str, port: int = 3306):
        self.cnx = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, autocommit=True)

    def read_word_embedding(self, word: str, corpus: str, dim: int) -> Vector:
        cursor = self.cnx.cursor()
        query = (
            "SELECT id "
            "FROM cl_words_cache "
            "WHERE word = %s "
            "AND corpus = %s "
            "AND dim = %s"
        )

        cursor.execute(query, (word, corpus, dim))
        (word_id) = cursor.fetchone()

        return self._word_from_db_id(word_id)

    def _word_from_db_id(self, word_id: int) -> Vector:
        cursor = self.cnx.cursor()
        query = (
            "SELECT `value` "
            "FROM cl_word_components "
            "WHERE word_id = %s "
            "ORDER BY `index` ASC"
        )

        cursor.execute(query, word_id)

        components = map(lambda t: (t or [None])[0], cursor.fetchall())  # hacky way to unpack single-element tuples
        return Vector(*components)

    def read_corpus(self, corpus: str, dim: int) -> Dict[str, Vector]:
        cursor = self.cnx.cursor()
        query = (
            "SELECT `id`, word "
            "FROM cl_words_cache "
            "WHERE corpus = %s "
            "AND dim = %s"
        )

        cursor.execute(query, (corpus, dim))
        db_words = cursor.fetchall()

        words = {}
        for (word_id, word_str) in db_words:
            words[word_str] = self._word_from_db_id(word_id)

        return words

    def cache_word_embedding(self, word: str, embedding: Vector, corpus: str):
        cursor = self.cnx.cursor()
        query = (
            "INSERT INTO cl_words_cache "
            "(corpus, dim, word) "
            "VALUES (%s, %s, %s)"
        )

        cursor.execute(query, (corpus, embedding.dim(), word))
        insert_id = cursor.lastrowid

        query = (
            "INSERT INTO cl_word_components "
            "(word_id, `index`, `value`) "
            "VALUES (%s, %s, %s)"
        )

        for index, component in enumerate(embedding):
            cursor.execute(query, (insert_id, index, component))
