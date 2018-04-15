from model import User
from resource.condition import Condition, Operator as Op
from resource.sortEnum import Sort


class PySQL:

    def sort(self, row: str, sort: Sort = Sort.Asc):
        self.query += f"ORDER BY {row} {sort.value} "

    def group(self, key: str):
        self.query += f"GROUP BY {key} "

    def limit(self, number: int):
        self.query += f"LIMIT {number} "


if __name__ == '__main__':
    u = User.get(Condition("id", Op.equ, 1))
    print(u)
