import sqlite3

from Class.condition import Condition


class Table:

    def __init__(self, table_name, table_row: tuple, path_database: str = "example.db"):
        self.table_name = table_name
        self.query = self.Query(table_name, path_database)

        for row in table_row:
            setattr(self, row, f"{table_name}.{row}")

    class Query:

        def __init__(self, table_name, path_database):
            self.conn = sqlite3.connect(path_database)
            self.table_name = table_name

        @staticmethod
        def fetch_to_dic(selected):
            list_of_data = []
            for items in selected.fetchall():
                data = {}
                for key, value in zip(selected.description, items):
                    data[key[0]] = value
                list_of_data.append(data)

            return list_of_data

        def exec(self, query: str, commit: bool = False):
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
            all_keys = "".join(key + "," for key in columns.keys())[0:-1]
            all_values = "".join(f"'{value}'," for value in columns.values())[0:-1]
            return self.exec(f"INSERT INTO {self.table_name} ({all_keys}) VALUES ({all_values})", True)

        def delete(self, condition: Condition, commit=False):
            return self.exec(f"DELETE FROM {self.table_name} WHERE {condition}", commit)

    def __str__(self):
        return self.table_name
