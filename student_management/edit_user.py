from student_management import app #  truy cap vao __init__ lay app
from flask import flash, redirect, url_for, render_template, request,session# lay models trong pakage
from student_management.models import * # import ^ la loay cac du lieu trong cai moduules day
from sqlalchemy import and_


@app.route("/home_user")
def home_user():
    if 'user' in session: # kiem tra sesion da luu 
        user_= User.query.get(session['user'])#lay ra user(voi vien dc luu user id) tren session de tim kiem va lay ra class user do
        user_code = user_.username# lay uẻnam de so sanh voi ma sinh vien 
        user = Student.query.filter_by(student_code=user_code).first()# tim kiem xem ten user cos trong danh sach sinh vien hay ko
        if user:# neu tim thay sinh vien co msv tuong ung
            student = Student.query.get(user_code)# lay sv voi key msv
            scores={} #tao ra dict de luu giu diem
            semesters = Semester.query.all()# lay hoc ky ra
            if student: # kiem tra student co ton tai
                class_ = Class.query.get(student.id_student_class)# lay ra class voi truong id_class khoa ngoai trong bang sinh vien
                for i in semesters:#cgo chay cac hoc ku
                    scores[f"{i.semester_code}: {i.start_date} -> {i.end_date}"] = Score.query.filter(and_(Score.student_code==user_code, Score.semester_id==i.id)).all()# moi hoc ky se la key va value la 1 lít cac sv trog hoc ky do
                for information in scores.values():# chay tung value trong dict
                    for score in information:# chay tung value trong list
                        score.subject_name = Subject.query.filter_by(id=score.id_subject).first().subject_name# lay ten mon hoc mon hoc ra gan voi truong da tao truoc
                return render_template("pages/user/home_user.html", student=student, class_=class_, scores=scores, error='')# tra ve trang home user
            else:#ko co sinh vien
                return render_template("pages/user/home_user.html", error='student not found')
        else:# nau khong tim thay sinh vien tuong ung
            return render_template("pages/user/home_user.html", error='no student is compatible with user')# tra ve lôi la tên user khong trung voi msv nao ca
    else:# neu sesion ko gia tri
        return redirect(url_for('login'))# tra ve url login la cai ham login o trong file loin

@app.route("/user_student_out")#  thoat khoi trang student
def user_student_out():
    session.pop('user', None)# pop ra la lay ra va xoa khoi sesion
    return redirect(url_for('login'))# tra lại trang login