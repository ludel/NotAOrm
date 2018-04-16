import sqlite3

from .query import Query


class Table(Query):

    def __init__(self, table_name, table_row: tuple, path_database: str = "main.db"):
        self.conn = sqlite3.connect(path_database)
        self.table_name = table_name

        for row in table_row:
            setattr(self, row, f"{table_name}.{row}")

    def __str__(self):
        return self.table_name
