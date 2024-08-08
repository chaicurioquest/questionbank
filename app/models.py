from . import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(500), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    bt = db.Column(db.String(10), nullable=False)
    co = db.Column(db.String(10), nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    answer_key = db.Column(db.String(500), nullable=False)
    question_type = db.Column(db.String(50), nullable=False)
    files = db.relationship('File', backref='question', lazy=True)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)
    file_name = db.Column(db.String(100), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
