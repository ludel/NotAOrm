from model import User
from resource.condition import Condition as Con, Operator as Op
from resource.sortEnum import Sort


if __name__ == '__main__':
    u = User.all()
    print(User.table_row.get("id"))
