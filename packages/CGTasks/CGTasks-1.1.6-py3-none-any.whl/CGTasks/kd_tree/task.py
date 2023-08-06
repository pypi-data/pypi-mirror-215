from CGLib.algo.kd_tree_method import kd_tree
from CGLib.models.point import Point
from MarkLib.task import Task
from MarkLib.taskstage import TaskStage
from MarkLib.taskitem import TaskItem
from CGTasks.kd_tree.model import KdTree, KdTreeOrderedLists, KdTreePartitionTable, KdTreeSearchTable
from .builder import KdTreeModelBuilder


class KdTreeItemOrderedList(TaskItem):
    description = "Побудувати відсортований по X список."
    answer: KdTreeOrderedLists


class KdTreeItemPartition(TaskItem):
    description = "Рекурсивно розбити площину на прямокутники."
    answer: KdTreePartitionTable


class KdTreeStagePreprocessing(TaskStage):
    description = "Попередня обробка"
    items = [KdTreeItemOrderedList, KdTreeItemPartition]


class KdTreeItemTree(TaskItem):
    description = "Побудувати дерево пошуку."
    answer: KdTree


class KdTreeStageTree(TaskStage):
    description = "Побудувати дерево пошуку."
    items = [KdTreeItemTree]


class KdTreeItemSearch(TaskItem):
    description = "Здійснити пошук у дереві."
    answer: KdTreeSearchTable


class KdTreeStageSearch(TaskStage):
    description = "Здійснити пошук у дереві."
    items = [KdTreeItemSearch]


class KdTreeTask(Task):
    item_answer_builder = KdTreeModelBuilder
    description = "Метод kd-дерева"
    stages = [
        KdTreeStagePreprocessing,
        KdTreeStageTree,
        KdTreeStageSearch
    ]
    solution_method = kd_tree

    @property
    def unwrapped_condition(self):
        return [
            [Point(p.x, p.y) for p in self.condition.point_list],
            self.condition.region.x_range,
            self.condition.region.y_range
        ]
