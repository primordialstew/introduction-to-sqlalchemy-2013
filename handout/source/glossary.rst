.. _glossary:

========
Glossary
========

The glossary is broken into two distinct areas of terminology, for those who
want to read the whole thing.

:ref:`glossary_relational`

:ref:`glossary_sqlalchemy`

.. _glossary_relational:

Relational Terms
================

.. glossary::
    :sorted:

    constraint
    constraints
        Rules established within a relational database that ensure
        the validity and consistency of data.   Common forms
        of constraint include :term:`primary key constraint`,
        :term:`foreign key constraint`, and :term:`check constraint`.

        .. seealso::

            :ref:`consistency`

    primary key
    primary key constraint

        A :term:`constraint` that uniquely defines the characteristics
        of each :term:`row`. The primary key has to consist of
        characteristics that cannot be duplicated by any other row.
        The primary key may consist of a single attribute or a
        multiple attributes in combination.
        (via Wikipedia)

        The primary key of a table is typically, though not always,
        defined within the ``CREATE TABLE`` :term:`DDL`:

        .. sourcecode:: sql

            CREATE TABLE employee (
                 emp_id INTEGER,
                 emp_name VARCHAR(30),
                 dep_id INTEGER,
                 PRIMARY KEY (emp_id)
            )

        .. seealso::

            :ref:`primary_key`

            http://en.wikipedia.org/wiki/Primary_Key

    foreign key constraint
        A referential constraint between two tables.  A foreign key is a field in a
        relational table that matches a :term:`candidate key` of another table.
        The foreign key can be used to cross-reference tables.
        (via Wikipedia)

        A foreign key constraint can be added to a table in standard
        SQL using :term:`DDL` like the following:

        .. sourcecode:: sql

            ALTER TABLE employee ADD CONSTRAINT dep_id_fk
            FOREIGN KEY (employee) REFERENCES department (dep_id)

        .. seealso::

            :ref:`foreign_key`

            http://en.wikipedia.org/wiki/Foreign_key_constraint

    candidate key

        A relational algebra term referring to an attribute or set
        of attributes that form a uniquely identifying key for a
        row.  A row may have more than one candidate key, each of which
        is suitable for use as the primary key of that row.
        The primary key of a table is always a candidate key.

        .. seealso::

            :ref:`primary_key`

            http://en.wikipedia.org/wiki/Candidate_key

    check constraint

        A check constraint is a
        condition that defines valid data when adding or updating an
        entry in a table of a relational database. A check constraint
        is applied to each row in the table.

        (via Wikipedia)

        A check constraint can be added to a table in standard
        SQL using :term:`DDL` like the following:

        .. sourcecode:: sql

            ALTER TABLE distributors ADD CONSTRAINT zipchk CHECK (char_length(zipcode) = 5);

        .. seealso::

            http://en.wikipedia.org/wiki/Check_constraint

    unique constraint
    unique key index
        A unique key index can uniquely identify each row of data
        values in a database table. A unique key index comprises a
        single column or a set of columns in a single database table.
        No two distinct rows or data records in a database table can
        have the same data value (or combination of data values) in
        those unique key index columns if NULL values are not used.
        Depending on its design, a database table may have many unique
        key indexes but at most one primary key index.

        (via Wikipedia)

        .. seealso::

            http://en.wikipedia.org/wiki/Unique_key#Defining_unique_keys

    ACID
    ACID model
        An acronym for "Atomicity, Consistency, Isolation,
        Durability"; a set of properties that guarantee that
        database transactions are processed reliably.
        (via Wikipedia)

        .. seealso::

            :ref:`acid_model`

            http://en.wikipedia.org/wiki/ACID_Model

    atomicity
        Atomicity is one of the components of the :term:`ACID` model,
        and requires that each transaction is "all or nothing":
        if one part of the transaction fails, the entire transaction
        fails, and the database state is left unchanged. An atomic
        system must guarantee atomicity in each and every situation,
        including power failures, errors, and crashes.
        (via Wikipedia)

        .. seealso::

            :ref:`atomicity`

            http://en.wikipedia.org/wiki/Atomicity_(database_systems)

    consistency
        Consistency is one of the compoments of the :term:`ACID` model,
        and ensures that any transaction will
        bring the database from one valid state to another. Any data
        written to the database must be valid according to all defined
        rules, including but not limited to :term:`constraints`, cascades,
        triggers, and any combination thereof.
        (via Wikipedia)

        .. seealso::

            :ref:`consistency`

            http://en.wikipedia.org/wiki/Consistency_(database_systems)

    isolation
        The isolation property of the :term:`ACID` model
        ensures that the concurrent execution
        of transactions results in a system state that would be
        obtained if transactions were executed serially, i.e. one
        after the other. Each transaction must execute in total
        isolation i.e. if T1 and T2 execute concurrently then each
        should remain independent of the other.[citation needed]
        (via Wikipedia)

        .. seealso::

            :ref:`isolation`

            http://en.wikipedia.org/wiki/Isolation_(database_systems)

    durability
        Durability is a property of the :term:`ACID` model
        which means that once a transaction has been committed,
        it will remain so, even in the event of power loss, crashes,
        or errors. In a relational database, for instance, once a
        group of SQL statements execute, the results need to be stored
        permanently (even if the database crashes immediately
        thereafter).
        (via Wikipedia)

        .. seealso::

            :ref:`durability`

            http://en.wikipedia.org/wiki/Durability_(database_systems)

    commit
        Denotes the successful completion of a :term:`transaction`.
        In SQL, we normally denote the commit using the ``COMMIT`` statement:

        .. sourcecode:: sql

            BEGIN TRANSACTION

            INSERT INTO employee (emp_id, emp_name, dep_id)
                        VALUES (1, 'dilbert', 1);

            INSERT INTO employee (emp_id, emp_name, dep_id)
                        VALUES (2, 'wally', 1);

            COMMIT

        Above, the row ``employee`` rows for ``dilbert`` and ``wally``
        will be permanently available following the ``COMMIT`` statement.

    rollback
        Denotes a premature end to a :term:`transaction` which reverses
        all the effects of the transaction that have proceeded thus far; the
        state established within the transaction is discarded.   In SQL,
        this is normally denoted using the ``ROLLBACK`` statement:

        .. sourcecode:: sql

            BEGIN TRANSACTION

            INSERT INTO employee (emp_id, emp_name, dep_id)
                        VALUES (1, 'dilbert', 1);

            INSERT INTO employee (emp_id, emp_name, dep_id)
                        VALUES (2, 'wally', 1);

            ROLLBACK

        Above, no new rows will be present in the database following
        the ``ROLLBACK`` statement; both rows inserted for ``dilbert``
        and ``wally`` will be discarded.

    multi version concurrency control
    MVCC
        A system by which modern databases provide concurrent
        access to database data.   By assigning *versions* to
        snapshots of data in time, multiple transactions may simultaneously
        view different versions of the data, relative to the time
        that they were begun.

        .. seealso::

            :ref:`isolation`

            http://en.wikipedia.org/wiki/Multiversion_concurrency_control

    transaction
    transactional
        A transaction comprises a unit of work (not to be confused
        with SQLAlchemy's :term:`unit of work` pattern, which is
        similar) performed within a database management system
        against a database, and treated in a coherent and reliable way
        independent of other transactions. Transactions in a database
        environment have two main purposes:

            * To provide reliable units of work that allow correct
              recovery from failures and keep a database consistent even
              in cases of system failure, when execution stops
              (completely or partially) and many operations upon a
              database remain uncompleted, with unclear status.

            * To provide isolation between programs accessing a database
              concurrently. If this isolation is not provided, the
              program's outcome are possibly erroneous.

        (via Wikipedia)

        .. seealso::

            http://en.wikipedia.org/wiki/Database_transaction

            :ref:`acid_model`

            :term:`commit`

            :term:`rollback`


    surrogate primary key

        A :term:`primary key` that is not derived from application
        data.

        (via Wikipedia)

        Surrogate primary keys in practice are often
        integer values generated by database sequences
        or other incrementing counters,
        or less commonly global unique identifiers (GUIDs).

        .. seealso::

            :term:`natural primary key`

            http://en.wikipedia.org/wiki/Surrogate_key

    natural primary key

        A :term:`primary key` that is formed of attributes that
        already exist in the real world. For example, a USA citizen's
        social security number could be used as a natural key. In
        other words, a natural key is a :term:`candidate key` that has a
        logical relationship to the attributes within that :term:`row`.

        (via Wikipedia)

        .. seealso::

            :term:`surrogate primary key`

            http://en.wikipedia.org/wiki/Natural_key

    FROM clause
        A component of the ``SELECT`` statement which specifies the source
        tables or subqueries from which rows are to be selected.  The ``FROM``
        clause follows the :term:`columns clause` and may contain a comma-separated
        list of tables and subqueries, as well as :term:`join` expressions:

        .. sourcecode:: sql

            -- FROM clause illustrating an explicit join

            SELECT id, name, email_address
             FROM user_account
             JOIN email_address ON user_account.id=email_address.user_account_id

            -- FROM clause illustrating an implicit join

            SELECT id, name, email_address
             FROM user_account, email_address
             WHERE user_account.id=email_address.user_account_id

    WHERE clause
        A component of the ``SELECT`` statement which specifies logical criteria
        to be applied to each row retrieved from the :term:`FROM clause`.
        The ``SELECT`` statement discards all rows which do not evaluate to
        "true" for a given WHERE clause.

        Below, we select rows from the ``email_address`` table, but use the
        WHERE clause to limit those rows to only those which refer to email
        addresses that contain ``@gmail.com``:

        .. sourcecode:: sql

            SELECT id, email_address FROM email_address
            WHERE email_address LIKE '%@gmail.com'


    columns clause
        The portion of a ``SELECT`` statement that enumerates a series of SQL
        expressions to be evaulated as the returned result set.  Typically,
        these expressions refer directly to table columns.  The columns
        clause follows the ``SELECT`` keyword and precedes the ``FROM``
        keyword.

        In the following ``SELECT`` statement, the "id" and "name" columns
        will be returned for each row, and this enumeration of columns
        forms the "columns clause":

        .. sourcecode:: sql

            SELECT id, name FROM user_account


    column
    columns
        A vertical unit of storage in a :term:`table`.   The table
        defines one or more columns as fixed types of data to
        be stored within rows.

    table
        A fundamental storage component used by relational databases.
        The table corresponds to what's known as a :term:`relation`
        in :term:`relational algebra`, and defines a series of
        :term:`columns`, each of which represents a particular
        type of data value to be stored in the table.  The columns
        are then organized at the data storage level into a collection
        of :term:`rows`, each of which corresponds to a unit of
        data.

    row
    rows
        A horizontal unit of storage in a :term:`table`.  Each new data
        record inserted into a table comprises a row; the row in turn
        is broken into individual :term:`column` values.

    tuple
    tuples
    row value
        An ordered collection of typed values, such as
        ``(1, 'ed', 'ed@msn.com')``.

    table value
    rowset
        An ordered collection of row values, each of the same length and types.


    normalization
        Database normalization is the process of organizing the fields
        and tables of a relational database to minimize redundancy and
        dependency. Normalization usually involves dividing large
        tables into smaller (and less redundant) tables and defining
        relationships between them. The objective is to isolate data
        so that additions, deletions, and modifications of a field can
        be made in just one table and then propagated through the rest
        of the database via the defined relationships.
        (via Wikipedia)

        .. seealso::

            http://en.wikipedia.org/wiki/Database_normalization

    relational model
    relational algebra
        The relational model for database management is a database model
        based on first-order predicate logic, first formulated and
        proposed in 1969 by :term:`Edgar F. Codd`. In the relational model
        of a database, all data is represented in terms of :term:`tuples`, grouped
        into :term:`relations`. A database organized in terms of the relational
        model is a relational database.
        (via Wikipedia)

        .. seealso::

            http://en.wikipedia.org/wiki/Relational_model

    Edgar Codd
    Edgar F. Codd
        Creator of the :term:`relational model`.

        .. seealso::

            http://en.wikipedia.org/wiki/Edgar_F._Codd


    Structured Query Language
    SQL
        SQL (pron.: /s kju l/ "S-Q-L";[3] or Structured Query
        Language) is a special-purpose programming language designed
        for managing data in relational database management systems
        (RDBMS).

        Originally based upon relational algebra and tuple relational
        calculus, its scope includes data insert, query, update and
        delete, schema creation and modification, and data access
        control.

        (via Wikipedia)

        .. seealso::

            http://en.wikipedia.org/wiki/Sql

    cartesian product
        A mathematical operation which returns a set (or product set) from multiple sets.
        The Cartesian product is the result of crossing members of each set with one another.
        (via Wikipedia)

        .. seealso::

            http://en.wikipedia.org/wiki/Cartesian_product

    relation
    relations
        In :term:`relational algebra`, a single grid of data represented by
        zero or more :term:`tuples`. In a SQL database, the most common
        relation is the :term:`table`, which defines one or more columns of zero
        or more :term:`rows`. The output of a ``SELECT`` statement is also a relation.


    data manipulation language
    DML
        The SQL commands that manipulate data.
        For example, ``SELECT``, ``INSERT``, ``UPDATE`` and ``DELETE``.

        .. seealso::

            :ref:`dml`

            http://en.wikipedia.org/wiki/Data_Manipulation_Language


    data definition language
    DDL
        The SQL commands that define a schema.
        For example, ``CREATE TABLE``, ``DROP TABLE``, ``ALTER TABLE``.

        .. seealso::

            :ref:`ddl`

            http://en.wikipedia.org/wiki/Data_Definition_Language

    query
    queries
        The means of interrogating a relational database for
        data.   The primary feature in SQL used for querying
        is the ``SELECT`` statement.

        .. seealso::

            :ref:`queries`

            http://en.wikipedia.org/wiki/Sql#Queries


    join
    inner join
        Combines the rows of two tables.  Considers each pair of rows
        in turn, and returns one combined row for each pair that
        matches an ON criteria.

        .. sourcecode:: sql

            SELECT ua.id, ua.name, ea.email, ea.user_account_id
             FROM user_account AS ua
              JOIN email_address AS ea
              ON ua.id = ea.user_account_id

             id | name  |      email     | user_account_id
            ----+-------+----------------+----------------
              1 | jack  |  jack@jack.com |       1
              2 | ed    |  ed@yahoo.com  |       2
              2 | ed    |  ed@msn.com    |       2
              3 | wendy |  wendy@nyt.com |       3

        The result of the join can be defined in a logical
        sense by first
        determining the :term:`cartesian product` of the left and
        right side tables; then, for each row within this product,
        evaluating ``ON`` clause for each row, selecting only those
        rows for which the clause evaluates to "true".
        In practice, relational database systems
        use more efficient approaches internally in order to evaluate
        the result of a join.

        Usage of the ``JOIN`` or ``INNER JOIN`` keyword is logically
        equivalent to a so-called *implicit join*, where the ``JOIN``
        keyword is not present, and instead the left and right side
        expressions are delivered to the :term:`FROM clause` as a comma
        separated list, with the ON criteria stated instead in
        the ``WHERE`` clause:

        .. sourcecode:: sql

            SELECT ua.id, ua.name, ea.email, ea.user_account_id
             FROM user_account AS ua, email_address.ea
             WHERE ua.id = ea.user_account_id


        .. seealso::

            :term:`left outer join`

            http://en.wikipedia.org/wiki/Sql_join


    left outer join
        A variant of the :term:`join` whereby the criteria for
        including rows from the "left" side is relaxed, such that
        not only left-side rows which correspond to the right side
        are returned, but also left-side rows for which no right
        side row corresponds.   In the case where no right
        side row corresponds, all columns from the right side
        are returned as NULL.

        Below, we illustrate selecting all user names from the
        ``user_account`` table, in addition to all the ``email_address``
        rows for each ``user_account`` row, but also including
        rows from ``user_account`` for which no row in ``email_address``
        is present:

        .. sourcecode:: sql


            SELECT ua.id, ua.name, ea.email, ea.user_account_id
             FROM user_account AS ua
              JOIN email_address AS ea
              ON ua.id = ea.user_account_id

             id | name  |      email     | user_account_id
            ----+-------+----------------+----------------
              1 | jack  |  jack@jack.com |       1
              2 | ed    |  ed@yahoo.com  |       2
              2 | ed    |  ed@msn.com    |       2
              3 | wendy |  wendy@nyt.com |       3
              4 | mary  |     (null)     |     (null)

        The left outer join is a key technique used in object relational
        systems in order to resolve a :term:`one to many` collection,
        that is a series of objects that contain zero or more related objects.

        .. seealso::

            :term:`join`

    right outer join
        Like a :term:`left outer join`, except the left and right side
        are swapped.  At least
        one row will be returned for every row in the right table, and
        columns from the left row will be filled with NULL if the ON
        criteria does not match.  In SQLAlchemy, outer joins are left
        outer join.

    subquery
        A ``SELECT`` statement embedded in another ``SELECT`` statement.  Data
        returned from the inner ``SELECT`` is available for use by the
        outer.

        The subquery is a fundamental capability in SQL that allows
        so-called *derived tables* to be created; meaning, the rows
        from a particular ``SELECT`` statement can be named as a unit of
        rows within an enclosing ``SELECT`` that causes it to behave more or
        less like a plain :term:`table`.

        Example:

        .. sourcecode:: sql

            SELECT user_account.name, subq.ad_count FROM
                user_account JOIN
                (SELECT user_account_id, count(id) AS ad_count
                FROM email_address GROUP BY user_account_id) AS subq
                ON user_account.id=subq.user_account_id

        Subqueries can be placed in a variety of ways inside of an enclosing
        ``SELECT`` statement.    Three common locations include the :term:`columns clause`,
        the :term:`WHERE clause`, and the :term:`FROM clause`.   The placement
        of the subquery has an impact on the kind of data the query must return.
        In standard SQL, subqueries placed within the columns or WHERE clause must
        be :term:`scalar subqueries`, i.e. queries that return a single value, unless
        they are evaluated by a boolean aggregation operator such as :term:`IN`,
        :term:`EXISTS`, ``ANY`` or ``ALL``.   A subquery used in the :term:`FROM clause`,
        on the other hand, can return any number of rows and columns.

        Subqueries within the WHERE clause or columns clause are often :term:`correlated subqueries`
        as well, as they are invoked for each row received in the enclosing query.
        For a FROM clause subquery, correlation is not an option as the FROM clause
        is evaluated before the correlatable rows are chosen.

    scalar subquery
    scalar subqueries
        A scalar subquery is a :term:`subquery` that returns a single column from a
        single row.  Scalar subqueries can be used like columns or anywhere
        an expression is required, which typically includes the :term:`columns clause`
        or :term:`WHERE clause` of a ``SELECT`` statement.

        Below, a scalar subquery is used in the columns clause to select the ``name``
        column from the ``user_account`` table for each row selected from the
        ``email_address`` table:

        .. sourcecode:: sql


            SELECT
                email_address.email,
                (SELECT user_account.name FROM user_account WHERE id=1) AS name
            FROM email_address WHERE email_address.user_account_id=1

                 email     | name
            ---------------+----------
             jack@jack.com | jack

        Selecting an email address by user name, using a scalar subquery
        in the ``WHERE`` clause:

        .. sourcecode:: sql

            SELECT email_address.email FROM email_address
            WHERE email_address.user_account_id=(SELECT id FROM user_account WHERE name='jack')

                email
            ---------------
             jack@jack.com

    uncorrelated subquery
        A :term:`subquery` is uncorrelated if the database can execute it in
        isolation, without referring to the enclosing ``SELECT``
        statement.

        .. sourcecode:: sql

            SELECT user_account.name FROM user_account
            WHERE user_account.id IN (SELECT user_account_id FROM email_address)

             name
            -------
             jack
             ed
             wendy

    correlated subquery
    correlated subqueries
        A :term:`subquery` is correlated if it depends on data in the
        enclosing ``SELECT``.

        Below, a subquery selects the aggregate value ``MIN(a.id)``
        from the ``email_address`` table, such that
        it will be invoked for each value of ``user_account.id``, correlating
        the value of this column against the ``email_address.user_account_id``
        column:

        .. sourcecode:: sql

            SELECT user_account.name, email_address.email
             FROM user_account
             JOIN email_address ON user_account.id=email_address.user_account_id
             WHERE email_address.id = (
                SELECT MIN(a.id) FROM email_address AS a
                WHERE a.user_account_id=user_account.id
             )

        The above subquery refers to the ``user_account`` table, which is not itself
        in the ``FROM`` clause of this nested query.   Instead, the ``user_account``
        table is recieved from the enclosing query, where each row selected from
        ``user_account`` results in a distinct execution of the subquery.

        A correlated subquery is nearly always present in the :term:`WHERE clause`
        or :term:`columns clause` of the enclosing ``SELECT`` statement, and never
        in the :term:`FROM clause`; this is because
        the correlation can only proceed once the original source rows from the enclosing
        statement's FROM clause are available.


    IN
    IN operator
        A comparison operator.  Compares an expression against a list of
        values, and is true if it matches at least one of them.

        .. sourcecode:: sql

            SELECT email FROM email_address
            WHERE user_account_id IN (1, 2)


        A :term:`subquery` can be used in place of a literal list of values:

        .. sourcecode:: sql

            SELECT email FROM email_address
            WHERE user_account_id IN
            (SELECT id FROM user_account WHERE name='jack' OR name='ed')


    EXISTS
    EXISTS operator
        The EXISTS operator tests a subquery and returns true if the
        subquery returns any rows:

        .. sourcecode:: sql

            SELECT name FROM user_account
             WHERE EXISTS
             (SELECT * FROM email_address WHERE email_address.user_account_id=user_account.id)

             name
            -------
             jack
             ed
             wendy

        The columns selected by the subquery are ignored.  Only the
        number of rows are considered: no rows or at least one.
        ``EXISTS <subquery>`` is a :term:`scalar`, boolean expresion
        and can be used like any other boolean value in a WHERE clause:

        .. sourcecode:: sql

            SELECT name FROM user_account
              WHERE EXISTS (SELECT * FROM email_address WHERE email_address.user_account_id=user_account.id)
              AND name='ed'

             name
            ------
              ed

        The subquery used within an ``EXISTS`` expression is nearly always
        a :term:`correlated subquery`.


.. _glossary_sqlalchemy:

SQLAlchemy Core / Object Relational Terms
==========================================


.. glossary::
    :sorted:

    orphan
        A mapped instance with a severed link to a collection or parent object.

    pending
        An instance which has been saved into a session but not yet persisted to the database.

    persistent
        An instance which is present in a session and in the database.

    query
        1. A SQL statement which is processed by a database to return results.
        2. A SQLAlchemy ORM object which defines search criterion and returns mapped instances.

    threadlocal
        A shared data structure whose data members are visible only to
        the thread which set them. The concept of "thread local" in
        Python is normally provided by the ``threading.local``
        construct.

        .. seealso::

            http://docs.python.org/2/library/threading.html#threading.local

    reflection
        The process of constructing SQLAlchemy Table objects
        programatically at runtime by querying a live database's
        system tables for column and key definitions.


    column
        1. a database column, as defined within a CREATE TABLE
        statement

        2. a SQLAlchemy :class:`.Column` construct, which is a data
        structure that stores information about the name of a database
        column, its constraints, data type, and information on its
        default value.

    detached
        An instance which is not present in any session, but whose
        state information is present in the database. A detached
        instance may have further pending changes on it which will
        only be persisted if the instance is updated into a session
        and then flushed.

    engine
        The primary facade for a database. An :class:`.Engine` manages a pool of
        database connections and provides methods to execute SQL
        statements and fetch result sets.

        .. seealso::

            :ref:`sqla:engines_toplevel`

            :ref:`sqla:connections_toplevel`

    explicit execution
        Applying a SQLAlchemy action or statement to a specific database
        or connection.

    flush
        The operation by which a :class:`.Session` assembles all pending
        changes in memory to a set of objects, and emits INSERT, UPDATE
        and DELETE statements to the current database connection in order
        to synchronize those changes with the database.

        The flush is a key component of the :term:`unit of work`
        object relational pattern.

    identity map
        A per-session, one-to-one mapping between Python instances and
        database identity.  Ensures that only one mapped instance
        exists at a time, no matter how how it is queried or
        associated.

    implicit execution
        Application of a bound SQLAlchemy action or statement, affects the
        database specified in the bind. Provides a lightweight syntax when
        only a single database is required.

    instance
        The result of calling a Python class constructor; a single, unique
        Python object.

    instrumentation
        The injection of an observer into a method or attribute.
        SQLAlchemy uses instrumentation to detect changes made to managed
        attributes and track changes in collection membership. Changes
        raise events which can cascade to related instances.

    mapper
        An object which translates database rows to and from instances
        of a class.  Mappers define which columns will be translated
        to object attributes, and how foreign key relationships will
        be translated to collection-holding attributes.  A mapper
        installs instrumentation on the Python class to manage mapped
        attributes.

    MetaData
        A collection of related :class:`.Table` objects.  These objects
        collected together may define :class:`.ForeignKey` objects which refer
        to other tables as dependencies.   The full collection of tables can
        be created and dropped in a target database schema en masse.

        .. seealso::

            :ref:`sqla:metadata_toplevel`

    attribute
        In Python, a field of an instance or class.  In SQLAlchemy,
        managed instance attributes are instrumented to detect
        changes, and class attributes can be used in the construction
        of queries.

    autocommit
        A style of SQL execution in which each statement is
        transparently wrapped in its own transaction.  Autocommit is
        often used for interactive SQL command line prompts and it is
        the default behavior of SQLAlchemy if no explicit transaction
        is in effect.

    bind
        The association between a database and a SQLAlchemy component
        such as a table or ORM session.  Components which are bound
        are linked to a single database and can act upon it
        implicitly.  Unbound components can be used with any number of
        databases but must explicitly combined: "act upon database
        A, now act upon database B."

    cascade
        The propagation of events from one mapped instance to another.
        The cascade follows the path defined by relations between the
        mappings. Cascaded events communicate session state. For example,
        adding a lead instance to a session will add all associated
        instances as well.

    collection
        In Python, a container class such as a list, set, or dict. In
        SQLAlchemy relationships, the same, except the collection is
        automatically filled with instances retrieved from the database.

    connection
        An active link to a database. In SQLAlchemy, connections are
        managed in a pool and idle connections are reused for new
        tasks.  An active connection has a transactional state.

    transient
        An instance of a mapped class which has not been saved into a
        session or loaded from the database.


    Unit of Work
        The bundling together of all pending mapped instance creations,
        modifications and deletions.  The workhorse behind an ORM session
        flush, the Unit of Work translates un-flushed session activity
        into a properly ordered series of INSERT, UPDATE and DELETE
        statements.

    scalar
    scalar value
        A single value, such as ``'a'``, ``123`` or ``'2008-02-01'``.

    single table inheritance
        Columns for all classes in an inheritance hierarchy are stored
        in a single table. A discriminator column indicates which
        class a given row represents.  Columns not needed by a
        particular class are left empty.

        E.g.::


            id | type  | amount |    date    | cnum | expiry_year | expiry_mon
           ----+-------+--------+------------+------+-------------+------------
             1 | check | 100.00 | 2008-02-01 |   12 |             |
             2 | ccard |  50.75 | 2008-02-02 |      |        2010 |          2

        .. seealso::

           :term:`joined table inheritance`

           :term:`concrete table inheritance`

    joined table inheritance
        Columns for classes in an inheritance hierarchy are stored in one
        table per class. The tables are joined together to represent an
        instance columns for the instance's types are combined with
        columns of its super class and so on. The primary key of the base
        class in the hierarchy is shared among all of class tables.  The
        base class table also contains a discriminator column to identify
        the type of any given row.

        .. sourcecode:: sql

            CREATE TABLE payment (
                id SERIAL PRIMARY KEY,
                type VARCHAR(16) NOT NULL,
                amount NUMERIC(10,2),
                "date" DATE )

            CREATE TABLE check_payment (
                id INTEGER PRIMARY KEY REFERENCES payment (id),
                cnum INTEGER )

            CREATE TABLE ccard_payment (
                id INTEGER PRIMARY KEY REFERENCES payment (id),
                expiry_year INTEGER,
                expiry_mon INTEGER )

            INSERT INTO payment (type, amount, "date")
                VALUES ('check', 100.0, '2008-02-01')

            INSERT INTO check_payment VALUES (1, 12)

            INSERT INTO payment (type, amount, "date")
                VALUES ('ccard', 50.75, '2008-02-02')

            INSERT INTO ccard_payment VALUES (2, 2010, 2)

            SELECT * FROM payment
                NATURAL LEFT JOIN check_payment
                NATURAL LEFT JOIN ccard_payment

             id | type  | amount |    date    | cnum | expiry_year | expiry_mon
            ----+-------+--------+------------+------+-------------+------------
              1 | check | 100.00 | 2008-02-01 |   12 |             |
              2 | ccard |  50.75 | 2008-02-02 |      |        2010 |          2

            SELECT * FROM payment NATURAL JOIN check_payment WHERE type='check'

             id | type  | amount |    date    | cnum
            ----+-------+--------+------------+------
              1 | check | 100.00 | 2008-02-01 |   12

            SELECT * FROM payment NATURAL JOIN ccard_payment WHERE type='ccard'

             id | type  | amount |    date    | expiry_year | expiry_mon
            ----+-------+--------+------------+-------------+------------
              2 | ccard |  50.75 | 2008-02-02 |        2010 |          2

        .. seealso::

            :term:`single table inheritance`

            :term:`concrete table inheritance`

    concrete table inheritance
        Columns for classes in an inheritance hierarchy are stored in
        one table per class.  Each table contains the full set of
        columns used by its class, and primary key values are not
        unique among tables.  The tables are fully independent.

        .. sourcecode:: sql

            CREATE TABLE check_payment (
                id SERIAL PRIMARY KEY,
                amount NUMERIC(10,2),
                "date" DATE,  cnum INTEGER )

            CREATE TABLE ccard_payment (
                id SERIAL PRIMARY KEY,
                amount NUMERIC(10,2),
                "date" DATE,
                expiry_year INTEGER,
                expiry_mon INTEGER )

            INSERT INTO check_payment (amount, "date", cnum)
                VALUES (100.0, '2008-02-01', 12)

            INSERT INTO ccard_payment (amount, "date", expiry_year, expiry_mon)
                VALUES (50.75, '2008-02-02', 2010, 2)

            SELECT * FROM check_payment

             id | amount |    date    | cnum
            ----+--------+------------+------
              1 | 100.00 | 2008-02-01 |   12

            SELECT * FROM ccard_payment

             id | amount |    date    | expiry_year | expiry_mon
            ----+--------+------------+-------------+------------
              1 |  50.75 | 2008-02-02 |        2010 |          2

        .. seealso::

            :term:`single table inheritance`

            :term:`joined table inheritance`

    many to many
        An intermediary table modeling a many-to-many relationship.
        Given:

        .. sourcecode:: sql

            CREATE TABLE cars (
                car_id INTEGER PRIMARY KEY,
                model VARCHAR(100) )

            CREATE TABLE colors (
                color_id INTEGER PRIMARY KEY,
                name VARCHAR(100) )

        and the relationship "car models are available in multiple colors",
        the relation can be modeled with a two-column table:

        .. sourcecode:: sql

            CREATE TABLE car_colors (
                car_id INTEGER REFERENCES cars (car_id),
                color_id INTEGER REFERENCES colors (color_id),
                PRIMARY KEY (car_id, color_id) )

        .. seealso::

            :term:`association table`

    association table
    association relationship
        A :term:`relationship` between two tables that is further
        qualified by information specific to each pair of linked rows:

        .. sourcecode:: sql

            CREATE TABLE cars (
                car_id INTEGER PRIMARY KEY,
                model VARCHAR(100) )

            CREATE TABLE colors (
                color_id INTEGER PRIMARY KEY,
                name VARCHAR(100) )

        and the relationship "car models are available in multiple colors,
        each for a limited time-span", the relation can be modeled with an
        association table containing additional columns:

        .. sourcecode:: sql

            CREATE TABLE car_colors (
                car_id INTEGER REFERENCES cars (car_id),
                color_id INTEGER REFERENCES colors (color_id),
                available_starting DATE NOT NULL,
                available_ending DATE NOT NULL,
                PRIMARY KEY (car_id, color_id) )

        .. seealso::

            :term:`many to many`


    relationship
        In SQLAlchemy, the junction of two mapped classes, or of a
        mapped class to itself.  The relationship usually corresponds
        to a foreign key relationship between two tables or
        selectables.

        .. seealso::

            :ref:`sqla:relationship_config_toplevel`

    scoped_session
        A front end for sessionmaker which provides a "global"
        registry of sessions, each mapped to the current thread.

        .. seealso::

            :ref:`sqla:unitofwork_contextual` - an in-depth
            introduction to the :class:`.scoped_session` object.

    selectable
        What relational algebra refers to as a relation, SQLAlchemy
        refers to as a selectable. A table, subquery, or any other
        table-valued SQL expression.

    Session
        The container or scope for ORM database operations. Sessions
        load instances from the database, track changes to mapped
        instances and persist changes in a single unit of work when
        flushed.

        .. seealso::

            :ref:`session_toplevel`

    session transaction
        ORM-level transaction. Session activity may span multiple
        databases, and the session transaction coordinates a
        connection-level transaction for each. Database features such
        as save points and two-phase transactions are also supported.

    sessionmaker
        An optional, configurable factory object used to create new
        Session instances using a chosen set of construction
        arguments.

