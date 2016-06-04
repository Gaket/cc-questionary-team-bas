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
            type = questions[key][0]
            text = questions[key][1]
            values = questions[key][2]
            if type == "numeric":
                q = NumericQuestion(text, values[0], values[1], values[2])
            elif type == "mult":
                values_list = []
                for value in values:
                    values_list.append(value)
                q = MultipleAnswersQuestion(text, values_list)
            elif type == "open":
                q = OpenQuestion(text)
            else:
                print("Type error")
            questions_list.append(q)
    return questions_list

print(getQuestions("..\data\questions.json"))
