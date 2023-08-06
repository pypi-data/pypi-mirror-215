from enum import Enum
from pydantic import BaseModel
from MarkLib.models.base import BinTree, HeaderTable, Point, Region, TableCell, TableRow


class KdTreePoint(Point):
    pass


class KdTreeOrderedLists(BaseModel):
    ordered_x: "list[KdTreePoint]"
    ordered_y: "list[KdTreePoint]"


class KdTree(BinTree):
    region: Region


class Partition(str, Enum):
    vertical = "vertical"
    horizontal = "horizontal"


class ToAddKdTree(str, Enum):
    yes = "yes"
    no = "no"


class Intersection(str, Enum):
    yes = "yes"
    no = "no"


class KdTreePointCell(TableCell):
    content: KdTreePoint


class KdTreePartitionCell(TableCell):
    content: Partition


class KdTreeToAddCell(TableCell):
    content: ToAddKdTree


class KdTreeInterscetionCell(TableCell):
    content: Intersection


class KdTreePartitionTableRow(TableRow):
    cells: "tuple[KdTreePointCell, KdTreePartitionCell]"


class KdTreeSearchTableRow(TableRow):
    cells: "tuple[KdTreePointCell, KdTreeToAddCell, KdTreeInterscetionCell]"


class KdTreePartitionTable(HeaderTable):
    rows: "list[KdTreePartitionTableRow]"
    headers: "tuple[str, str]" = ('', '')    


class KdTreeSearchTable(HeaderTable):
    rows: "list[KdTreeSearchTableRow]"
    headers: "tuple[str, str, str]" = ('', '', '')
