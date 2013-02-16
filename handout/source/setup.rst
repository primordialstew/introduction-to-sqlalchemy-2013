=============
Package Setup
=============

Contents
========

This package contains:

* student handout, buildable as HTML or PDF via Sphinx, in handout/

* Software installs in sw/

* Interactive Python slide runner


Prerequisites
=============

A minimum version of Python 2.6 is recommended;
Python 2.7, 3.1, 3.2 or 3.3 are also fine.

For database access, the tutorials use the SQLite database by default,
which is included as part of the Python standard library.

If your Python was custom built and does not include SQLite, it
can be added in by rebuilding with the SQLite libraries available or
by installing pysqlite.

To build the documentation, the Sphinx documentation system and
its prerequistites must be installed.

To install the slide runner and dependencies, virtualenv is strongly
recommended, available at http://pypi.python.org/pypi/virtualenv.   Students are encouraged to gain rudimental familiarity with virtualenv prior to the class.

Obtaining the Package
======================

The most recent version of this package is available using git::

	git clone https://bitbucket.org/zzzeek/pycon2013_student_package.git

Building the Documentation Handout
==================================

The documentation can be built using standard Sphinx techniques.

To build HTML on Linux / OSX::

	cd handout/
	make html

To build HTML on Windows::

	cd handout/
	make html

The documentation can also be built as PDF or any other format supported by Sphinx.   See the Sphinx documentation at http://sphinx-doc.org/ for further documentation.

Installing the Slide Environment
================================

The slide environment features a working SQLAlchemy environment as well as several tutorial-style Python scripts which illustrate usage patterns.   The slides are best run using a specialized "slide runner" application, which we
will be running as part of the class.

To make the installation as easy as possible, as well as to minimize the need for network access, most of the non-standard prerequisite libraries are included here in the sw/ directory.    However, the system is best run using a Python virtualenv environment, so that system-wide installation is not required.

Steps to install:

1. Create a local virtualenv::

	$ virtualenv --no-site-packages .venv

2. Run the ``install.py`` script, which will install packages from the ``sw/``
   directory into the local virtualenv::

	$ .venv/bin/python install.py

3. A particular tutorial script can be run using the ``sliderepl`` program::

	$ .venv/bin/sliderepl 01_engine_usage.py

