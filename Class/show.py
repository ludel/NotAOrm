from Class.query import Query


class Show(Query):

    def __init__(self, table_name, path_database):
        super().__init__(table_name, path_database)
        self.table_name = table_name

    def all(self) -> list:
        return self.exec(f"SELECT * FROM {self.table_name} `{self.table_name}`")

    def get(self, *rows) -> list:
        all_rows = ""
        for row in rows:
            all_rows += row + ","

        return self.exec(f"SELECT {all_rows[0:-1]} FROM {self.table_name} `{self.table_name}` ")

    def filter(self, condition) -> list:
        query = f"SELECT * FROM {self.table_name} `{self.table_name}` "
        query += f"WHERE {condition.sql()} "

        return self.exec(query)

    def add(self, table, condition) -> list:
        query = f"SELECT * FROM {self.table_name} `{self.table_name}` "
        instruction = "JOIN" if "JOIN" not in query else "AND"
        query += f"{instruction} {table} `{table}` ON {condition.sql()}"

        return self.exec(query)
