from NotAOrm.Enum.operatorEnum import Operator


class Condition:

    def __init__(self, left, operator: Operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    @property
    def first_part(self):
        return self.left, self.operator.value
