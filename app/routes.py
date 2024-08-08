from flask import current_app as app, request, render_template, redirect, url_for, send_file
from . import db
from .forms import QuestionForm, SearchForm
from .models import Question, File
from io import BytesIO

@app.route('/')
def index():
    questions = Question.query.all()
    return render_template('index.html', questions=questions)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = QuestionForm()

    topics = db.session.query(Question.topic.distinct().label("topic")).all()
    courses = db.session.query(Question.course_name.distinct().label("course_name")).all()

    form.topic.choices = [(topic.topic, topic.topic) for topic in topics] + [("new", "Enter new topic")]
    form.course_name.choices = [(course.course_name, course.course_name) for course in courses] + [("new", "Enter new course name")]

    if form.validate_on_submit():
        question = Question(
            question_text=form.question_text.data,
            topic=form.new_topic.data if form.new_topic.data else form.topic.data,
            marks=form.marks.data,
            bt=form.bt.data,
            co=form.co.data,
            course_name=form.new_course_name.data if form.new_course_name.data else form.course_name.data,
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

        return redirect(url_for('index'))

    return render_template('add.html', form=form)

@app.route('/file/<int:file_id>')
def file(file_id):
    file_record = File.query.get_or_404(file_id)
    return send_file(BytesIO(file_record.file_data), attachment_filename=file_record.file_name, mimetype=file_record.file_type)

@app.route('/delete/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    query = Question.query

    if form.validate_on_submit():
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

        results = query.all()
        return render_template('index.html', questions=results, form=form)

    return render_template('search.html', form=form)
