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
from model import requests, site

requests.show.all()

site.show.get(site.id, site.url)

requests.show.filter(Condition(requests.siteId, Operator.supEq, 3))

requests.show.filter([Condition(Requests.id, Operator.sup, 2), Condition(Requests.id, Operator.inf, 10)])

requests.show.add(site, Condition(site.id, Operator.inf, requests.siteId))

site.change.insert(url="http://foo.fo")

site.change.update(Condition(site.id, Operator.equ, 5), url="http://google.com")

site.change.delete((Condition(site.url, Operator.str, "http://google.com"), commit=True)
```
