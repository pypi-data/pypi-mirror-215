from CGLib.algo.graham import graham
from CGLib.models.point import Point
from MarkLib.task import Task
from MarkLib.taskstage import TaskStage
from MarkLib.taskitem import TaskItem
from CGTasks.graham.model import GrahamPoint, GrahamPointList, GrahamTable
from .builder import GrahamModelBuilder


class GrahamItemInternalPoint(TaskItem):
    description = "Задана множина S із N точок на площині. Знайти внутрішню точку q."
    answer: GrahamPoint


class GrahamStageInternalPoint(TaskStage):
    description = "Задана множина S із N точок на площині. Знайти внутрішню точку q."
    items = [GrahamItemInternalPoint]


class GrahamItemOrderedList(TaskItem):
    description = "Використовуючи q як початок координат, побудувати упорядкований за полярним кутом список точок множини S, починаючи із точки \"початок\" проти годинникової стрілки."
    answer: GrahamPointList


class GrahamStageOrderedList(TaskStage):
    description = "Використовуючи q як початок координат, побудувати упорядкований за полярним кутом список точок множини S, починаючи із точки \"початок\" проти годинникової стрілки."
    items = [GrahamItemOrderedList]


class GrahamItemOriginPoint(TaskItem):
    description = "Знайти точку \"початок\"."
    answer: GrahamPoint


class GrahamStageOriginPoint(TaskStage):
    description = "Знайти точку \"початок\"."
    items = [GrahamItemOriginPoint]


class GrahamItemLookup(TaskItem):
    description = "Організувати обхід."
    answer: GrahamTable


class GrahamStageLookup(TaskStage):
    description = "Організувати обхід."
    items = [GrahamItemLookup]


class GrahamTask(Task):
    item_answer_builder = GrahamModelBuilder
    description = "Метод Грехема"
    stages = [
        GrahamStageInternalPoint,
        GrahamStageOrderedList,
        GrahamStageOriginPoint,
        GrahamStageLookup
    ]
    solution_method = graham

    @property
    def unwrapped_condition(self):
        return [[Point(p.x, p.y) for p in self.condition.point_list]]
