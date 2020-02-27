from typing import Sequence

from notaorm.condition import Condition
from notaorm.operator_enum import Comparator
from notaorm.query import Show, Change
from notaorm.sql import order, creation


class Table:
    def __init__(self, name: str, rows: Sequence['_Row']):
        self.table_name = name
        self.show = Show(name, rows)
        self.change = Change(name)
        self.rows = rows
        self.pk = _Row('ROWID', table_name=name)

        for row in rows:
            row.table_name = name
            setattr(self, row.row_name, row)

    def create(self):
        row_sql = ', '.join(row.get_sql_creation() for row in self.rows)
        full_sql = creation.CREATE_TABLE.format(row_sql)
        self.change.exec(full_sql)

        for row_unique in [r for r in self.rows if r.unique]:
            self.change.exec(creation.UNIQUE.format(row_name=row_unique.row_name))

    def __str__(self):
        return self.table_name


class _Row:
    prefix: str

    def __init__(self, row_name: str, table_name=None, not_null=False, unique=False, default=None):
        self.row_name = row_name.replace(' ', '_')
        self.not_null = not_null
        self.unique = unique
        self.table_name = table_name
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
