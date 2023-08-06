from typing import Callable, Iterable
from collections import Counter
from itertools import cycle
from MarkLib.markdata import MarkData, Mistake


def default_grading(correct, answer, sub=0.0):
    return [] if correct == answer else [Mistake(sub=sub)]


def iterable_grading(correct: Iterable, answer: Iterable, sub=0.0, big_sub=0.0, item_grading=default_grading):
    diff = len(correct) - len(answer)
    extra = [
        Mistake(sub=sub, big_sub=big_sub, data="Too many items")
        for _ in range(-diff)
    ] if diff < 0 else [
        Mistake(sub=sub, big_sub=big_sub, data="Too few items")
        for _ in range(diff)
    ]

    return [
        Mistake(sub=sub, big_sub=big_sub)
        for c, a in zip(correct, answer)
        if item_grading(c, a) != []
    ] + extra


def mistakes_sub_pairs(mistakes):
    counter = Counter(mistakes)
    return {
        mistake: mistake.big_sub if mistake.systematic and count > 1 else mistake.sub
        for mistake, count
        in counter.items()
    }


class Grader:
    markdata: MarkData
    item_grading_methods: Iterable[Callable] = cycle([default_grading])

    @classmethod
    def grade(cls, correct, answer):
        mistakes = [
            method(correct_stage, answer_stage)
            for method, correct_stage, answer_stage 
            in zip(cls.item_grading_methods, correct, answer)
        ]

        by_items = list(zip(cls.markdata.items, mistakes))

        by_items_counter = [
            (stage, mistakes_sub_pairs(mistakes))
            for stage, mistakes
            in by_items
        ]

        marks_per_item = [
            (item, max(item.min_mark, item.max_mark - sum(counter.values())))
            for item, counter
            in by_items_counter
        ]

        mark = sum(mark for item, mark in marks_per_item)

        return mark, marks_per_item
