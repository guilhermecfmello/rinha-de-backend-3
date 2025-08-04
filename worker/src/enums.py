from enum import Enum


class ProcessorType(str, Enum):
    DEFAULT = "default"
    FALLBACK = "fallback"
    ERROR = "error"