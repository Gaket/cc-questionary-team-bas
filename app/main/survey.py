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
        questions = json.load(questions_file)
        q = dict()
        for key in questions:
            if questions[key]["archived"]:
                pass
            if questions[key]["type"] == "num":
                q[key] = NumericQuestion(**questions[key])
            elif questions[key]["type"] == "mult":
                q[key] = MultipleAnswersQuestion(**questions[key])
            elif questions[key]["type"] == "open":
                q[key] = OpenQuestion(**questions[key])
            else:
                print("Type error")
    return q
