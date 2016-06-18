from app.main.const import QUESTIONS_TO_SHOW
from app.model.db.models import QuestionEn, AnswerNum
from app.model.db.models import AnswerEn
from app import db
from app.main.survey import getQuestionsFromJSON

qDict = getQuestionsFromJSON("../app/data/questions.json", "en", [1,2,3,4,5,6,7])
for elem in qDict:
    q = QuestionEn(elem, qDict[elem].type, qDict[elem].text)
    db.session.add(q)
    if q.type == "mult":
        for variant in qDict[elem].variants:
            v = AnswerEn(variant, q.id)
            db.session.add(v)
    elif qDict[elem].type == "num":
        v = AnswerNum(qDict[elem].min, qDict[elem].max, qDict[elem].step, q.id)
        db.session.add(v)
    db.session.commit()


