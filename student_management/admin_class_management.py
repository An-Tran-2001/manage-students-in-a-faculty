from flask import flash, redirect, url_for, render_template, request, session
from student_management.models import *
import os
import csv
from werkzeug.utils import secure_filename
from student_management import app, ALLOWED_EXTENSIONS


@app.route('/admin_class_management')
def admin_class_management():
    if 'user' in session:
        success = request.args.get('success')
        classes = Class.query.all()
        if success:
            return render_template('pages/admin/admin_class_management.html', success=success, classes=classes)
        return render_template('pages/admin/admin_class_management.html', classes=classes)
    else:
        return redirect(url_for('login'))


@app.route('/admin_add_class')
def admin_add_class():
    class_code = request.args.get('class_code')
    class_name = request.args.get('class_name')
    lead_teacher_name = request.args.get('lead_teacher_name')
    phone_number_of_lead_teacher = request.args.get(
        'phone_number_of_lead_teacher')
    student_number = request.args.get('student_number')
    class_ = Class(class_code=class_code, class_name=class_name, lead_teacher_name=lead_teacher_name,
                   student_number=student_number, phone_number_of_lead_teacher=phone_number_of_lead_teacher)
    db.session.add(class_)
    db.session.commit()
    return redirect(url_for('admin_class_management', success="Add class successfully"))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/admin_add_class_csv', methods=['GET', 'POST'])
def admin_add_class_csv():  # phần này đã đc cải tiến bởi AI
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
                filename = secure_filename(file.filename)  # lấy tên file
                # lưu file vào thư mục upload
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # mở file csv
                with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as csv_file:
                    csv_reader = csv.reader(
                        csv_file, delimiter=',')  # đọc file csv
                    line_count = 0  # đếm số dòng của file csv
                    for row in csv_reader:  # duyệt từng dòng trong file csv
                        if line_count == 0:  # nếu là dòng đầu tiên thì bỏ qua bởi vì dòng đầu tiên lưu tên trường nên ko cần lưu ko thì có thể bỏ
                            line_count += 1
                        else:  # nếu không phải dòng đầu tiên thì thực hiện
                            class_code = row[0]
                            class_name = row[1]
                            lead_teacher_name = row[2]
                            phone_number_of_lead_teacher = row[3]
                            student_number = row[4]
                            class_ = Class(class_code=class_code, class_name=class_name, lead_teacher_name=lead_teacher_name,
                                           phone_number_of_lead_teacher=phone_number_of_lead_teacher, student_number=student_number)
                            db.session.add(class_)
                            db.session.commit()
                            line_count += 1
                return redirect(url_for('admin_class_management', success="Add class successfully"))

            else:
                flash('File extension not allowed')
                return redirect(request.url)
        return render_template('pages/admin/admin_add_class_csv.html')
    else:
        return redirect(url_for('login'))
#


@app.route('/admin_edit_class')
def admin_edit_class():
    if 'user' in session:
        class_id = request.args.get('class_id')
        class_ = Class.query.get(class_id)

        class_code = request.args.get('class_code')
        class_name = request.args.get('class_name')
        lead_teacher_name = request.args.get('lead_teacher_name')
        phone_number_of_lead_teacher = request.args.get('phone_number_of_lead_teacher')
        if class_code and class_name and lead_teacher_name and phone_number_of_lead_teacher:
            class_.class_code = class_code
            class_.class_name = class_name
            class_.lead_teacher_name = lead_teacher_name
            class_.phone_number_of_lead_teacher = phone_number_of_lead_teacher
            db.session.commit()
            return redirect(url_for('admin_class_management', success="Edit class successfully"))
        return render_template('pages/admin/admin_edit_class.html', class_=class_)
    else:
        return redirect(url_for('login'))


@app.route('/admin_delete_class')
def admin_delete_class():
    if 'user' in session:
        class_id = request.args.get('class_id')
        class_ = Class.query.get(class_id)
        db.session.delete(class_)
        db.session.commit()
        return redirect(url_for('admin_class_management', success="Delete class successfully"))
    else:
        return redirect(url_for('login'))
