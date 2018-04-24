from model import Requests, Site

print(Site.show.all(order=Site.id))

print(Site.show.get(Site.id, Site.url, limit=2))

print(Requests.show.filter(Requests.siteId > 3, group=Requests.siteId))

print(Requests.show.add(Site, Site.id == Requests.siteId, limit=10))

Site.change.insert(url="http://foo.fo")

Site.change.update(Site.id >= 5, url="http://google.com")

Site.change.delete(Site.url == "http://google.com", commit=False)
