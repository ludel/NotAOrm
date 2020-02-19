from enum import Enum


class Comparator(Enum):
    str = 'LIKE'
    equ = '=='
    sup = '>'
    supEq = '>='
    inf = '<'
    infEq = '<='
    diff = '!='


class Conditional(Enum):
    and_ = ' AND '
    or_ = ' OR '
