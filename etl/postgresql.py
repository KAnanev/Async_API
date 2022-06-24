from __future__ import annotations  # Если версия python не поддерживает аннотации.

from datetime import datetime

from config import state_path
from sql_queries import genres_query, movies_query, persons_query
from state import JsonFileStorage, State


class PGLoader:
    def __init__(self, pg_conn, state_key='time'):
        self.conn = pg_conn
        self.cursor = self.conn.cursor()
        self.state_value = State(JsonFileStorage(state_path)).get_state(state_key)
        self.batch_size = 500
        self.data = []

    def get_state_value(self) -> str | datetime:
        if self.state_value is None:
            return datetime.min
        return self.state_value

    def pg_loader(self, index_name: str) -> list:
        queries = {'movies': movies_query,
                   'persons': persons_query,
                   'genres': genres_query
                   }

        query = queries.get(index_name)

        self.cursor.execute(query % self.get_state_value())
        while records := self.cursor.fetchmany(self.batch_size):
            for row in records:
                self.data.append(row)
        return self.data
