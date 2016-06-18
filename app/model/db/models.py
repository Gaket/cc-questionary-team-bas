from app import db


class QuestionEn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32), index=True)
    text = db.Column(db.String(256), index=True)
    answers = db.relationship('AnswerEn', backref='question')
    params = db.relationship('AnswerNum', backref='question', uselist=False)

    def __init__(self, id, type, text):
        self.type = type
        self.text = text
        self.id = id

    def __repr__(self):
        return '<Question %r>' % (self.text)


class AnswerEn(db.Model):
    text = db.Column(db.String(140), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question_en.id'), primary_key=True)

    def __init__(self, text, question_id):
        self.text = text
        self.question_id = question_id

    def __repr__(self):
        return self.text


class AnswerNum(db.Model):
    question_id = db.Column(db.Integer, db.ForeignKey('question_en.id'), primary_key=True)
    min = db.Column(db.SmallInteger)
    max = db.Column(db.SmallInteger)
    step = db.Column(db.SmallInteger)

    def __init__(self, min, max, step, question_id):
        self.min = min
        self.max = max
        self.step = step
        self.question_id = question_id

    def __repr__(self):
        return '<Max %r>' % (self.max)
