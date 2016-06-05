from array import array


class Question:
    def __init__(self, **params):
        self.id = params['id']
        self.text = params['text']
        self.key = params['key']


class MultipleAnswersQuestion(Question):
    def __init__(self, **params):
        super().__init__(**params)
        self.type = 'mult'
        self.variants = params['variants']


class NumericQuestion(Question):
    def __init__(self, **params):
        super().__init__(**params)
        self.min = int(params['variants'][0])
        self.max = int(params['variants'][1])
        self.step = int(params['variants'][2])
        self.type = 'num'


class OpenQuestion(Question):
    def __init__(self, **params):
        super().__init__(**params)
        self.type = 'open'
