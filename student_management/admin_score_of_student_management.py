from flask import flash, redirect, url_for, render_template, request, session
from student_management.models import *
import os
import csv
from werkzeug.utils import secure_filename
from student_management import app, ALLOWED_EXTENSIONS

@app.route('/admin_score_of_student_management')
def admin_score_of_student_management():
    if 'user' in session:
        success = request.args.get('success')
        classes = Class.query.all()
        semesters = Semester.query.all()
        subjects = Subject.query.all()
        if success:
            return render_template('pages/admin/admin_score_of_student_management.html', success=success, classes=classes, semesters=semesters, subjects=subjects)
        return render_template('pages/admin/admin_score_of_student_management.html', classes=classes, semesters=semesters, subjects=subjects)
    else:
        return redirect(url_for('login'))

@app.route('/admin_add_score_of_student')
def admin_add_score_of_student():
    student_code = request.args.get('student_code')
    student_name = request.args.get('student_name')
    student_birthday = request.args.get('student_birthday')
    id_student_class = request.args.get('id_class')
    id_subject = request.args.get('id_subject')
    semester_id = request.args.get('id_semester')
    final_score = request.args.get('final_score')
    test_score = request.args.get('test_score')
    specialized_score = request.args.get('specialized_score')
    student_ = Student(student_code=student_code, student_name=student_name, student_birthday=student_birthday, id_student_class=id_student_class, id_subject=id_subject, semester_id=semester_id, final_score=final_score, test_score=test_score, specialized_score=specialized_score)
    db.session.add(student_)
    db.session.commit()
    return redirect(url_for('admin_score_of_student_management', success='add student success'))