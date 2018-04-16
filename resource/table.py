import sqlite3

from resource.condition import Condition


class Query:

    @staticmethod
    def fetch_to_dic(selected):
        list_of_data = []
        for items in selected.fetchall():
            data = {}
            for key, value in zip(selected.description, items):
                data[key[0]] = value
            list_of_data.append(data)

        return list_of_data

    def exec(self, query, commit=False):
        req = self.conn.execute(query)
        if commit:
            req.execute("COMMIT ")

        return self.fetch_to_dic(req)

    def all(self):
        return self.exec(f"SELECT * FROM {self.table_name} `{self.table_name}`")

    def get(self, *rows):
        all_rows = ""
        for row in rows:
            all_rows += row + ","
        return self.exec(f"SELECT {all_rows[0:-1]} FROM {self.table_name} `{self.table_name}` ")

    def filter(self, *condition: Condition):
        query = f"SELECT * FROM {self.table_name} `{self.table_name}` "
        for condition_item in condition:
            instruction = "WHERE" if "WHERE" not in query else "AND"
            query += f"{instruction} {condition_item} "

        return self.exec(query)

    def add(self, table, *condition: Condition):
        query = f"SELECT * FROM {self.table_name} `{self.table_name}` "
        for condition_item in condition:
            instruction = "JOIN" if "JOIN" not in query else "AND"
            query += f"{instruction} {table} `{table}` ON {condition_item}"

        return self.exec(query)

    def update(self, **columns):
        set_value = ""
        for key, value in columns.items():
            set_value += f"{key} = '{value}',"

        return self.exec(f"UPDATE {self.table_name} SET {set_value[0:-1]} ", True)

    def insert(self, **columns):
        all_keys = "".join(key + "," for key in columns.keys())
        all_values = "".join(f"'{value}'," for value in columns.values())
        return self.exec(f"INSERT INTO {self.table_name} ({all_keys[0:-1]}) VALUES ({all_values[0:-1]})", True)

    def delete(self, commit=False):
        return self.exec(f"DELETE FROM {self.table_name} ", commit)


class Table(Query):

    def __init__(self, table_name, table_row: tuple, path_database: str = "main.db"):
        self.conn = sqlite3.connect(path_database)
        self.table_name = table_name
        for row in table_row:
            setattr(self, row, f"{table_name}.{row}")

    def __str__(self):
        return self.table_name
