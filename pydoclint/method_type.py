from enum import Enum, auto


class MethodType(Enum):
    INSTANCE_METHOD = auto()
    CLASS_METHOD = auto()
    STATIC_METHOD = auto()
