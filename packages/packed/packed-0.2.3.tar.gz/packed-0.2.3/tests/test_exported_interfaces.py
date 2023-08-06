from packed import pack, packable, unpack

from ._test_utils.steps import given, then, when


def test_exported_interfaces():
    with given:
        @packable
        class CustomClass:
            def __packed__(self):
                return {}
        packed = pack(CustomClass())

    with when:
        actual = unpack(packed)

    with then:
        assert isinstance(actual, CustomClass)
