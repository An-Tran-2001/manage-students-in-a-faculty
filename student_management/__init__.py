from flask import Flask, render_template,request
from student_management.models import *

UPLOAD_FOLDER = 'student_management/path/upload'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.secret_key = 'secret123'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:admin@localhost:5432/student_management"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/new_table")
def new_table():
    db.create_all()


@app.route("/")
def index():
    score = None # điều kiện của phần tìm kiếm cần để tìm kiếm dữ liệu
    error = request.args.get('error')
    if error:
        return render_template('pages/index.html', error=error, score=score)
    return render_template("pages/index.html", score=score)



import student_management.login
import student_management.home_search
import student_management.edit_admin
import student_management.admin_subject_management
import student_management.admin_student_management
import student_management.admin_account_management
import student_management.admin_class_management
import student_management.admin_semester_management
import student_management.admin_score_of_student_management
import student_management.edit_user


