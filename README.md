# NotAOrm
A sample python library for managing a SQLite database


## Download and Install
`pip install NotAOrm` or `git clone https://github.com/ludel/NotAOrm.git` in your project

There are no hard dependencies other than the Python standard library. NotAOrm run with python 3.6+.

## Examples

### Create a new model
```python
from NotAOrm.table import Table


Site = Table(table_name='site', table_row=('id', 'url', 'visitor', 'date'))
```

Make sure you have created the table `site` before.

### Show methods

#### Get one element
```python
Site.show.get(Site.url == 'google.com')
```
or if we want specific columns
```python
Site.show.get(Site.url == 'google.com', [Site.url, Site.date])
```

#### Get all elements
```python
all_sites = Site.show.all()
for site in all_sites:
    print('=>', site.id, site.url, site.visitor, site.date, sep='\t')
```

We can order and limit the request

```python
last_sites = Site.show.all(order_by=Site.date, limit=3)
```

#### Filter by where clause
```python
filter_sites = Site.show.filter(Site.visitor >= 10, Site.id)
for site in filter_sites:
    print('=>', site.id, sep='\t')
```

#### Group by and math methods
- By SUM
```python
sites_visitor = Site.show.all(Site.visitor.sum, group_by=Site.date)
```
- By COUNT
```python
sites_count = Site.show.all(Site.visitor.count, group_by=Site.date)
```

### Change methods

#### Insert 
```python
Site.change.insert(url='google.com')
```

#### Update 
```python
Site.change.update(Site.url.like('bing'), url='google.com')
```

#### Delete 
```python
Site.change.delete(Site.visitor == 0, commit=True)
```
By default in the delete method, commit is set to false 


## License

NotAOrm is MIT licensed.