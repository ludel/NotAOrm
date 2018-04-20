from Class.change import Change
from Class.show import Show


class Table:

    def __init__(self, table_name, table_row: tuple, path_database: str = "example.db"):
        self.table_name = table_name
        self.show = Show(table_name, path_database)
        self.change = Change(table_name, path_database)

        for row in table_row:
            setattr(self, row, f"{table_name}.{row}")

    def __str__(self):
        return self.table_name
