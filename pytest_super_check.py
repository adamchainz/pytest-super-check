# -*- encoding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import inspect
from collections import defaultdict

import pytest
import six
from _pytest.unittest import UnitTestCase

__version__ = '1.0.0'


def pytest_collection_modifyitems(session, config, items):
    errors = defaultdict(list)

    for item in items:
        parent = getattr(item, 'parent', None)
        if (
            parent is None or
            not isinstance(parent, UnitTestCase) or
            parent in errors
        ):
            continue

        klass = parent.cls

        for name in ('setUpClass', 'setUpTestData', 'setUp', 'tearDown', 'tearDownClass'):
            try:
                klass.__dict__[name]
            except KeyError:
                # Not defined in this class (may be in superclass)
                continue

            func = getattr(klass, name)  # Fetch *bound* method

            real_func = get_real_func(func)

            # Unwrap any decorators, we only care about inspecting the innermost
            while hasattr(real_func, '__wrapped__'):
                real_func = get_real_func(real_func.__wrapped__)

            code = six.get_function_code(real_func)
            if 'super' not in code.co_names:
                errors[parent].append(name)

    if errors:
        raise pytest.UsageError(*[
            error_msg(p, names) for p, names in six.iteritems(errors)
        ])


def get_real_func(func):
    """
    Copied from patchy.

    Duplicates some of the logic implicit in inspect.getsource(). Basically
    some function-esque things, such as classmethods, aren't functions but we
    can peel back the layers to the underlying function very easily.
    """
    if inspect.ismethod(func):
        try:
            # classmethod, staticmethod
            real_func = func.__func__
        except AttributeError:
            real_func = func.im_func
    else:
        real_func = func

    return real_func


def error_msg(parent, names):
    return '{parent_id} does not call super() in {names}'.format(
        parent_id=parent.nodeid,
        names=', '.join(names),
    )
