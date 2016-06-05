import json
from app.model.question import NumericQuestion
from app.model.question import MultipleAnswersQuestion
from app.model.question import OpenQuestion

class Survey:
    def __init__(self, questionsAddr):
        self.questions = getQuestions(questionsAddr)

def getQuestions(questionsAddr):
    # Parse JSON to get data and return list of questions (childs of Question)
    with open(questionsAddr) as questions_file:
        questions = json.load(questions_file)
        questions_list = []
        for key in questions:
            text = questions[key]["text"]
            variants = questions[key]["variants"]
            if questions[key]["type"] == "num":
                q = NumericQuestion(text, variants)
            elif questions[key]["type"] == "mult":
                q = MultipleAnswersQuestion(text, variants)
            elif questions[key]["type"] == "open":
                q = OpenQuestion(text)
            else:
                print("Type error")
            questions_list.append(q)
    return questions_list
