from flask import redirect, url_for, request
from functools import wraps
from flask_login import current_user, logout_user

from app.models import EmployeeRole


# def login_required_admin(f):
#     @wraps(f)
#     def check(*args, **kwargs):
#         if not current_user.is_authenticated:
#             return redirect(url_for("login_employee", next=request.url))
#
#         if current_user.employee_role != EmployeeRole.ADMIN:
#             logout_user()
#             return redirect(url_for("login_employee", next=request.url))
#
#         return f(*args, **kwargs)
#
#     return check


def login_required_user(f):
    @wraps(f)
    def check(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("login_employee", next=request.url))

        if current_user.employee_role != EmployeeRole.EMPLOYEE:
            logout_user()
            return redirect(url_for("login_employee", next=request.url))

        return f(*args, **kwargs)

    return check
