from enum import Enum


class Operator(Enum):
    car = "LIKE"
    equ = "=="
    sup = ">"
    supEq = ">="
    inf = "<"
    infEq = "<="
    diff = "!="

