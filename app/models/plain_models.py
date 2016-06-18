class Question:
    def __init__(self):
        id = -1


class MultipleAnswersQuestion(Question):
    variants = []

    def __init__(self, text, variants):
        self.text = text
        self.type = 'mult'
        self.variants = variants


class NumericQuestion(Question):
    def __init__(self, text, min, max, step):
        self.text = text
        self.min = int(min)
        self.max = int(max)
        self.step = int(step)
        self.type = 'num'

    def __init__(self, text, values):
        self.text = text
        self.min = int(values[0])
        self.max = int(values[1])
        self.step = int(values[2])
        self.type = 'num'


class OpenQuestion(Question):
    def __init__(self, text):
        self.type = 'open'
        self.text = text


class Answer:
    def __init__(self):
        question_id = -1


class MultipleAnswersAnswer(Answer):
    def __init__(self):
        variants = []


class NumericAnswer(Answer):
    def __init__(self):
        min = 1
        max = 10
        step = 1


class OpenAnswer(Answer):
    def __init__(self):
        text = ''
