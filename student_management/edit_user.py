from student_management import app
from flask import flash, redirect, url_for, render_template, request
from student_management.models import *


@app.route("/home_user")
def home_user():
    return render_template("pages/user/home_user.html")
