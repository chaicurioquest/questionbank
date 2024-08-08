from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, FileField, SubmitField
from wtforms.validators import DataRequired

class QuestionForm(FlaskForm):
    question_text = TextAreaField('Question Text', validators=[DataRequired()])
    topic = SelectField('Topic', validators=[DataRequired()])
    new_topic = StringField('Or enter a new topic')
    marks = IntegerField('Marks', validators=[DataRequired()])
    bt = SelectField('BT (Bloom Taxonomy)', choices=[('L1', 'L1'), ('L2', 'L2'), ('L3', 'L3'), ('L4', 'L4'), ('L5', 'L5'), ('L6', 'L6')], validators=[DataRequired()])
    co = SelectField('CO (Course Outcome)', choices=[('CO1', 'CO1'), ('CO2', 'CO2'), ('CO3', 'CO3'), ('CO4', 'CO4'), ('CO5', 'CO5')], validators=[DataRequired()])
    course_name = SelectField('Course Name', validators=[DataRequired()])
    new_course_name = StringField('Or enter a new course name')
    answer_key = TextAreaField('Answer Key', validators=[DataRequired()])
    question_type = SelectField('Question Type', choices=[('descriptive', 'Descriptive'), ('numerical', 'Numerical')], validators=[DataRequired()])
    files = FileField('Files', render_kw={"multiple": True})
    submit = SubmitField('Add Question')

class SearchForm(FlaskForm):
    topic = StringField('Topic')
    marks = IntegerField('Marks')
    bt = SelectField('BT (Bloom Taxonomy)', choices=[('L1', 'L1'), ('L2', 'L2'), ('L3', 'L3'), ('L4', 'L4'), ('L5', 'L5'), ('L6', 'L6')])
    co = SelectField('CO (Course Outcome)', choices=[('CO1', 'CO1'), ('CO2', 'CO2'), ('CO3', 'CO3'), ('CO4', 'CO4'), ('CO5', 'CO5')])
    course_name = StringField('Course Name')
    answer_key = TextAreaField('Answer Key')
    question_type = SelectField('Question Type', choices=[('descriptive', 'Descriptive'), ('numerical', 'Numerical')])
    submit = SubmitField('Search')
