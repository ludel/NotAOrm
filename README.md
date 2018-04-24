# pySQL
Python methods for managing a SQLite database

# Example

## Model
```python
from Class.table import Table

requests = Table(table_name="requests", table_row=('id', 'number', 'siteId', 'date'))
site = Table(table_name="site", table_row=('id', 'url'))
```

## Condition and Operator
```python
from Class.condition import Condition, Operator

condition = Condition(user.id, Operator.equ, 1)
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
