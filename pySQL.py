from model import User, Requests, Site
from resource.condition import Condition as Con, Operator as Op

print(Requests.filter(Con(Requests.siteId, Op.equ, 18)))
