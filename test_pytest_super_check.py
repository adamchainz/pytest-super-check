pytest_plugins = ["pytester"]


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


def test_it_complains_when_a_case_does_not_super_in_setUp(testdir):
    testdir.makepyfile(
        test_one="""
        from unittest import TestCase


        class MyTests(TestCase):

            def setUp(self):
                self.x = 1

            def test_one(self):
                pass
        """
    )
    out = testdir.runpytest()
    assert out.ret > 0
    out.stderr.fnmatch_lines(
        ["ERROR: test_one.py::MyTests does not call super() in setUp"]
    )


def test_it_complains_when_a_case_does_not_super_in_tearDown(testdir):
    testdir.makepyfile(
        test_one="""
        from unittest import TestCase


        class MyTests(TestCase):

            def tearDown(self):
                self.x = 1

            def test_one(self):
                pass
        """
    )
    out = testdir.runpytest()
    assert out.ret > 0
    out.stderr.fnmatch_lines(
        ["ERROR: test_one.py::MyTests does not call super() in tearDown"]
    )


def test_it_complains_when_a_case_does_not_super_in_setUpClass(testdir):
    testdir.makepyfile(
        test_one="""
        from unittest import TestCase


        class MyTests(TestCase):

            @classmethod
            def setUpClass(cls):
                cls.x = 1

            def test_one(self):
                pass
        """
    )
    out = testdir.runpytest()
    assert out.ret > 0
    out.stderr.fnmatch_lines(
        ["ERROR: test_one.py::MyTests does not call super() in setUpClass"]
    )


def test_it_complains_when_a_case_does_not_super_in_setUpTestData(testdir):
    testdir.makepyfile(
        test_one="""
        from unittest import TestCase

        class TestData(object):  # Fake for Django test case
            @classmethod
            def setUpTestData(cls):
                pass


        class MyTests(TestData, TestCase):

            @classmethod
            def setUpTestData(cls):
                cls.x = 1

            def test_one(self):
                pass
        """
    )
    out = testdir.runpytest()
    assert out.ret > 0
    out.stderr.fnmatch_lines(
        ["ERROR: test_one.py::MyTests does not call super() in setUpTestData"]
    )


def test_it_complains_when_a_case_does_not_super_in_tearDownClass(testdir):
    testdir.makepyfile(
        test_one="""
        from unittest import TestCase


        class MyTests(TestCase):

            @classmethod
            def tearDownClass(cls):
                cls.x = 1

            def test_one(self):
                pass
        """
    )
    out = testdir.runpytest()
    assert out.ret > 0
    out.stderr.fnmatch_lines(
        ["ERROR: test_one.py::MyTests does not call super() in tearDownClass"]
    )


def test_it_complains_when_a_case_does_not_super_in_setUp_and_setUpClass(testdir):
    testdir.makepyfile(
        test_one="""
        from unittest import TestCase


        class MyTests(TestCase):

            @classmethod
            def setUpClass(cls):
                cls.x = 1

            def setUp(self):
                self.y = 1

            def test_one(self):
                pass
        """
    )
    out = testdir.runpytest()
    assert out.ret > 0
    out.stderr.fnmatch_lines(
        ["ERROR: test_one.py::MyTests does not call super() in setUpClass, setUp"]
    )


def test_it_does_not_complain_when_a_decorator_is_used_but_super_is_called(testdir):
    testdir.makepyfile(
        test_one="""
        from functools import wraps
        from unittest import TestCase


        def mydecorator(func):
            @wraps(func)
            def wrapper(self):
                return func(self)
            wrapper.__wrapped__ = func  # Python 2.7 compat
            return wrapper


        class MyTests(TestCase):

            @mydecorator
            def setUp(self):
                super(MyTests, self).setUp()

            def test_one(self):
                pass
        """
    )
    out = testdir.runpytest()
    out.assert_outcomes(passed=1, failed=0)


def test_it_complains_when_a_decorator_is_used_and_super_is_not_called(testdir):
    testdir.makepyfile(
        test_one="""
        from functools import wraps
        from unittest import TestCase


        def mydecorator(func):
            @wraps(func)
            def wrapper(self):
                return func(self)
            wrapper.__wrapped__ = func  # Python 2.7 compat
            return wrapper


        class MyTests(TestCase):

            @mydecorator
            def setUp(self):
                self.x = 1

            def test_one(self):
                pass
        """
    )
    out = testdir.runpytest()
    assert out.ret > 0
    out.stderr.fnmatch_lines(
        ["ERROR: test_one.py::MyTests does not call super() in setUp"]
    )
