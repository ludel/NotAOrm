# pySQL
Python methods for managing a SQLite database

# Doc

## Model Example
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

requests.query.all()

site.query.get(Condition(site.id, Operator.inf, 2))

requests.query.add(site, Condition(site.id, Operator.inf, requests.siteId))

site.query.insert(url="http://foo.fo")

site.query.update(Condition(site.id, Operator.equ, 5), url="http://google.com")

site.query.delete((Condition(site.url, Operator.str, "http://google.com"), commit=True)
```