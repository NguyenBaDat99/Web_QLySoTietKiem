from datetime import timedelta

from app import app, login, decorator, dao, api
from flask import render_template, session, Blueprint
from flask_login import login_user
from flask_paginate import Pagination, get_page_parameter, get_page_args
import hashlib
from dateutil.relativedelta import relativedelta

from datetime import datetime


@app.route("/")
@decorator.login_required_user
def index():
    return redirect(url_for("passbook_list"))


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

                    dao.add_activity_log(activity="Đăng nhập",
                                         description="",
                                         employee_id=current_user.id)

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

            dao.add_activity_log(activity="Báo quên mật khẩu",
                                 description="Yêu cầu quản trị viên đặt lại mật khẩu mặc định",
                                 employee_id=emp.id)
        else:
            err_msg_pass = "Tài khoản không tồn tại"
    return render_template("accounts/login.html", msg_pass=msg_pass, err_msg_pass=err_msg_pass, msg=msg)


@app.route("/logout-employee")
def logout_employee():
    if dao.add_activity_log(activity="Đăng xuất",
                            description="",
                            employee_id=current_user.id):
        logout_user()
    return redirect(url_for("index"))


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
        dao.add_activity_log(activity="Sửa thông tin tài khoản",
                             description=description,
                             employee_id=current_user.id)

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
    if request.method == "POST":
        passbook_id = request.form.get("passbookID")

    passbooks = dao.get_passbook_list(passbook_id)
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(passbooks)
    pagination_passbooks = passbooks[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    passbook_types = dao.get_passbook_type()

    return render_template("layouts/passbook_list.html",
                           passbooks=pagination_passbooks,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           passbook_types=passbook_types)


@app.route("/open-passbook", methods=["get", "post"])
@decorator.login_required_user
def open_passbook():
    customers = dao.find_customer()
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(customers)
    pagination_customers = customers[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    return render_template("layouts/open_passbook.html",
                           customers=pagination_customers,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           passbook_type=dao.get_passbook_type())


@app.route("/transaction-passbook/<passbook_id>", methods=["get", "post"])
@decorator.login_required_user
def transaction_passbook(passbook_id):
    if passbook_id != "0":
        passbook = dao.find_passbook(passbook_id)
        if passbook:
            if passbook.balance_amount != 0:
                customer = dao.get_customer_by_id(passbook.customer_id)
                passbook_type = dao.get_passbook_type(passbook.passbook_type_id)
                transaction_slips = dao.get_transaction_slip(passbook_id=passbook.id)

                if passbook_type[0].term == 0:
                    withdraw_date = (passbook.open_date + timedelta(days=passbook_type[0].minimum_deposit_date))
                    last_transaction_date = dao.get_last_transaction_date(passbook_id=passbook.id)

                    deposit_month = 0
                    if last_transaction_date:
                        deposit_month = (datetime.now().year - last_transaction_date.year) * 12 + \
                                        datetime.now().month - last_transaction_date.month
                    else:
                        deposit_month = (datetime.now().year - passbook.open_date.year) * 12 + \
                                        datetime.now().month - passbook.open_date.month

                    return render_template("layouts/transaction_passbook.html",
                                           passbook=passbook,
                                           customer=customer,
                                           transaction_slips=transaction_slips,
                                           passbook_type=passbook_type[0],
                                           withdraw_date=withdraw_date.date(),
                                           deposit_month=deposit_month,
                                           datenow=datetime.now().date(), )
                else:
                    last_maturity_date = dao.get_last_transaction_date(passbook_id=passbook.id)
                    maturity_times = dao.get_maturity_time(passbook_id=passbook.id, open_date=passbook.open_date)

                    maturity_date = passbook.open_date
                    interest_money = maturity_times * \
                                     passbook_type[0].interest_rate * \
                                     passbook_type[0].term * \
                                     passbook.balance_amount

                    if last_maturity_date and last_maturity_date > passbook.open_date:
                        maturity_date = last_maturity_date
                    maturity_date += relativedelta(months=+passbook_type[0].term)

                    return render_template("layouts/transaction_passbook.html",
                                           passbook=passbook,
                                           customer=customer,
                                           transaction_slips=transaction_slips,
                                           passbook_type=passbook_type[0],
                                           maturity_date=maturity_date.date(),
                                           interest_money=interest_money,
                                           maturity_times=maturity_times,
                                           datenow=datetime.now().date(), )
            else:
                return render_template("layouts/transaction_passbook.html",
                                       msg="Sổ tiết kiệm đã bị đóng")
        else:
            return render_template("layouts/transaction_passbook.html",
                                   msg="Mã sổ không tồn tại")
    return render_template("layouts/transaction_passbook.html")


@app.route("/report", methods=["get", "post"])
@decorator.login_required_manager
def report():
    passbook_types = dao.get_passbook_type()
    if request.method == "POST":
        date = request.form.get("date")

        passbook_type = request.form.get("passbookType")
        month = request.form.get("month")

        if date:
            report_revenue_day = dao.report_revenue_day(date)

            return render_template("layouts/report.html",
                                   passbook_types=passbook_types,
                                   report_revenue_day=report_revenue_day)

    return render_template("layouts/report.html",
                           passbook_types=passbook_types)


@login.user_loader
def load_user(user_id):
    return Employee.query.get(user_id)


if __name__ == "__main__":
    from app.admin_view import *

    app.run(debug=True)
