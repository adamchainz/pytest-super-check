import inspect
from collections import defaultdict
from typing import Any, Callable, List

import pytest
from _pytest.config import Config
from _pytest.nodes import Item
from _pytest.unittest import UnitTestCase


def pytest_collection_modifyitems(config: Config, items: List[Item]) -> None:
    errors = defaultdict(list)

    for item in items:
        parent = getattr(item, "parent", None)
        if parent is None or not isinstance(parent, UnitTestCase) or parent in errors:
            continue

        klass = parent.cls

        for name in (
            "setUpClass",
            "setUpTestData",
            "setUp",
            "tearDown",
            "tearDownClass",
        ):
            try:
                klass.__dict__[name]
            except KeyError:
                # Not defined in this class (may be in superclass)
                continue

            func = getattr(klass, name)  # Fetch *bound* method

            real_func = get_real_func(func)

            # Unwrap any decorators, we only care about inspecting the innermost
            while hasattr(real_func, "__wrapped__"):
                real_func = get_real_func(
                    real_func.__wrapped__  # type: ignore [attr-defined]
                )

            if "super" not in real_func.__code__.co_names:
                errors[parent].append(name)

    if errors:
        raise pytest.UsageError(*(error_msg(p, names) for p, names in errors.items()))


def get_real_func(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Copied from patchy.

    Duplicates some of the logic implicit in inspect.getsource(). Basically
    some function-esque things, such as classmethods, aren't functions but we
    can peel back the layers to the underlying function very easily.
    """
    if inspect.ismethod(func):
        return func.__func__
    else:
        return func


def error_msg(parent: UnitTestCase, names: List[str]) -> str:
    return "{parent_id} does not call super() in {names}".format(
        parent_id=parent.nodeid, names=", ".join(names)
    )
