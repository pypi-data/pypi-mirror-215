from functools import partial
from MarkLib.grader import Grader, iterable_grading
from MarkLib.markdata import MarkData, ItemMarkData
from .model import KdTree, KdTreeOrderedLists, KdTreePartitionTable, KdTreeSearchTable


iterable025 = partial(iterable_grading, sub=0.25)
iterable1 = partial(iterable_grading, sub=1.0)


def grade_ordered_lists(correct: KdTreeOrderedLists, answer: KdTreeOrderedLists):
    return (
        iterable025(correct.ordered_x, answer.ordered_x) +
        iterable025(correct.ordered_y, answer.ordered_y)
    )


def grade_partition_table(correct: KdTreePartitionTable, answer: KdTreePartitionTable):
    return iterable_grading(correct.rows, answer.rows, sub=0.75)


def grade_search_tree(correct: KdTree, answer: KdTree):
    return iterable1(correct.nodes, answer.nodes)


def grade_search_table(correct: KdTreeSearchTable, answer: KdTreeSearchTable):
    return iterable1(correct.rows, answer.rows)


ordered_lists = ItemMarkData(max_mark=0.25)
partition_table = ItemMarkData(max_mark=0.75)
search_tree = ItemMarkData(max_mark=1)
search_table = ItemMarkData(max_mark=1)


class KdTreeGrader(Grader):
    markdata = MarkData(items=[ordered_lists, partition_table, search_tree, search_table])
    item_grading_methods = [
        grade_ordered_lists,
        grade_partition_table,
        grade_search_tree,
        grade_search_table
    ]
