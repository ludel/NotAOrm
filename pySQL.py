from model import Requests, User, Site
from Class.condition import Condition, Operator as Op

print(Requests.query.all())
print(User.query.get(User.pseudo, User.password))
print(Site.query.delete(Condition(Site.id, Op.equ, 5), False))
print(Requests.query.filter([Condition(Requests.id, Op.sup, 2), Condition(Requests.id, Op.inf, 10)]))

