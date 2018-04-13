import sqlite3
from resource.sortEnum import Sort
from resource.condition import Condition, Operator


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
        self.query += f"WHERE {condition.row_from} {condition.operator.value} {condition.row_to} "
        return self

    def join(self, table: str, condition: Condition):
        self.query += f"JOIN {table} `{table}` ON {condition.row_from} {condition.operator.value} {condition.row_to} "

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
        return self.query


if __name__ == '__main__':
    o = PySQL('main.db')
    ob = o.get("site").where(Condition("id", Operator.Diff, 15)).order("id", Sort.Desc).limit(10)
    print(ob.exec())
