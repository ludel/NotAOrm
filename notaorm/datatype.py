from notaorm.condition import Condition
from notaorm.operator_enum import Comparator
from notaorm.sql import creation
from notaorm.table import _Row, MathFunction, Table


class _Generic(_Row):
    prefix: str

    def get_sql_creation(self):
        return super().get_sql_creation().format(prefix=self.prefix)


class _Number(_Generic):
    @property
    def sum(self):
        return MathFunction('SUM', self.__repr__(), f'sum_{self.row_name}')

    @property
    def avg(self):
        return MathFunction('AVG', self.__repr__(), f'avg_{self.row_name}')

    @property
    def min(self):
        return MathFunction('MIN', self.__repr__(), f'min_{self.row_name}')

    @property
    def max(self):
        return MathFunction('MAX', self.__repr__(), f'max_{self.row_name}')


class Int(_Number):
    prefix = creation.INTEGER

    def __init__(self, row_name: str, primary_key=False, **kwargs):
        super().__init__(row_name, **kwargs)
        self.primary_key = primary_key

    def get_sql_creation(self):
        if self.primary_key:
            self.prefix += f' {creation.PRIMARY_KEY} {creation.AUTO_INCREMENT}'
        return super().get_sql_creation().format(prefix=self.prefix)


class Float(_Number):
    prefix = creation.FLOAT


class Varchar(_Generic):
    def __init__(self, row_name, length=255, **kwargs):
        super().__init__(row_name, **kwargs)
        self.prefix = creation.VARCHAR.format(length)

    def like(self, search: str):
        return Condition(self.__repr__(), Comparator.str, '?', [search])

    def start_with(self, search: str):
        return self.like(f'{search}%')

    def end_with(self, search: str):
        return self.like(f'%{search}')

    def contain(self, search: str):
        return self.like(f'%{search}%')


class Text(_Generic):
    def __init__(self, row_name, length=5000, **kwargs):
        super().__init__(row_name, **kwargs)
        self.prefix = creation.TEXT.format(length)


class Date(_Generic):
    prefix = creation.DATE
    now = 'CURRENT_DATE '

    def __init__(self, row_name: str, default=None, **kwargs):
        kwargs['default'] = self.now if default == 'now' else f'`{default}`'
        super().__init__(row_name, **kwargs)


class Datetime(Date):
    prefix = creation.TIMESTAMP
    now = 'CURRENT_TIMESTAMP '


class Bool(_Generic):
    prefix = creation.BOOLEAN

    def __init__(self, row_name: str, default=None, **kwargs):
        if default is not None:
            kwargs['default'] = 1 if default else 0
        super().__init__(row_name, **kwargs)


class ForeignKey(_Generic):
    prefix = creation.FOREIGNKEY

    def __init__(self, row_name: str, reference: Table, **kwargs):
        self.references_table = reference
        self.prefix = self.prefix.format(row_name=row_name, *repr(reference.pk).replace("'", '').split('.'))
        super().__init__(row_name, **kwargs)
