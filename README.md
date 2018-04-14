# pySQL
Python methods for managing a SQLite database

```python
#Database connect.
request = PySQL('DataBase.bd')

#Extract data from tables.
#SELECT column1, column2 FROM table_1
request.get("table_1", "column1, column2")

#Associate multiple tables in a single query.
#JOIN TABLE_2 ON table_1.id == table_2.id
request.add("table_2", Condition("table_1.id", Opp.equ, "table_2.id"))

#Extract only those records that fulfill a specified condition
#WHERE table_1.id > 10
request.where(Condition("table_1.id", Opp.sup, 10))

#Sort the result-set in ascending or descending order.
#ORDER BY table_1.id DESC
request.sort("table_1.id", Sort.Desc)

#Specify the maximum number of results.
#LIMIT 5
request.limit(5)

#Execute the request
request.exec()
```
