from model import User, Requests, Site
from resource.condition import Condition as Con, Operator as Op

if __name__ == '__main__':
    print(User.all())
    print(Requests.get(Con(Requests.id, Op.equ, 18)))

    print(Site.add(Requests, Con(Site.id, Op.equ, Requests.siteId)))
