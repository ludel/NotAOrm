import sqlite3

from resource.condition import Condition, Operator
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

        return self

    def where(self, condition: Condition):
        instruction = "WHERE" if not "WHERE" in self.query else "AND"
        self.query += f"{instruction} {condition.row_from} {condition.operator.value} {condition.row_to} "

        return self

    def join(self, table: str, condition: Condition):
        instruction = "JOIN" if "JOIN" not in self.query else "AND"
        self.query += f"{instruction} {table} `{table}`" \
                      f" ON {condition.row_from} {condition.operator.value} {condition.row_to} "

        return self

    def order(self, key: str, sort: Sort = Sort.Asc):
        self.query += f"ORDER BY {key} {sort.name} "

        return self

    def group(self, key: str):
        self.query += f"GROUP BY {key} "

        return self

    def limit(self, number: int):
        self.query += f"LIMIT {number} "

        return self

    def update(self, table: str, **columns):
        set_value = ""
        for key, value in columns.items():
            set_value += f"{key} = '{value}'"
        self.query = f"UPDATE {table} SET {set_value} "

        return self

    def delete(self, table):
        self.query = f"DELETE FROM {table} "

        return self

    def __str__(self):
        return "SQL Request : "+self.query


if __name__ == '__main__':
    o = PySQL('main.db')
    ob = o.get("site").where(Condition("id", Operator.Sup, 10)).where(Condition("id", Operator.Inf, 20))
    print(ob)
