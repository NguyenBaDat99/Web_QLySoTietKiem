from app import db, admin, app, decorator, dao
from flask import redirect, url_for, request
from datetime import datetime

from flask_login import current_user
from flask_login import logout_user

from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView, Admin

from app.models import Position, Employee, ActivityLog, PassbookTypes, EmployeeRole


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated \
               and current_user.employee_role == EmployeeRole.ADMIN \
               and current_user.active == True

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        dao.add_activity_log(activity="Đăng xuất tự động",
                             description="Nhân viên truy cập vào trang không được phân quyền",
                             employee_id=current_user.id)
        logout_user()
        return redirect(url_for('login_employee', next=request.url))


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated \
               and current_user.employee_role == EmployeeRole.ADMIN \
               and current_user.active == True

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        dao.add_activity_log(activity="Đăng xuất tự động",
                             description="Nhân viên truy cập vào trang không được phân quyền",
                             employee_id=current_user.id)
        logout_user()
        return redirect(url_for('login_employee', next=request.url))


class AboutUsView(AuthenticatedBaseView):
    @expose("/")
    def index(self):
        return self.render("admin/about-us.html")


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        dao.add_activity_log(activity="Đăng xuất",
                             description="",
                             employee_id=current_user.id)
        logout_user()
        return redirect("/")

    def is_accessible(self):
        return current_user.is_authenticated


class PositionModelView(AuthenticatedModelView):
    column_display_pk = True
    can_export = True
    form_columns = ('position_name',)
    form_filters = ('position_name',)
    page_size = 10


class EmployeeModelView(AuthenticatedModelView):
    column_display_pk = True
    can_export = True
    can_delete = False
    show_column = 'name', 'username', 'gender', 'date_of_birth', 'phone', 'address', 'start_work_date', 'position', \
                  'active', 'employee_role',
    form_columns = show_column
    column_filters = show_column
    column_list = show_column
    page_size = 10


class ActivityLogModelView(AuthenticatedModelView):
    column_display_pk = True
    can_export = True
    can_create = False
    can_delete = False
    can_edit = False
    column_filters = ('activity_time', 'activity', 'employee_id')
    page_size = 10


class PassbookTypesModelView(AuthenticatedModelView):
    can_export = True
    can_edit = False
    can_delete = False
    show_column = 'passbook_type_name', 'minimum_deposit', 'minimum_deposit_date', 'interest_rate', 'apply_date', 'term',
    column_filters = show_column
    form_columns = show_column
    page_size = 10


admin.add_view(PositionModelView(Position, db.session))
admin.add_view(EmployeeModelView(Employee, db.session))
admin.add_view(ActivityLogModelView(ActivityLog, db.session))
admin.add_view(PassbookTypesModelView(PassbookTypes, db.session))
# admin.add_view(AboutUsView(name="About us"))
admin.add_view(LogoutView(name="Logout"))
