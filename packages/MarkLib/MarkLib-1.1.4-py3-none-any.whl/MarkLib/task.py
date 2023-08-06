from typing import Callable
from MarkLib.taskstage import TaskStage
from MarkLib.taskitem import TaskItem
from .models.condition import Condition
from pydantic import create_model


class Task:
    description: str = ""
    stages: list[TaskStage] = []
    solution_method: Callable = None
    item_answer_builder = None

    def __init__(self, condition: Condition):
        self.condition = condition
        raw_answers = self.__class__.solution_method(*self.unwrapped_condition)
        answers = self.item_answer_builder.build(raw_answers)
        self.stages = [
            stage_class(answers) 
            for stage_class
            in self.__class__.stages
        ]

    @property
    def items(self) -> list[TaskItem]:
        return [item for stage in self.stages for item in stage.items]

    @property
    def answers(self):
        return [item.answer for item in self.items]

    @classmethod
    def answer_schema(cls):
        item_classes = [
            item_class
            for stage_class in cls.stages 
            for item_class in stage_class.items
        ]
        item_dataclasses = [
            item_class.__annotations__.get("answer", None) 
            for item_class 
            in item_classes
        ]
        d = {
            item_class.__name__: (item_dataclass, None) 
            for item_class, item_dataclass
            in zip(item_classes, item_dataclasses)
        }
        return create_model(f"{cls.__name__}Model", **d).schema()

