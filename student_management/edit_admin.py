from flask import flash, redirect, url_for, render_template, request
from student_management.models import *
from student_management import app
import datetime


@app.route("/admin_edit_profile")
def admin_edit_profile():
    user = User.query.get(request.args.get('user_id'))
    username = request.args.get('username')
    email = request.args.get('email')
    phone = request.args.get('phone_number')
    if username and email and phone:
        user.username = username
        user.email = email
        user.phone_number = phone
        user.updated_at = datetime.datetime.now()
        db.session.commit()
        return render_template('pages/admin/home_admin.html', user=user, success="Update profile successfully")
    return render_template("pages/admin/edit_profile.html", user=user)


@app.route("/admin_change_password")
def admin_change_password():
    user = User.query.get(request.args.get('user_id'))
    password = request.args.get('confirm_password')
    if password:
        user.password = password
        user.updated_at = datetime.datetime.now()
        db.session.commit()
        return render_template('pages/admin/home_admin.html', user=user, success="Update password successfully")
    return render_template("pages/admin/change_password.html", user=user)


@app.route("/admin_logout")
def admin_logout():
    return redirect(url_for('login'))
