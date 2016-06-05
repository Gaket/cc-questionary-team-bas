import json
import time
import hashlib
from app.model.question import NumericQuestion
from app.model.question import MultipleAnswersQuestion
from app.model.question import OpenQuestion


class Survey:
    def __init__(self, questionsAddr):
        self.hash = str(int(time.time())).__hash__()
        self.questions = getQuestions(questionsAddr)


def getQuestions(questionsAddr):
    # Parse JSON to get data and return list of questions (childs of Question)
    with open(questionsAddr) as questions_file:
        questions = json.load(questions_file)['questions']
        q = list()
        for question in questions:
            if question["archived"]:
                pass
            if question["type"] == "num":
                q.append(NumericQuestion(**question))
            elif question["type"] == "mult":
                q.append(MultipleAnswersQuestion(**question))
            elif question["type"] == "open":
                q.append(OpenQuestion(**question))
            else:
                print("Type error")
    return q
