from ast import Not
from flask import flash, redirect, url_for, render_template, request, session
from student_management.models import *
import os
import csv
from werkzeug.utils import secure_filename
from student_management import app, ALLOWED_EXTENSIONS

@app.route('/admin_student_management')
def admin_student_management():
    if 'user' in session:
        classes = Class.query.all()
        success = request.args.get('success')
        student = Student.query.filter_by(student_code=request.args.get('student_code')).first()

        if student:
            class_ = Class.query.filter_by(id=request.args.get('class_id')).first() 
            styles = None
        else:
            student = None
            class_ = None
            styles = 'style = display:none'
        if success:
            return render_template('pages/admin/admin_student_management.html', success=success, classes=classes , student=student, class_=class_)
        return render_template('pages/admin/admin_student_management.html', classes=classes, student=student, class_=class_, styles=styles)
    else:
        return redirect(url_for('login'))
    
@app.route('/admin_add_student')
def admin_add_student():
    student_code = request.args.get('student_code')
    student_name = request.args.get('student_name')
    student_sex = request.args.get('sex')
    student_birthday = request.args.get('student_birthday')
    id_class = request.args.get('id_class')
    student_course = request.args.get('student_course')
    student_study_time = request.args.get('student_study_time')
    student_ = Student(student_code=student_code, student_name=student_name, student_sex=student_sex, student_birthday=student_birthday, id_student_class=id_class, student_course=student_course, student_study_time=student_study_time)
    db.session.add(student_)
    db.session.commit()
    return redirect(url_for('admin_student_management', success='add student success'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route('/admin_add_list_student', methods=['GET', 'POST'])
def admin_add_list_student():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    student_code = row['student_code']
                    student_name = row['student_name']
                    student_sex = row['student_sex']
                    student_birthday = row['student_birthday']
                    id_class = row['id_class']
                    student_course = row['student_course']
                    student_study_time = row['student_study_time']
                    student_ = Student(student_code=student_code, student_name=student_name, student_sex=student_sex, student_birthday=student_birthday, id_student_class=id_class, student_course=student_course, student_study_time=student_study_time)
                    db.session.add(student_)
                    db.session.commit()
            return redirect(url_for('admin_student_management', success='add list student success'))
        else:
            return redirect(url_for('admin_student_management', success='file not allowed'))
    else:
        return redirect(url_for('admin_student_management'))

@app.route('/admin_search_student')
def admin_search_student():
    student_code = request.args.get('student_code')
    student = Student.query.filter_by(student_code=student_code).first()
    if student:
        return redirect(url_for('admin_student_management', student_code=student_code, class_id=student.id_student_class))
    else:
        return redirect(url_for('admin_student_management', success='student not found'))

@app.route('/admin_student_edit')
def admin_student_edit():
    student_id = request.args.get('student_id')
    student = Student.query.filter_by(id=student_id).first()
    classes = Class.query.all()
    return render_template('pages/admin/admin_student_edit.html', student=student, classes=classes)

@app.route('/admin_student_delete')
def admin_student_delete():
    student_id = request.args.get('student_id')
    student = Student.query.filter_by(id=student_id).first()
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('admin_student_management', success='delete student success'))