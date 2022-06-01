from ast import Not
from flask import flash, redirect, url_for, render_template, request, session
from student_management.models import *
import os
import csv
from werkzeug.utils import secure_filename
from student_management import app, ALLOWED_EXTENSIONS


@app.route('/admin_subject_management')
def admin_subject_management():
    if 'user' in session:
        success = request.args.get('success')
        subjects = Subject.query.all()


        if success:
            return render_template('pages/admin/admin_subject_management.html', subjects=subjects, success=success)
        
        return render_template('pages/admin/admin_subject_management.html', subjects=subjects)
    else:
        return redirect(url_for('login'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/admin_subject_add')
def admin_subject_add():
    if 'user' in session:
        subject_code = request.args.get('subject_code')
        subject_name = request.args.get('subject_name')
        number_of_credit = request.args.get('number_of_credit')
        teacher_name = request.args.get('teacher_name')
        subject = Subject(subject_code=subject_code, subject_name=subject_name,
                          number_of_credits=number_of_credit, teacher_name=teacher_name)
        db.session.add(subject)
        db.session.commit()
        return redirect(url_for('admin_subject_management', success="Add subject successfully"))
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin_subject_add_csv', methods=['GET', 'POST'])
def admin_subject_add_csv():
    if 'user' in session:
        if request.method == 'POST':
            # kiểm tra xem có file được chọn không
            if 'file' not in request.files:
                flash('No file part')
                # hàm request trả lại url hiện tại
                return redirect(request.url)
            file = request.files['file']  # lấy file được chọn với pt post
            # Nếu không chọn thì trình duyệt tự gửi file không có tên
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # appconfig là địa chỉ của file đã khai báo ở trên file __init__
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('load_file_subjects',
                                        filename=filename))
    else:
        return redirect(url_for('admin_login'))


@app.route("/load_file_subjects")
def load_file_subjects():
    filename = request.args.get('filename')
    # r ở đây là read đọc file, appconfig là địa chỉ của file đã khai báo ở trên file __init__
    file = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r')
    data = csv.reader(file)
    for subject_code, subject_name, number_of_credit, teacher_name in data:
        subject = Subject(subject_code=subject_code, subject_name=subject_name,
                          number_of_credits=number_of_credit, teacher_name=teacher_name)
        db.session.add(subject)
        db.session.commit()
    return redirect(url_for('admin_subject_management', success="Add file subject successfully"))


@app.route('/admin_subject_search')
def admin_subject_search():
    if 'user' in session:
        subject = request.args.get('subject')
        subjects = Subject.query.filter_by(subject_code=subject).all()
        if subjects == []:
            subjects = Subject.query.filter_by(subject_name=subject).all()
            if subjects == []:
                return redirect(url_for('admin_subject_management', success="Not found subject"))
        return render_template('pages/admin/admin_subject_management.html', subjects=subjects, success='final search')
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin_subject_edit')
def admin_subject_edit():
    if 'user' in session:
        subject = Subject.query.get(request.args.get('subject_id'))
        subject_code = request.args.get('subject_code')
        subject_name = request.args.get('subject_name')
        number_of_credit = request.args.get('number_of_credit')
        teacher_name = request.args.get('teacher_name')
        if subject_code and subject_name and number_of_credit and teacher_name:
            subject.subject_code = subject_code
            subject.subject_name = subject_name
            subject.number_of_credits = number_of_credit
            subject.teacher_name = teacher_name
            db.session.commit()
            return redirect(url_for('admin_subject_management', success="Edit subject successfully"))
        return render_template('pages/admin/admin_subject_edit.html', subject=subject)
        
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin_subject_delete')
def admin_subject_delete():
    if 'user' in session:
        subject = Subject.query.get(request.args.get('subject_id'))
        db.session.delete(subject)
        db.session.commit()
        return redirect(url_for('admin_subject_management', success="Delete subject successfully"))
    else:
        return redirect(url_for('admin_login'))
