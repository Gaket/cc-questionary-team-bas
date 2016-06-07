import codecs
import json
import time
from app.model.question import NumericQuestion
from app.model.question import MultipleAnswersQuestion
from app.model.question import OpenQuestion

class Survey:
    def __init__(self, questionsAddr, lang, question_numbers):
        self.hash = str(int(time.time())).__hash__()
        self.questions = getQuestions(questionsAddr, lang, question_numbers)

def getQuestions(questionsAddr, lang, question_numbers):
    # Parse JSON to get data and return list of questions (childs of Question)
    with open(questionsAddr) as questions_file:
        questions = json.load(codecs.open(questionsAddr, 'r', 'utf-8-sig'))
        q = dict()
        for key in questions:
            if int(key) in question_numbers:
                text = questions[key][lang]["text"]
                variants = questions[key][lang]["variants"]
                if questions[key]["type"] == "num":
                    q[key] = NumericQuestion(text, variants)
                elif questions[key]["type"] == "mult":
                    q[key] = MultipleAnswersQuestion(text, variants)
                elif questions[key]["type"] == "open":
                    q[key] = OpenQuestion(text)
                else:
                    print("Type error")
    return q
