from __future__ import annotations

import copy
import json
from dataclasses import Field, asdict, dataclass, field, fields, is_dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Generic,
    Iterable,
    NoReturn,
    Optional,
    Protocol,
    Sequence,
    TypeVar,
    cast,
    overload,
)


from tensordict import TensorDictBase
from tensordict import tensorclass as tensorclass_wrap
from torch import Size
from torch import device as Device
from typing_extensions import Self, dataclass_transform

__all__ = []


class DataclassInstance(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


Dataclass = TypeVar("Dataclass", bound=DataclassInstance)
DataclassType = TypeVar("DataclassType", bound=type[DataclassInstance])


def read_fields(cls) -> Iterable[str]:
    """
    Reads the names of all fields of a dataclass that are (a subclass of) one of the given types.
    """
    yield from (f.name for f in fields(cls))


def to_dict(self: DataclassInstance) -> dict[str, Any]:
    if not is_dataclass(self):
        raise TypeError(f"Expected dataclass, got {type(self)}")
    return asdict(self)


def to_json(self: DataclassInstance, **json_dumps_kwargs) -> str:
    # Note: cannot use __dict__ as this does not cover the case of nested dataclasses and slots
    # data = {f.name: getattr(self, f.name) for f in fields(self)}
    # for key in data.keys():
    #     value = data[key]
    #     if is_dataclass(value):
    #         data[key] = to_json(value)
    data = to_dict(self)
    return json.dumps(data, **json_dumps_kwargs)


def from_dict(cls: type[Dataclass], data: dict) -> Dataclass:
    if not is_dataclass(cls):
        raise TypeError(f"Expected dataclass, got {type(cls)}")
    anns = {f.name: f for f in fields(cls)}
    for key in data.keys():
        ann = anns[key]
        if isinstance(ann.type, type) and is_dataclass(ann.type):
            data[key] = from_dict(ann.type, data[key])
    return cls(**data)  # type: ignore


def from_json(cls: type[Dataclass], src: str) -> Dataclass:
    data = json.loads(src)
    if not isinstance(data, dict):
        raise ValueError(f"Expected dict, got {type(data)}")
    return from_dict(cls, data)


class serializable(Generic[DataclassType]):
    """
    Decorator and registry for serialiable dataclasses.

    Use as a decorator to add to/from json/dict methods.
    Use as a function to get a registry object that can be used to decorate
    dataclasses as either source or target for serialization.
    """

    @overload
    def __new__(cls, cls_decorated: DataclassType, /) -> DataclassType:
        ...

    @overload
    def __new__(cls, cls_decorated: None = None, /) -> serializable:
        ...

    def __new__(cls, cls_decorated: Optional[DataclassType] = None, /):
        self = super().__new__(cls)
        if cls_decorated is not None:
            return self(cls_decorated)
        return self

    def __init__(self):
        self._targets = set()

    def __len__(self):
        return len(self._targets)

    def __iter__(self):
        return iter(self._targets)

    def __contains__(self, other):
        return other in self._targets

    def target(self, cls: type[Dataclass]) -> type[Dataclass]:
        self._targets.add(cls)

        return self(cls)

    def _target_from_dict(self, data: dict) -> DataclassInstance:
        for cls in self._targets:
            try:
                return from_dict(cls, data)
            except (KeyError, TypeError, ValueError):
                pass
        raise TypeError(f"None of {self._targets} can be deserialized from {data}")

    def _target_from_json(self, src: str) -> DataclassInstance:
        data = json.loads(src)
        return self._target_from_dict(data)

    def source(self, cls: type[Dataclass]) -> type[Dataclass]:
        if not is_dataclass(cls):
            raise TypeError(f"Expected dataclass, got {type(cls)}")

        cls.from_dict = staticmethod(self._target_from_dict)
        cls.from_json = staticmethod(self._target_from_json)

        init_subclass = cls.__init_subclass__

        def __init_subclass__(cls, **kwargs):
            init_subclass(**kwargs)
            self._targets.add(cls)

        return cls

    def __call__(self, cls: type[Dataclass]) -> type[Dataclass]:
        if not is_dataclass(cls):
            raise TypeError(f"Expected dataclass, got {type(cls)}")

        cls.from_dict = classmethod(from_dict)
        cls.from_json = classmethod(from_json)
        cls.to_dict = to_dict
        cls.to_json = to_json

        return cls


if TYPE_CHECKING:

    @dataclass()
    class TensorclassTypeMixin(TensorDictBase):
        batch_size: Sequence[int] | Size = field(kw_only=True)
        device: Device | str | None = field(kw_only=True)

        def __init_subclass__(cls) -> None:
            cls.__annotations__["batch_size"] = Sequence[int] | Size
            cls.__annotations__["device"] = Device | str | None

            return super().__init_subclass__()

        def __new__(cls, *args, **kwargs) -> NoReturn:
            raise TypeError(f"Cannot instantiate {cls.__name__} directly")

else:
    TensorclassTypeMixin = object


Tensorclass = TypeVar("Tensorclass", bound=TensorclassTypeMixin)


@dataclass_transform()
def tensorclass(cls: type[Tensorclass]) -> type[Tensorclass]:
    """
    Extends the ``tensorclass`` function provided by the ``tensordict`` package
    to support a type mixin that imporves the developer experience.

    The type mixin is removed in this decorator, such that the resulting class
    acts like a canonical tensorclass at runtime.
    """
    # # Remove the type mixin from the mro
    # # This involves also removing all parent classes of the type mixin
    # # that are not in the mro of the original class.
    # cls_mro = tuple(c for c in cls.__mro__ if c is object or c not in TensorclassTypeMixin.__mro__)

    # assert len(cls_mro) > 1, "Expected at least one parent class"
    # assert cls_mro[0] is cls, "Expected the original class to be the first parent class"

    # # Create a bare class with the same name and dict
    # cls_bare = type(cls.__name__, cls_mro, dict(cls.__dict__))

    # Wrap the bare class with the tensorclass decorator
    cls_wrap = tensorclass_wrap(cls)  # type: ignore

    # Cast it to the original type
    return cast(type[Tensorclass], cls_wrap)
