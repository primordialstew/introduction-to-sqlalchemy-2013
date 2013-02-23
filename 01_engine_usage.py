### slide:: s

from sqlalchemy import create_engine
import os

if os.path.exists("some.db"):
    os.remove("some.db")
e = create_engine("sqlite:///some.db")
e.execute("""
    create table employee (
        emp_id integer primary key,
        emp_name varchar
    )
""")

e.execute("""
    create table employee_of_month (
        emp_id integer primary key,
        emp_name varchar
    )
""")

e.execute("""insert into employee(emp_name) values ('ed')""")
e.execute("""insert into employee(emp_name) values ('jack')""")
e.execute("""insert into employee(emp_name) values ('fred')""")

### slide::
# Connecting to a database starts with the create_engine() function.
# this creates an Engine object which will serve as "home base" for
# new connections to the database.  It is not a connection itself,
# and in fact the Engine doesn't make any connection to the database
# until it is first used.

from sqlalchemy import create_engine

engine = create_engine("sqlite:///some.db")

### slide:: p
# Engine features an execute() method which will make it's first connection
# to the database and run a query for us.

result = engine.execute(
             "select emp_id, emp_name from "
             "employee where emp_id=:emp_id",
             emp_id=3)

### slide::
# the result object we get back features methods like fetchone(),
# fetchall()
row = result.fetchone()

### slide:: i
# the row looks like a tuple
row

### slide:: i
# but also acts like a dictionary
row['emp_name']

### slide::
# the result object closes itself automatically when all rows are exhausted,
# but we can also close it explicitly.   Only when the result is closed
# are the database connection resources obtained by Engine.execute() released.
result.close()

### slide:: p
# the result object from a SELECT is also a Python iterable,
# so we usually don't need to call fetchone()...

result = engine.execute("select * from employee")
for row in result:
    print row

### slide:: p
# the fetchall() method is a shortcut to producing a list
# of all rows.
result = engine.execute("select * from employee")
print result.fetchall()

### slide:: p
# The execute() method of Engine will *autocommit*
# statements like INSERT by default.

engine.execute("insert into employee_of_month (emp_name) values (:emp_name)",
                    emp_name='fred')

### slide:: p
# for more control over when the engine connects and disconnects,
# we can establish a *Connection*, using the connect() method.
# Here, we close() the connection to release resources.

conn = engine.connect()
result = conn.execute("select * from employee")
result.fetchall()
conn.close()

### slide:: p
# to run several statements inside a transaction, Connection
# features a begin() method that returns a Transaction.

conn = engine.connect()
trans = conn.begin()
conn.execute("insert into employee (emp_name) values (:emp_name)", emp_name="wendy")
conn.execute("update employee_of_month set emp_name = :emp_name", emp_name="wendy")
trans.commit()
conn.close()

### slide:: p
# A shortcut for running statements in a transaction is to use
# the engine.begin() context manager.   Connection resources are closed
# automatically and the transaction handled.

with engine.begin() as conn:
    conn.execute("insert into employee (emp_name) values (:emp_name)", emp_name="mary")
    conn.execute("update employee_of_month set emp_name = :emp_name", emp_name="mary")


### slide::


