from MarkLib.models.base import Point, HeaderTable, TableCell, TableRow, PointList
from enum import Enum
from pydantic import BaseModel


class GrahamPoint(Point):
    pass

class Point(BaseModel):
    x: float = 0
    y: float = 0

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Point) and
            isclose(self.x, other.x, abs_tol=1e-3) and
            isclose(self.y, other.y, abs_tol=1e-3)
        )


class GrahamPointList(PointList):
    pass


class GrahamTrinityCell(TableCell):
    content: "tuple[Point, Point, Point]"


class PiCompare(str, Enum):
    less = "less"
    more = "more"


class GrahamPiCompareCell(TableCell):
    content: PiCompare


class GrahamCenterPointCell(TableCell):
    content: GrahamPoint


class ToAddGraham(str, Enum):
    yes = "yes"
    no = "no"


class GrahamToAddCell(TableCell):
    content: ToAddGraham


class GrahamTableRow(TableRow):
    cells: "tuple[GrahamTrinityCell, GrahamPiCompareCell, GrahamCenterPointCell, GrahamToAddCell]"


class GrahamTable(HeaderTable):
    rows: "list[GrahamTableRow]"
    headers: "tuple[str, str, str, str]" = ('', '', '', '')
