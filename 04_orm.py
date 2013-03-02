### slide::

# The *declarative* system is normally used to configure
# object relational mappings.

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

### slide::
# a basic mapping.   __repr__ is optional.

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
# the User class now has a Table object associated with it.

User.__table__

### slide::
# The Mapper object mediates the relationship between User
# and the "user" Table object.

User.__mapper__

### slide::
# User has a default constructor, accepting field names
# as arguments.

ed_user = User(name='ed', fullname='Edward Jones')

### slide::
# The "id" field is the primary key, which starts as None
# if we didn't set it explicitly.

print(ed_user.name, ed_user.fullname)
print(ed_user.id)

### slide:: p
# The MetaData object is here too, available from the Base.

from sqlalchemy import create_engine
engine = create_engine('sqlite://')
Base.metadata.create_all(engine)

### slide::
# To persist and load User objects from the database, we
# use a Session object.

from sqlalchemy.orm import Session
session = Session(bind=engine)

### slide::
# new objects are placed into the Session using add().
session.add(ed_user)

### slide:: pi
# the Session will *flush* *pending* objects
# to the database before each Query.

our_user = session.query(User).filter_by(name='ed').first()
our_user

### slide::
# the User object we've inserted now has a value for ".id"
print(ed_user.id)

### slide::
# the Session maintains a *unique* object per identity.
# so "ed_user" and "our_user" are the *same* object

ed_user is our_user


### slide::
# Add more objects to be pending for flush.

session.add_all([
    User(name='wendy', fullname='Wendy Weathersmith'),
    User(name='mary', fullname='Mary Contrary'),
    User(name='fred', fullname='Fred Flinstone')
])

### slide::
# modify "ed_user" - the object is now marked as *dirty*.

ed_user.fullname = 'Ed Jones'

### slide::
# the Session can tell us which objects are dirty...

session.dirty

### slide::
# and can also tell us which objects are pending...

session.new

### slide:: p i
# The whole transaction is committed.  Commit always triggers
# a final flush of remaining changes.

session.commit()

### slide:: p
# After a commit, theres no transaction.  The Session
# *invalidates* all data, so that accessing them will automatically
# start a *new* transaction and re-load from the database.

ed_user.fullname

### slide::
# Make another "dirty" change, and another "pending" change,
# that we might change our minds about.

ed_user.name = 'Edwardo'
fake_user = User(name='fakeuser', fullname='Invalid')
session.add(fake_user)

### slide::
# run a query, our changes are flushed; results come back.

session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all()

### slide::
# But we're inside of a transaction.  Roll it back.
session.rollback()

### slide:: p
# ed_user's name is back to normal
ed_user.name

### slide::
# "fake_user" has been evicted from the session.
fake_user in session

### slide::
# and the data is gone from the database too.

session.query(User).filter(User.name.in_(['ed', 'fakeuser'])).all()

### slide::
# Exercises:
#
# 1. Create a class/mapping for this table, call the class Network
#
# CREATE TABLE network (
#      network_id INTEGER PRIMARY KEY,
#      name VARCHAR(100) NOT NULL,
# )
#
# 2. emit Base.metadata.create_all(engine) to create the table
#
# 3. commit a few Network objects to the database:
#
# Network(name='net1'), Network(name='net2')
#
#

### slide::
# The attributes on our mapped class act like Column objects, and
# produce SQL expressions.

print(User.name == "ed")

### slide:: p
# These SQL expressions are compatible with the select() object
# we introduced earlier.

from sqlalchemy import select

sel = select([User.name, User.fullname]).\
        where(User.name == 'ed').\
        order_by(User.id)

session.connection().execute(sel).fetchall()


### slide:: p
# but when using the ORM, the Query() object provides a lot more functionality,
# here selecting the User *entity*.

query = session.query(User).filter(User.name == 'ed').order_by(User.id)

query.all()


### slide:: p
# Query can also return individual columns

for name, fullname in session.query(User.name, User.fullname):
    print(name, fullname)

### slide:: p
# and can mix entities / columns together.

for row in session.query(User, User.name):
    print(row.User, row.name)

### slide:: p
# Array slices produce LIMIT/OFFSET, or equivalent

for u in session.query(User).order_by(User.id)[1:3]:
    print(u)

### slide:: p
# the WHERE clause is either by filter_by(), which is convenient

for name, in session.query(User.name).\
                filter_by(fullname='Ed Jones'):
    print(name)

### slide:: p
# or filter(), which is more flexible

for name, in session.query(User.name).\
                filter(User.fullname == 'Ed Jones'):
    print(name)

### slide:: p
# conjunctions can be passed to filter() as well

from sqlalchemy import or_

for name, in session.query(User.name).\
                filter(or_(User.fullname == 'Ed Jones', User.id < 5)):
    print(name)

### slide::
# multiple filter() calls join by AND just like select().where()

for user in session.query(User).\
                        filter(User.name == 'ed').\
                        filter(User.fullname == 'Ed Jones'):
    print(user)

### slide::
# Query has some variety for returning results

query = session.query(User).filter_by(fullname='Ed Jones')

### slide:: p
# all() returns a list

query.all()

### slide:: p
# first() returns the first row, or None

query.first()

### slide:: p
# one() returns the first row and verifies that there's one and only one

query.one()

### slide:: p
# if there's not one(), you get an error

query = session.query(User).filter_by(fullname='nonexistent')
query.one()

### slide:: p
# if there's more than one(), you get an error

query = session.query(User)
query.one()

### slide::

# Exercises
#
# 1. Produce a Query object representing the list of "fullname" values for
# all User objects in alphabetical order.
#
# 2. call .all() on the query to make sure it works!
#
# 3. build a second Query object from the first that also selects
# only User rows with the name "mary" or "ed".
#
# 4. return only the second row of the Query from #3.


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

### slide:: p
# A major feature of Query is its great ability to build compound statements
# using multiple SELECTs.  The subquery() method of Query combines the select()
# and alias() Core constructs to return a new "derived table" from any Query.

from sqlalchemy import func

subq = session.query(func.count(Address.id).label('count'), Address.user_id).\
            group_by(Address.user_id).\
            subquery()

session.query(User.name, subq.c.count).join(subq, User.id==subq.c.user_id).all()

### slide:: p
# The subquery() feature and aliased() constructs can be combined together,
# so that we can load entities from a subquery.  This is an example of
# mapping an arbitrary row to a domain object.

stmt = session.query(Address).\
                 filter(Address.email_address == 'jack@gmail.com').\
                 subquery()
adalias = aliased(Address, stmt)

for user, address in session.query(User, adalias).\
         join(adalias, User.addresses):
     print(user, address)

### slide::
# Part VI. Eager loading

### slide:: p
# A key issue when working with object relationships in ORMs is the
# so-called "N+1" problem.  When we iterate through a series of User
# objects and their Address collections, we see that many SQL statements are emitted

for user in session.query(User):
    print(user, user.addresses)

### slide:: p
# To deal with this issue, we need to selectively apply *eager load*
# directives at *query time* so that the ORM knows what relationships should
# be loaded up front.  subqueryload() is one such directive that emits
# a second query to load all collections at once.

from sqlalchemy.orm import subqueryload

session.expire_all()

for user in session.query(User).options(subqueryload(User.addresses)):
    print(user, user.addresses)

### slide:: p
# The subqueryload directive is complemented by the joinedload() directive,
# which emits a JOIN in one statement.  It's particularly useful
# for many-to-one loads.

from sqlalchemy.orm import joinedload

session.expire_all()

for address in session.query(Address).\
                options(joinedload(Address.user)):
    print(address, address.user)

### slide:: p
# an important thing about joinedload() is that
# it does not change the results of the query.
# You can't ORDER BY the joinedload(), you use join() for that.
for address in session.query(Address).\
                join(Address.user).\
                filter(User.name=='jack').\
                options(joinedload(Address.user)):
    print(address, address.user)

### slide:: p
# to join *and* eagerload at the same time without using two
# JOIN clauses, use contains_eager.

from sqlalchemy.orm import contains_eager

for address in session.query(Address).\
                join(Address.user).\
                filter(User.name=='jack').\
                options(contains_eager(Address.user)):
    print(address, address.user)

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

### slide:: p
# now, removing an Address from a user means that it gets
# *deleted*.
session = Session(bind=engine)

u1 = session.query(User).filter_by(name="jack").one()

del u1.addresses[1]
session.commit()

### slide:: p
# deleting the User also deletes all the Address objects
# associated with it.

session.delete(u1)
session.commit()

### slide::


