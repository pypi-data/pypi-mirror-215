import pytest

from ddocs import ModulesManager


def test_handle_module():

    import builtins

    m = ModulesManager("tests")

    module = m.handle_module("builtins")

    assert module["doc"] == builtins.__doc__
    assert module["members"]["str"]["doc"] == str.__doc__

def test_handle_entity():

    import builtins

    m = ModulesManager("tests")

    for name, actual in (("strip", str.strip), ("split", str.split), ("capitalize", str.capitalize)):

        e = m.handle_entity(builtins.str, name, depth=1)

        assert e["doc"] == actual.__doc__