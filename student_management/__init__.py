from flask import Flask, render_template
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
    return render_template("pages/index.html")



import student_management.login
import student_management.home_search
import student_management.edit_admin
import student_management.admin_subject_management
import student_management.admin_account_management
import student_management.admin_class_management
import student_management.edit_user


