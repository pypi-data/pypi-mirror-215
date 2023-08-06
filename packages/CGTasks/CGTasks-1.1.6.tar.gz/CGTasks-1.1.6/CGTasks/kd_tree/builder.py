from MarkLib.builder import ModelBuilder
from MarkLib.models.base import BinTreeNode, Point, Region
from .model import Intersection, KdTree, KdTreeInterscetionCell, KdTreeOrderedLists, KdTreePartitionCell, KdTreePartitionTableRow, KdTreePoint, KdTreePartitionTable, KdTreePointCell, KdTreeSearchTable, KdTreeSearchTableRow, KdTreeToAddCell, Partition, ToAddKdTree


class KdTreeModelBuilder(ModelBuilder):

    @classmethod
    def _build_methods(cls):
        return [
            cls._build_ordered_list,
            cls._build_partition_table,
            cls._build_tree,
            cls._build_search_table
        ]
    
    @staticmethod
    def _build_ordered_list(answer):
        return KdTreeOrderedLists(
            ordered_x=[KdTreePoint(x=p.x, y=p.y) for p in answer[0]],
            ordered_y=[KdTreePoint(x=p.x, y=p.y) for p in answer[1]]
        )
    
    @staticmethod
    def _build_partition_table(answer):
        partition = lambda x: Partition.vertical if x else Partition.horizontal
        rows = [
            KdTreePartitionTableRow(cells=(
                KdTreePointCell(content=KdTreePoint(x=row[0].x, y=row[0].y)),
                KdTreePartitionCell(content=partition(row[1]))
            ))
            for row in answer
        ]

        return KdTreePartitionTable(rows=rows)
    
    @staticmethod
    def _build_tree(answer):
        return KdTree(
            nodes=[
                BinTreeNode(
                    data=Point(x=node[0].x, y=node[0].y),
                    left=Point(x=node[1].x, y=node[1].y) if node[1] else None,
                    right=Point(x=node[2].x, y=node[2].y) if node[2] else None
                )
                for node in answer.nodes
            ],
            region=Region(x_range=answer.x_range, y_range=answer.y_range)
        )
    
    @staticmethod
    def _build_search_table(answer):
        to_add = lambda x: ToAddKdTree.yes if x else ToAddKdTree.no
        intersection = lambda x: Intersection.yes if x else Intersection.no
        rows = [
            KdTreeSearchTableRow(cells=(
                KdTreePointCell(content=KdTreePoint(x=row[0].x, y=row[0].y)),
                KdTreeToAddCell(content=to_add(row[1])),
                KdTreeInterscetionCell(content=intersection(row[2]))
            ))
            for row in answer
        ]

        return KdTreeSearchTable(rows=rows)
