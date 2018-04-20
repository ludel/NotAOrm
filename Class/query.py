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

    def exec(self, query: str, commit: bool = False) -> list:
        req = self.conn.execute(query)
        if commit:
            req.execute("COMMIT ")

        return self.fetch_to_dic(req)


