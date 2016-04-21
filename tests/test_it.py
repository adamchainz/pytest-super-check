# -*- encoding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import six

if six.PY3:
    pytest_plugins = ['pytester']
else:
    pytest_plugins = [b'pytester']


def test_it_does_not_complain_when_everything_supers_correctly(testdir):
    testdir.makepyfile(
        test_one="""
        from unittest import TestCase


        class MyTests(TestCase):

            @classmethod
            def setUpClass(cls):
                super(MyTests, cls).setUpClass()

            @classmethod
            def setUpTestData(cls):
                super(MyTests, cls).setUpTestData()

            def setUp(self):
                super(MyTests, self).setUp()

            def test_one(self):
                pass

            def tearDown(self):
                super(MyTests, self).tearDown()

            @classmethod
            def tearDownClass(cls):
                super(MyTests, cls).tearDownClass()
        """
    )
    out = testdir.runpytest()
    out.assert_outcomes(passed=1, failed=0)
