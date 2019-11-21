==================
pytest-super-check
==================

.. image:: https://img.shields.io/travis/adamchainz/pytest-super-check.svg
        :target: https://travis-ci.org/adamchainz/pytest-super-check

.. image:: https://img.shields.io/pypi/v/pytest-super-check.svg
        :target: https://pypi.python.org/pypi/pytest-super-check

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black

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

Install from pip with:

.. code-block:: bash

    pip install pytest-super-check

Python 3.5 to 3.8 supported.

Usage
=====

Pytest will automatically find and use the plugin. Test discovery will then
blow up if any subclasses of ``unittest.TestCase`` are found that have
``setUp`` etc. methods that don't call ``super()``.

You can disable the plugin by passing the options ``-p no:super_check`` to
``pytest``.
