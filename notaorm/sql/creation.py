CREATE_TABLE = "create table TABLE_NAME({});"

NOT_NULL = 'NOT NULL '
DEFAULT = 'DEFAULT {} '
PRIMARY_KEY = 'constraint TABLE_NAME_pk primary key '
AUTO_INCREMENT = 'autoincrement '
UNIQUE = 'create unique index TABLE_NAME_{row_name}_uindex on "TABLE_NAME" ({row_name})'

INTEGER = 'INTEGER'
VARCHAR = 'VARCHAR({})'
TEXT = 'TEXT({})'
FLOAT = 'FLOAT'
DATE = 'DATE'
TIMESTAMP = 'TIMESTAMP'
BOOLEAN = 'BOOLEAN'
FOREIGNKEY = '{row_name} INTEGER, FOREIGN KEY({row_name}) REFERENCES {}({})'