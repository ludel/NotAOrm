import sqlite3
from NotAOrm.SQLQueries import DELETE, INSERT, SELECT_ALL, SELECT_WHERE, UPDATE


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
            query += f" GROUP BY {kwargs['group']}"
        if kwargs.get('order'):
            query += f" ORDER BY {kwargs['order']}"
        if kwargs.get('limit'):
            query += f" LIMIT {kwargs['limit']}"
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

        return self.exec(UPDATE.format(self.table_name, set_value[0:-1], condition.sql()), commit=True)

    def insert(self, **columns) -> list:
        all_keys = ",".join(key for key in columns.keys())
        all_values = ",".join(f"'{value}'" for value in columns.values())
        return self.exec(INSERT.format(self.table_name, all_keys, all_values), commit=True)

    def delete(self, condition, commit=False) -> list:
        return self.exec(DELETE.format(self.table_name, condition.sql()), commit=commit)


class Show(Query):

    def __init__(self, table_name, path_database):
        super().__init__(table_name, path_database)
        self.table_name = table_name

    def all(self, **kwargs) -> list:
        return self.exec(SELECT_ALL.format(self.table_name), **kwargs)

    def get(self, condition, **kwargs) -> list:
        return self.exec(SELECT_WHERE.format(self.table_name, condition.sql()), **kwargs)

