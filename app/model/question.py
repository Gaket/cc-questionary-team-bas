from array import array


class Question:
    def __init__(self):
        id = -1
        text = ''


class MultipleAnswersQuestion(Question):
    def __init__(self):
        variants = []


class NumericQuestion(Question):
    def __init__(self):
        min = 1
        max = 10
        step = 1


class OpenQuestion(Question):
    pass