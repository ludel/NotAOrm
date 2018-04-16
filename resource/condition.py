from .operatorEnum import Operator


class Condition:

    def __init__(self, row, operator: Operator, verification):
        self.row_from = row
        self.operator = operator
        self.row_to = verification

    def __str__(self):
        return f"{self.row_from} {self.operator.value} {self.row_to}"

