from typing import Iterable
from MarkLib.taskitem import TaskItem

class TaskStage:
    description: str = ""
    items: list[TaskItem] = []

    def __init__(self, staged_answers: Iterable):
        self.items = [item_class(answer=answer) for item_class, answer in zip(self.__class__.items, staged_answers)]