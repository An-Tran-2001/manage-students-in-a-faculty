from flask_sqlalchemy import SQLAlchemy
# import một modules của flask_sqlalchemy

db = SQLAlchemy()

#  tạo ra 1 class để lưu trữ dữ liệu kế thừa từ class có sẵn vs cứ pháp SQLAlchemy().Model
#  gọi class trong package SQLAlchemy() với tên đã được gán là db
#  tạo các thuộc tính cho class đó với tên là id, name, email, password,... ứng với các trường trong database


class User(db.Model):
    __tablename__ = 'users'
    # Khóa chính ( phân biệt nếu bị trùng dữ liệu kháo chính là duy nhất)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    grant_permission = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)


class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(255), nullable=False)
    subject_name = db.Column(db.String(255), nullable=False)
    number_of_credits = db.Column(db.Integer, nullable=False)
    teacher_name = db.Column(db.String(255), nullable=False)


class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    class_code = db.Column(db.String(255), nullable=False)
    class_name = db.Column(db.String(255), nullable=False)
    lead_teacher_name = db.Column(db.String(255), nullable=False)
    phone_number_of_lead_teacher = db.Column(db.String(255), nullable=False)
    student_number = db.Column(db.Integer, nullable=False)


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    student_code = db.Column(db.String(255), nullable=False)
    student_name = db.Column(db.String(255), nullable=False)
    student_birthday = db.Column(db.String(255), nullable=False)
    id_student_class = db.Column(
        db.Integer, db.ForeignKey('classes.id'), nullable=False)
    id_subject = db.Column(db.Integer, db.ForeignKey(
        'subjects.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
