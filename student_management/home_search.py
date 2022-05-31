from student_management import app
from flask import flash, redirect, url_for, render_template, request
from student_management.models import *


@app.route("/search")
def search():
    return render_template("pages/index.html")
