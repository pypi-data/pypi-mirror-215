from functools import partial
from MarkLib.grader import Grader, default_grading, iterable_grading
from MarkLib.markdata import MarkData, ItemMarkData, Mistake
from .model import GrahamPointList, GrahamTable, PiCompare


default025 = partial(default_grading, sub=0.25)
iterable025 = partial(iterable_grading, sub=0.25)


def ordered_grading(correct: GrahamPointList, answer: GrahamPointList):
    return iterable025(correct.points, answer.points)


def steps_table_grading(correct: GrahamTable, answer: GrahamTable):
    """"
    row.cells[0] - points' triple
    row.cells[1] - less/more than pi (True/False)
    row.cells[2] - center point
    row.cells[3] - add/delete the point (True/False)
    """
    mistakes = []
    correct_triples = [row.cells[0] for row in correct.rows]
    answer_triples = [row.cells[0] for row in answer.rows]
    correct_angles = [row.cells[1] for row in correct.rows]
    answer_angles = [row.cells[1] for row in answer.rows]
    correct_less_than_pi = [
        (row.cells[1], row.cells[3], correct.rows[i+1].cells[0])
        for i, row in enumerate(correct.rows[:-1])
        if row.cells[1].content == PiCompare.less
    ]
    answer_less_than_pi = [
        (row.cells[1], row.cells[3], correct.rows[i+1].cells[0])
        for i, row in enumerate(answer.rows[:-1])
        if row.cells[1].content == PiCompare.less
    ]
    correct_more_than_pi = [
        (row.cells[1], row.cells[3], correct.rows[i+1].cells[0])
        for i, row in enumerate(correct.rows[:-1])
        if row.cells[1].content == PiCompare.more
    ]
    answer_more_than_pi = [
        (row.cells[1], row.cells[3], correct.rows[i+1].cells[0])
        for i, row in enumerate(answer.rows[:-1])
        if row.cells[1].content == PiCompare.more
    ]
    mistakes_last = [
        Mistake(sub=0.25)
        for row in answer.rows
        if row.cells[0].content[1] == answer.rows[0].cells[0].content[0]
    ] + ([Mistake(sub=0.25)] if answer.rows[-1] != correct.rows[-1] else [])

    mistakes.extend(iterable_grading(correct_triples, answer_triples, sub=0.15))
    mistakes.extend(iterable_grading(correct_angles, answer_angles, sub=0.15))
    mistakes.extend(iterable_grading(correct_less_than_pi, answer_less_than_pi, sub=0.25))
    mistakes.extend(iterable_grading(correct_more_than_pi, answer_more_than_pi, sub=0.3, big_sub=0.6))
    mistakes.extend(mistakes_last)

    return mistakes


internal_point = ItemMarkData(max_mark=0.25)
ordered = ItemMarkData(max_mark=0.25)
origin = ItemMarkData(max_mark=0.25)
steps_table = ItemMarkData(max_mark=1.25)


class GrahamGrader(Grader):
    markdata = MarkData(items=[internal_point, ordered, origin, steps_table])
    item_grading_methods = [default025, ordered_grading, default025, steps_table_grading]
