from student_management import app
from flask import flash, redirect, url_for, render_template, request,session
from student_management.models import *
from sqlalchemy import and_


@app.route("/home_user")
def home_user():
    if 'user' in session:
        user_= User.query.get(session['user'])#lay ra user(voi vien dc luu user id) tren session de tim kiem va lay ra class user do
        user_code = user_.username
        user = Student.query.filter_by(student_code=user_code).first()# tim kiem xem ten user cos trong danh sach sinh vien hay ko
        if user:
            student = Student.query.get(user_code)
            scores={}
            semesters = Semester.query.all()
            if student:
                class_ = Class.query.get(student.id_student_class)
                for i in semesters:
                    scores[f"{i.semester_code}: {i.start_date} -> {i.end_date}"] = Score.query.filter(and_(Score.student_code==user_code, Score.semester_id==i.id)).all()
                for information in scores.values():
                    for score in information:
                        score.subject_name = Subject.query.filter_by(id=score.id_subject).first().subject_name
                return render_template("pages/user/home_user.html", student=student, class_=class_, scores=scores, error='')
            else:
                return render_template("pages/user/home_user.html", error='student not found')
        else:
            return render_template("pages/user/home_user.html", error='no student is compatible with user')
    else:
        return redirect(url_for('login'))

@app.route("/user_student_out")
def user_student_out():
    session.pop('user', None)
    return redirect(url_for('login'))