from enum import Enum


class Operator(Enum):
    Str = "LIKE"
    Equ = "=="
    Sup = ">"
    SupEq = ">="
    Inf = "<"
    InfEq = "<="
    Diff = "!="

