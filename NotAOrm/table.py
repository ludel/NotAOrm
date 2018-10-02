from NotAOrm.Enum.operatorEnum import Operator
from NotAOrm.condition import Condition
from NotAOrm.query import Show, Change


class Table:

    def __init__(self, table_name: str, table_row: tuple, database: str = "example.db"):
        self.table_name = table_name
        self.show = Show(table_name, database)
        self.change = Change(table_name, database)

        for row in table_row:
            setattr(self, row, Row(row, table_name))

    def __str__(self):
        return self.table_name


class Row:
    def __init__(self, row_name, table_name):
        self.row_name = row_name
        self.table_name = table_name

    def __eq__(self, other):
        return Condition(f"{self.table_name}.{self.row_name}", Operator.equ, other)

    def __ne__(self, other):
        return Condition(f"{self.table_name}.{self.row_name}", Operator.diff, other)

    def __lt__(self, other):
        return Condition(f"{self.table_name}.{self.row_name}", Operator.inf, other)

    def __le__(self, other):
        return Condition(f"{self.table_name}.{self.row_name}", Operator.infEq, other)

    def __gt__(self, other):
        return Condition(f"{self.table_name}.{self.row_name}", Operator.sup, other)

    def __ge__(self, other):
        return Condition(f"{self.table_name}.{self.row_name}", Operator.supEq, other)

    def __repr__(self):
        return f"{self.table_name}.{self.row_name}"
