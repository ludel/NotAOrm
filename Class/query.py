import sqlite3


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

        return self.fetch_to_dic(req)
