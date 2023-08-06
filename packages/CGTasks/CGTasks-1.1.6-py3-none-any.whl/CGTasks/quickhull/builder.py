from MarkLib.builder import ModelBuilder
from .model import QuickhullInitialPartition, QuickhullNodeData, QuickhullPartition, QuickhullPoint, QuickhullTree, QuickhullTreeNode


class QuickhullModelBuilder(ModelBuilder):
    @classmethod
    def _build_methods(cls):
        return [
            cls._build_partition,
            cls._build_tree
        ]
    
    @staticmethod
    def _build_partition(answer):
        initial_partition = QuickhullInitialPartition(
            min_point=QuickhullPoint(x=answer[0].x, y=answer[0].y),
            max_point=QuickhullPoint(x=answer[1].x, y=answer[1].y),
            s1=[QuickhullPoint(x=p.x, y=p.y) for p in answer[2]],
            s2=[QuickhullPoint(x=p.x, y=p.y) for p in answer[3]]
        )

        return QuickhullPartition(
            initial_partition=initial_partition,
            tree=QuickhullModelBuilder._build_tree(answer[4])
        )
    
    @staticmethod
    def _build_tree(answer):
        return QuickhullTree(nodes=[
            QuickhullTreeNode(
                data=QuickhullNodeData(
                    points=[QuickhullPoint(x=p.x, y=p.y) for p in node[0].points],
                    h=QuickhullPoint(x=node[0].h.x, y=node[0].h.y) if node[0].h else None,
                    hull_piece=[QuickhullPoint(x=p.x, y=p.y) for p in node[0].hull_piece]
                ),
                left=QuickhullNodeData(
                    points=[QuickhullPoint(x=p.x, y=p.y) for p in node[1].points],
                    h=QuickhullPoint(x=node[1].h.x, y=node[1].h.y) if node[1].h else None,
                    hull_piece=[QuickhullPoint(x=p.x, y=p.y) for p in node[1].hull_piece]
                ) if node[1] else None,
                right=QuickhullNodeData(
                    points=[QuickhullPoint(x=p.x, y=p.y) for p in node[2].points],
                    h=QuickhullPoint(x=node[2].h.x, y=node[2].h.y) if node[2].h else None,
                    hull_piece=[QuickhullPoint(x=p.x, y=p.y) for p in node[2].hull_piece]
                ) if node[2] else None,
            )
            for node in answer.nodes
        ])
