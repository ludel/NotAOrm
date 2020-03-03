import sqlite3
from collections import namedtuple
from typing import Generator, NamedTuple, Optional

import notaorm
from notaorm.condition import Condition
from notaorm.sql import option, order

sqlite3.register_converter("BOOLEAN", lambda v: v.decode() == 'True')


class Query:
    def __init__(self, table_name, table_rows=(), init_condition=None):
        self.table_name = table_name
        self.init_condition = init_condition
        self.foreign_rows = [r for r in table_rows if type(r).__name__ is 'ForeignKey']
        self._conn = sqlite3.connect(notaorm.database, detect_types=sqlite3.PARSE_DECLTYPES)

        if notaorm.print_query:
            self._conn.set_trace_callback(print)

    def _get_table_object(self, descriptions: tuple):
        return namedtuple(self.table_name, [desc[0] for desc in descriptions])

    @staticmethod
    def _append_option(query: str, **kwargs):
        for key in kwargs.keys():
            if not hasattr(option, key.upper()):
                raise NotImplementedError('Option not implement')

        sorted_option = {k: v for k, v in sorted(kwargs.items(), key=lambda t: getattr(option, t[0].upper())[1])}
        for key, value in sorted_option.items():
            if not hasattr(option, key.upper()):
                raise NotImplementedError('Option not implement')
            append_option = getattr(option, key.upper())[0]

            if type(value) == list:
                append_option = append_option.format(*value)
            else:
                append_option = append_option.format(value)
            query += append_option

        return query

    def _set_relation(self, fetch, response):
        fetch = list(fetch)
        for row in self.foreign_rows:
            all_row = [desc[0] for desc in response.description]
            index_foreign_row = all_row.index(row.row_name)
            fetch[index_foreign_row] = Relation(fetch[index_foreign_row], row)

        return fetch

    def _fetch(self, query: str, columns, condition=None, **kwargs):
        if columns is not '*':
            columns = ','.join(repr(c) for c in columns) if type(columns) is list else repr(columns)

        condition_values = []
        if condition is not None:
            if self.init_condition is not None:
                condition &= self.init_condition
            condition_values = condition.values
            kwargs['condition'] = condition.left_side
        elif type(self.init_condition) is Condition:
            condition_values = self.init_condition.values
            kwargs['condition'] = self.init_condition.left_side

        full_query = self._append_option(query, **kwargs).replace('COLUMNS_NAME', columns)
        res = self.exec(full_query, *condition_values, commit=False)
        table_obj = self._get_table_object(res.description)

        return res, table_obj

    def _fetch_all(self, columns, **kwargs):
        res, table_obj = self._fetch(order.SELECT, columns, **kwargs)
        fetch = res.fetchall()

        for items in fetch:
            yield table_obj(*items)

    def fetch_one(self, columns, **kwargs):
        res, table_obj = self._fetch(order.SELECT, columns, **kwargs)
        fetch = res.fetchone()
        if fetch is None:
            return

        fetch = self._set_relation(fetch, res)
        return table_obj(*fetch)

    def exec(self, query: str, *args, commit=True):
        query = query.replace('TABLE_NAME', self.table_name)
        res = self._conn.execute(query, args)

        if commit:
            self._conn.commit()

        return res


class Change(Query):
    def update(self, condition, **columns) -> sqlite3.Cursor:
        columns_to_set = ','.join(f'{key} = ?' for key in columns.keys())
        values = list(columns.values()) + condition.values

        return self.exec(order.UPDATE.format(columns_to_set, condition.left_side), *values)

    def insert(self, **columns) -> sqlite3.Cursor:
        keys = ",".join(columns.keys())
        values = ','.join('?' * len(columns.values()))

        return self.exec(order.INSERT.format(keys, values), *columns.values())

    def delete(self, condition: Condition, commit=False) -> sqlite3.Cursor:
        return self.exec(order.DELETE.format(condition.left_side), *condition.values, commit=commit)


class Show(Query):
    def all(self, columns='*', **options) -> Generator:
        return self._fetch_all(columns, **options)

    def filter(self, condition: Condition, columns='*', **options) -> Generator:
        return self._fetch_all(columns, condition=condition, **options)

    def get(self, condition: Condition, columns='*', **options) -> Optional[NamedTuple]:
        return self.fetch_one(columns, condition=condition, **options)

    def first(self, columns='*') -> Optional[NamedTuple]:
        return self.fetch_one(columns, order_by_asc=f'{self.table_name}.ROWID', limit=1)

    def last(self, columns='*') -> Optional[NamedTuple]:
        return self.fetch_one(columns, order_by_desc=f'{self.table_name}.ROWID', limit=1)


class Relation(Show):
    def __init__(self, value, row):
        self._ref_table = row.references_table
        self.pk = value
        super().__init__(self._ref_table.table_name, self._ref_table.rows,
                         init_condition=(self._ref_table.pk == self.pk))

    def __repr__(self):
        return f'<Relation: {self._ref_table} {self.pk}>'
