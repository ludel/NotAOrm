import sqlite3

from resource.condition import Condition


class Table:
    path_database = "main.db"

    def __init__(self, table_name, table_row: tuple):
        self.table_name = table_name
        self.conn = sqlite3.connect(self.path_database)
        for row in table_row:
            setattr(self, row, f"{table_name}.{row}")

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
        print(query)
        req = self.conn.execute(query)
        if commit:
            req.execute("COMMIT ")

        return self.fetch_to_dic(req)

    def all(self):
        return self.exec(f"SELECT * FROM {self.table_name} `{self.table_name}` ")

    def get(self, *condition: Condition, order: str = "id", limit: int = 500):
        query = f"SELECT * FROM {self.table_name} `{self.table_name}` "
        for condition_item in condition:
            instruction = "WHERE" if "WHERE" not in query else "AND"
            query += f"{instruction} {condition_item} "
        query += f"ORDER BY {order} LIMIT {limit}"

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

    def __str__(self):
        return self.table_name
