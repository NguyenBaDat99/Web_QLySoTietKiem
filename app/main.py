from app import app, login, decorator, dao
from flask import render_template, request, jsonify, session
from flask_login import login_user, logout_user
import hashlib
import json

from datetime import datetime


@app.route("/")
@decorator.login_required_user
def index():
    return render_template("layouts/base.html")


@app.route("/login-employee", methods=["post", "get"])
def login_employee():
    msg = ""
    msg_deactive = ""
    try_login = 0

    if 'try_login' in session and session['try_login']:
        try_login = session['try_login']
    else:
        session['try_login'] = 0

    if request.method == "POST":
        username = request.form.get("username")
        # password = request.form.get("password", "")
        # password = hashlib.sha512(password.strip().encode("utf-8")).hexdigest()
        password = request.form.get("password", "")
        captcha = request.form.get("g-recaptcha-response")

        if captcha or try_login <= 3:
            emp = Employee.query.filter(Employee.username == username.strip(),
                                        Employee.password == password).first()
            if emp:
                if emp.active:
                    login_user(user=emp)
                    session.pop('try_login', None)
                    activity_time = datetime.now()
                    activity = "Đăng nhập"
                    description = ""
                    employee_id = current_user.id
                    dao.add_activity_log(activity_time=activity_time, activity=activity,
                                         description=description, employee_id=employee_id)
                    if emp.employee_role == EmployeeRole.ADMIN:
                        return redirect("/admin")
                    else:
                        return redirect("/")
                else:
                    msg_deactive = "Tài khoản đã bị vô hiệu hóa"
            else:
                msg = "Sai tên đăng nhập hoặc mật khẩu"
                session['try_login'] = try_login + 1
        else:
            msg = "Lỗi xác thực captcha"
    return render_template("accounts/login.html", msg=msg, msg_deactive=msg_deactive, try_login=try_login)


@app.route("/report-password", methods=["post", "get"])
def report_password():
    msg_pass = ""
    err_msg_pass = ""
    msg = "Sai tên đăng nhập hoặc mật khẩu"
    if request.method == "POST":
        username = request.form.get("username")
        emp = Employee.query.filter(Employee.username == username.strip()).first()
        if emp:
            dao.set_employee_status(emp.id)
            msg_pass = "Vô hiệu hóa tài khoản thành công"

            activity_time = datetime.now()
            activity = "Báo quên mật khẩu"
            description = "Yêu cầu quản trị viên đặt lại mật khẩu mặc định"
            employee_id = emp.id
            dao.add_activity_log(activity_time=activity_time, activity=activity,
                                 description=description, employee_id=employee_id)
        else:
            err_msg_pass = "Tài khoản không tồn tại"
    return render_template("accounts/login.html", msg_pass=msg_pass, err_msg_pass=err_msg_pass, msg=msg)


@app.route("/logout-employee")
def logout_employee():
    activity_time = datetime.now()
    activity = "Đăng xuất"
    description = ""
    employee_id = current_user.id
    if dao.add_activity_log(activity_time=activity_time, activity=activity,
                            description=description, employee_id=employee_id):
        logout_user()
    return redirect(url_for("index"))


@app.route("/api/logout-employee-auto/<int:employee_id>", methods=["post"])
def logout_employee_auto(employee_id):
    activity_time = datetime.now()
    activity = "Đăng xuất tự động"
    description = "Nhân viên không có hoạt động"
    employee_id = current_user.id
    if dao.add_activity_log(activity_time=activity_time, activity=activity,
                            description=description, employee_id=employee_id):
        logout_user()
        return jsonify({"status": 200})

    return jsonify({"status": 500, "error_message": "Something Wrong!!!"})


@app.route("/setting-employee", methods=["get", "post"])
@decorator.login_required
def setting_employee():
    msg_info = ""
    msg_pass = ""
    err_msg_info = ""
    err_msg_pass = ""
    description = ""

    if request.method == "POST":
        if request.form['save'] == 'saveInformation':

            name = request.form.get("name")
            gender = request.form.get("gender")
            date_of_birth = request.form.get("dateOfBirth")
            phone = request.form.get("phone")
            address = request.form.get("address")
            # password_confirm = hashlib.sha512(request.form.get("passwordConfirm")
            #                                   .strip().encode("utf-8")).hexdigest()
            password_confirm = request.form.get("passwordConfirm")

            if current_user.password == password_confirm:
                dao.change_employee_info(current_user.id, name, gender, date_of_birth, phone, address)
                msg_info = "Cập nhật thông tin tài khoản thành công"
                description = msg_info
            else:
                err_msg_info = "Mật khẩu không chính xác"
                description = err_msg_info
        if request.form['save'] == 'savePassword':

            new_password = hashlib.sha512(request.form.get("newPassword")
                                          .strip().encode("utf-8")).hexdigest()
            new_password_confirm = hashlib.sha512(request.form.get("newPasswordConfirm")
                                                  .strip().encode("utf-8")).hexdigest()
            old_password_confirm = hashlib.sha512(request.form.get("oldPasswordConfirm")
                                                  .strip().encode("utf-8")).hexdigest()

            if new_password == new_password_confirm:
                if current_user.password == old_password_confirm:
                    dao.change_employee_pass(current_user.id, new_password)
                    msg_pass = "Đổi mật khẩu thành công"
                    description = msg_pass
                else:
                    err_msg_pass = "Mật khẩu cũ không chính xác"
                    description = err_msg_pass
            else:
                err_msg_pass = "Mật khẩu mới không khớp"
                description = err_msg_pass

    if description != "":
        activity_time = datetime.now()
        activity = "Sửa thông tin tài khoản"
        employee_id = current_user.id
        dao.add_activity_log(activity_time=activity_time, activity=activity,
                             description=description, employee_id=employee_id)

    if current_user.employee_role == EmployeeRole.EMPLOYEE:
        return render_template("accounts/setting_employee.html",
                               msg_info=msg_info, err_msg_info=err_msg_info,
                               msg_pass=msg_pass, err_msg_pass=err_msg_pass)
    else:
        return render_template("accounts/setting_admin.html",
                               msg_info=msg_info, err_msg_info=err_msg_info,
                               msg_pass=msg_pass, err_msg_pass=err_msg_pass)


@app.route("/passbook-list", methods=["get", "post"])
@decorator.login_required_user
def passbook_list():
    passbook_id = None
    customer_id = None
    if request.method == "POST":
        passbook_id = request.form.get("passbookID")
    passbooks = dao.get_passbook_list(passbook_id)
    return render_template("layouts/passbook_list.html", passbooks=passbooks)


@app.route("/open-passbook", methods=["get", "post"])
@decorator.login_required_user
def open_passbook():
    if request.method == "POST":
        pass
    return render_template("layouts/open_passbook.html",
                           customers=dao.find_customer(),
                           passbook_type=dao.get_passbook_type())


@app.route("/api/create-passbook", methods=["post"])
@decorator.login_required_user
def create_passbook():
    try:
        data = json.loads(request.data)
        customer_id = data.get('customer_id')
        passbook_type_id = data.get('passbook_type_id')
        balance_amount = data.get('balance_amount')

        passbook = dao.create_passbook(customer_id=customer_id,
                                       passbook_type_id=passbook_type_id,
                                       balance_amount=balance_amount)
        return jsonify({"status": 200, "passbook": [passbook.dump()]})
    except Exception as ex:
        return jsonify({"status": 500, "error": ex})


@app.route("/api/update-passbook", methods=["post"])
@decorator.login_required_user
def update_passbook():
    try:
        data = json.loads(request.data)
        passbook_id = data.get('passbook_id')
        passbook_type_id = data.get('passbook_type_id')
        balance_amount = data.get('balance_amount')

        passbook = dao.update_passbook(passbook_id=passbook_id,
                                       passbook_type_id=passbook_type_id,
                                       balance_amount=balance_amount)
        return jsonify({"status": 200, "passbook": [passbook.dump()]})
    except Exception as ex:
        return jsonify({"status": 500, "error": ex})


@app.route("/api/create-customer", methods=["post"])
@decorator.login_required_user
def create_customer():
    try:
        data = json.loads(request.data)
        name = data.get('name')
        identity_card_number = data.get('identity_card_number')
        phone = data.get('phone')

        customer = dao.create_customer(name=name, identity_card_number=identity_card_number, phone=phone)
        return jsonify({"status": 200, "id": customer.id, "name": customer.name})
    except Exception as ex:
        return jsonify({"status": 500, "error": ex})


@app.route("/api/update-customer", methods=["post"])
@decorator.login_required_user
def update_customer():
    try:
        data = json.loads(request.data)
        customer_id = data.get('customer_id')
        phone = data.get('phone')

        customer = dao.update_customer(customer_id=customer_id, phone=phone)
        return jsonify({"status": 200, "customer": customer.dump()})
    except Exception as ex:
        return jsonify({"status": 500, "error": ex})


@app.route("/api/find-customer", methods=["post"])
@decorator.login_required_user
def find_customer():
    try:
        data = json.loads(request.data)
        customer_id = data.get('customer_id')
        identity_number = data.get('identity_number')
        name = data.get('name')

        customers = dao.find_customer(customer_id=customer_id, identity_number=identity_number, name=name)
        return jsonify({"status": 200, "customers": [c.dump() for c in customers]})

    except Exception as ex:
        return jsonify({"status": 500, "error": ex})


@app.route("/api/find-passbook-type", methods=["post"])
@decorator.login_required_user
def find_passbook_type():
    try:
        data = json.loads(request.data)
        passbook_type_id = data.get('passbook_type_id')

        passbook_types = dao.get_passbook_type(passbook_type_id=passbook_type_id)
        return jsonify({"status": 200, "passbook_types": [passbook_type.dump() for passbook_type in passbook_types]})

    except Exception as ex:
        return jsonify({"status": 500, "error": ex})


@app.route("/api/find-passbook", methods=["post"])
@decorator.login_required_user
def find_passbook():
    try:
        data = json.loads(request.data)
        passbook_id = data.get('passbook_id')
        customer_id = data.get('customer_id')
        passbook_type_id = data.get('passbook_type_id')
        open_date = data.get('open_date')

        passbooks = dao.get_passbook_list(passbook_id=passbook_id,
                                          customer_id=customer_id,
                                          passbook_type_id=passbook_type_id,
                                          open_date=open_date)
        return jsonify({"status": 200, "passbooks": [passbook.dump() for passbook in passbooks]})

    except Exception as ex:
        return jsonify({"status": 500, "error": ex})


@login.user_loader
def load_user(user_id):
    return Employee.query.get(user_id)


if __name__ == "__main__":
    from app.admin_view import *

    app.run(debug=True)
