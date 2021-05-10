=======
History
=======

2.3.0 (2021-05-10)
------------------

* Support Python 3.10.

* Stop distributing tests to reduce package size. Tests are not intended to be
  run outside of the tox setup in the repository. Repackagers can use GitHub's
  tarballs per tag.

2.2.0 (2020-12-13)
------------------

* Drop Python 3.5 support.
* Support Python 3.9.
* Move license from BSD to MIT License.

2.1.0 (2019-12-19)
------------------

* Update Python support to 3.5-3.8, as 3.4 has reached its end of life.
* Converted setuptools metadata to configuration file. This meant removing the
  ``__version__`` attribute from the package. If you want to inspect the
  installed version, use
  ``importlib.metadata.version("pytest-super-check")``
  (`docs <https://docs.python.org/3.8/library/importlib.metadata.html#distribution-versions>`__ /
  `backport <https://pypi.org/project/importlib-metadata/>`__).

2.0.0 (2019-02-28)
------------------

* Drop Python 2 support, only Python 3.4+ is supported now.

1.0.0 (2016-04-22)
------------------

* First release on PyPI
