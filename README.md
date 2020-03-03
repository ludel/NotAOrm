# NotAOrm
A sample python library for managing a SQLite database


## Download and Install
`pip install NotAOrm` or `git clone https://github.com/ludel/NotAOrm.git` in your project

There are no hard dependencies other than the Python standard library. NotAOrm run with python 3.6+.

## Documentation

### Data types list
SQL | Python | lib | Args | Note
--- | --- | --- | --- | ---
INTEGER | `int` | `Int` |  `not_null`, `unique`, `default`, `primary_key` | Automatic incrementation is activated when the primary_key argument is true
FLOAT | `float` | `Float` | `not_null`, `unique`, `default`
VARCHAR | `str` | `Varchar` | `not_null`, `unique`, `default`, `length` | By default length is 255
TEXT | `str` | `Text` | `length`, `not_null`, `unique`, `default` | By default length is 5000
DATE | `datetime.date` | `Date` | `not_null`, `unique`, `default` | if default argument is set to `now`, the date will be automatically generate  
TIMESTAMP | `datetime.datetime` | `Datetime` | `not_null`, `unique`, `default` | Same as `Date`
BOOLEAN | `bool` | `Bool` | `not_null`, `unique`, `default`
FOREIGN KEY | `Relation` | `ForeignKey` | `reference`, `not_null`, `unique`, `default` | Reference argument must be a Table object

## Examples

### Create a new model
```python
import notaorm
from notaorm.table import Table
from notaorm.datatype import Int, Varchar, Date

notaorm.database = 'test.db'


site = Table('site', rows=(
    Int('id', primary_key=True, not_null=True),
    Varchar('url', length=255, unique=True, not_null=True),
    Int('visitor', default=0),
    Date('last_check', default='now')
))
site.create()
```

### Show methods

#### Get one element
```python
site.show.get(site.url == 'google.com')
```
or if we want specific columns
```python
site.show.get(site.url.end_with('.com'), columns=[site.url, site.last_check])
```

#### Get all elements
```python
all_sites = site.show.all()
for site in all_sites:
    print('=>', site.id, site.url, site.visitor, site.last_check, sep='\t')
```

We can order and limit the request

```python
order_asc_sites = site.show.all(order_by=site.last_check, limit=3)
order_desc_sites = site.show.all(order_by_desc=site.last_check, limit=3)
```

#### Filter by where clause
```python
filter_sites = site.show.filter(site.visitor >= 10, site.id)
for site in filter_sites:
    print('=>', site.id, sep='\t')
```

With several conditions
```python
condition_or = (site.visitor >= 10) | (site.id > 2)
site.show.filter(condition_or, site.id)

condition_and = (site.visitor >= 10) & (site.id > 2)
site.show.filter(condition_and, site.id)
```

#### Group by and math methods
##### By Sum
```python
visitor_sum = site.show.all(site.visitor.sum, group_by=site.last_check)
```
##### By Count
```python
visitor_count = site.show.all(site.visitor.count, group_by=site.last_check)
```
##### By Max, Min, Avg
```python
visitor_max = site.show.first(columns=site.visitor.max).max_visitor
visitor_min = site.show.first(columns=site.visitor.min).min_visitor
visitor_avg = site.show.first(columns=site.visitor.avg).avg_visitor
```

### Foreign key

#### New webmaster model

New model with a foreign key link to site model
```python
from notaorm.datatype import Int, Varchar, ForeignKey
from notaorm.table import Table

webmaster = Table('webmaster', rows=(
    Int('id', primary_key=True, not_null=True),
    Varchar('email'),
    ForeignKey('site', reference=site),
))
webmaster.create()
```

#### Request
```python
webmaster = webmaster.show.first()
print(webmaster.site.pk)

linked_site = webmaster.site.first()
print(linked_site.id, linked_site.url, linked_site.visitor, sep='\t')
```
It is better to use the pk field rather than the name of the primary key field because access to the pk field does not require
the execution of a new sql request.

### Change methods
#### Insert 
```python
site.change.insert(url='google.com')
```

#### Update 
```python
site.change.update(site.url.start_with('bing'), url='google.com')
```

#### Delete 
```python
site.change.delete(site.visitor == 0, commit=True)
```
By default in the delete method, commit is set to false 


## License

notaorm is MIT licensed.