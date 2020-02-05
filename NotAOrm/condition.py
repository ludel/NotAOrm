from NotAOrm.Enum.operatorEnum import Conditional
from NotAOrm.SQLQueries import WHERE


class Condition:
    def __init__(self, left, operator, right, values: list):
        self.left_side = WHERE.format(left, operator.value, right)
        self.values = values

    def __and__(self, other: 'Condition'):
        self.values.extend(other.values)
        return Condition(self.left_side, Conditional.and_, other.left_side, self.values)

    def __or__(self, other: 'Condition'):
        self.values.extend(other.values)
        return Condition(self.left_side, Conditional.or_, other.left_side, self.values)
