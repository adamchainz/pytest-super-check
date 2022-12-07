==================
pytest-super-check
==================

.. image:: https://img.shields.io/github/workflow/status/adamchainz/pytest-super-check/CI/main?style=for-the-badge
   :target: https://github.com/adamchainz/pytest-super-check/actions?workflow=CI

.. image:: https://img.shields.io/pypi/v/pytest-super-check.svg?style=for-the-badge
   :target: https://pypi.org/project/pytest-super-check/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
   :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=for-the-badge
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

Unmaintained (2022-12-07)
-------------------------

I stopped maintaining this package as it has never been popular.
I think it would be better to use a lint rule to enforce calling ``super()`` in test cases.

----

Pytest plugin to check your TestCase classes call super in setUp, tearDown,
etc.

Features
========

This plugin checks all ``TestCase`` classes in your test suite to ensure that
their ``setUp``, ``tearDown``, ``setUpClass``, ``tearDownClass``, and
``setUpTestData`` (Django extension) methods all call ``super()``. You might
care about this when you have extensions to these methods in your project
specific base class that when skipped (by accidentally missing ``super()``),
cause subtle bugs.

About
=====

I developed this feature in a closed source Nose plugin whilst working on the
big Django project at YPlan. We had some custom enhancements and fixes on top
of the Django test classes, but some ``TestCase`` classes didn't call
``super()`` in e.g. ``setUp``, which caused the tests to fail, or incorrectly
pass, in rather subtle ways. This problem is exacerbated by Django's ``setUp``
etc. doing magic around not requiring ``super()`` to be called. Our solution
was to just ensure every ``TestCase`` always calls ``super()`` in those
methods. This is a Pytest port of that plugin.

Installation
============

Install with:

.. code-block:: bash

    python -m pip install pytest-super-check

Python 3.7 to 3.11 supported.

----

**Testing a Django project?**
Check out my book `Speed Up Your Django Tests <https://adamchainz.gumroad.com/l/suydt>`__ which covers loads of ways to write faster, more accurate tests.

----

Usage
=====

Pytest will automatically find and use the plugin. Test discovery will then
blow up if any subclasses of ``unittest.TestCase`` are found that have
``setUp`` etc. methods that don't call ``super()``.

You can disable the plugin by passing the options ``-p no:super_check`` to
``pytest``.
