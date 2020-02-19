from typing import Sequence

import NotAOrm
from NotAOrm.condition import Condition
from NotAOrm.operator_enum import Comparator
from NotAOrm.query import Show, Change
from NotAOrm.sql import order, creation


class Table:
    def __init__(self, table_name: str, table_row: Sequence['Row']):
        self.table_name = table_name
        self.show = Show(table_name, NotAOrm.database)
        self.change = Change(table_name, NotAOrm.database)
        self._table_row = table_row
        self.pk = Row('OID')

        for row in table_row:
            row.table_name = table_name
            setattr(self, row.row_name, row)

    def create(self):
        row_sql = ', '.join(row.get_sql_creation() for row in self._table_row)
        full_sql = creation.CREATE_TABLE.format(row_sql)
        self.change.exec(full_sql)

        for row_unique in [r for r in self._table_row if r.unique]:
            self.change.exec(creation.UNIQUE.format(row_name=row_unique.row_name))

    def __str__(self):
        return self.table_name


class Row:
    def __init__(self, row_name: str, not_null=False, unique=False, default=None):
        self.row_name = row_name.replace(' ', '_')
        self.not_null = not_null
        self.unique = unique
        self.table_name = None
        self.default = default

    def __eq__(self, other):
        return Condition(self.__repr__(), Comparator.equ, '?', [other])

    def __ne__(self, other):
        return Condition(self.__repr__(), Comparator.diff, '?', [other])

    def __lt__(self, other):
        return Condition(self.__repr__(), Comparator.inf, '?', [other])

    def __le__(self, other):
        return Condition(self.__repr__(), Comparator.infEq, '?', [other])

    def __gt__(self, other):
        return Condition(self.__repr__(), Comparator.sup, '?', [other])

    def __ge__(self, other):
        return Condition(self.__repr__(), Comparator.supEq, '?', [other])

    def __repr__(self):
        return f'{self.table_name}.{self.row_name}' if self.table_name else self.row_name

    @property
    def count(self):
        return MathFunction('COUNT', self.__repr__(), f'count_{self.row_name}')

    def get_sql_creation(self):
        sql = f'{self.row_name} {{prefix}} '
        if self.default is not None:
            sql += creation.DEFAULT.format(self.default)
        if self.not_null:
            sql += f'{creation.NOT_NULL}'
        return sql


class MathFunction:
    def __init__(self, math, row, label):
        self.math = math
        self.row = row
        self.label = label

    def __repr__(self):
        return getattr(order, self.math).format(self.row, self.label)
