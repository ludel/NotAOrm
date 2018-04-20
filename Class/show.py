from Class.condition import Condition
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

    def filter(self, condition: Condition) -> list:
        query = f"SELECT * FROM {self.table_name} `{self.table_name}` "
        for condition_item in condition:
            instruction = "WHERE" if "WHERE" not in query else "AND"
            query += f"{instruction} {condition_item} "

        return self.exec(query)

    def add(self, table, condition: Condition) -> list:
        query = f"SELECT * FROM {self.table_name} `{self.table_name}` "
        for condition_item in condition:
            instruction = "JOIN" if "JOIN" not in query else "AND"
            query += f"{instruction} {table} `{table}` ON {condition_item}"

        return self.exec(query)
