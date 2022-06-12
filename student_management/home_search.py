from student_management import app
from flask import flash, redirect, url_for, render_template, request
from student_management.models import *
from sqlalchemy import and_


@app.route("/search")
def search():
    student_code =request.args.get('student_code')
    scores={}
    semesters = Semester.query.all()
    student = Student.query.get(student_code)
    if student:
        class_ = Class.query.get(student.id_student_class)
        for i in semesters:
            scores[f"{i.semester_code}: {i.start_date} -> {i.end_date}"] = Score.query.filter(and_(Score.student_code==student_code, Score.semester_id==i.id)).all()
        for information in scores.values():
            for score in information:
                score.subject_name = Subject.query.filter_by(id=score.id_subject).first().subject_name
        return render_template("pages/index.html", student=student, class_=class_, scores=scores)
    else:
        return redirect(url_for('index', error='student not found'))