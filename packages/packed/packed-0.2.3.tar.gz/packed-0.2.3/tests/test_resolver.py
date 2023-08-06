import pytest
from pytest import raises

from packed import Resolver

from ._test_utils.steps import given, then, when


@pytest.fixture
def resolver():
    return Resolver()


def test_register(*, resolver):
    with given:
        class CustomClass:
            pass

    with when:
        actual = resolver.register(CustomClass)

    with then:
        assert actual is None


def test_register_already_registered(*, resolver):
    with given:
        class CustomClass:
            pass
        resolver.register(CustomClass)

    with when, raises(Exception) as exception:
        resolver.register(CustomClass)

    with then:
        assert exception.type is KeyError


def test_register_already_registered_with_custom_name(*, resolver):
    with given:
        class CustomClass:
            pass
        resolver.register(CustomClass, "custom_class")

    with when:
        actual = resolver.register(CustomClass)

    with then:
        assert actual is None


def test_resolve_type(*, resolver):
    with given:
        class CustomClass:
            pass
        resolver.register(CustomClass)

    with when:
        actual = resolver.resolve_type(CustomClass.__name__)

    with then:
        assert actual == CustomClass


def test_resolve_type_with_custom_name(*, resolver):
    with given:
        class CustomClass:
            pass
        resolver.register(CustomClass, "custom_class")

    with when:
        actual = resolver.resolve_type("custom_class")

    with then:
        assert actual == CustomClass


def test_resolve_type_without_register(*, resolver):
    with when, raises(Exception) as exception:
        resolver.resolve_type("custom_class")

    with then:
        assert exception.type is KeyError


def test_resolve_name(*, resolver):
    with given:
        class CustomClass:
            pass

        class AnotherCustomClass:
            pass

        resolver.register(CustomClass)
        resolver.register(AnotherCustomClass)

    with when:
        actual = resolver.resolve_name(AnotherCustomClass)

    with then:
        assert actual == AnotherCustomClass.__name__


def test_resolve_custom_name(*, resolver):
    with given:
        class CustomClass:
            pass
        resolver.register(CustomClass, "custom_class")

    with when:
        actual = resolver.resolve_name(CustomClass)

    with then:
        assert actual == "custom_class"


def test_resolve_name_without_register(*, resolver):
    with given:
        class ParentClass:
            pass

        class ChildClass(ParentClass):
            pass

    with when, raises(Exception) as exception:
        resolver.resolve_name(ChildClass)

    with then:
        assert exception.type is KeyError
