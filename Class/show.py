from Class.query import Query


class Show(Query):

    def __init__(self, table_name, path_database):
        super().__init__(table_name, path_database)
        self.table_name = table_name

    def all(self, **kwargs) -> list:
        return self.exec(f"SELECT * FROM {self.table_name} `{self.table_name}`", **kwargs)

    def get(self, *rows, **kwargs) -> list:
        all_rows = ""
        for row in rows:
            all_rows += str(row) + ","

        return self.exec(f"SELECT {all_rows[0:-1]} FROM {self.table_name} `{self.table_name}` ", **kwargs)

    def filter(self, condition, **kwargs) -> list:
        query = f"SELECT * FROM {self.table_name} `{self.table_name}` " \
                f"WHERE {condition.sql()} "
        return self.exec(query, **kwargs)

    def add(self, table, condition, **kwargs) -> list:
        query = f"SELECT * FROM {self.table_name} `{self.table_name}` " \
                f"JOIN {table} `{table}` ON {condition.sql()}"

        return self.exec(query, **kwargs)
