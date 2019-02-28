import re

from setuptools import setup


def get_version(filename):
    with open(filename, 'r') as fp:
        contents = fp.read()
    return re.search(r"__version__ = ['\"]([^'\"]+)['\"]", contents).group(1)


version = get_version('pytest_super_check.py')

with open('README.rst', 'r') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst', 'r') as history_file:
    history = history_file.read().replace('.. :changelog:', '')


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
    install_requires=[
        'pytest',
    ],
    python_requires='>=3.4',
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
