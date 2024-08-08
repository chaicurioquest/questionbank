from flask import Blueprint, render_template, request, redirect, url_for
from .forms import QuestionForm, SearchForm
from .models import Question, File, db  # Import File model

main = Blueprint('main', __name__)

@main.route('/')
def index():
    questions = Question.query.all()
    return render_template('index.html', question=questions)

@main.route('/add', methods=['GET', 'POST'])
def add():
    form = QuestionForm()

    # Fetch existing topics and courses from the database
    topics = db.session.query(Question.topic.distinct().label("topic")).all()
    courses = db.session.query(Question.course_name.distinct().label("course_name")).all()

    # Update the form choices
    form.topic.choices = [(topic.topic, topic.topic) for topic in topics] + [("new", "Enter new topic")]
    form.course_name.choices = [(course.course_name, course.course_name) for course in courses] + [("new", "Enter new course name")]

    if form.validate_on_submit():
        topic = form.new_topic.data if form.new_topic.data else form.topic.data
        course_name = form.new_course_name.data if form.new_course_name.data else form.course_name.data

        question = Question(
            question_text=form.question_text.data,
            topic=topic,
            marks=form.marks.data,
            bt=form.bt.data,
            co=form.co.data,
            course_name=course_name,
            answer_key=form.answer_key.data,
            question_type=form.question_type.data
        )
        db.session.add(question)
        db.session.commit()

        for file in request.files.getlist('files'):
            file_data = file.read()
            file_record = File(
                question_id=question.id,
                file_data=file_data,
                file_name=file.filename,
                file_type=file.content_type
            )
            db.session.add(file_record)
            db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('add.html', form=form)

@main.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    questions = []

    if form.validate_on_submit():
        query = Question.query

        if form.topic.data:
            query = query.filter(Question.topic.ilike(f'%{form.topic.data}%'))
        if form.marks.data:
            query = query.filter_by(marks=form.marks.data)
        if form.bt.data:
            query = query.filter_by(bt=form.bt.data)
        if form.co.data:
            query = query.filter_by(co=form.co.data)
        if form.course_name.data:
            query = query.filter(Question.course_name.ilike(f'%{form.course_name.data}%'))
        if form.answer_key.data:
            query = query.filter(Question.answer_key.ilike(f'%{form.answer_key.data}%'))
        if form.question_type.data:
            query = query.filter_by(question_type=form.question_type.data)

        questions = query.all()

    return render_template('search.html', form=form, questions=questions)
