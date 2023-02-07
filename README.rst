django-cms-helpers
==================

.. image:: https://img.shields.io/pypi/v/django-cms-helpers.svg
   :target: https://pypi.org/project/django-cms-helpers/
   :alt: Latest Version

.. image:: https://github.com/stephrdev/django-cms-helpers/workflows/Test/badge.svg?branch=master
   :target: https://github.com/stephrdev/django-cms-helpers/actions?workflow=Test
   :alt: CI Status

.. image:: https://codecov.io/gh/stephrdev/django-cms-helpers/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/stephrdev/django-cms-helpers
   :alt: Coverage Status

.. image:: https://readthedocs.org/projects/django-cms-helpers/badge/?version=latest
   :target: https://django-cms-helpers.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status


django-cms-helpers is a collection of helpers when working with django-cms.


Features
--------

* templatetag for getting title extension object.
* anylink extension for cms pages.
* boilerplate code for ExtensionToolbar.
* FilerFileField extension to validate file extension and make default_alt_text required.

Requirements
------------

django-cms-helpers supports Python 3 only and requires at least Django 3.2 and django-cms 3.9.


Prepare for development
-----------------------

A Python 3.8+ interpreter is required in addition to poetry.

.. code-block:: shell

    $ poetry install


Now you're ready to run the tests:

.. code-block:: shell

    $ poetry run py.test


Resources
---------

* `Documentation <https://django-cms-helpers.readthedocs.io>`_
* `Bug Tracker <https://github.com/stephrdev/django-cms-helpers/issues>`_
* `Code <https://github.com/stephrdev/django-cms-helpers/>`_
