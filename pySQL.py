from model import User, Requests, Site
from resource.condition import Condition as Con, Operator as Op

if __name__ == '__main__':
    s = Site
    print(s.add(Requests, Con(Site.id, Op.equ, Requests.siteId)))
