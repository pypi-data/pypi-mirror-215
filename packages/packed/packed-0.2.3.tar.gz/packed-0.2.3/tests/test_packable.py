from unittest.mock import Mock, call

import pytest

from packed import Packable, Resolver

from ._test_utils.steps import given, then, when


@pytest.fixture
def resolver_():
    return Mock(Resolver)


def test_packable(*, resolver_):
    with given:
        packable = Packable(resolver_)

    with when:
        @packable
        class CustomClass:
            pass

    with then:
        assert resolver_.register.mock_calls == [call(cls=CustomClass)]


def test_packable_with_custom_name(*, resolver_):
    with given:
        packable = Packable(resolver_)

    with when:
        @packable("custom_name")
        class CustomClass:
            pass

    with then:
        assert resolver_.register.mock_calls == [call(cls=CustomClass, name="custom_name")]
