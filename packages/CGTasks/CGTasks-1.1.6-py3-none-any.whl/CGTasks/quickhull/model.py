from typing import Optional
from pydantic import BaseModel
from MarkLib.models.base import BinTree, BinTreeNode, Point


class QuickhullPoint(Point):
    pass


class QuickhullInitialPartition(BaseModel):
    min_point: QuickhullPoint
    max_point: QuickhullPoint
    s1: "list[QuickhullPoint]"
    s2: "list[QuickhullPoint]"


class QuickhullNodeData(BaseModel):
    points: "list[QuickhullPoint]"
    h: Optional[QuickhullPoint]
    hull_piece: "list[QuickhullPoint]"


class QuickhullTreeNode(BinTreeNode):
    data: QuickhullNodeData
    left: Optional[QuickhullNodeData]
    right: Optional[QuickhullNodeData]


class QuickhullTree(BinTree):
    nodes: "list[QuickhullTreeNode]"

    @property
    def leaves(self):
        return [n for n in self.nodes if n.left is None and n.right is None]


class QuickhullPartition(BaseModel):
    initial_partition: QuickhullInitialPartition
    tree: QuickhullTree
