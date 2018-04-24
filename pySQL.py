from model import Requests
print(Requests.show.filter(Requests.siteId == 18 or Requests.id == 3))
