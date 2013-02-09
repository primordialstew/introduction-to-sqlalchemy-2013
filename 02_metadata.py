### slide::
# the basic unit of database metadata is the Table,
# which is stored in a collection called MetaData.
# It's syntax is designed to resemble a CREATE TABLE
# statement.

from sqlalchemy import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String

metadata = MetaData()
user_table = Table('user', metadata,
               Column('id', Integer, primary_key=True),
               Column('name', String),
               Column('fullname', String)
             )

### slide::
# Once created, Table acts as a global object used
# to represent a particular table in a database.
user_table.name

### slide::
# The .c. attribute of Table is an associative array
# of Column objects, keyed on name.
user_table.c.name

### slide::
# It's a bit like a Python dictionary but not totally.
print user_table.c

### slide::
# Table has other information available, such as the columns
# which comprise the table's primary key.
user_table.primary_key

### slide::
# The Table object is at the core of the SQL expression
# system - this is a quick preview of that.
print user_table.select()

### slide:: -*- no_exec -*-
# Table and MetaData objects can be used to generate a schema
# in a database.
from sqlalchemy import create_engine
engine = create_engine("sqlite://")
metadata.create_all(engine)

### slide:: -*- no_exec -*-
# 'reflection' refers to a Table object that loads its
# column and constraint information from an existing
# database.
metadata2 = MetaData()

user_reflected = Table('user', metadata2, autoload=True, autoload_with=engine)

### slide:: -*- no_clear -*-
print user_reflected.c

### slide::
# Table metadata also allows us to specify constraints and typing
# information more specifically.   Type information and NOT NULL
# constraints affect how CREATE TABLE is emitted, and foreign key
# directives are very significant when using the ORM.
from sqlalchemy import ForeignKey
addresses_table = Table('address', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('email_address', String(100), nullable=False),
                    Column('user_id', Integer, ForeignKey('user.id'))
                  )

### slide:: -*- no_exec, no_clear -*-
# the create_all() method checks the database first
# for each table, so can be called repeatedly to generate
# only those tables that haven't been created already.
metadata.create_all(engine)

### slide::

