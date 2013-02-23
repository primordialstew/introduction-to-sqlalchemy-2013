### slide::
# Part I.  Basic Configuration.

### slide::

# when using the ORM, we typically declare our mapped
# classes using the *declarative* system, which allows
# us to define classes and associated table metadata at
# the same time.  By extending our classes from Base
# below, a set of classes can refer to each other by name
# during configuration.

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

### slide::
# The User class defines id, name, fullname columns
# on a table named 'user'.  __repr__() is optional.

from sqlalchemy import Column, Integer, String
class User(Base):
     __tablename__ = 'user'

     id = Column(Integer, primary_key=True)
     name = Column(String)
     fullname = Column(String)

     def __repr__(self):
        return "<User(%r, %r)>" % (
                self.name, self.fullname
            )

### slide::
# the declarative system created Table metadata for us -
# we can get to it via the __table__ attribute.

User.__table__

### slide::
# Another attribute, __mapper__, illustrates the *mapper* object,
# which represents the mapping of the User class to the 'user'
# table.  This object usually stays behind the scenes.

User.__mapper__

### slide:: -*- no_exec -*-
# The Base class holds onto a MetaData object which collects
# each Table as declared.   Using this MetaData we can create
# an Engine and create tables using the usual create_all()
# mechanism.

from sqlalchemy import create_engine
engine = create_engine('sqlite://')
Base.metadata.create_all(engine)

### slide::
# Part II.  Working with objects and Sessions.

### slide::
# The User class gets assigned a default constructor,
# that allows us to pass in fields by name.

ed_user = User(name='ed', fullname='Edward Jones')

### slide::
# our User object has "name" and "fullname" assigned,
# but the "id" field, which is the primary key, is not
# yet present.

print ed_user.name
print ed_user.fullname
print ed_user.id

### slide::
# So far, ed_user is not associated with a database in any way.
# The ORM uses an object called the Session to handle the conversation
# with the database.  We create Session objects using a factory
# called a sessionmaker, which we normally configure given an
# Engine as a source of connectivity.

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

### slide::
# our factory is called 'Session', and we create a new session
# object from it, and assign it to the name 'session'.

session = Session()

### slide::
# to put data into the Session, we usually use the add() method.
# When ed_user is added, we say the object is *pending*.  No connection
# to the database has been established yet.
session.add(ed_user)

### slide:: p
# however, when we ask the Session object to query for data, three
# things happen: it establishes connectivity to the database, it
# *flushes* all pending changes to the database, then emits a SELECT
# statement for the data we want.

our_user = session.query(User).filter_by(name='ed').first()
### slide:: p, i
our_user

### slide::
# at the point, the Session is now maintaining an open transaction
# to the database, which will remain until we commit or roll back.
# Note this is the opposite of the "autocommit" behavior featured
# by the Engine by itself.

session.connection()

### slide:: p
# connection() returns a core Connection object, with the usual
# execute() method.
session.connection().execute("select * from user").fetchall()

### slide::
# now that the flush has occurred, and the row for "ed" was INSERTed,
# the database's primary key generation mechanism has generated a
# primary key.   The ORM applies this value to the appropriate attribute
# or attributes present on the mapped object.

print ed_user.id

### slide::
# the Session uses an important pattern called the *identity map*.
# This pattern provides that one and only one copy of an object be
# present for a given primary key.   This means the "our_user" object
# we queried for is the *same* object as the "ed_user" we added - one
# identity per primary key per Session.

ed_user is our_user


### slide::
# we add some more User objects to facilitate the demonstration.
# these three objects are pending until the next flush.

session.add_all([
     User(name='wendy', fullname='Wendy Williams'),
     User(name='mary', fullname='Mary Contrary'),
     User(name='fred', fullname='Fred Flinstone')
])

### slide::
# while we have three objects pending, we will also
# modify part of ed_user.

ed_user.fullname = 'Ed Jones'

### slide::
# We can look into the Session to see which objects have been marked
# as "dirty"...

session.dirty

### slide::
# and also look to see which objects are considered pending, or "new"...

session.new

### slide:: p i
# We instruct the Session to commit the transaction.  This implies a final
# flush of all remaining changes not yet flushed, then the transaction
# is committed.

session.commit()


### slide:: p
# After a commit, the Session by default invalidates, or *expires* the state of all the
# objects inside.   On the next access of any of the objects, a new transaction
# is begun, and the data is re-fetched.  While this is configurable, by default
# it ensures that data changes committed by other, concurrent transactions
# is pulled into the local Session.

ed_user.fullname

### slide:: pi
# hitting it again, the value is locally present.
ed_user.fullname


### slide::
# to illustrate a rollback, we'll change ed_user again, and also add a new user
# we're going to change our mind about.

ed_user.name = 'Edwardo'
fake_user = User(name='fakeuser', fullname='Invalid')
session.add(fake_user)

### slide::
# we query for the changes we just made.  The pending state is flushed,
# the SELECT is emitted, and we see the results.

session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all()

### slide::
# however, this is all inside of a transaction.  We can emit a ROLLBACK.
# the Session rolls back the state and again invalidates all object
# attributes.
session.rollback()

### slide::
# where we see that ed_user's "name" is reset...
ed_user.name

### slide::
# and the "fake_user" has been evicted from the session.
fake_user in session

### slide::
# a new SELECT reveals that the "fakeuser" row previously INSERTed is
# now gone.

session.query(User).filter(User.name.in_(['ed', 'fakeuser'])).all()


### slide::
# Part III.  Querying

### slide::
# the first thing to note about the ORM and querying is that our
# mapped class User has some of the same behavior as the Table
# objects we worked with in the core.  We can refer to columns from
# the class directly to generate SQL expressions.

print User.name == "ed"

### slide::
# We can, if we wanted, use these expressions to a large degree within
# Core constructs such as SELECT.

from sqlalchemy import select

print select([User.name, User.fullname]).\
        where(User.name == 'ed').\
        order_by(User.id)

### slide::
# This is mostly* equivalent to using the Table metadata that we've mapped;
# the Table here is just like the Table we created using the core.
#
# * there are some behavioral differences between User.<somename> and
# User.__table__.<somename>, but these are only apparent in more
# advanced situations.

user_table = User.__table__

print select([user_table.c.name, user_table.c.fullname]).\
        where(user_table.c.name == 'ed').\
        order_by(user_table.c.id)

### slide::
# However, the needs of mapped classes as well as the usage of the Session
# warrants that we normally use the Query object, at least as the starting
# point of SELECTing for data based on ORM classes.

query = session.query(User).order_by(User.id)
print query

### slide:: p
# among other things, a Query is automatically associated with its parent
# Session as well as the ongoing transaction.  It can be iterated directly;
# there is no explicit execute() method needed.

for instance in query:
    print instance.name, instance.fullname

### slide:: p
# Besides querying for whole objects, we can query for individual columns...

for name, fullname in session.query(User.name, User.fullname):
    print name, fullname

### slide:: p
# ... and we can also query for a combination of objects and columns.  The
# Query returns a named tuple in all cases except for the case of a single
# mapped class.

for row in session.query(User, User.name):
    print row.User, row.name

### slide:: p
# Query includes slicing capability that automatically emits LIMIT
# and OFFSET directives, or the equivalent concept supported by the
# underlying database.

for u in session.query(User).order_by(User.id)[1:3]:
    print u

### slide:: p
# basic WHERE clause construction is provided by the filter_by() method,
# which accepts attribute names as keyword arguments, and compares on equality.

for name, in session.query(User.name).\
             filter_by(fullname='Ed Jones'):
    print name

### slide:: p
# the filter() method complements filter_by() by accepting any SQL expression
# element, including equality...

for name, in session.query(User.name).\
             filter(User.fullname=='Ed Jones'):
    print name

### slide:: p
# or a more complex expression, including comparison operators and
# conjunctions.

from sqlalchemy import or_

for name, in session.query(User.name).\
             filter(or_(User.fullname=='Ed Jones', User.id < 5)):
    print name

### slide::
# like the select() object, Query features the same system of "method chaining",
# which recall SQLAlchemy refers to as "generative".  Multiple calls to
# filter() or filter_by() are joined by "AND".

for user in session.query(User).\
          filter(User.name=='ed').\
          filter(User.fullname=='Ed Jones'):
    print user

### slide::
# Query result methods.   Start with a query that we know returns
# just one row.

query = session.query(User).filter_by(fullname='Ed Jones')

### slide:: p
# calling the all() method on the Query gives us a list of all results.

query.all()

### slide:: p
# the first() method, gives us just the first result as a scalar.

query.first()

### slide:: p
# there's also a method called one().

query.one()

### slide::
# first() and one() differ in that first() returns the first row
# or None, one() asserts that one and only one row exists.

query = session.query(User).filter_by(fullname='nonexistent')

### slide:: i

print query.first()

### slide:: i

query.one()

### slide::
# count() is another convenience method that performs a count
# of rows returned from a SELECT statement

session.query(User).filter(User.name.like('%ed')).count()

### slide::
# Part IV. Working with relationships.

### slide::
# New mapped domain class Address.
# This has a *many-to-one* relationship to User called
# 'user', with a *one-to-many* backreference on User called
# 'addresses'.

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User", backref="addresses")

    def __repr__(self):
        return "<Address(%r)>" % self.email_address

### slide:: p
# create the new table.

Base.metadata.create_all(engine)

### slide::
# now when we create a User, it gets an empty "addresses"
# collection as well.

jack = User(name='jack', fullname='Jack Bean')
jack.addresses

### slide::
# we populate this collection with new Address objects.

jack.addresses = [
                 Address(email_address='jack@gmail.com'),
                 Address(email_address='j25@yahoo.com'),
                 Address(email_address='jack@hotmail.com'),
            ]

### slide::
# the mechanics of "backref" mean that the "user" attribute
# is automatically assigned when we manipulate the "addresses"
# collection, and vice versa.

jack.addresses[1]
jack.addresses[1].user

### slide::
# when we add "jack" to the Session, the operation *cascades* to
# the "addresses" collection as well, so that each Address object
# is also added to the session.

session.add(jack)
session.new

### slide:: p
# committing the data we can see the new rows generated.
session.commit()

### slide:: p
# the commit() expired all attributes, including the "addresses"
# collection.  When we next access 'addresses', a *lazy load* is emitted against
# the related table to load those rows back in.
jack.addresses

### slide:: i
# SQLAlchemy collections remain present in memory by default,
# so subsequent access does not emit SQL.
jack.addresses

### slide::
# We can perform any manipulation of the addresses/user
# relationship just by changing Python references.  We can
# move an Address over to "fred" for example.

fred = session.query(User).filter_by(name='fred').one()
jack.addresses[1].user = fred

fred.addresses

### slide::
# if we remove an address totally all addresses collections,
# by default the foreign key "user_id" is set to None.
# we have the option of applying a *cascade rule* that would instead emit
# a DELETE for the Address object.

del fred.addresses[0]
session.commit()

### slide::
# Part V. Querying with relationships.

### slide::
# When querying with SQL, we can refer to multiple tables in one statement.
# When we do this, we usually want to *join* the two tables on some criteria,
# usually along configured relationships.

### slide::
# Possibly the simplest form of join is the *implicit join*.  The SELECT statement
# has two tables in its FROM clause, and the tables are related to each other
# in the WHERE clause.

session.query(User, Address).filter(User.id==Address.user_id).all()

### slide::
# Normally, we'll want to use the JOIN SQL keyword explicitly.  We
# can achieve this most easily using the join() method of Query.
# join() is a key workhorse of the Query object, with many options.  Often,
# it can figure out for us how to join things, just given a "target".

session.query(User, Address).join(Address).all()

### slide::
# We can also give it exactly what we want, using an explicit ON clause.

session.query(User, Address).join(Address, User.id==Address.user_id).all()

### slide::
# Though probably the best middle ground of these two calling styles
# is just to explictly name the relationship() we'd like to JOIN along.

session.query(User, Address).join(User.addresses).all()

### slide::
# When we join(), we can refer to either entity freely within the
# query.  There's no requirement to load the columns back either.

session.query(User.name).join(User.addresses).\
    filter(Address.email_address == 'jack@gmail.com').first()


### slide::
# join() in all cases only accepts the *right* side of the JOIN, where the
# left side is inferred from either the last thing we joined to, or from
# the leftmost query() argument.   If we want the leftmost side to be something
# specific, we can use select_from()

session.query(User, Address).select_from(Address).join(Address.user).all()

### slide::
# if we need to join() to the same table twice, we use a SQL *alias*.  This names
# a particular table with a unique name in the statement.   Below we query for
# a user that has two specific addresses.

from sqlalchemy.orm import aliased

a1, a2 = aliased(Address), aliased(Address)
session.query(User).\
        join(a1).\
        join(a2).\
        filter(a1.email_address=='jack@gmail.com').\
        filter(a2.email_address=='jack@hotmail.com').\
        all()

### slide:: -*-no_exec-*-
# A major feature of Query is its great ability to build compound statements
# using multiple SELECTs.  The subquery() method of Query combines the select()
# and alias() Core constructs to return a new "derived table" from any Query.

from sqlalchemy import func

subq = session.query(func.count(Address.id).label('count'), Address.user_id).\
            group_by(Address.user_id).\
            subquery()

session.query(User.name, subq.c.count).join(subq, User.id==subq.c.user_id).all()

### slide:: -*-no_exec-*-
# The subquery() feature and aliased() constructs can be combined together,
# so that we can load entities from a subquery.  This is an example of
# mapping an arbitrary row to a domain object.

stmt = session.query(Address).\
                 filter(Address.email_address == 'jack@gmail.com').\
                 subquery()
adalias = aliased(Address, stmt)

for user, address in session.query(User, adalias).\
         join(adalias, User.addresses):
     print user, address

### slide::
# Part VI. Eager loading

### slide:: -*-no_exec-*-
# A key issue when working with object relationships in ORMs is the
# so-called "N+1" problem.  When we iterate through a series of User
# objects and their Address collections, we see that many SQL statements are emitted

for user in session.query(User):
    print user, user.addresses

### slide:: -*-no_exec-*-
# To deal with this issue, we need to selectively apply *eager load*
# directives at *query time* so that the ORM knows what relationships should
# be loaded up front.  subqueryload() is one such directive that emits
# a second query to load all collections at once.

from sqlalchemy.orm import subqueryload

session.expire_all()

for user in session.query(User).options(subqueryload(User.addresses)):
    print user, user.addresses

### slide:: -*-no_exec-*-
# The subqueryload directive is complemented by the joinedload() directive,
# which emits a JOIN in one statement.  It's particularly useful
# for many-to-one loads.

from sqlalchemy.orm import joinedload

session.expire_all()

for address in session.query(Address).\
                options(joinedload(Address.user)):
    print address, address.user

### slide:: -*-no_exec-*-
# an important thing about joinedload() is that
# it does not change the results of the query.
# You can't ORDER BY the joinedload(), you use join() for that.
for address in session.query(Address).\
                join(Address.user).\
                filter(User.name=='jack').\
                options(joinedload(Address.user)):
    print address, address.user

### slide:: -*-no_exec-*-
# to join *and* eagerload at the same time without using two
# JOIN clauses, use contains_eager.

from sqlalchemy.orm import contains_eager

for address in session.query(Address).\
                join(Address.user).\
                filter(User.name=='jack').\
                options(contains_eager(Address.user)):
    print address, address.user

### slide::
# Part VII. Cascades
# we want to show a variant of the mapping setup we're working with,
# so to keep things straightforward we will recreate it here.
Base = declarative_base()

class User(Base):
     __tablename__ = 'user'

     id = Column(Integer, primary_key=True)
     name = Column(String)
     fullname = Column(String)

     def __repr__(self):
        return "<User(%r, %r)>" % (
                self.name, self.fullname
            )

### slide::
# The address class below places a *cascade* directive on the
# *one-to-many* side of the User relationship.

from sqlalchemy.orm import backref
class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User",
            backref=backref("addresses", cascade="all, delete, delete-orphan"))

    def __repr__(self):
        return "<Address(%r)>" % self.email_address

### slide:: -*-no_exec-*-
# now, removing an Address from a user means that it gets
# *deleted*.
session = Session()

u1 = session.query(User).filter_by(name="jack").one()

del u1.addresses[1]
session.commit()

### slide:: -*-no_exec-*-
# deleting the User also deletes all the Address objects
# associated with it.

session.delete(u1)
session.commit()

### slide::


