from CGLib.algo.quickhull import quickhull
from CGLib.models.point import Point
from MarkLib.task import Task
from MarkLib.taskitem import TaskItem
from MarkLib.taskstage import TaskStage
from CGTasks.quickhull.model import QuickhullPartition, QuickhullTree
from .builder import QuickhullModelBuilder


class QuickhullItemPartition(TaskItem):
    description = "Здійснити розбиття. Подати у вигляді дерева."
    answer: QuickhullPartition


class QuickhullStagePartition(TaskStage):
    description = "Здійснити розбиття. Подати у вигляді дерева."
    items = [QuickhullItemPartition]


class QuickhullItemMerge(TaskItem):
    description = "Злиття. Рекурсивний підйом, результат - конкатенація списків. Починаючи із листків дерева, рекурсивно конкатенуємо упорядковані за годинниковою стрілкою списки."
    answer: QuickhullTree


class QuickhullStageMerge(TaskStage):
    description = "Злиття. Рекурсивний підйом, результат - конкатенація списків. Починаючи із листків дерева, рекурсивно конкатенуємо упорядковані за годинниковою стрілкою списки."
    items = [QuickhullItemMerge]


class QuickhullTask(Task):
    item_answer_builder = QuickhullModelBuilder
    description = "Метод Швидкобол"
    stages = [QuickhullStagePartition, QuickhullStageMerge]
    solution_method = quickhull

    @property
    def unwrapped_condition(self):
        return [[Point(p.x, p.y) for p in self.condition.point_list]]
