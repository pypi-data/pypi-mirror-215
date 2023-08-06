__all__ = [
    "Walker",
    "WalkerMeta",
]

import enum
import dataclasses

from . import dispatcher


class WalkerMeta(dispatcher.DispatcherMeta):
    pass


class GenericPath:
    def __init__(self, path):
        self.__path = path
        return super().__init__()

    def __str__(self):
        return self.__path.__str__()

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self)})"

    @property
    def path(self):
        return self.__path


class IndexPath(GenericPath):
    def __str__(self):
        return f"[{self.path}]"


class AttributePath(GenericPath):
    def __str__(self):
        return f".{self.path}]"


class HashPath(GenericPath):
    def __str__(self):
        return f"{{{self.path}}}"


class Walker(dispatcher.Dispatcher, metaclass=WalkerMeta):
    @dispatcher.Hook(tuple, list)
    def dispatch_ordered_sequence(self, instance):
        for (index, item) in enumerate(instance):
            yield (item, instance, index, IndexPath)
            yield from self(item)

    @dispatcher.Hook(set, frozenset)
    def dispatch_unordered_sequence(self, instance):
        for item in instance:
            yield (item, instance, item, HashPath)
            yield from self(item)

    @dispatcher.Hook(dataclasses.is_dataclass)
    def dispatch_dataclass(self, instance):
        for field in dataclasses.fields(instance):
            key = field.name
            value = getattr(instance, key)
            yield (value, instance, key, AttributePath)
            yield from self(value)

    @dispatcher.Hook(dict)
    def dispatch_mapping(self, instance):
        for (key, value) in instance.items():
            yield (key, instance, key, HashPath)
            yield from self(key)
            yield (value, instance, key, IndexPath)
            yield from self(value)

    @dispatcher.Hook(object)
    def dispatch_object(self, instance, path=()):
        yield from ()
