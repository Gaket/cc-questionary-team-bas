from array import array


class Question:
    def __init__(self):
        id = -1
        text = ''


class MultipleAnswersQuestion(Question):
    variants = []

    def __init__(self, text, variants):
        self.text = text
        self.variants = self.variants


class NumericQuestion(Question):
    def __init__(self, text, min, max, step):
        self.text = text
        self.min = int(min)
        self.max = int(max)
        self.step = int(step)


class OpenQuestion(Question):
    def __init__(self, text):
        self.text = text
