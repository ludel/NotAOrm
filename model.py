from resource.table import Table

User = Table(table_name="user", table_row=('id', 'pseudo', 'password'))
Requests = Table(table_name="requests", table_row=('id', 'number', 'siteId', 'date'))
Site = Table(table_name="site", table_row=('id', 'url'))
