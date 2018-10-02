from NotAOrm.Enum.operatorEnum import Operator


class Condition:

    def __init__(self, right, operator: Operator, left):
        self.right = right
        self.operator = operator
        self.left = left

    def sql(self):
        return f"{self.right} {self.operator.value} {self.left}"
