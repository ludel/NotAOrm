from model import Requests, User, Site
from Class.condition import Condition, Operator as Op

print(Requests.query.all())
print(User.query.get(User.pseudo, User.password))
print(Site.query.delete(Condition(Site.id, Op.equ, 5), False))
