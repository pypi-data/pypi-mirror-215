from unittest.mock import sentinel

import pytest
from pytest import raises

from packed import Packer, Resolver

from ._test_utils.steps import given, then, when


@pytest.fixture
def resolver():
    return Resolver()


@pytest.fixture
def packer(resolver):
    return Packer(resolver)


def test_pack(*, resolver, packer):
    with given:
        class CustomClass:
            def __packed__(self):
                return {}
        resolver.register(CustomClass)

    with when:
        actual = packer.pack(CustomClass())

    with then:
        assert isinstance(actual, bytes)


def test_pack_inherited(*, resolver, packer):
    with given:
        class ParentClass:
            def __packed__(self):
                return {}

        class ChildClass(ParentClass):
            pass

        resolver.register(ChildClass)

    with when:
        actual = packer.pack(ChildClass())

    with then:
        assert isinstance(actual, bytes)


def test_pack_unregistered(*, resolver, packer):
    with given:
        class CustomClass:
            def __packed__(self):
                return {}

    with when, raises(Exception) as exception:
        packer.pack(CustomClass())

    with then:
        assert exception.type is KeyError


def test_pack_without_packed_method(*, resolver, packer):
    with given:
        class CustomClass:
            pass
        resolver.register(CustomClass)

    with when, raises(Exception) as exception:
        packer.pack(CustomClass())

    with then:
        assert exception.type is AttributeError


def test_unpack(*, resolver, packer):
    with given:
        class CustomClass:
            def __packed__(self):
                return {}
        resolver.register(CustomClass)
        packed = packer.pack(CustomClass())

    with when:
        actual = packer.unpack(packed)

    with then:
        assert isinstance(actual, CustomClass)


def test_unpack_with_ext_resolver(*, resolver, packer):
    with given:
        class CustomClass:
            def __init__(self, *, injected):
                self._injected = injected

            def __packed__(self):
                return {}

        resolver.register(CustomClass)
        packed = packer.pack(CustomClass(injected=sentinel.injected))

        def resolver(cls, **kwargs):
            return cls(**kwargs, injected=sentinel.injected)

    with when:
        actual = packer.unpack(packed, {type(sentinel): None, CustomClass: resolver})

    with then:
        assert isinstance(actual, CustomClass)


def test_unpack_with_ext_resolvers(*, resolver, packer):
    with given:
        class ParentClass:
            pass

        class ChildClass(ParentClass):
            def __init__(self, *, injected):
                self._injected = injected

            def __packed__(self):
                return {}

        resolver.register(ChildClass)
        packed = packer.pack(ChildClass(injected=sentinel.injected))

        def resolver(cls, **kwargs):
            return cls(**kwargs, injected=sentinel.injected)

    with when:
        actual = packer.unpack(packed, {ParentClass: resolver})

    with then:
        assert isinstance(actual, ChildClass)


@pytest.mark.parametrize("value", [
    None,
    3.14,
    42,
    "banana",
    [],
    {},
    b"101010",
])
def test_unpack_native_types(value, *, packer):
    with given:
        packed = packer.pack(value)

    with when:
        actual = packer.unpack(packed)

    with then:
        assert actual == value
