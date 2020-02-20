import sqlite3
from collections import namedtuple
from typing import Generator

from notaorm.condition import Condition
from notaorm.sql import option, order


class Query:
    def __init__(self, table_name, path_database):
        self.table_name = table_name
        self._conn = sqlite3.connect(path_database, detect_types=sqlite3.PARSE_DECLTYPES)
        sqlite3.register_converter("BOOLEAN", lambda v: v.decode() == 'True')

    def _get_table_object(self, descriptions: tuple):
        return namedtuple(self.table_name, [desc[0] for desc in descriptions])

    @staticmethod
    def _append_option(query: str, **kwargs):
        for key, value in kwargs.items():
            if not hasattr(option, key.upper()):
                raise NotImplementedError('Option not implement')

            query += getattr(option, key.upper()).format(value)
        return query

    def _fetch(self, query: str, *args, **kwargs):
        columns = kwargs.pop('columns')
        if columns is not '*':
            columns = ','.join(repr(c) for c in columns) if type(columns) is list else repr(columns)

        full_query = self._append_option(query, **kwargs).replace('COLUMNS_NAME', columns)
        res = self.exec(full_query, *args, commit=False)
        table_obj = self._get_table_object(res.description)

        return res, table_obj

    def _fetch_all(self, query: str, *args, **kwargs):
        res, table_obj = self._fetch(query, *args, **kwargs)

        for items in res.fetchall():
            yield table_obj(*items)

    def _fetch_one(self, query: str, *args, **kwargs):
        res, table_obj = self._fetch(query, *args, **kwargs)

        fetch = res.fetchone()
        if fetch is not None:
            return table_obj(*fetch)

    def exec(self, query: str, *args, commit=True):
        query = query.replace('TABLE_NAME', self.table_name)
        res = self._conn.execute(query, args)

        if commit:
            self._conn.commit()

        return res


class Change(Query):
    def update(self, condition, **columns) -> sqlite3.Cursor:
        columns_to_set = ",".join(f'{key} = ?' for key in columns.keys())
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
        return self._fetch_all(order.SELECT_ALL, columns=columns, **options)

    def filter(self, condition: Condition, columns='*', **options) -> Generator:
        return self._fetch_all(
            order.SELECT_WHERE.format(condition.left_side),
            *condition.values,
            columns=columns,
            **options
        )

    def get(self, condition: Condition, columns='*', **options) -> tuple:
        return self._fetch_one(
            order.SELECT_WHERE.format(condition.left_side),
            *condition.values,
            columns=columns,
            **options
        )

    def first(self, columns='*') -> tuple:
        return self._fetch_one(order.SELECT_ALL, columns=columns, order_by_asc=f'{self.table_name}.OID', limit=1)

    def last(self, columns='*') -> tuple:
        return self._fetch_one(order.SELECT_ALL, columns=columns, order_by_desc=f'{self.table_name}.OID', limit=1)
