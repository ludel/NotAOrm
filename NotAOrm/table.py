from NotAOrm import database, SQLQueries
from NotAOrm.Enum.operatorEnum import Comparator
from NotAOrm.condition import Condition
from NotAOrm.query import Show, Change


class Table:
    def __init__(self, table_name: str, table_row: tuple):
        self.table_name = table_name
        self.show = Show(table_name, database)
        self.change = Change(table_name, database)

        for row in table_row:
            setattr(self, row.replace(' ', '_'), Row(row, table_name))

    def __str__(self):
        return self.table_name


class Row:
    def __init__(self, row_name, table_name):
        self.row_name = row_name
        self.table_name = table_name

    @property
    def sum(self):
        return MathFunction('SUM', self.__repr__(), f'sum_{self.row_name}')

    @property
    def count(self):
        return MathFunction('COUNT', self.__repr__(), f'count_{self.row_name}')

    def __eq__(self, other):
        return Condition(f"{self.table_name}.{self.row_name}", Comparator.equ, '?', [other])

    def like(self, other):
        return Condition(f"{self.table_name}.{self.row_name}", Comparator.supEq, '?', [other])

    def __ne__(self, other):
        return Condition(f"{self.table_name}.{self.row_name}", Comparator.diff, '?', [other])

    def __lt__(self, other):
        return Condition(f"{self.table_name}.{self.row_name}", Comparator.inf, '?', [other])

    def __le__(self, other):
        return Condition(f"{self.table_name}.{self.row_name}", Comparator.infEq, '?', [other])

    def __gt__(self, other):
        return Condition(f"{self.table_name}.{self.row_name}", Comparator.sup, '?', [other])

    def __ge__(self, other):
        return Condition(f"{self.table_name}.{self.row_name}", Comparator.supEq, '?', [other])

    def __repr__(self):
        return f'{self.table_name}.{self.row_name}'


class MathFunction:
    def __init__(self, math, row, label):
        self.math = math
        self.row = row
        self.label = label

    def __repr__(self):
        return getattr(SQLQueries, self.math).format(self.row, self.label)
