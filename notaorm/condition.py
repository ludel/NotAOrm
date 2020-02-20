from typing import Union

from notaorm.operator_enum import Conditional, Comparator
from notaorm.sql.order import WHERE


class Condition:
    def __init__(self, left: str, operator: Union[Conditional, Comparator], right: str, values: list):
        self.left_side = WHERE.format(left, operator.value, right)
        self.values = values

    def __and__(self, other: 'Condition'):
        self.values.extend(other.values)
        return Condition(self.left_side, Conditional.and_, other.left_side, self.values)

    def __or__(self, other: 'Condition'):
        self.values.extend(other.values)
        return Condition(self.left_side, Conditional.or_, other.left_side, self.values)
