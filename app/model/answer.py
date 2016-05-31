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

class OpenQuestion(Answer):
    def __init__(self):
        text = ''
