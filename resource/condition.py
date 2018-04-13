from .operatorEnum import Operator


class Condition:

    def __init__(self, row: str, operator: Operator, verification):
        self.row_from = row
        self.operator = operator
        self.row_to = verification

