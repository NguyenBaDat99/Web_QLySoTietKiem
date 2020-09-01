from app import app, login, decorator, dao
from flask import render_template, request
from flask_login import login_user, logout_user
import hashlib


@app.route("/")
@decorator.login_required_user
def index():
    return render_template("layouts/base.html")


@app.route("/login-employee", methods=["post", "get"])
def login_employee():
    msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = hashlib.md5(password.strip().encode("utf-8")).hexdigest()
        emp = Employee.query.filter(Employee.username == username.strip(),
                                    Employee.password == password).first()
        if emp:
            login_user(user=emp)
            if emp.employee_role == EmployeeRole.ADMIN:
                return redirect("/admin")
            else:
                return redirect("/")
        else:
            msg = "Sai tên đăng nhập hoặc mật khẩu"
    return render_template("accounts/login.html", msg=msg)


@app.route("/logout-employee")
def logout_employee():
    logout_user()
    return redirect(url_for("index"))


@app.route("/setting-employee", methods=["get", "post"])
def setting_employee():
    msg_info = ""
    msg_pass = ""
    err_msg_info = ""
    err_msg_pass = ""
    if request.method == "POST":
        if request.form['save'] == 'saveInformation':

            name = request.form.get("name")
            gender = request.form.get("gender")
            date_of_birth = request.form.get("dateOfBirth")
            phone = request.form.get("phone")
            address = request.form.get("address")
            password_confirm = hashlib.md5(request.form.get("passwordConfirm")
                                           .strip().encode("utf-8")).hexdigest()

            if current_user.password == password_confirm:
                dao.employee_change_info(current_user.id, name, gender, date_of_birth, phone, address)
                msg_info = "Cập nhật thông tin tài khoản thành công"
                return render_template("accounts/setting.html", msg_info=msg_info)
            else:
                err_msg_info = "Mật khẩu không chính xác"
                return render_template("accounts/setting.html", err_msg_info=err_msg_info)
        if request.form['save'] == 'savePassword':

            new_password = hashlib.md5(request.form.get("newPassword")
                                       .strip().encode("utf-8")).hexdigest()
            new_password_confirm = hashlib.md5(request.form.get("newPasswordConfirm")
                                               .strip().encode("utf-8")).hexdigest()
            old_password_confirm = hashlib.md5(request.form.get("oldPasswordConfirm")
                                               .strip().encode("utf-8")).hexdigest()

            if new_password == new_password_confirm:
                if current_user.password == old_password_confirm:
                    dao.employee_change_pass(current_user.id, new_password)
                    msg_pass = "Đổi mật khẩu thành công"
                    return render_template("accounts/setting.html", msg_pass=msg_pass)
                else:
                    err_msg_pass = "Mật khẩu cũ không chính xác"
                    return render_template("accounts/setting.html", err_msg_pass=err_msg_pass)
            else:
                err_msg_pass = "Mật khẩu mới không khớp"
                return render_template("accounts/setting.html", err_msg_pass=err_msg_pass)
    return render_template("accounts/setting.html")


@login.user_loader
def load_user(user_id):
    return Employee.query.get(user_id)


if __name__ == "__main__":
    from app.admin_view import *

    app.run(debug=True)
