from flask import flash, redirect, url_for, render_template, request,session
from student_management.models import *
import os
import csv
import datetime
from werkzeug.utils import secure_filename
from student_management import app, ALLOWED_EXTENSIONS


@app.route("/admin_account_management")
def admin_account_management():
    if 'user' in session:
        username = request.args.get('username')
        password = request.args.get('password')
        email = request.args.get('email')
        phone = request.args.get('phone_number')
        grant_permission = bool(request.args.get('grant_permission'))# kiểu bool trẻ vè True Flas khi ko có dữ liệu False có duẽ liệu là True
        if username and email and phone and password:
            created_at = datetime.datetime.now()
            user = User(username=username, password=password, email=email,
                        phone_number=phone, grant_permission=grant_permission, created_at=created_at)
            db.session.add(user)
            db.session.commit()
            return render_template("pages/admin/account_management.html", success="Add account successfully")
        return render_template("pages/admin/account_management.html")
    else:
        return redirect(url_for('login'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Goi method post de upload file
@app.route("/admin_account_management_upload_file", methods=['GET', 'POST'])
def admin_account_management_upload_file():
    if request.method == 'POST':
        # kiểm tra xem có file được chọn không
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)  # hàm request trả lại url hiện tại
        file = request.files['file']  # lấy file được chọn với pt post
        # Nếu không chọn thì trình duyệt tự gửi file không có tên
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))#appconfig là địa chỉ của file đã khai báo ở trên file __init__
            return redirect(url_for('load_file',
                                    filename=filename))


@app.route("/load_file")
def load_file():
    filename = request.args.get('filename')
    file = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r')# r ở đây là read đọc file, appconfig là địa chỉ của file đã khai báo ở trên file __init__
    data = csv.reader(file)
    for username, password, email, phone_number, grant_permission in data:
        created_at = datetime.datetime.now()
        if grant_permission == 'True':
            grant_permission = True
        else:
            grant_permission = False
        user = User(username=username, password=password, email=email,
                    phone_number=phone_number, grant_permission=grant_permission, created_at=created_at)
        db.session.add(user)
        db.session.commit()
    return render_template("pages/admin/account_management.html", success="Add account successfully")


@app.route("/admin_account_management_search_account")
def admin_account_management_search_account():
    search = request.args.get('search')
    if search:
        users = User.query.filter(User.username.like("%" + search + "%")).all()# tìm kiếm tất cả giá trị với điều kiện like là '%Biến%' sẽ trả về tất cả giá trị username có chứa Biến đó
        return render_template("pages/admin/account_management.html", users=users)


@app.route("/admin_account_management_delete_account")
def admin_account_management_delete_account():
    user_id = request.args.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return render_template("pages/admin/account_management.html", success="Delete account successfully")


@app.route("/admin_account_management_edit_account")
def admin_account_management_edit_account():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    username = request.args.get('username')
    email = request.args.get('email')
    phone = request.args.get('phone_number')
    grant_permission = bool(request.args.get('grant_permission'))
    if username and email and phone:
        user.username = username
        user.email = email
        user.phone_number = phone
        user.grant_permission = grant_permission
        user.updated_at = datetime.datetime.now()
        db.session.commit()
        return render_template('pages/admin/account_management.html', success="Update profile successfully")
    return render_template("pages/admin/edit_account.html", user=user)
