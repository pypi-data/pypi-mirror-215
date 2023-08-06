from typing import Callable
from MarkLib.task import Task


class ModelBuilder:
    
    @classmethod
    def build(cls, raw_answers) -> None:
        pairs = zip(cls._build_methods(), raw_answers)
        return (method(answer) for method, answer in pairs)
