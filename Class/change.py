from Class.query import Query


class Change(Query):

    def __init__(self, table_name, path_database):
        super().__init__(table_name, path_database)
        self.table_name = table_name

    def update(self, condition, **columns) -> list:
        set_value = ""
        for key, value in columns.items():
            set_value += f"{key} = '{value}',"

        return self.exec(f"UPDATE {self.table_name} SET {set_value[0:-1]} WHERE {condition}", True)

    def insert(self, **columns) -> list:
        all_keys = "".join(key + "," for key in columns.keys())[0:-1]
        all_values = "".join(f"'{value}'," for value in columns.values())[0:-1]

        return self.exec(f"INSERT INTO {self.table_name} ({all_keys}) VALUES ({all_values})", True)

    def delete(self, condition, commit=False) -> list:
        return self.exec(f"DELETE FROM {self.table_name} WHERE {condition}", commit)
