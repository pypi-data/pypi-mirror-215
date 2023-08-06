from typing import Any
from pydantic import BaseModel


class TaskItem(BaseModel):
    description: str = ""
    answer: Any
