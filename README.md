# pySQL
Python methods for managing a SQLite database

# Example

## Model
```python
from Class.table import Table

Requests = Table(table_name="requests", table_row=('id', 'number', 'siteId', 'date'))
Site = Table(table_name="site", table_row=('id', 'url'))
```

## Application
```python
from model import Requests, Site

print(Requests.show.all(order=Requests.date))

print(Site.show.get(Site.id, Site.url, limit=2))

print(Requests.show.filter(Requests.siteId > 3, group=Requests.siteId))

print(Requests.show.add(Site, Site.id == Requests.siteId))

Site.change.insert(url="http://foo.fo")

Site.change.update(Site.id >= 5, url="http://google.com")

Site.change.delete(Site.url == "http://google.com", commit=False)
```
