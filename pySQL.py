import sqlite3

from resource.condition import Condition, Operator as Opp
from resource.sortEnum import Sort


class PySQL:
    query = ""

    def __init__(self, path_database):
        self.path_database = path_database
        self.conn = sqlite3.connect(path_database)

    @staticmethod
    def fetch_to_dic(selected):
        list_of_data = []
        for items in selected.fetchall():
            data = {}
            for key, value in zip(selected.description, items):
                data[key[0]] = value
            list_of_data.append(data)

        return list_of_data

    def exec(self, commit=False):
        req = self.conn.execute(self.query)
        if commit:
            req.execute("COMMIT ")

        return self.fetch_to_dic(req)

    def get(self, table: str, row: str = "*"):
        self.query = f"SELECT {row} FROM {table} `{table}` "

    def where(self, condition: Condition):
        instruction = "WHERE" if "WHERE" not in self.query else "AND"
        self.query += f"{instruction} {condition.row_from} {condition.operator.value} {condition.row_to} "

    def add(self, table: str, condition: Condition):
        instruction = "JOIN" if "JOIN" not in self.query else "AND"
        self.query += f"{instruction} {table} `{table}`" \
                      f" ON {condition.row_from} {condition.operator.value} {condition.row_to} "


    def order(self, key: str, sort: Sort = Sort.Asc):
        self.query += f"ORDER BY {key} {sort.value} "

    def group(self, key: str):
        self.query += f"GROUP BY {key} "

    def limit(self, number: int):
        self.query += f"LIMIT {number} "

    def update(self, table: str, **columns):
        set_value = ""
        for key, value in columns.items():
            set_value += f"{key} = '{value}',"
        self.query = f"UPDATE {table} SET {set_value[0:-1]} "

        return self.query

    def insert(self, table: str, **columns):
        all_keys = "".join(key + "," for key in columns.keys())
        all_values = "".join(f"'{value}'," for value in columns.values())
        self.query = f"INSERT INTO {table} ({all_keys[0:-1]}) VALUES ({all_values[0:-1]}) "

    def delete(self, table):
        self.query = f"DELETE FROM {table} "

        return self.query

    def __str__(self):
        return "SQL Request : " + self.query


if __name__ == '__main__':
    # Exemple 
        # o = PySQL('#DataBase.bd')
        # o.get("TABLE_1", "column1, column2")
        # o.join("TABLE_2", Condition("value_table_2.id", Opp.equ, "value_table_1.id"))
        # o.where(Condition("value_table_1.id", Opp.sup, 10))
        # o.order("value_table_1.id", Sort.Desc)
        # o.limit(5)
        # print(o.exec())
