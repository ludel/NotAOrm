from enum import Enum


class Operator(Enum):
    str = "LIKE"
    equ = "=="
    sup = ">"
    supEq = ">="
    inf = "<"
    infEq = "<="
    diff = "!="

