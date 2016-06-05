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

    def __init__(self, text, values):
        self.text = text
        self.min = int(values[0])
        self.max = int(values[1])
        self.step = int(values[2])


class OpenQuestion(Question):
    def __init__(self, text):
        self.text = text
