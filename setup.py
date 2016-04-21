#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(filename):
    """
    Return package version as listed in `__version__` in `filename`.
    """
    init_py = open(filename).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('pytest_super_check.py')


if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'Version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'pytest',
    'six',
]

setup(
    name='pytest-super-check',
    version=version,
    description='Pytest plugin to check your TestCase classes call super in setUp, tearDown, etc.',
    long_description=readme + '\n\n' + history,
    author="Adam Johnson",
    author_email='me@adamj.eu',
    url='https://github.com/adamchainz/pytest-super-check',
    py_modules=['pytest_super_check'],
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='pytest, super, unittest, testcase',
    entry_points={
        'pytest11': ['super_check = pytest_super_check'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)
