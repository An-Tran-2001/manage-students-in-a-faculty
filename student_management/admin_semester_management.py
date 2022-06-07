from flask import flash, redirect, url_for, render_template, request, session
from student_management.models import *
import os
import csv
from werkzeug.utils import secure_filename
from student_management import app, ALLOWED_EXTENSIONS

@app.route('/admin_semester_management')
def admin_semester_management():
    if 'user' in session:
        success = request.args.get('success')
        semesters = Semester.query.all()
        if success:
            return render_template('pages/admin/admin_semester_management.html', success=success, semesters=semesters)
        return render_template('pages/admin/admin_semester_management.html', semesters=semesters)
    else:
        return redirect(url_for('login'))

@app.route('/admin_add_semester')
def admin_add_semester():
    semester_code = request.args.get('semester_code')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    semester = Semester(semester_code=semester_code, start_date=start_date, end_date=end_date)
    db.session.add(semester)
    db.session.commit()
    return redirect(url_for('admin_semester_management', success="Add semester successfully"))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin_add_semester_csv', methods=['GET', 'POST'])
def admin_add_semester_csv():  # phần này đã đc cải tiến bởi AI
    if 'user' in session:
        if request.method == 'POST':
            # kiểm tra xem có file được chọn không
            if 'file' not in request.files:
                flash('No file part')
                # hàm request trả lại url hiện tại
                return redirect(request.url)
            file = request.files['file']
            # Nếu không chọn thì trình duyệt tự gửi file không có tên
            if file.filename == '':
                flash('No selected file')
                # nêys file name ko giá trị thì giả về url hiện tại và thông báo ko chọn file
                return redirect(request.url)
            # kiểm tra xem file có đúng định dạng không
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # đặt tên file mới
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # đọc file csv
                with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    for row in csv_reader:
                        if line_count == 0:
                            line_count += 1
                        else:
                            semester_code = row[0]
                            start_date = row[1]
                            end_date = row[2]
                            semester = Semester(semester_code=semester_code, start_date=start_date, end_date=end_date)
                            db.session.add(semester)
                            db.session.commit()
                            line_count += 1
                flash('Add semester successfully')
                return redirect(url_for('admin_semester_management'))
            else:
                flash('File extension not allowed')
                return redirect(request.url)

@app.route('/admin_edit_semester')
def admin_edit_semester():
    semester_id = request.args.get('semester_id')
    semester = Semester.query.filter_by(id=semester_id).first()
    return render_template('pages/admin/admin_edit_semester.html', semester=semester)

@app.route('/admin_edit_semester_submit', methods=['GET', 'POST'])
def admin_edit_semester_submit():
    semester_id = request.args.get('semester_id')
    semester = Semester.query.filter_by(id=semester_id).first()
    semester_code = request.args.get('semester_code')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    semester.semester_code = semester_code
    semester.start_date = start_date
    semester.end_date = end_date
    db.session.commit()
    return redirect(url_for('admin_semester_management', success="Edit semester successfully"))

@app.route('/admin_delete_semester')
def admin_delete_semester():
    semester_id = request.args.get('semester_id')
    semester = Semester.query.filter_by(id=semester_id).first()
    db.session.delete(semester)
    db.session.commit()
    return redirect(url_for('admin_semester_management', success="Delete semester successfully"))