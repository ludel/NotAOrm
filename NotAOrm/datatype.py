from NotAOrm.condition import Condition
from NotAOrm.operator_enum import Comparator
from NotAOrm.sql import creation
from NotAOrm.table import Row, MathFunction


class _Generic(Row):
    prefix = ''

    def get_sql_creation(self):
        return super().get_sql_creation().format(prefix=self.prefix)


class Int(_Generic):
    prefix = creation.INTEGER

    def __init__(self, row_name: str, primary_key=False, **kwargs):
        super().__init__(row_name, **kwargs)
        self.primary_key = primary_key

    def get_sql_creation(self):
        if self.primary_key:
            self.prefix += f' {creation.PRIMARY_KEY} {creation.AUTO_INCREMENT}'
        return super().get_sql_creation().format(prefix=self.prefix)

    @property
    def sum(self):
        return MathFunction('SUM', self.__repr__(), f'sum_{self.row_name}')


class Float(_Generic):
    prefix = creation.FLOAT

    @property
    def sum(self):
        return MathFunction('SUM', self.__repr__(), f'sum_{self.row_name}')


class Varchar(_Generic):
    def __init__(self, row_name, length=255, **kwargs):
        super().__init__(row_name, **kwargs)
        self.prefix = creation.VARCHAR.format(length)

    def is_like(self, other):
        return Condition(self.__repr__(), Comparator.str, '?', [other])


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
