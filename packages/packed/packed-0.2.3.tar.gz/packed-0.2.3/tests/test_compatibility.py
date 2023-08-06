from packed import Packer, Resolver

from ._test_utils.steps import given, then, when


class CustomClassV1:
    def __init__(self, field):
        self.field = field

    def __packed__(self):
        return {"field": self.field}

    @classmethod
    def __unpacked__(cls, *, field, **kwargs):
        return cls(field)


class CustomClassV2:
    def __init__(self, field, new_field=None):
        self.field = field
        self.new_field = new_field

    def __packed__(self):
        return {"field": self.field, "new_field": self.new_field}

    @classmethod
    def __unpacked__(cls, *, field, new_field=None, **kwargs):
        return cls(field, new_field)


def test_backward_compatibility():
    with given:
        client_resolver = Resolver()
        client_resolver.register(CustomClassV1, "custom_class")
        client_packer = Packer(client_resolver)

        server_resolver = Resolver()
        server_resolver.register(CustomClassV2, "custom_class")
        server_packer = Packer(server_resolver)

        packed = client_packer.pack(CustomClassV1("value"))

    with when:
        actual = server_packer.unpack(packed)

    with then:
        assert actual.field == "value"


def test_forward_compatibility():
    with given:
        client_resolver = Resolver()
        client_resolver.register(CustomClassV2, "custom_class")
        client_packer = Packer(client_resolver)

        server_resolver = Resolver()
        server_resolver.register(CustomClassV1, "custom_class")
        server_packer = Packer(server_resolver)

        packed = client_packer.pack(CustomClassV2("value"))

    with when:
        actual = server_packer.unpack(packed)

    with then:
        assert actual.field == "value"
