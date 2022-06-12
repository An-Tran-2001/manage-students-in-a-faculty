from flask import flash, redirect, url_for, render_template, request,session
from student_management.models import *
from student_management import app


@app.route("/login")
def login():
    if 'user' in session: # luu dang nhap
        user_id = session['user'] # lay ra user id trong session
        user = User.query.filter_by(id=user_id).first()
        if user.grant_permission:# kiem tra user co quyen truy cap hay ko
            return render_template("pages/admin/home_admin.html", user=user)
        else:
            return redirect(url_for('home_user'))
    else:
        name = request.args.get('username')
        password = request.args.get('password')
        if name and password:  # kiểm tra xem co dữ liệu đc đưa vào chưa
            # tìm kiếm tài khoản dựa trên tên tài khoản xuất hiện đầu tiên
            user = User.query.filter_by(username=name).first()
            if user:  # kiểm tra xem tài khoản có tồn tại ko chính xác là có tìm ra đc tài khoản với tên tài khoản tương ứng không
                if user.grant_permission:  # kiểm tra cấp quyền của tài khoản True là được cấp quyền chỉnh sửa của giáo viên False là không được cấp quyền chỉnh sửa
                    if user.password == password:  # kiểm tra mật khẩu của tài khoản có trùng với mật khẩu được nhập vào không
                        # chạy đến file và giả lại user
                        session['user'] = user.id
                        return render_template("pages/admin/home_admin.html", user=user)# chạy thẳng đén file home_admin
                    else:
                        return render_template('pages/login.html', error="Password is incorrect")
                else:  # ngược lại, tài khoản thường không có quyền chỉnh sửa là tài khoản sinh viên vẫn đc kiểm tra mật khẩu như trên nhưng sẽ đưa về hàm xử lý khác nhau
                    if user.password == password:
                        # chạy đến hàm được gọi là home_user
                        session['user'] = user.id
                        return redirect(url_for('home_user'))
                    else:
                        # không trùng mật khẩu sẽ trả lại biến lõi sai viws value là sai mật khẩu rùi
                        return render_template('pages/login.html', error="Password is incorrect")
            else:  # ngược lại với việc ko tìm kiếm được tên tài kkhoanr trung với tên tài khoản được nhập vào thì sẽ trả lại biến lỗi sai viws value là sai tên tài khoản hoạc tài khoản không tồn tại
                return render_template('pages/login.html', error="User does not exist or incorrect username")
        # cuối cùng đơn giản là trả lại hàm login bth nếu ko có dữ liệu được nhập vào
        return render_template("pages/login.html")
