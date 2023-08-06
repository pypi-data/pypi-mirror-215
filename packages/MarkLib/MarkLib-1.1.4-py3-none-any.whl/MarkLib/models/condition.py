from pydantic import BaseModel
from MarkLib.models.base import Point, Graph, Region


class Condition(BaseModel):
    pass


class GraphAndPointCondition(Condition):
    graph: Graph
    point: Point


class PointListCondition(Condition):
    point_list: list[Point]


class PointListAndRegionCondition(PointListCondition):
    region: Region
