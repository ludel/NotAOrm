# pySQL
Methodes python permettant la gestion d'une base de donnée SQLite
 
```python
# select database SQLite
o = PySQL('DataBase.bd')

# select column1, column2 form TABLE_1
o.get("TABLE_1", "column1, column2")
o.join("TABLE_2", Condition("value_table_2.id", Opp.equ, "value_table_1.id"))
o.where(Condition("value_table_1.id", Opp.sup, 10))
o.order("value_table_1.id", Sort.Desc)
o.limit(5)
print(o.exec())
```
