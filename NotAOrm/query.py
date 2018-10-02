import sqlite3


class Query:

    def __init__(self, table_name, path_database):
        self.conn = sqlite3.connect(path_database)
        self.table_name = table_name

    @staticmethod
    def fetch_to_list(selected):
        list_of_data = []
        for items in selected.fetchall():
            data = {}
            for key, value in zip(selected.description, items):
                data[key[0]] = value
            list_of_data.append(data)

        return list_of_data

    def exec(self, query: str, **kwargs) -> list:
        if kwargs.get('group'):
            query += f" GROUP BY {kwargs.get('group')}"
        if kwargs.get('order'):
            query += f" ORDER BY {kwargs.get('order')}"
        if kwargs.get('limit'):
            query += f" LIMIT {kwargs.get('limit')}"
        req = self.conn.execute(query)

        if kwargs.get('commit'):
            req.execute("COMMIT ")

        return self.fetch_to_list(req)


class Change(Query):

    def __init__(self, table_name, path_database):
        super().__init__(table_name, path_database)
        self.table_name = table_name

    def update(self, condition, **columns) -> list:
        set_value = ""
        for key, value in columns.items():
            set_value += f"{key} = '{value}',"

        return self.exec(f"UPDATE {self.table_name} SET {set_value[0:-1]} WHERE {condition.sql()}", commit=True)

    def insert(self, **columns) -> list:
        all_keys = ",".join(key + "," for key in columns.keys())
        all_values = ",".join(f"'{value}'" for value in columns.values())

        return self.exec(f"INSERT INTO {self.table_name} ({all_keys}) VALUES ({all_values})", commit=True)

    def delete(self, condition, commit=False) -> list:
        return self.exec(f"DELETE FROM {self.table_name} WHERE '{condition.sql()}'", commit=commit)


class Show(Query):

    def __init__(self, table_name, path_database):
        super().__init__(table_name, path_database)
        self.table_name = table_name

    def all(self, **kwargs) -> list:
        return self.exec(f"SELECT * FROM {self.table_name} `{self.table_name}`", **kwargs)

    def get(self, *rows, **kwargs) -> list:
        all_rows = ",".join(rows)

        return self.exec(f"SELECT {all_rows} FROM {self.table_name} `{self.table_name}` ", **kwargs)

    def filter(self, condition, **kwargs) -> list:
        query = f"SELECT * FROM {self.table_name} `{self.table_name}` " \
                f"WHERE {condition.sql()}"

        return self.exec(query, **kwargs)

    def add(self, table, condition, **kwargs) -> list:
        query = f"SELECT * FROM {self.table_name} `{self.table_name}` " \
                f"JOIN {table} `{table}` ON {condition.sql()}"

        return self.exec(query, **kwargs)
