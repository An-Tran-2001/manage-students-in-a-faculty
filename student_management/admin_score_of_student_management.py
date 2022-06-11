from re import template
from flask import flash, redirect, url_for, render_template, request, session
from student_management.models import *
import os
import csv
from werkzeug.utils import secure_filename
from student_management import app, ALLOWED_EXTENSIONS
from sqlalchemy import and_

@app.route('/admin_score_of_student_management')
def admin_score_of_student_management():
    if 'user' in session:
        success = request.args.get('success')
        semesters = Semester.query.all()
        subjects = Subject.query.all()
        scores = None
        if success:
            return render_template('pages/admin/admin_score_of_student_management.html', success=success, semesters=semesters, subjects=subjects,scores=scores)
        return render_template('pages/admin/admin_score_of_student_management.html', semesters=semesters, subjects=subjects, scores=scores)
    else:
        return redirect(url_for('login'))

@app.route('/admin_add_score_of_student')
def admin_add_score_of_student():
    student = Student.query.filter_by(student_code=request.args.get('student_code')).first()
    if student:
        student_code = request.args.get('student_code')
        id_subject = request.args.get('id_subject')
        semester_id = request.args.get('id_semester')
        final_score = request.args.get('final_score')
        test_score = request.args.get('test_score')
        specialized_score = request.args.get('specialized_score')
        average_score = float(float(final_score)*0.6 + float(test_score)*0.3 + float(specialized_score)*0.1)
        student_ = Score(student_code=student_code, id_subject=id_subject, semester_id=semester_id, final_score=final_score, test_score=test_score, specialized_score=specialized_score, average_score=average_score)
        db.session.add(student_)
        db.session.commit()
        return redirect(url_for('admin_score_of_student_management', success='add student success'))
    else:
        return redirect(url_for('admin_score_of_student_management', success='student not found'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin_add_score_of_student_csv', methods=['GET', 'POST'])
def admin_add_score_of_student_csv():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count=0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        student_code = row[0]
                        id_subject = row[1]
                        semester_id = row[2]
                        final_score = row[3]
                        test_score = row[4]
                        specialized_score = row[5]
                        average_score = float(float(final_score)*0.6 + float(test_score)*0.3 + float(specialized_score)*0.1)
                        student_ = Score(student_code=student_code, id_subject=id_subject, semester_id=semester_id, final_score=final_score, test_score=test_score, specialized_score=specialized_score, average_score=average_score)
                        db.session.add(student_)
                        db.session.commit()
                        line_count += 1
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('admin_score_of_student_management', success='add student success'))
    return redirect(url_for('admin_score_of_student_management', success='add student success'))
    
@app.route('/admin_search_score_of_student')
def admin_search_score_of_student():
    student_code = request.args.get('student_code')
    scores={}
    semesters = Semester.query.all()
    for i in semesters:
        scores[f"{i.semester_code} - {i.start_date} - {i.end_date}"] = Score.query.filter(and_(Score.student_code==student_code, Score.semester_id==i.id)).all()
    for information in scores.values():
        for score in information:
            score.subject_name = Subject.query.filter_by(id=score.id_subject).first().subject_name
            db.session.commit()

    return render_template('pages/admin/admin_score_of_student_management.html', scores=scores, semesters=semesters, subjects=Subject.query.all())

@app.route('/admin_score_edit')
def admin_score_edit():
    score_id = request.args.get('score_id')
    score = Score.query.filter_by(id=score_id).first()
    final_score = request.args.get('final_score')
    test_score = request.args.get('test_score')
    specialized_score = request.args.get('specialized_score')
    average_score = float(float(final_score)*0.6 + float(test_score)*0.3 + float(specialized_score)*0.1)
    if final_score and test_score and specialized_score:
        score.final_score = final_score
        score.test_score = test_score
        score.specialized_score = specialized_score
        score.average_score = average_score
        db.session.commit()
        return redirect(url_for('admin_score_of_student_management', success='edit score success'))
    return template('pages/admin/admin_score_edit.html', score=score)

@app.route('/admin_score_delete')
def admin_score_delete():
    score_id = request.args.get('score_id')
    score = Score.query.filter_by(id=score_id).first()
    db.session.delete(score)
    db.session.commit()
    return redirect(url_for('admin_score_of_student_management', success='delete score success'))